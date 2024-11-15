import random as ran
from random import choice

class bancoPreguntas:
    def __init__(self):
        self.numUno = 0
        self.numDos = 0
        self.numTres = 0
        self.respuesta = 0
        self.preguntaActual = None
        self.preguntas = []
        self.respuestaActual = None
        # Genera las preguntas al inicio
        self.elige_pregunta()
    
    def generar_numeros(self):
        self.numUno = ran.randint(-11, 11)
        self.numDos = ran.randint(-11, 11)
        self.numTres = ran.randint(-11, 11)
        
    def generar_preguntasNivel1(self):
        # Genera nuevos números antes de cada pregunta
        
        operacion1 = self.numUno + self.numDos * self.numTres
        respuestaMala = ran.randint(-51, 50)
        respuestaMala2 = ran.randint(-51, 50)
        operacion2 = self.numUno * self.numDos * self.numTres
        operacion3 = self.numUno - self.numDos - self.numTres
        operacion4=self.numUno+self.numDos+self.numTres
        operacion5=self.numUno*self.numDos+self.numTres
        
        self.preguntas = [
            {"pregunta": f"¿Cuánto es {self.numUno} + {self.numDos} * {self.numTres}?\n"
                         f"a) {operacion1}\n"
                         f"b) {respuestaMala}\n"
                         f"c) {respuestaMala2}", 
             "respuesta": "a"},

            {"pregunta": f"¿Cuánto es {self.numUno} * {self.numDos} * {self.numTres}?\n"
                         f"a) {respuestaMala2}\n"
                         f"b) {operacion2}\n"
                         f"c) {respuestaMala}",
             "respuesta": "b"},

            {"pregunta": f"¿Cuánto es {self.numUno} - {self.numDos} - {self.numTres}?\n"
                         f"a) {respuestaMala}\n"
                         f"b) {respuestaMala2}\n"
                         f"c) {operacion3}",
             "respuesta": "c"},

            {"pregunta": f"¿Cuánto es {self.numUno} + {self.numDos} + {self.numTres}?\n"
                         f"a) {respuestaMala}\n"
                         f"b) {respuestaMala2}\n"
                         f"c) {operacion4}",
             "respuesta": "c"},
            
            {"pregunta": f"¿Cuánto es {self.numUno} * {self.numDos} + {self.numTres}?\n"
                         f"a) {respuestaMala2}\n"
                         f"b) {operacion5}\n"
                         f"c) {respuestaMala}",
             "respuesta": "b"},

        ]
    
    def elige_pregunta(self):
        # Generar nuevas preguntas cada vez que se elige una pregunta
        self.generar_numeros()
        self.generar_preguntasNivel1()
        seleccionado = choice(self.preguntas)
        self.preguntaActual = seleccionado["pregunta"]
        self.respuestaActual = seleccionado["respuesta"]