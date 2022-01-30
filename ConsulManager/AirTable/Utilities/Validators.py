from ConsulManager.AirTable import VALID_CUENTAS_LIST, PAGOS_ESTATUS_LIST

def valid_currency(value=0):
    if value >= 0:
        return True
    return False

def valid_cuenta(value=None):
    if value is None:
        return None
    return value in VALID_CUENTAS_LIST

def valid_pago_estatus(value=None):
    if value is None:
        return False
    return value in PAGOS_ESTATUS_LIST
