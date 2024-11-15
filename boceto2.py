from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from pygame.locals import *
from PIL import Image
import numpy as np
import trimesh
import traceback

class PersonajesDeTodos:
    def __init__(self, nombre, modelo, posicion=(0, 0, 0), rotacion=(0, 0, 0), escala=(1.0, 1.0, 1.0)):
        self.nombre = nombre
        self.modelo = modelo
        self.posicion = posicion
        self.rotacion = rotacion  # Ahora es una tupla (x, y, z)
        self.escala = escala
        self.textures = {}
        
        try:
            # Cargar el modelo como escena para mantener los materiales
            self.scene = trimesh.load(self.modelo)
            
            # Convertir la escena a una lista de mallas si es necesario
            if isinstance(self.scene, trimesh.Scene):
                self.meshes = list(self.scene.geometry.items())  # Guardamos los nombres y las mallas
            else:
                self.meshes = [("default", self.scene)]
            
            # Verificar que las mallas se cargaron correctamente
            if not self.meshes:
                raise ValueError("No se pudieron cargar las mallas del modelo")
            
            # Inicializar las transformaciones
            self._initialize_transforms()
            
        except Exception as e:
            print(f"Error al cargar el modelo {self.modelo}: {str(e)}")
            print(traceback.format_exc())
            raise

    def _initialize_transforms(self):
        """Inicializa las transformaciones básicas del modelo"""
        try:
            self.set_position(*self.posicion)
            self.set_scale(*self.escala)
        except Exception as e:
            print(f"Error al inicializar transformaciones: {str(e)}")

    def set_position(self, x, y, z):
        """Cambiar la posición del modelo de forma segura"""
        try:
            self.posicion = (x, y, z)
            for _, mesh in self.meshes:
                if mesh is not None:
                    mesh.apply_translation((x, y, z))
        except Exception as e:
            print(f"Error al establecer posición: {str(e)}")

    def set_scale(self, x, y, z):
        """Escalar el modelo de forma segura"""
        try:
            self.escala = (x, y, z)
            for _, mesh in self.meshes:
                if mesh is not None:
                    mesh.apply_scale([x, y, z])
        except Exception as e:
            print(f"Error al establecer escala: {str(e)}")

    def set_rotation(self, x, y, z):
        """Establecer la rotación en los tres ejes"""
        self.rotacion = (x, y, z)

    def render(self):
        """Renderizar el modelo 3D en OpenGL con manejo de errores"""
        try:
            glPushMatrix()
            
            # Configuración básica de OpenGL
            glEnable(GL_DEPTH_TEST)
            glEnable(GL_LIGHTING)
            glEnable(GL_LIGHT0)
            
            # Configurar luz
            glLightfv(GL_LIGHT0, GL_POSITION, (1.0, 1.0, 1.0, 0.0))
            glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
            glLightfv(GL_LIGHT0, GL_AMBIENT, (0.3, 0.3, 0.3, 1.0))
            
            # Aplicar rotaciones en los tres ejes
            glRotatef(self.rotacion[0], 1, 0, 0)  # Rotación en X
            glRotatef(self.rotacion[1], 0, 1, 0)  # Rotación en Y
            glRotatef(self.rotacion[2], 0, 0, 1)  # Rotación en Z
            
            # Renderizar cada malla
            for name, mesh in self.meshes:
                if mesh is not None:
                    self._render_mesh(name, mesh)
            
            # Restaurar configuraciones de OpenGL
            glPopMatrix()
            
        except Exception as e:
            print(f"Error durante el renderizado: {str(e)}")
            print(traceback.format_exc())

    def _get_mesh_color(self, mesh):
        """Obtiene el color del material de la malla, con comprobación de errores"""
        try:
            # Intentar obtener el color del material
            if hasattr(mesh, 'visual') and hasattr(mesh.visual, 'material'):
                material = mesh.visual.material
                # Verificar si 'baseColorFactor' está definido y es iterable
                if material is not None and hasattr(material, 'baseColorFactor') and material.baseColorFactor is not None:
                    return material.baseColorFactor[:3]  # Usar los primeros 3 valores (RGB)
                elif hasattr(material, 'diffuse') and material.diffuse is not None:
                    return material.diffuse[:3]

            # Si la malla tiene colores por vértice
            if hasattr(mesh.visual, 'vertex_colors') and mesh.visual.vertex_colors is not None:
                # Promedio de los colores de vértice
                colors = mesh.visual.vertex_colors
                return np.mean(colors[:, :3] / 255.0, axis=0)

            # Si la malla tiene color uniforme
            if hasattr(mesh.visual, 'face_colors') and mesh.visual.face_colors is not None:
                colors = mesh.visual.face_colors
                return np.mean(colors[:, :3] / 255.0, axis=0)
                
        except Exception as e:
            print(f"Error al obtener color: {e}")
        
        # Color por defecto si no se encuentra ningún color
        return (0.8, 0.8, 0.8)

    def _render_mesh(self, name, mesh):
        """Renderiza una malla individual de forma segura"""
        try:
            if not hasattr(mesh, 'vertices') or not hasattr(mesh, 'faces'):
                return

            vertices = mesh.vertices
            faces = mesh.faces

            # Obtener el color de la malla
            color = self._get_mesh_color(mesh)
            
            # Configuración del material y el color para cada malla
            glPushAttrib(GL_ALL_ATTRIB_BITS)  # Guardar el estado de OpenGL
            glMaterialfv(GL_FRONT, GL_DIFFUSE, color + (1.0,))  # RGB + Alpha
            glMaterialfv(GL_FRONT, GL_AMBIENT, tuple(c * 0.2 for c in color) + (1.0,))
            glMaterialfv(GL_FRONT, GL_SPECULAR, (0.2, 0.2, 0.2, 1.0))
            glMaterialf(GL_FRONT, GL_SHININESS, 32.0)

            # Renderizar la geometría
            glBegin(GL_TRIANGLES)
            for face in faces:
                # Calcular normal de la cara
                v0 = vertices[face[0]]
                v1 = vertices[face[1]]
                v2 = vertices[face[2]]
                normal = np.cross(v1 - v0, v2 - v0)
                normal = normal / np.linalg.norm(normal) if np.any(normal) else [0, 1, 0]
                
                # Aplicar normal y vértices
                glNormal3fv(normal)
                for vertex_id in face:
                    glVertex3fv(vertices[vertex_id])
            glEnd()

            glPopAttrib()  # Restaurar el estado de OpenGL

        except Exception as e:
            print(f"Error al renderizar malla: {str(e)}")
            print(traceback.format_exc())
