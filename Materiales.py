from pygltflib import GLTF2

# Cargar el archivo .glb
gltf = GLTF2().load("golem6.glb")

# Imprimir los materiales
for material in gltf.materials:
    print(f"Material: {material.name}")
    if hasattr(material, 'pbrMetallicRoughness'):
        pbr = material.pbrMetallicRoughness
        if hasattr(pbr, 'baseColorFactor'):
            print(f"  Color base: {pbr.baseColorFactor}")
        if hasattr(pbr, 'metallicFactor'):
            print(f"  Factor metálico: {pbr.metallicFactor}")
        if hasattr(pbr, 'roughnessFactor'):
            print(f"  Factor rugosidad: {pbr.roughnessFactor}")
