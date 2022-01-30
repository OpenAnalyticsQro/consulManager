from ConsulManager.AirTable import ListaTratamientos
import ConsulManager.env
from ConsulManager.Logger import logger as log
from pyairtable import Table
from os import getenv
from ConsulManager.AirTable import (
    AIRTABLE_API_KEY,
    CONSULTORIO_2022_BASE_ID_AIR_TABLE,
    LISTA_TRATAMIENTOS_AIR_TABLE,
)

from ConsulManager.AirTable.ListaTratamientos import FIELDS as FD
import re


WORDS_REGEX = re.compile(r"[A-Z]*")

class ListaTratamientosAir(object):
    def __init__(self):
        self.__table = Table(
            api_key=getenv(AIRTABLE_API_KEY),
            base_id=getenv(CONSULTORIO_2022_BASE_ID_AIR_TABLE),
            table_name=getenv(LISTA_TRATAMIENTOS_AIR_TABLE),
        )
        self.__tratamientos_list = []
    
    def update_tratamientos_list(self):
        try:
            self.__tratamientos_list.clear()
            for item in self.__table.all():
                self.__tratamientos_list.append({"id":item['id'], "data":item['fields'][FD.TRATAMIENTO_ID].upper()})
                print(f"{item['fields'][FD.TRATAMIENTO_ID]}")
        except Exception as e:
            log.error(f"{self.__class__.show_all.__qualname__}: {e}")

    def show_all(self):
        try:
            for item in self.__table.all():
                print(item)
        except Exception as e:
            log.error(f"{self.__class__.show_all.__qualname__}: {e}")

    def find_tratamiento(self, tratamiento=""):
        tratamientos_str = tratamiento.upper()
        name_reg_str = self.__get_name_regex_from_str(paciente=tratamientos_str)
        print(name_reg_str)
        if name_reg_str != "":
            name_reg = re.compile(name_reg_str)
            name_list = list(filter(lambda x:name_reg.match(x["data"]), self.__tratamientos_list))
        else:
            name_list = []

        return name_list[:49]

    def __get_name_regex_from_str(self, paciente=""):
        # Find Words
        paciente_words = ""
        for word in WORDS_REGEX.findall(paciente):
            if word == '':
                continue
            paciente_words += f".*{word}"
        if paciente_words != "":
            paciente_words += ".*"
        return paciente_words


if __name__ == "__main__":
    tratamientos = ListaTratamientosAir()
    # tratamientos.show_all()
    tratamientos.update_tratamientos_list()
    # tratamientos.find_tratamiento("extr")
    x_list = tratamientos.find_tratamiento("Pro")
    for item in x_list:
        print(item)