from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from pygame.locals import *
import trimesh
import numpy as np
import traceback

class PersonajesDeTodos:
    def __init__(self, nombre, modelo, posicion=(0, 0, 0), rotacion=(0, 0, 0), escala=(1.0, 1.0, 1.0)):
        self.nombre = nombre
        self.modelo = modelo
        self.posicion = posicion
        self.rotacion = rotacion
        self.escala = escala
        
        try:
            # Cargar el modelo como escena
            self.scene = trimesh.load(self.modelo)
            
            # Asegurarse de que la escena contiene geometría
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
        except Exception as e:
            print(f"Error al establecer posición: {str(e)}")

    def set_scale(self, x, y, z):
        """Escalar el modelo de forma segura"""
        try:
            self.escala = (x, y, z)
        except Exception as e:
            print(f"Error al establecer escala: {str(e)}")

    def set_rotation(self, x, y, z):
        """Establecer la rotación en los tres ejes"""
        self.rotacion = (x, y, z)

    def render(self):
        """Renderizar el modelo 3D en OpenGL sin iluminación ni efectos de materiales"""
        try:
            glPushMatrix()

            # Deshabilitar iluminación y otros efectos de OpenGL
            glDisable(GL_LIGHTING)
            glDisable(GL_DEPTH_TEST)

            # Aplicar transformaciones (rotaciones y escalado)
            glTranslatef(*self.posicion)  # Aplicar la posición
            glRotatef(self.rotacion[0], 1, 0, 0)  # Rotación en X
            glRotatef(self.rotacion[1], 0, 1, 0)  # Rotación en Y
            glRotatef(self.rotacion[2], 0, 0, 1)  # Rotación en Z
            glScalef(*self.escala)  # Aplicar escala

            # Renderizar cada malla
            for name, mesh in self.meshes:
                if mesh is not None:
                    self._render_mesh(mesh)
            
            # Restaurar configuraciones de OpenGL
            glPopMatrix()
            
        except Exception as e:
            print(f"Error durante el renderizado: {str(e)}")
            print(traceback.format_exc())

    def _render_mesh(self, mesh):
        """Renderiza una malla individual de forma segura sin materiales"""
        try:
            if not hasattr(mesh, 'vertices') or not hasattr(mesh, 'faces'):
                return

            vertices = mesh.vertices
            faces = mesh.faces

            # Color simple para la malla
            color = (0.8, 0.8, 0.8)  # Color gris predeterminado

            # Configuración del color para cada malla
            glPushAttrib(GL_ALL_ATTRIB_BITS)  # Guardar el estado de OpenGL
            glColor3fv(color)  # Establecer color RGB (sin material)

            # Renderizar la geometría
            glBegin(GL_TRIANGLES)
            for face in faces:
                for vertex_id in face:
                    glVertex3fv(vertices[vertex_id])
            glEnd()

            glPopAttrib()  # Restaurar el estado de OpenGL

        except Exception as e:
            print(f"Error al renderizar malla: {str(e)}")
            print(traceback.format_exc())
