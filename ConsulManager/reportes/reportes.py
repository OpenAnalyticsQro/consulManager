import env
from consulManager.reportes import REPORTE_TABLE_NAME_AIR_TABLE, SEMANA_ID, TOTAL_CONSULTAS, FECHA, RECORD_ID
from pyairtable import Table
from os import getenv
from consulManager.AirTable import AIRTABLE_API_KEY, CONSULTORIO_2022_BASE_ID_AIR_TABLE
from datetime import datetime, date
from calendar import monthcalendar

# data dictionary reference
# {'SEMANA-2-2022': {'FECHA': '2022-01-02', 'SEMANA_ID': 'SEMANA-2-2022', 'TOTAL_CONSULTAS': 2, 'RECORD_ID': 
# 'recueMG9u9ILOVvzP'}}

def get_week_id(year=2022, month=1, day=1):
    date_iso = date(year=year, day=day, month=month).isocalendar()
    if (month == 1) and (date_iso[1] >)
    return True


def get_all_weeks(year=2022):
    for month in range(1,12):
        for week in monthcalendar(year=year, month=month):
            if week[6] != 0:
                date = f"{year}-{month:02d}-{week[6]:02d}"
                week_number = date(year=year, month=month, day=week[6]).isocalendar().week
                week = f"SEMANA-{week_number}-{year}"
                yield (week, date)

class reporteApi(object):
    def __init__(self):
        self.__table = Table(api_key=getenv(AIRTABLE_API_KEY),
                            base_id=getenv(CONSULTORIO_2022_BASE_ID_AIR_TABLE),
                            table_name=getenv(REPORTE_TABLE_NAME_AIR_TABLE))
        self.__data = {}

    def clean_data(self):
        for item in self.__table.all(fields=[SEMANA_ID]):
            if item['fields'][SEMANA_ID] == 'SEMANA-NaN-NaN':
                print(f"Deletign record: {item['id']}")
                self.__table.delete(record_id=item['id'])

    def sync_data(self):
        self.__data.clear()
        for item in self.__table.all(fields=[SEMANA_ID, TOTAL_CONSULTAS, FECHA]):
            self.__data[item["fields"][SEMANA_ID]] = item["fields"]
            self.__data[item["fields"][SEMANA_ID]][RECORD_ID] = item["id"]
        print(self.__data)

    def generate_all_weeks(self, year=2022):
        for (week, date) in get_all_weeks(year=year):
            if week in self.__data.keys():
                print("Value exits")
            else:
                print(f"Values not exist: {week}")

if __name__ == "__main__":
    reporte_table = reporteApi()
    # reporte_table.clean_data()
    reporte_table.sync_data()
    reporte_table.generate_all_weeks()