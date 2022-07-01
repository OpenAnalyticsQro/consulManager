from ConsulManager.AirTable import Cobros
import ConsulManager.env
from pathlib import Path
from ConsulManager.Logger import logger as log
from pyairtable import Table
from pyairtable.formulas import match
from os import getenv
from ConsulManager.AirTable import (
    AIRTABLE_API_KEY,
    CONSULTORIO_2022_BASE_ID_AIR_TABLE,
    COBROS_TABLE_NAME_AIR_TABLE,
    PACIENTES_TABLE_AIR_TABLE
)
from ConsulManager.AirTable.Cobros import FIELD as FD
from ConsulManager.AirTable.Utilities import Validators
from ConsulManager.AirTable.Utilities.Fechas import get_valid_date
#from ConsulManager.ConsulCli.validator import dateValidator, MontoValidator
from ConsulManager.AirTable import PAGOS_ESTATUS_LIST, VALID_CUENTAS_LIST
import re


class FacturasCli(object):
    __FORMAT_FACTURA = None
    def __init__(self):
        # cobros table
        self.__table_cobros = Table(
            api_key=getenv(AIRTABLE_API_KEY),
            base_id=getenv(CONSULTORIO_2022_BASE_ID_AIR_TABLE),
            table_name=getenv(COBROS_TABLE_NAME_AIR_TABLE),
        )
        # Pacientes Table
        self.__table_pacientes = Table(
            api_key=getenv(AIRTABLE_API_KEY),
            base_id=getenv(CONSULTORIO_2022_BASE_ID_AIR_TABLE),
            table_name=getenv(PACIENTES_TABLE_AIR_TABLE),
        )
        self.get_format_factura()

    def get_paciente_from_record(self, record=None):
        if record is None:
            return None

        try:
            paciente = self.__table_pacientes.get(record_id=record)
            return paciente
        except Exception as e:
            log.error(f"{self.__class__.show_all.__qualname__}: {e}")

    def show_all_cobros(self):
        try:
            for item in self.__table_cobros.all():
                print(self.paciente_to_str(paciente=item['fields']))
                return item
        except Exception as e:
            log.error(f"{self.__class__.show_all.__qualname__}: {e}")

    def get_all_pending_facturas(self):
        formula = match({"FACTURA":"PENDIENTE"})
        facturas_list = []
        try:
            for item in self.__table_cobros.all(formula=formula):
                # print(item)
                record = item['fields']['PACIENTE'][0]
                paciente = self.get_paciente_from_record(record=record)
                #       print(paciente)
                facturas_list.append(self.paciente_to_str(paciente=paciente['fields'], cobro=item['fields']))
            return facturas_list
        except Exception as e:
            log.error(f"{self.__class__.show_all.__qualname__}: {e}")

    def paciente_to_str(self, paciente=None, cobro=None):
        if paciente is None:
            return ""
        if cobro is None:
            return ""
        if self.__FORMAT_FACTURA is None:
            return None
        return self.__FORMAT_FACTURA.format(NAME=paciente.get('NOMBRE_DE_FACTURACION', ''),
                                            RFC=paciente.get('RFC', ''),
                                            CORREO=paciente.get('CORREO', ''),
                                            MONTO=cobro.get('MONTO', ''),
                                            METHOD_PAGO=cobro.get('Metodo De Pago', ''),
                                            ADRRES=paciente.get('DOMICILIO', ''),
                                            CP=paciente.get('CODIGO_POSTAL', ''))

    def get_format_factura(self):
        file_path = Path(r"C:\Users\uidk4253\Documents\OpenAnalytics\ConsulManager\consulManager\ConsulManager\FacturasCli\FORMAT_FACTURA.txt")
        with open(file_path, "r") as fd:
            self.__FORMAT_FACTURA = fd.read()




if __name__ == "__main__":
    from ConsulManager.AirTable import VALID_PAGOS_ESTATUS, VALID_CUENTAS_AIR_TABLE

    cobros_table = FacturasCli()
    facturas = cobros_table.get_all_pending_facturas()
    print("\n".join(facturas))