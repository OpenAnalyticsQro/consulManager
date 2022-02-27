import ConsulManager.env
from ConsulManager.Logger import logger as log
from pyairtable import Table
from os import getenv
from ConsulManager.AirTable import (
    AIRTABLE_API_KEY,
    CONSULTORIO_2022_BASE_ID_AIR_TABLE,
    COBROS_TABLE_NAME_AIR_TABLE,
)
from ConsulManager.AirTable.Cobros import FIELD as FD
from ConsulManager.AirTable.Utilities import Validators
from ConsulManager.AirTable.Utilities.Fechas import get_valid_date
#from ConsulManager.ConsulCli.validator import dateValidator, MontoValidator
from ConsulManager.AirTable import PAGOS_ESTATUS_LIST, VALID_CUENTAS_LIST
import re


class CobrosManagerAir(object):
    def __init__(self):
        self.__table = Table(
            api_key=getenv(AIRTABLE_API_KEY),
            base_id=getenv(CONSULTORIO_2022_BASE_ID_AIR_TABLE),
            table_name=getenv(COBROS_TABLE_NAME_AIR_TABLE),
        )
        self.__data = {}

    def show_all(self):
        try:
            for item in self.__table.all():
                print(item)
        except Exception as e:
            log.error(f"{self.__class__.show_all.__qualname__}: {e}")

    def create_cobro(self, monto=None, cuenta=None, estatus=None, fecha=None, factura=None, semana=None):
        if Validators.valid_currency(value=monto) is False:
            log.error(
                f"{self.__class__.create_cobro.__qualname__}: invalid monto: {monto}"
            )
            return None
        if Validators.valid_cuenta(value=cuenta) is False:
            log.error(
                f"{self.__class__.create_cobro.__qualname__}: invalid cuenta: {cuenta}"
            )
            return None
        if Validators.valid_pago_estatus(value=estatus) is False:
            log.error(
                f"{self.__class__.create_cobro.__qualname__}: invalid estatus: {estatus}"
            )
            return None
        try:
            record = self.__table.create(
                {FD.MONTO: monto, FD.CUENTA: cuenta, FD.ESTATUS: estatus, FD.FECHA: fecha, FD.FACTURA: factura, FD.SEMANA: semana}
            )
            return record
        except Exception as e:
            log.error(f"{self.__class__.create_cobro.__qualname__}: {e}")

    # COMMAND LINE COMMANDS
    def get_cobros_data_cli(self, default_date="01/01/2022"):
        questions_list = []
        questions_list.append(self.get_date_cli(default_date=default_date))
        questions_list.append(self.get_monto_cli())
        questions_list.append(self.get_valid_cuenta_cli())
        questions_list.append(self.get_valid_cobro_status_cli())
        print("Crear un Nuevo Cobro:")
        answers = prompt(questions_list, style=custom_style_3)
        print(answers)
        print(self.print_cobro_cli(answers=answers))
        answers_confirm = prompt([self.confirm_cobro_cli()], style=custom_style_3)
        
        if answers_confirm['createCobro']:
            valid_date = re.compile(r'(\d\d)\/(\d\d)\/(\d\d\d\d)')
            (day, month, year) = valid_date.match(string=answers['date']).groups()
            return self.create_cobro(
                monto=float(answers['monto']),
                cuenta=answers['cuenta'],
                estatus=answers['pago_status'],
                fecha=get_valid_date(year=int(year), month=int(month), day=int(day)),
            )
        return None
    
    def print_cobro_cli(self, answers={}):
        if answers is {}:
            return ""
        return f"NUEVO Cobro:\n  *Fecha: {answers['date']}\n  *Monto: ${answers['monto']}-{answers['cuenta']}-{answers['pago_status']}"

    def confirm_cobro_cli(self):
        question = {
            'type': 'confirm',
            'name': 'createCobro',
            'message': 'Crear Cobro con la informacion anterior?',
            'default': True
        }
        return question

    def get_date_cli(self, default_date=None):
        question = {
            "type": "input",
            "name": "date",
            "message": "Fecha (DD/MM/YYY):",
            "default": f"{default_date}",
            "validate": dateValidator,
            }
        return question

    def get_monto_cli(self):
        question = {
            "type": "input",
            "name": "monto",
            "message": "Monto: ",
            "validate": MontoValidator
        }
        return question

    def get_valid_cuenta_cli(self):
        question = {
            "type": "rawlist",
            "name": "cuenta",
            'message': 'Cuenta de Abono: ',
            'choices': VALID_CUENTAS_LIST
        }
        return question

    def get_valid_cobro_status_cli(self):
        question = {
            "type": "rawlist",
            "name": "pago_status",
            'message': 'Estatus del Pago: ',
            'choices': PAGOS_ESTATUS_LIST
        }
        return question



if __name__ == "__main__":
    from ConsulManager.AirTable import VALID_PAGOS_ESTATUS, VALID_CUENTAS_AIR_TABLE
    
    from pyairtable.utils import datetime_to_iso_str

    log.info("Hola Mundo")
    cobros_table = CobrosManagerAir()
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
