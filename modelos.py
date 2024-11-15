from direct.showbase.ShowBase import ShowBase
from panda3d.core import PointLight, Vec4
from direct.task import Task
import gc
import atexit
from nivel import Nivel1

class MiAplicacion(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # Configurar la luz
        luz = PointLight('luz')
        luz.setColor(Vec4(1, 1, 1, 1))  # Luz blanca
        self.luzNodePath = self.render.attachNewNode(luz)
        self.luzNodePath.setPos(5, -10, 10)
        self.render.setLight(self.luzNodePath)

        # Inicializar el Nivel 1
        self.nivel1 = Nivel1(self.render)

        # Eventos de teclado para rotar el personaje
        self.accept("arrow_left", self.rotar_izquierda)
        self.accept("arrow_right", self.rotar_derecha)
        self.accept("escape", self.cleanup)  # Agregamos la tecla escape para limpieza manual

        # Registrar la función de limpieza para que se ejecute al cerrar
        atexit.register(self.cleanup)

    def rotar_izquierda(self):
        """ Rotar hacia la izquierda en 10 grados """
        self.nivel1.personaje_panda.modelo.setH(self.nivel1.personaje_panda.modelo.getH() + 10)

    def rotar_derecha(self):
        """ Rotar hacia la derecha en 10 grados """
        self.nivel1.personaje_panda.modelo.setH(self.nivel1.personaje_panda.modelo.getH() - 10)

    def cleanup(self):
        """ Función de limpieza """
        print("Limpieza realizada.")
