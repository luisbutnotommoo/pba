from direct.showbase.ShowBase import ShowBase
from panda3d.core import PointLight, Vec4
from direct.task import Task
import gc
import atexit



class MiAplicacion(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # Cargar el modelo del personaje
        self.personaje = self.loader.loadModel("prueba\gltf\Wolf-Blender-2.82a.gltf")
        self.personaje.reparentTo(self.render)
        self.personaje.setPos(0, 15, 0)
        
        # Configurar la luz
        luz = PointLight('luz')
        luz.setColor(Vec4(4, 4, 4, 1))
        self.luzNodePath = self.render.attachNewNode(luz)
        self.luzNodePath.setPos(5, -10, 10)
        self.render.setLight(self.luzNodePath)
        
        # Tarea para rotar el personaje continuamente
        self.taskMgr.add(self.rotar_personaje, "RotarPersonajeTask")
        
        # Configuración de eventos de teclado para rotar manualmente
        self.accept("arrow_left", self.rotar_izquierda)
        self.accept("arrow_right", self.rotar_derecha)
        self.accept("escape", self.cleanup)  # Agregamos la tecla escape para limpieza manual
        
        # Registrar la función de limpieza para que se ejecute al cerrar
        atexit.register(self.cleanup)

    def rotar_personaje(self, task):
        # Incrementar el ángulo de rotación en el eje Z (Heading) continuamente
        self.personaje.setH(self.personaje.getH() + 0.5)
        return Task.cont

    def rotar_izquierda(self):
        # Rotar hacia la izquierda en 10 grados en el eje Z
        self.personaje.setH(self.personaje.getH() + 10)
    
    def rotar_derecha(self):
        # Rotar hacia la derecha en 10 grados en el eje Z
        self.personaje.setH(self.personaje.getH() - 10)

    def cleanup(self):
        """Método para limpiar recursos y liberar memoria al cerrar"""
        print("Iniciando limpieza de recursos...")
        
        try:
            # Detener todas las tareas
            self.taskMgr.remove("RotarPersonajeTask")
            
            # Limpiar el caché del cargador
            self.loader.clearCache()
            
            # Remover el modelo y la luz
            if hasattr(self, 'personaje'):
                self.personaje.removeNode()
                self.personaje = None
            
            if hasattr(self, 'luzNodePath'):
                self.render.clearLight(self.luzNodePath)
                self.luzNodePath.removeNode()
                self.luzNodePath = None
            
            # Forzar la recolección de basura de Python
            gc.collect()
            
            print("Limpieza completada exitosamente")
            
        except Exception as e:
            print(f"Error durante la limpieza: {e}")
        
        finally:
            # Asegurarse de que se realice una última recolección de basura
            gc.collect()

if __name__ == "__main__":
    app = MiAplicacion()
    app.run()