


from direct.showbase.ShowBase import ShowBase
from panda3d.core import PointLight, Vec4


class MiAplicacion(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Cargar el modelo GLB (en este caso 'personaje.glb')
        self.personaje = self.loader.loadModel("medico.glb")  # Asegúrate de que 'personaje.glb' esté en tu carpeta
        self.personaje.reparentTo(self.render)  # Agregar el modelo a la escena
        self.personaje.setPos(0, 10, 0)  # Posicionarlo en la escena

        # Configurar una luz para iluminar el modelo
        luz = PointLight('luz')
        luz.setColor(Vec4(1, 1, 1, 1))  # Luz blanca
        self.luzNodePath = self.render.attachNewNode(luz)
        self.luzNodePath.setPos(10, -10, 10)  # Posición de la luz
        self.render.setLight(self.luzNodePath)

if __name__ == "__main__":
    app = MiAplicacion()
    app.run()
