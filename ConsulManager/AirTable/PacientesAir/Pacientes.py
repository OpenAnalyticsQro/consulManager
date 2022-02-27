from msilib import type_key
from unicodedata import name
import ConsulManager.env
from ConsulManager.Logger import logger as log
from pyairtable import Table
from os import getenv
from ConsulManager.AirTable import (
    AIRTABLE_API_KEY,
    CONSULTORIO_2022_BASE_ID_AIR_TABLE,
    PACIENTES_TABLE_AIR_TABLE,
)

from ConsulManager.AirTable.PacientesAir import FIELDS as FD
from ConsulManager.AirTable.Utilities import Validators
from PyInquirer import prompt
from examples import custom_style_3
from ConsulManager.AirTable.Utilities.Fechas import get_valid_date
from ConsulManager.ConsulCli.validator import dateValidator, MontoValidator
from ConsulManager.AirTable import PAGOS_ESTATUS_LIST, VALID_CUENTAS_LIST
import re

# REGEX EXPRESIONS
WORDS_REGEX = re.compile(r"[A-Z]*")
DIGITS_REGEX = re.compile(r"\d")


class PacientesAir(object):
    def __init__(self):
        self.__table = Table(
            api_key=getenv(AIRTABLE_API_KEY),
            base_id=getenv(CONSULTORIO_2022_BASE_ID_AIR_TABLE),
            table_name=getenv(PACIENTES_TABLE_AIR_TABLE),
        )
        self.__pacientes_list = []
    
    def update_pacientes_list(self):
        try:
            self.__pacientes_list.clear()
            index = 0
            for item in self.__table.all():
                # self.__pacientes_list.append(item['fields'][FD.PACIENTE_ID])
                self.__pacientes_list.append({"id":item['id'], "data":item['fields'][FD.PACIENTE_ID]})
                # print(f" {index} => {item['id']} {item['fields'][FD.PACIENTE_ID]}")
                index += 1
        except Exception as e:
            log.error(f"{self.__class__.show_all.__qualname__}: {e}")

    def get_paciente_from_id(self, record_id=None):
        if record_id is None:
            return None
        
        for paciente in self.__pacientes_list:
            if record_id == paciente["id"]:
                return paciente["data"]
        return None

    def show_all(self):
        try:
            index = 0
            for item in self.__table.all():
                print(f"index:{index} {item}")
                index += 1
        except Exception as e:
            log.error(f"{self.__class__.show_all.__qualname__}: {e}")
    
    def __get_phone_regex_from_str(self, paciente=""):
        if paciente == "":
            return ""
        
        paciente_phone_list = DIGITS_REGEX.findall(paciente)

        # find Phone Number
        if paciente_phone_list == []:
            return ""

        paciente_phone = ".*\("
        for number in paciente_phone_list[:3]:
            paciente_phone += number

        if len(paciente_phone_list) <= 2:
            paciente_phone += ".*"
            return paciente_phone

        paciente_phone += "\).*"
        for number in paciente_phone_list[3:6]:
            paciente_phone += number
        
        if len(paciente_phone_list) <= 5:
            paciente_phone += ".*"
            return paciente_phone

        paciente_phone += "-"
        for number in paciente_phone_list[6:10]:
            paciente_phone += number

        paciente_phone += ".*"
        return paciente_phone

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

    def find_paciente(self, paciente=""):
        pacientes_str = paciente.upper()
        # paciente_words = WORDS_REGEX.findall(pacientes_str)

        # print(f"name regex: {self.__get_name_regex_from_str(paciente=pacientes_str)}")
        # print(f"phone regex {self.__get_phone_regex_from_str(paciente=pacientes_str)}")

        name_reg_str = self.__get_name_regex_from_str(paciente=pacientes_str)
        if name_reg_str != "":
            name_reg = re.compile(name_reg_str)
            # name_list = list(filter(name_reg.match, self.__pacientes_list))
            name_list = list(filter(lambda x:name_reg.match(x["data"]), self.__pacientes_list))
        else:
            name_list = []

        phone_reg_str = self.__get_phone_regex_from_str(paciente=pacientes_str)
        if phone_reg_str != "":
            phone_reg = re.compile(phone_reg_str)
            # phone_list = list(filter(phone_reg.match, self.__pacientes_list))
            phone_list = list(filter(lambda x:phone_reg.match(x["data"]), self.__pacientes_list))
        else:
            phone_list = []

        # print(f"name list: {name_list}")
        # print(f"phone list: {phone_list}")

        # for px in phone_list:
        #     if (px in name_list) is False:
        #         name_list.append(px)
        valid_phone = True
        for px in phone_list:
            for px_name in name_list:
                if px["data"] == px_name["data"]:
                    valid_phone = False
                    break
            if valid_phone is True:
                name_list.append(px)
        return name_list[:49]
    
    def create_paciente(self, name=None, apellidos=None, telefono=None):
        data = {}
        if name is not None:
            data[FD.NAME] = name.upper()
        else:
            log.error(f"{self.__class__.create_paciente.__qualname__}: invalid name: {name}")
            return None
        if apellidos is not None:
            data[FD.APELLIDOS] = apellidos.upper()
        else:
            log.error(f"{self.__class__.create_paciente.__qualname__}: invalid name: {apellidos}")
            return None
        if telefono is not None:
            data[FD.TELEFONO] = f"({telefono[:3]}) {telefono[3:7]}-{telefono[7:]}"
        else:
            log.error(f"{self.__class__.create_paciente.__qualname__}: invalid name: {telefono}")
            return None
        
        try:
            record = self.__table.create(data)
            return record
        except Exception as e:
            log.error(f"{self.__class__.create_paciente.__qualname__}: {e}")
            return None

        # print("_______________")
        # print (**data)
        




if __name__ == "__main__":
    pacientes = PacientesAir()
    # pacientes.show_all()
    # pacientes.create_paciente(name="luis hirvin", apellidos="velasco", telefono="3321477452")
    pacientes.update_pacientes_list()
    x_list = pacientes.find_paciente("diana flo")
    for item in x_list:
        print(item)