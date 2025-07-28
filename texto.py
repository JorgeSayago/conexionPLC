import csv
import time

# Funcion para imprimir la base de datos del PLC en un archivo.csv para guaras los dato enviados
def imprimir(plc,DB_NUMBER,START_ADDRESS,SIZE):
    with open("registro.csv","w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Producto", "Valor","Estado"])

        for _ in range(10):
            db = plc.db_read(DB_NUMBER, START_ADDRESS, SIZE)
            product_name = db[2:256].decode('UTF-8').strip('\x00')
            product_vlue = int.from_bytes(db[256:258], byteorder='big')
            product_status = bool(db[258])

            writer.writerow([product_name,product_vlue, product_status])
            print(" Registro Guardado")
            time.sleep(3)