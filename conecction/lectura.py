import snap7

def leer_datos(plc, DB_NUMBER=2, START_ADRESS=0,SIZE=259):
    db = plc.db_read(DB_NUMBER,START_ADRESS,SIZE)
    product_name =db[2:256].decode('UTF-8').strip('\x00')
    product_value = int.from_bytes(db[256:258], byteorder='big')
    product_status = bool(db[258])

    return{
        "Producto": product_name,
        "Valor": product_value,
        "Estado": product_status
    }