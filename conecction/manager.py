import snap7
from snap7.util import get_bool
from snap7.util import set_bool
from conecction.lectura import leer_datos
from database.database import guardar_dato
import time

class PLCManager:
    def __init__(self, ip="192.168.1.10", rack=0,slot=1):
        self.ip = ip
        self.rack = rack
        self.slot = slot
        self.client = snap7.client.Client()
        self.conectado = False

        try:
            self.client.connect(self.ip,self.rack,self.slot)
            self.conectado = True
        except RuntimeError as e:
            print(" Error al conectar el PLC: {e}")
        except Exception as e:
            print("Error inesperado: {e}")

    def leer_y_guardar(self):
        datos = leer_datos(self.client)
        guardar_dato(datos["Producto"], datos["Valor"],datos["Estado"])
        return datos
    
    def leer_bit_vida(self, db=3, byte=0, bit=0, size=258):
        try:
            db_data = self.client.db_read(db, byte, size)
            actual = get_bool(db_data, 0, bit)

            if "anterior" not in self.bit_vida_cache:
                self.bit_vida_cache["anterior"] = actual
                return "⏳ Esperando siguiente lectura..."

            if actual != self.bit_vida_cache["anterior"]:
                self.bit_vida_cache["anterior"] = actual
                return "✅ PLC activo (bit cambió)"
            else:
                return "⚠️ El PLC no respondió (bit congelado)"

        except Exception as e:
            return f"❌ Error al leer bit de vida: {e}"
    
    def enviar_bit_vida(self, paso,db=3,byte_index=258):
        data_to_write = bytearray(259)

        patrones = [
            [True, False, False, False],
            [False, True, False, False],
            [False, False, True, False],
            [False, False, False, True],            
        ]

        for i in range(4):
            set_bool(data_to_write, byte_index, i, patrones[paso][i])
        
        self.client.db_write(db,0,data_to_write)