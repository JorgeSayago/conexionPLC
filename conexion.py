import time
import snap7
from snap7.util import set_int, set_bool, set_string
from texto import imprimir  

IP = "192.168.1.10"
RACK = 0
SLOT = 1

DB_NUMBER = 2
START_ADDRESS = 0
SIZE = 259

DB_NUMBER_WRITE = 3

START_ADDRESS_WRITE = 0
SIZE_WRITE = 259

plc = snap7.client.Client()
plc.connect(IP, RACK, SLOT)

plc_info = plc.get_cpu_info()
print(f'Module Type: {plc_info.ModuleTypeName}')

state = plc.get_cpu_state()
print(f'State:{state}')

db = plc.db_read(DB_NUMBER, START_ADDRESS, SIZE)

product_name = db[2:256].decode('UTF-8').strip('\x00')
print(f'PRODUCT NAME: {product_name}')

product_value = int.from_bytes(db[256:258], byteorder='big')
print(f'PRODUCT VALUE: {product_value}')

product_status = bool(db[258])
print(product_status)





# Crear el buffer para enviar datos
data_to_write = bytearray(SIZE_WRITE)


# El string empieza desde el byte 2
set_string(data_to_write, 0, "caja ", max_size=254)

# --- Escribir un valor entero (INT) ---
set_int(data_to_write, 256, 1234)  # INT ocupa 2 bytes

# --- Escribir un booleano ---
set_bool(data_to_write, 258, 0, True)  # Byte 258, bit 0

# Enviar los datos al DB
plc.db_write(DB_NUMBER_WRITE, START_ADDRESS_WRITE, data_to_write)

imprimir(plc,DB_NUMBER,START_ADDRESS , SIZE)

time.sleep(15)