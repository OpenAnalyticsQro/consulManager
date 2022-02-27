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
from pyairtable.formulas import match


class TratamientoManagerAir(object):
    def __init__(self):
        self.__table = Table(
            api_key=getenv(AIRTABLE_API_KEY),
            base_id=getenv(CONSULTORIO_2022_BASE_ID_AIR_TABLE),
            table_name=getenv(TRATAMIEMTO_TABLE_NAME_AIR_TABLE),
        )
        self.__data = {}

        self.paciente_activo = None

    def show_all(self):
        try:
            for item in self.__table.all():
                print(item)
        except Exception as e:
            log.error(f"{self.__class__.show_all.__qualname__}: {e}")

    def update_paciente_activo(self, paciente=None):
        self.paciente_activo = paciente

    def get_active_tratamientos(self, paciente_id=None):
        try:
            # if paciente_id is None:
            formula = match({FD.ESTADO_DE_PAGOS: 0, FD.PACIENTE: self.paciente_activo})
            # else:
            #     formula = match({FD.ESTADO_DE_PAGOS: 0, FD.PACIENTE: paciente_id})
            list_active_tratamientos = []
            for item in self.__table.all(formula=formula):
                # print(f"{item['fields']['TRATAMIENTO_ID']} -> {item['fields']['PACIENTE']}" )
                # print(item)
                list_active_tratamientos.append({"id":item["id"], "data":item['fields']['TRATAMIENTO_ID']})

            return list_active_tratamientos

        except Exception as e:
            log.error(f"{self.__class__.show_all.__qualname__}: {e}")

    def create_tratamiento(self, tratamiento=None, cantidad=None, costo_final=None, fecha=None):
        try:
            record = self.__table.create(
                {FD.TRATAMIENTO: tratamiento, FD.CANTIDAD: cantidad, FD.COSTO_FINAL: costo_final, FD.FECHA: fecha}
            )
            return record
        except Exception as e:
            log.error(f"{self.__class__.create_tratamiento.__qualname__}: {e}")

    # COMMAND LINE COMMANDS




if __name__ == "__main__":
    from ConsulManager.AirTable import VALID_PAGOS_ESTATUS, VALID_CUENTAS_AIR_TABLE
    
    from pyairtable.utils import datetime_to_iso_str

    log.info("Hola Mundo")
    tratamiento_table = TratamientoManagerAir()
    # tratamiento_table.show_all()
    
    list_trata = tratamiento_table.get_active_tratamientos(paciente_id="ESTELA MENDOZA-(442) 704-7158")
    for item in list_trata:
        print(item)

    # tratamiento_table.create_tratamiento(
    #     tratamiento=None,
    #     cantidad=1,
    #     costo_final=1,
    #     fecha=get_valid_date(year=2022, day=15, month=2)
    # )
