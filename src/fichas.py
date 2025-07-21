class Ficha:
    def __init__(self, color):
        self.color = color
        self.posicion = -1          
        self.en_llegada = False     

    def sacar_de_la_carcel(self):
        self.posicion = 0  

    def mover(self, pasos):
        if self.posicion != -1 and not self.en_llegada:
            self.posicion += pasos
            if self.posicion >= 67:
                self.en_llegada = True
                self.posicion = -2  
                print(f"Ficha {self.color} llegó a la meta 🎯")

    def enviar_a_la_carcel(self):
        print(f"Ficha {self.color} fue enviada a la cárcel")
        self.posicion = -1
