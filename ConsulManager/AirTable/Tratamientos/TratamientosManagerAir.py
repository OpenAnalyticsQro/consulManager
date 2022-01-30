import ConsulManager.env
from ConsulManager.Logger import logger as log
from pyairtable import Table
from os import getenv
from ConsulManager.AirTable import (
    AIRTABLE_API_KEY,
    CONSULTORIO_2022_BASE_ID_AIR_TABLE,
    TRATAMIEMTO_TABLE_NAME_AIR_TABLE,
)
# from ConsulManager.AirTable.Cobros import FIELD as FD
from ConsulManager.AirTable.Tratamientos import FIELD as FD
from ConsulManager.AirTable.Utilities import Validators
from PyInquirer import prompt
from examples import custom_style_3
from ConsulManager.AirTable.Utilities.Fechas import get_valid_date
from ConsulManager.ConsulCli.validator import dateValidator, MontoValidator
from ConsulManager.AirTable import PAGOS_ESTATUS_LIST, VALID_CUENTAS_LIST
import re


class TratamientoManagerAir(object):
    def __init__(self):
        self.__table = Table(
            api_key=getenv(AIRTABLE_API_KEY),
            base_id=getenv(CONSULTORIO_2022_BASE_ID_AIR_TABLE),
            table_name=getenv(TRATAMIEMTO_TABLE_NAME_AIR_TABLE),
        )
        self.__data = {}

    def show_all(self):
        try:
            for item in self.__table.all():
                print(item)
        except Exception as e:
            log.error(f"{self.__class__.show_all.__qualname__}: {e}")

    def create_tratamiento(self, tratamiento=None, cantidad=None, costo_final=None):
        try:
            record = self.__table.create(
                {FD.TRATAMIENTO: tratamiento, FD.CANTIDAD: cantidad, FD.COSTO_FINAL: costo_final}
            )
            return record
        except Exception as e:
            log.error(f"{self.__class__.create_tratamiento.__qualname__}: {e}")

    # COMMAND LINE COMMANDS




if __name__ == "__main__":
    from ConsulManager.AirTable import VALID_PAGOS_ESTATUS, VALID_CUENTAS_AIR_TABLE
    
    from pyairtable.utils import datetime_to_iso_str

    log.info("Hola Mundo")
    cobros_table = TratamientoManagerAir()
    cobros_table.show_all()
    # cobros_table.get_cobros_data_cli()
    # cobros_table.show_all()
    # from datetime import datetime
    # my_date = datetime.now()
    # # valid_fecha = get_valid_date(year=2022, day=14, month=1)
    # print(my_date.isoformat())
    # cobros_table.create_cobro(
    #     monto=100,
    #     cuenta=VALID_CUENTAS_AIR_TABLE.BBVA,
    #     estatus=VALID_PAGOS_ESTATUS.PAGADO,
    #     fecha=get_valid_date()
    # )
