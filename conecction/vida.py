from snap7.util import get_bool

def verificarBitVida(plc, db_number=10, byte_index=0, bit_index=0,size=1,cache={}):
    db = plc.client.db_read(db_number, byte_index, size)
    actual = get_bool(db,0,bit_index)

    if "anterior" not in cache:
        cache["anterior"]=actual
        return "esperando siguiente lectura"
    
    if actual != cache["anterior"]:
        cache["anterior"] = actual
        return "PLC activo (bit cambio)"
    else:
        return "El PLC no respondio (bit congelado)"