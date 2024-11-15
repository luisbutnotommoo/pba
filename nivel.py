import pygame
from OpenGL.GLU import*
from OpenGL.GL import*
from OpenGL.GLUT import*
from pygame.locals import*
from PIL import*
import objetos as obj
import escenario as esc
import viewPortPreguntas as view
import bancoPreguntas as bp
from boceto2 import  PersonajesDeTodos
 


class Nivel1:

    def __init__(self, display_size=(800, 600)):
        self.bandera = 0
        self.banderaJugador1=False
        self.banderaJugador2=False
        self.display = display_size
        self.show_message = False  # Controla cuándo se muestra el mensaje
        self.init_pygame()
        self.init_set_perspective()
        self.jugador_1_score=0
        self.jugador_2_score=0
        self.personaje=[
            PersonajesDeTodos("Medico","medico.gltf",(0,0,0),(0,-90,0), (5,5,5))
        ]
        self.objEscenario=esc.escenario("Imagenes/pasto.jpeg","Imagenes/castillo.jpg")
        self.objetoPregunta=bp.bancoPreguntas()
        self.asignar_posiciones_personajes()


    def asignar_posiciones_personajes(self):
        posiciones = [
            (2, -5, -25),  # Posición para personaje 1
            (4.5, -1.5, 0)    # Posición para personaje 4
        ]
        for personaje, (x, y, z) in zip(self.personaje, posiciones):
            personaje.set_position(x, y, z)
    
    def init_pygame(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        pygame.event.set_grab(True)

    def init_set_perspective(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, (self.display[0] / self.display[1]), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -50.0)


    def draw_scene(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # Dibujar escenario
    
        self.objEscenario.dibujar_piso_pared()
        glPushMatrix()
        obj.draw_rectangle(20,-10,-20,10,30,10)
        obj.draw_rectangle(-35,-10,-20,10,30,10)
        
        glPopMatrix()
        for personaje in self.personaje:
            personaje.render()  # Llamar al método dibujar del personaje
    
        if self.show_message:
            view.viewPort(self.display).draw_viewport(self.objetoPregunta)
       
        pygame.display.flip()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.bandera = 1
                    return False
                
                if self.show_message:  # Si la pregunta está en pantalla
                    if event.key == pygame.K_w or event.key == pygame.K_a or event.key == pygame.K_s or event.key == pygame.K_d:

                        if self.respuesta(event.key, player=1) and self.banderaJugador1==False:
                            self.jugador_1_score += 1  # Jugador 1 gana un punto
                            self.eventoParaGanar()
                        else:
                            self.banderaJugador1=True
                        
                    elif event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        if self.respuesta(event.key, player=2) and self.banderaJugador1==False:
                            self.jugador_2_score += 1  # Jugador 2 gana un punto
                            self.eventoParaGanar()
                        else:
                            self.banderaJugador2=True
                    if(self.banderaJugador1==True and self.banderaJugador2==True):
                        self.eventoNoAcertaron()



                if event.key == pygame.K_SPACE:  # Mostrar el mensaje al presionar la barra espaciadora
                    self.show_message = True
                if self.show_message and event.key == pygame.K_RETURN:
                    self.show_message = False  # Ocultar el mensaje al presionar Enter

        return True
    
    def eventoParaGanar(self):
        # Este método ejecuta algo especial tras una respuesta correcta
        print("Evento tras respuesta correcta")
        self.show_message = False  # Ocultar la pregunta
        self.objetoPregunta.elige_pregunta() 

    def respuesta(self, key,player):
        key_answer_map = {
            pygame.K_a: "a", 
            pygame.K_s: "b",
            pygame.K_d: "c",  
            pygame.K_LEFT: "a",
            pygame.K_DOWN: "b",
            pygame.K_RIGHT: "c"  # Jugador 2 presiona 'UP'
        }
        if key in key_answer_map and key_answer_map[key] == self.objetoPregunta.respuestaActual:
            return True
        return False
   
    def run(self):
        running = True
        while running:
            running = self.handle_input()
            self.draw_scene()
            pygame.time.wait(10)
           

    def cleanup(self):
        pygame.quit()

    
    def eventoParaGanar(self):
        # Este método ejecuta algo especial tras una respuesta correcta
        print("Evento tras respuesta correcta")
        self.show_message = False  # Ocultar la pregunta
        self.objetoPregunta.elige_pregunta()
        
    def eventoNoAcertaron(self):
        print("Evento error de los dos jugadores")
        self.show_message = False  # Ocultar la pregunta
        self.objetoPregunta.elige_pregunta()
        

if __name__ == "__main__":
    sP=Nivel1()
    sP.run()