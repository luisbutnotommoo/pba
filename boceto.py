from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from pygame.locals import *
from PIL import Image
import numpy as np
import trimesh

class PersonajesDeTodos:
    def __init__(self, nombre, modelo, posicion=(0, 0, 0), rotacion=0, escala=(1.0, 1.0, 1.0)):
        self.nombre = nombre
        self.modelo = modelo
        self.posicion = posicion
        self.escala = escala
        self.rotacion = rotacion

        # Cargar el modelo 3D
        self.mesh = trimesh.load(self.modelo)
        
        # Inicializar los materiales y la textura
        self.materials = None
        self.texture_id = None
        
        # Si es una escena, tomar la primera geometría
        if isinstance(self.mesh, trimesh.Scene):
            self.materials = self.mesh.geometry
            self.mesh = list(self.mesh.geometry.values())[0]  # Tomamos la primera malla
        else:
            self.materials = self.mesh.visual.material
        
        # Si el material tiene textura, cargarla
        if isinstance(self.materials, dict) and 'visual' in self.materials:
            visual = self.materials['visual']
            if 'diffuse' in visual.materials[0].__dict__:  # Verificar si hay una textura 'diffuse'
                texture_file = visual.materials[0].texture  # Obtener la ruta de la textura
                if texture_file:
                    self.texture_id = self.load_texture(texture_file)

        # Establecer posición y escala
        self.set_position(*self.posicion)
        self.set_scale(*self.escala)

    def load_texture(self, texture_file):
        """ Cargar la textura usando PIL y OpenGL """
        try:
            img = Image.open(texture_file)
            img = img.transpose(Image.FLIP_TOP_BOTTOM)  # OpenGL usa coordenadas de textura invertidas en Y
            img_data = np.array(img)

            # Generar un ID para la textura
            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)

            # Cargar la imagen de la textura en OpenGL
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

            return texture_id
        except Exception as e:
            print(f"Error cargando la textura: {e}")
            return None

    def set_position(self, x, y, z):
        """ Cambiar la posición del modelo """
        self.posicion = (x, y, z)
        self.mesh.apply_translation((x, y, z))

    def set_scale(self, x, y, z):
        """ Escalar el modelo """
        self.escala = (x, y, z)
        self.mesh.apply_scale([x, y, z])

    def dibujar(self, render):
        self.render()

    def render(self):
        """ Renderizar el modelo 3D en OpenGL """
        glPushMatrix()

        # Aplicar la rotación
        glRotatef(self.rotacion, 0, 1, 0)  # Rotación en torno al eje Y

        # Comprobar si el objeto cargado es una escena (scene) o una malla (trimesh)
        if isinstance(self.mesh, trimesh.Scene):
            # Si es una escena, tomar la primera malla
            for geometry in self.mesh.geometry.values():
                self._render_geometry(geometry)
        else:
            # Si es una malla, usar directamente sus vértices y caras
            self._render_geometry(self.mesh)

        glPopMatrix()

    def _render_geometry(self, geometry):
        """ Renderiza la geometría, aplicando texturas si están disponibles """
        vertices = geometry.vertices
        faces = geometry.faces
        
        # Si tenemos una textura, activarla
        if self.texture_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
        
        glBegin(GL_TRIANGLES)
        for face in faces:
            for vertex_index in face:
                vertex = vertices[vertex_index]
                
                # Intentar obtener las coordenadas UV
                try:
                    uv = geometry.visual.uv[vertex_index]  # Usar las coordenadas UV si existen
                except IndexError:
                    uv = (0, 0)  # Si no hay coordenadas UV, usar (0, 0)
                
                glTexCoord2fv(uv)  # Aplicar coordenadas de textura
                glVertex3fv(vertex)
        glEnd()

        if self.texture_id:
            glDisable(GL_TEXTURE_2D)

