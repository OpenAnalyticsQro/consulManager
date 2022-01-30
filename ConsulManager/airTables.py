from pyairtable.api import table
import env
from ConsulManager.AirTable import AIRTABLE_API_KEY, CONSULTORIO_2022_BASE_ID_AIR_TABLE, CONSULTAS_TABLE_NAME_AIR_TABLE, REPORTE_TABLE_NAME_AIR_TABLE
from pyairtable import Table
from pyairtable.formulas import match
from os import getenv

# Move to utilities
from datetime import date

def get_week(year=2022, month=1, day=1):
    _date = date(year=year,month=month, day=day)
    return f"SEMANA-{_date.isocalendar()[1]}-{year}"

if __name__ == "__main__":
    # print(getenv(CONSULTORIO_2022_BASE_ID_AIR_TABLE))
    # consultas_table = Table(api_key=getenv(AIRTABLE_API_KEY),
    #                         base_id=getenv(CONSULTORIO_2022_BASE_ID_AIR_TABLE),
    #                         table_name=getenv(CONSULTAS_TABLE_NAME_AIR_TABLE))
    # for item in consultas_table.all():
    #     print(item)
    my_week = get_week(year=2022, month=1, day=12)
    print(my_week)

    # reportes_table = Table(api_key=getenv(AIRTABLE_API_KEY),
    #                         base_id=getenv(CONSULTORIO_2022_BASE_ID_AIR_TABLE),
    #                         table_name=getenv(REPORTE_TABLE_NAME_AIR_TABLE))
    # # for item in reportes_table.all():
    # #     print(item)

    # match_week = match({"SEMANA_ID":my_week})
    # record = reportes_table.first(formula=match_week)
    # print(f"id_week = {record['id']}")

    # # test to create
    # consultas_table.create({'DENTISTA':'DIANA', 'SEMANA':[record['id']]})