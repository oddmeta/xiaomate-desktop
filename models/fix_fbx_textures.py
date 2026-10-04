# -*- coding: utf-8 -*-
"""
fix_fbx_textures.py —— 用原始 glb 内嵌的贴图，修复 Mixamo 自动绑定(rig)后 FBX 丢失的贴图。

流程：
  1. 从 glb 中提取所有内嵌贴图，并记录每张贴图的 PBR 角色（baseColor / normal / metallicRoughness）
  2. 在 Blender 中导入 Mixamo autorig FBX
  3. 重新链接丢失路径的贴图；按名称或 PBR 角色匹配；缺失时自动补接节点
  4. 删除 Blender 默认的 Camera 和 Light
  5. 打包贴图并导出新 FBX（贴图内嵌，不依赖外部文件）

用法（在命令行中运行，注意 -- 后面的参数才传给本脚本）：

  blender --background --python fix_fbx_textures.py -- ^
      --glb original.glb ^
      --fbx mixamo-autorig.fbx ^
      [--output result.fbx] ^
      [--tex-dir extracted_textures] ^
      [--keep-animations]

参数说明：
  --glb              原始的、带贴图、没有骨骼绑定的 .glb 文件（必填）
  --fbx              Mixamo autorig 后导出的 .fbx 文件（必填）
  --output           输出 FBX 路径（默认: <fbx名>-with-textures.fbx）
  --tex-dir          贴图提取目录（默认: <glb所在路径去扩展名>_textures）
  --keep-animations  导出时保留动画关键帧（默认不导出动画）
"""

import argparse
import base64
import json
import os
import struct
import sys

# ---------- GLB 解析（纯 Python，不依赖 Blender） ----------

GLB_MAGIC = b'glTF'
CHUNK_JSON = 0x4E4F534A  # 'JSON'
CHUNK_BIN = 0x004E4942   # 'BIN'


def read_glb(path):
    """读取 GLB，返回 (gltf JSON 字典, BIN chunk 字节串)。"""
    with open(path, 'rb') as f:
        data = f.read()
    if len(data) < 12 or data[:4] != GLB_MAGIC:
        raise SystemExit(f"[错误] '{path}' 不是有效的 GLB（二进制 glTF）文件。")
    offset = 12
    gltf = None
    bin_chunk = None
    while offset + 8 <= len(data):
        chunk_len, chunk_type = struct.unpack_from('<II', data, offset)
        payload = data[offset + 8: offset + 8 + chunk_len]
        if chunk_type == CHUNK_JSON:
            gltf = json.loads(payload)
        elif chunk_type == CHUNK_BIN:
            bin_chunk = payload
        offset += 8 + chunk_len
        offset = (offset + 3) & ~3  # chunk 头按 4 字节对齐
    if gltf is None:
        raise SystemExit(f"[错误] '{path}' 中没有 JSON chunk。")
    return gltf, bin_chunk


def image_roles(gltf):
    """从 glTF 材质定义中推断每张图片的语义角色。

    返回 {图片索引: {'baseColor'|'normal'|'metallicRoughness'|'occlusion', ...}}
    """
    textures = gltf.get('textures', [])
    roles = {}

    def tex_to_img(tex_index):
        if tex_index is not None and 0 <= tex_index < len(textures):
            return textures[tex_index].get('source')
        return None

    def add(tex_index, role):
        i = tex_to_img(tex_index)
        if i is not None:
            roles.setdefault(i, set()).add(role)

    for mat in gltf.get('materials', []):
        pbr = mat.get('pbrMetallicRoughness') or {}
        if 'baseColorTexture' in pbr:
            add(pbr['baseColorTexture'].get('index'), 'baseColor')
        if 'metallicRoughnessTexture' in pbr:
            add(pbr['metallicRoughnessTexture'].get('index'), 'metallicRoughness')
        if 'normalTexture' in mat:
            add(mat['normalTexture'].get('index'), 'normal')
        if 'occlusionTexture' in mat:
            add(mat['occlusionTexture'].get('index'), 'occlusion')
    return roles


def extract_textures(gltf, bin_chunk, out_dir):
    """把 glb 内嵌的图片提取到 out_dir，返回贴图条目列表。"""
    images = gltf.get('images', [])
    views = gltf.get('bufferViews', [])
    roles_by_img = image_roles(gltf)
    os.makedirs(out_dir, exist_ok=True)

    entries = []
    used = set()
    for i, img in enumerate(images):
        name = (img.get('name') or '').strip() or f"texture_{i:03d}"
        ext = '.jpg' if img.get('mimeType') in ('image/jpeg', 'image/jpg') else '.png'
        safe = ''.join(c if (c.isalnum() or c in '_-.') else '_' for c in name).strip('._') or f"texture_{i:03d}"
        base, n = safe, 1
        while base.lower() in used:
            base = f"{safe}_{n}"
            n += 1
        used.add(base.lower())
        path = os.path.join(out_dir, base + ext)

        if 'bufferView' in img and bin_chunk is not None:
            bv = views[img['bufferView']]
            blob = bin_chunk[bv['byteOffset']: bv['byteOffset'] + bv['byteLength']]
        elif 'uri' in img and img['uri'].startswith('data:'):
            blob = base64.b64decode(img['uri'].split(',', 1)[1])
        else:
            print(f"  [警告] 无法提取图片 '{name}'（没有内嵌数据，只有外部引用）")
            continue

        with open(path, 'wb') as f:
            f.write(blob)
        entry = {'name': name, 'path': path, 'roles': set(roles_by_img.get(i, set()))}
        entries.append(entry)
        print(f"  [提取] {os.path.basename(path)}  角色: {sorted(entry['roles']) or ['未知']}")
    return entries


def norm_name(s):
    """归一化名称用于匹配：去扩展名、去 Blender 的 .001 后缀、只保留字母数字。"""
    s = os.path.splitext(os.path.basename(s))[0]
    while '.' in s and len(s.rsplit('.', 1)[1]) == 3 and s.rsplit('.', 1)[1].isdigit():
        s = s.rsplit('.', 1)[0]
    return ''.join(c for c in s.lower() if c.isalnum())


# ---------- Blender 部分 ----------

import bpy  # noqa: E402  （本脚本需通过 blender --python 运行）

# Principled BSDF 输入 socket 名 -> glTF PBR 角色
_PRINCIPLED_ROLE = {
    'Base Color': 'baseColor',
    'Roughness': 'metallicRoughness',
    'Metallic': 'metallicRoughness',
    'Normal': 'normal',
    'Alpha': 'alpha',
    'Emission Color': 'emission',
}


def tex_node_role(tree, tex_node):
    """追踪贴图节点最终连到 Principled BSDF 的哪个通道（启发式）。"""
    frontier = [link.to_socket for out in tex_node.outputs for link in out.links]
    seen = set()
    while frontier:
        sock = frontier.pop()
        node = sock.node
        if node in seen:
            continue
        seen.add(node)
        if node.type == 'BSDF_PRINCIPLED':
            role = _PRINCIPLED_ROLE.get(sock.name)
            if role:
                return role
        elif node.type == 'NORMAL_MAP':
            frontier.extend(link.to_socket for link in node.outputs['Normal'].links)
        else:
            for out in node.outputs:
                frontier.extend(link.to_socket for link in out.links)
    return None


def image_role(img):
    """该图片在所有材质中被用作什么角色（取第一个非空结果）。"""
    for mat in bpy.data.materials:
        if not mat.use_nodes or not mat.node_tree:
            continue
        for node in mat.node_tree.nodes:
            if node.type == 'TEX_IMAGE' and node.image == img:
                role = tex_node_role(mat.node_tree, node)
                if role:
                    return role
    return None


def relink_images(entries):
    """把 FBX 中丢失路径的图片重新指向提取出的贴图文件（先按名称，再按角色）。"""
    by_name = {}
    for e in entries:
        by_name.setdefault(norm_name(e['name']), []).append(e)

    for img in bpy.data.images:
        if img.name in ('Render Result', 'Viewer Node'):
            continue
        entry = None
        cand = by_name.get(norm_name(img.name), [])
        if len(cand) == 1:
            entry = cand[0]
        elif len(cand) > 1:
            role = image_role(img)
            by_role = [e for e in cand if role and role in e['roles']]
            entry = (by_role or cand)[0]
            print(f"  [警告] 名称 '{img.name}' 匹配到多张贴图，按角色选择: {entry['name']}")
        if entry is None:
            role = image_role(img)
            by_role = [e for e in entries if role and role in e['roles']]
            if len(by_role) == 1:
                entry = by_role[0]
                print(f"  [提示] '{img.name}' 名称未匹配，按角色 '{role}' 匹配到: {entry['name']}")
        if entry is None:
            print(f"  [跳过] 无法匹配贴图: {img.name}")
            continue
        img.filepath = os.path.abspath(entry['path'])
        img.source = 'FILE'
        try:
            img.reload()
        except Exception as exc:
            print(f"  [警告] 重新加载 {img.name} 失败: {exc}")
        print(f"  [重链接] {img.name} -> {entry['path']}")


def _load_image(path):
    img = bpy.data.images.load(path, check_existing=True)
    return img


def _wire_metallic_roughness(tree, bsdf, entry, x, y):
    """glTF 规范：metallicRoughness 贴图的 G 通道=粗糙度，B 通道=金属度。"""
    tex = tree.nodes.new('ShaderNodeTexImage')
    tex.image = _load_image(entry['path'])
    tex.location = (x - 600, y - 400)
    sep = tree.nodes.new('ShaderNodeSeparateColor')
    sep.location = (x - 300, y - 400)
    tree.links.new(tex.outputs['Color'], sep.inputs['Color'])
    tree.links.new(sep.outputs['Green'], bsdf.inputs['Roughness'])
    tree.links.new(sep.outputs['Blue'], bsdf.inputs['Metallic'])


def rebuild_material_without_textures(entries):
    """材质完全没有贴图节点时（Mixamo 有时会替换材质），按角色重建基础连接。"""
    base = [e for e in entries if 'baseColor' in e['roles']]
    normal = [e for e in entries if 'normal' in e['roles']]
    mr = [e for e in entries if 'metallicRoughness' in e['roles']]
    for mat in bpy.data.materials:
        if not mat.use_nodes:
            mat.use_nodes = True
        if not mat.node_tree:
            continue
        if any(n.type == 'TEX_IMAGE' for n in mat.node_tree.nodes):
            continue
        bsdf = next((n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
        if not bsdf:
            bsdf = mat.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
            out = next((n for n in mat.node_tree.nodes if n.type == 'OUTPUT_MATERIAL'), None)
            if not out:
                out = mat.node_tree.nodes.new('ShaderNodeOutputMaterial')
            mat.node_tree.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
        x, y = bsdf.location.x, bsdf.location.y
        if len(base) > 1:
            print(f"  [跳过] 材质 '{mat.name}' 无贴图节点，但 glb 中有多张 baseColor 贴图，无法确定对应关系")
        else:
            if base:
                tex = mat.node_tree.nodes.new('ShaderNodeTexImage')
                tex.image = _load_image(base[0]['path'])
                tex.location = (x - 400, y)
                mat.node_tree.links.new(tex.outputs['Color'], bsdf.inputs['Base Color'])
                print(f"  [重建] 材质 '{mat.name}' 接入 Base Color 贴图")
            if normal:
                tex = mat.node_tree.nodes.new('ShaderNodeTexImage')
                tex.image = _load_image(normal[0]['path'])
                tex.location = (x - 600, y - 200)
                nm = mat.node_tree.nodes.new('ShaderNodeNormalMap')
                nm.location = (x - 300, y - 200)
                mat.node_tree.links.new(tex.outputs['Color'], nm.inputs['Color'])
                mat.node_tree.links.new(nm.outputs['Normal'], bsdf.inputs['Normal'])
                print(f"  [重建] 材质 '{mat.name}' 接入 Normal 贴图")
            if len(mr) == 1:
                _wire_metallic_roughness(mat.node_tree, bsdf, mr[0], x, y)
                print(f"  [重建] 材质 '{mat.name}' 接入 Metallic-Roughness 贴图")


def ensure_metallic_roughness(entries):
    """材质有贴图但缺少 Metallic-Roughness 连接时补上（FBX 导出常会丢这张图）。"""
    mr_entries = [e for e in entries if 'metallicRoughness' in e['roles']]
    if not mr_entries:
        return
    for mat in bpy.data.materials:
        if not mat.use_nodes or not mat.node_tree:
            continue
        bsdf = next((n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
        if not bsdf:
            continue
        has_mr = any(
            node.type == 'TEX_IMAGE' and node.image
            and tex_node_role(mat.node_tree, node) == 'metallicRoughness'
            for node in mat.node_tree.nodes
        )
        if has_mr:
            continue
        _wire_metallic_roughness(mat.node_tree, bsdf, mr_entries[0], bsdf.location.x, bsdf.location.y)
        print(f"  [补接] 材质 '{mat.name}' 添加 Metallic-Roughness 贴图")


def remove_camera_and_light():
    """删除 Blender 默认场景遗留的 Camera 和 Light 对象及孤立数据块。"""
    removed = []
    for obj in list(bpy.data.objects):
        if obj.type in ('CAMERA', 'LIGHT'):
            removed.append(f"{obj.name}({obj.type})")
            bpy.data.objects.remove(obj, do_unlink=True)
    for block in list(bpy.data.cameras):
        if block.users == 0:
            bpy.data.cameras.remove(block)
    for block in list(bpy.data.lights):
        if block.users == 0:
            bpy.data.lights.remove(block)
    if removed:
        print(f"  [删除] {', '.join(removed)}")
    else:
        print("  未发现 Camera/Light")


def pack_images():
    for img in bpy.data.images:
        if img.name in ('Render Result', 'Viewer Node') or img.packed_file:
            continue
        path = bpy.path.abspath(img.filepath)
        if path and os.path.exists(path):
            try:
                img.pack()
                print(f"  [打包] {img.name}")
            except Exception as exc:
                print(f"  [警告] 打包 {img.name} 失败: {exc}")


def export_fbx(path, keep_animations=False):
    bpy.ops.export_scene.fbx(
        filepath=path,
        use_selection=False,
        apply_unit_scale=True,
        add_leaf_bones=False,
        bake_anim=keep_animations,
        path_mode='COPY',
        embed_textures=True,
        axis_forward='-Z',
        axis_up='Y',
    )
    print(f"  [导出] {path}")


# ---------- 主流程 ----------

def parse_args():
    argv = sys.argv
    argv = argv[argv.index('--') + 1:] if '--' in argv else []
    parser = argparse.ArgumentParser(description='用原始 glb 的贴图修复 Mixamo autorig FBX 的贴图')
    parser.add_argument('--glb', required=True, help='原始的、带贴图、没有骨骼绑定的 .glb')
    parser.add_argument('--fbx', required=True, help='Mixamo autorig 后导出的 .fbx')
    parser.add_argument('--output', help='输出 FBX 路径（默认: <fbx名>-with-textures.fbx）')
    parser.add_argument('--tex-dir', help='贴图提取目录（默认: <glb路径去扩展名>_textures）')
    parser.add_argument('--keep-animations', action='store_true', help='导出时保留动画关键帧（默认不导出动画）')
    return parser.parse_args(argv)


def main():
    args = parse_args()
    glb_path = os.path.abspath(args.glb)
    fbx_path = os.path.abspath(args.fbx)
    out_path = os.path.abspath(args.output) if args.output else os.path.splitext(fbx_path)[0] + '-with-textures.fbx'
    tex_dir = os.path.abspath(args.tex_dir) if args.tex_dir else os.path.splitext(glb_path)[0] + '_textures'

    for p, label in ((glb_path, 'glb'), (fbx_path, 'fbx')):
        if not os.path.exists(p):
            raise SystemExit(f"[错误] 找不到{label}文件: {p}")

    print(f"== 1/5 提取 glb 内嵌贴图 -> {tex_dir}")
    gltf, bin_chunk = read_glb(glb_path)
    entries = extract_textures(gltf, bin_chunk, tex_dir)
    if not entries:
        raise SystemExit("[错误] glb 中没有可提取的贴图。")

    print(f"== 2/5 导入 Mixamo FBX: {fbx_path}")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=fbx_path)

    print("== 3/5 重链接贴图")
    relink_images(entries)
    rebuild_material_without_textures(entries)
    ensure_metallic_roughness(entries)

    print("== 4/5 删除 Camera / Light")
    remove_camera_and_light()

    print("== 5/5 打包贴图并导出 FBX")
    pack_images()
    export_fbx(out_path, args.keep_animations)

    print(f"\n完成！输出文件: {out_path}")


if __name__ == '__main__':
    main()
