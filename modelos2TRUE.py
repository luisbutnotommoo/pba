import trimesh
import numpy as np

def visualizar_glb(ruta_archivo):
    """
    Carga y visualiza un archivo GLB usando trimesh
    
    Parameters:
    ruta_archivo (str): Ruta al archivo GLB
    """
    # Cargar la escena desde el archivo GLB
    scene = trimesh.load(ruta_archivo)
    
    # Imprimir información sobre la escena
    print(f"Nombre de la escena: {scene.metadata.get('name', 'Sin nombre')}")
    print(f"Número de geometrías: {len(scene.geometry)}")
    
    # Mostrar información de cada malla en la escena
    for nombre, geom in scene.geometry.items():
        print(f"\nGeometría: {nombre}")
        print(f"Vértices: {len(geom.vertices)}")
        print(f"Caras: {len(geom.faces)}")
    
    # Mostrar la escena
    scene.show()

# Ejemplo de uso
if __name__ == "__main__":
    # Reemplaza 'modelo.glb' con la ruta a tu archivo
    ruta_modelo = "prueba\gltf\Wolf-Blender-2.82a.gltf"
    visualizar_glb(ruta_modelo)