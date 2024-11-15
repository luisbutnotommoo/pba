from pythreejs import PerspectiveCamera, WebGLRenderer, Scene, Mesh, MeshBasicMaterial
from pythreejs import GLTFLoader
from IPython.display import display
import numpy as np

# Función para cargar el modelo GLB sin cambiar colores ni textura
def cargar_modelo_glb(ruta_modelo):
    # Crear una escena y cámara
    scene = Scene()
    camera = PerspectiveCamera(75, 1.0, 0.1, 1000)
    camera.position.z = 5
    renderer = WebGLRenderer()
    renderer.set_size(800, 600)
    
    # Crear el cargador GLTF
    loader = GLTFLoader()

    # Cargar el modelo GLB y añadirlo a la escena
    modelo = loader.load(ruta_modelo)  # Usando el cargador GLTF para cargar el archivo
    scene.add(modelo)
    
    return scene, camera, renderer

# Función para renderizar la escena
def renderizar(scene, camera, renderer):
    renderer.render(scene, camera)
    display(renderer)

# Ruta al archivo GLB (asegúrate de usar la ruta correcta a tu archivo GLB)
ruta_modelo = 'golem6.glb'

# Cargar el modelo y configurar la escena
scene, camera, renderer = cargar_modelo_glb(ruta_modelo)

# Renderizar la escena
renderizar(scene, camera, renderer)
