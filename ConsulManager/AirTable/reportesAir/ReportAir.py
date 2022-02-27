import ConsulManager.env
from ConsulManager.Logger import logger as log
from pyairtable import Table
from pyairtable.formulas import match as airMatch
from os import getenv
from ConsulManager.AirTable import (
    AIRTABLE_API_KEY,
    CONSULTORIO_2022_BASE_ID_AIR_TABLE,
    REPORTE_TABLE_NAME_AIR_TABLE,
)
from ConsulManager.AirTable.Cobros import FIELD as FD
from ConsulManager.AirTable.Utilities import Validators
from ConsulManager.AirTable.Utilities.Fechas import get_week, get_valid_date
#from ConsulManager.ConsulCli.validator import dateValidator, MontoValidator
from ConsulManager.AirTable import PAGOS_ESTATUS_LIST, VALID_CUENTAS_LIST
import re


class ReportManagerAir(object):
    def __init__(self):
        self.__table = Table(
            api_key=getenv(AIRTABLE_API_KEY),
            base_id=getenv(CONSULTORIO_2022_BASE_ID_AIR_TABLE),
            table_name=getenv(REPORTE_TABLE_NAME_AIR_TABLE),
        )
        self.__data = {}

    def show_all(self):
        try:
            for item in self.__table.all():
                print(item)
        except Exception as e:
            log.error(f"{self.__class__.show_all.__qualname__}: {e}")
    
    def get_week_record(self, week=None):
        if week is None:
            return None
        return self.__table.first(formula=airMatch({"SEMANA_ID":week}))['id']
    
    # def get_week_record(self, default_date="01/01/2022"):
    #     valid_date = re.compile(r'(\d\d)\/(\d\d)\/(\d\d\d\d)')
    #     (day, month, year) = valid_date.match(string=default_date['date']).groups()
    #     return self.__get_week_record(week=get_valid_date(day=int(day), month=int(month),year=int(year)))

if __name__ == "__main__":
    report = ReportManagerAir()
    # report.show_all()
    valid_date = get_week(year=2022, month=1, day=16)
    print(f"looking for : {valid_date}")
    print(report.get_week_record(week=valid_date))