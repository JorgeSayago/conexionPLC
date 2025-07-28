import snap7
from conecction.lectura import leer_datos
from database.database import guardar_dato

class PLCManager:
    def __init__(self, ip="192.168.1.10", rack=0,slot=1):
        self.ip = ip
        self.rack = rack
        self.slot = slot
        self.client = snap7.client.Client()
        self.client.connect(self.ip,self.rack,self.slot)
    
    def leer_y_guardar(self):
        datos = leer_datos(self.client)
        guardar_dato(datos["Producto"], datos["Valor"],datos["Estado"])
        return datos

