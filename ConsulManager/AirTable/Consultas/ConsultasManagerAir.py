from ConsulManager.AirTable.Cobros.CobrosManagerAir import CobrosManagerAir
from ConsulManager.AirTable.PagosDentistas.PagosDentistas import PagosDentistasAir
from ConsulManager.AirTable.reportesAir.ReportAir import ReportManagerAir
import ConsulManager.env
from ConsulManager.Logger import logger as log
from pyairtable import Table
from os import getenv
from ConsulManager.AirTable import (
    AIRTABLE_API_KEY,
    CONSULTORIO_2022_BASE_ID_AIR_TABLE,
    CONSULTAS_TABLE_NAME_AIR_TABLE,
    )
from ConsulManager.AirTable.Consultas import FIELDS as FD
from ConsulManager.AirTable.Utilities import Validators
from ConsulManager.AirTable.Utilities.Fechas import get_valid_date, get_week
#from ConsulManager.ConsulCli.validator import dateValidator, MontoValidator
from ConsulManager.AirTable import PAGOS_ESTATUS_LIST, VALID_CUENTAS_LIST, DENTISTAS_LIST
import re


class ConsultasManagerAir(object):
    def __init__(self):
        self.__table = Table(
            api_key=getenv(AIRTABLE_API_KEY),
            base_id=getenv(CONSULTORIO_2022_BASE_ID_AIR_TABLE),
            table_name=getenv(CONSULTAS_TABLE_NAME_AIR_TABLE),
        )
        self.__data = {}

    def show_all(self):
        try:
            for item in self.__table.all():
                print(item)
        except Exception as e:
            log.error(f"{self.__class__.show_all.__qualname__}: {e}")

    def create_consulta(self, fecha=None, tratatamiento_id=None,cobros=[], pagos_dentistas=[], semana=[], dentista=None, paciente=None):
        if fecha is None:
            return False
        try:
            record = self.__table.create(
                {
                FD.FECHA: fecha,
                FD.COBROS: cobros,
                FD.PAGOS_DENTISTAS: pagos_dentistas,
                FD.SEMANA: semana,
                FD.DENTISTA: dentista,
                FD.PACIENTES: paciente,
                FD.TRATAMIENTOS: tratatamiento_id
                }
            )
            return record
        except Exception as e:
            log.error(f"{self.__class__.create_consulta.__qualname__}: {e}")

    # COMMAND LINE COMMANDS
    def get_consulta_data_cli(self, default_date="01/01/2022"):
        questions_list = []
        # questions_list.append(self.get_date_cli(default_date=default_date))
        # questions_list.append(self.get_monto_cli())
        # questions_list.append(self.get_valid_cuenta_cli())
        # questions_list.append(self.get_valid_pago_status_cli())
        print("Crear un Nueva Consulta:")
        answers = prompt([self.get_date_cli(default_date=default_date)], style=custom_style_3)
        print(answers)

        # get week
        valid_date = re.compile(r'(\d\d)\/(\d\d)\/(\d\d\d\d)')
        (day, month, year) = valid_date.match(string=answers['date']).groups()
        valid_week = get_week(year=int(year), month=int(month), day=int(day))

        new_report = ReportManagerAir()
        week_id = new_report.get_week_record(week=valid_week)
        print(week_id)

        #select Denstista
        answer_dentista = prompt([self.get_dentista_cli()], style=custom_style_3)


        # questions_list.append(self.confirm_consulta_week_cli(week=valid_week))
        answer_week = prompt([self.confirm_consulta_week_cli(week=valid_week)], style=custom_style_3)

        # create new Cobro
        cobro_record = self.get_cobro_cli(default_date=answers['date'])
        # create new Pago
        pago_record = self.get_pago_cli(default_date=answers['date'])
        # print(self.print_consulta_cli(answers=answers))
        
        questions_list.append(self.confirm_consulta_cli())
        answers_confirm = prompt(questions_list, style=custom_style_3)
        
        if answers_confirm['createConsulta']:
            valid_date = re.compile(r'(\d\d)\/(\d\d)\/(\d\d\d\d)')
            (day, month, year) = valid_date.match(string=answers['date']).groups()
            self.create_consulta(
                fecha=get_valid_date(year=int(year), month=int(month), day=int(day)),
                cobros=[cobro_record['id']],
                pagos_dentistas=[pago_record['id']],
                semana=[week_id],
                dentista=answer_dentista['dentista']

            )

    def get_report_cli(self):
        new_report = ReportManagerAir()

    def get_pago_cli(self, default_date="01/01/2022"):
        new_pago = PagosDentistasAir()
        return new_pago.get_pagos_data_cli(default_date=default_date)

    def get_cobro_cli(self, default_date="01/01/2022"):
        new_cobro = CobrosManagerAir()
        return new_cobro.get_cobros_data_cli(default_date=default_date)
    
    def get_date_cli(self, default_date=None):
        question = {
            "type": "input",
            "name": "date",
            "message": "Fecha (DD/MM/YYY):",
            "default": f"{default_date}",
            "validate": dateValidator,
            }
        return question
    
    def get_dentista_cli(self):
        question = {
            "type": "rawlist",
            "name": "dentista",
            'message': 'Dentista: ',
            'choices': DENTISTAS_LIST

        }
        return question
    
    def confirm_consulta_week_cli(self, week=None):
        question = {
            'type': 'confirm',
            'name': 'validWeek',
            'message': f'Confirmar el numero de semana ({week})',
            'default': True
        }
        return question

    def confirm_consulta_cli(self):
        question = {
            'type': 'confirm',
            'name': 'createConsulta',
            'message': 'Crear Consulta con la informacion anterior?',
            'default': True
        }
        return question



if __name__ == "__main__":
    consultas = ConsultasManagerAir()
    consultas.show_all()

    # from ConsulManager.AirTable.Cobros.CobrosManagerAir import CobrosManagerAir
    # from ConsulManager.AirTable import VALID_PAGOS_ESTATUS as PAGOS_ST
    # cobro = CobrosManagerAir()

    # cobro_record = cobro.create_cobro(monto=0, estatus=PAGOS_ST.PAGADO)
    # log.info(cobro_record['id'])

    # consultas.create_consulta(
    #                             fecha=get_valid_date(),
    #                             cobros=[cobro_record['id']]
    #                             )
    # consultas.get_consulta_data_cli()