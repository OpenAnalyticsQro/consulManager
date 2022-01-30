from ConsulManager.ConsulCli.ConsulLayoutBase import consulLayoutBase, INITIAL_STATE, FINAL_STATE, NEXT_STATE, FUNC_STATE, KEY_EVENT
from ConsulManager.ConsulCli import DINAMIC_LIST_AIR, LIST_MODE, DATE_PICKER, DINAMIC_LIST, CONFIRM_PICKER, FLOAT_NUMBER
from ConsulManager.AirTable import PAGOS_ESTATUS_LIST, VALID_CUENTAS_LIST, FACTURA_STATUS_LIST, DENTISTAS_LIST
from ConsulManager.AirTable.PacientesAir.Pacientes import PacientesAir
from ConsulManager.ConsulCli.newCobroApp import newCobroApp
from ConsulManager.ConsulCli.newPagoApp import newPagoApp
from ConsulManager.ConsulCli.newPacienteApp import newPacienteApp
from ConsulManager.ConsulCli.newTratamientoApp import newTratamientoApp

class newConsultaApp(consulLayoutBase):
    def __init__(self,init_state=INITIAL_STATE, debug_mode=False):
        super().__init__(init_state, debug_mode)
        self.__pacientes_table = PacientesAir()
        self.__pacientes_table.update_pacientes_list()
        self.function_call = self.__pacientes_table.find_paciente
        self.new_paciente = "<< NUEVO PACIENTE >>"

    def set_state_machine(self):
        self.state_machine = {
            INITIAL_STATE:{
                NEXT_STATE:"GET_PACIENTE_ID_ST",
                FUNC_STATE:self.inital_state,
                KEY_EVENT:self.update_choice_from_view,
                "KEY":"fecha"
                },
            "GET_PACIENTE_ID_ST":{
                NEXT_STATE:"GET_TRATAMIENTO_ID_ST",
                FUNC_STATE:self.consulta_paciente_id,
                KEY_EVENT:self.validate_new_paciente,
                "KEY":"paciente"
            },
            "GET_TRATAMIENTO_ID_ST":{
                NEXT_STATE:"GET_DENTISTA_ID_ST",
                FUNC_STATE:self.consulta_tratamiento_id,
                KEY_EVENT:self.start_tratamientos_app,
                "KEY":"tratatamiento_id"
            },
            "GET_DENTISTA_ID_ST":{
                NEXT_STATE:"GET_CONSULTA_NEW_COBRO",
                FUNC_STATE:self.consulta_dentista_id,
                KEY_EVENT:self.update_choice_from_view,
                "KEY":"dentista"
            },
            "GET_CONSULTA_NEW_COBRO":{
                NEXT_STATE:"GET_CONSULTA_NEW_PAGO",
                FUNC_STATE:self.consulta_cobros,
                KEY_EVENT:self.start_cobros_app,
                "KEY":"cobros"
            },
            "GET_CONSULTA_NEW_PAGO":{
                NEXT_STATE:FINAL_STATE,
                FUNC_STATE:self.consulta_pagos,
                KEY_EVENT:self.start_pagos_app,
                "KEY":"pagos_dentistas"
            },
            FINAL_STATE:{
                NEXT_STATE:None,
                FUNC_STATE:self.final_state,
                KEY_EVENT:self.comfirn_exit_choice,
                "KEY":None,
            }
        }
        pass
    
    def inital_state(self, stdscr=None):
        self.create_view(stdscr=stdscr,
            mode=DATE_PICKER,
            prompt_test="[NUEVA CONSULTA] Selecione la fecha de la consulta:",
            default_data=None)
    
    def consulta_paciente_id(self, stdscr=None):
        self.create_view(stdscr=stdscr,
            mode=DINAMIC_LIST_AIR,
            prompt_test="[NUEVA CONSULTA] Selecione al Paciente:",
            default_text="<< Nombre y/o telefono >>",
            default_data=self.new_paciente,
            generate_list_func=self.function_call
            )
    
    def validate_new_paciente(self, choice=None):
        if choice is None:
            return False

        
        if choice == 0:
            paciente_app = newPacienteApp()
            paciente_app.run(stdscr=self.stdscr)
            record = paciente_app.get_recor_id()
            self.__pacientes_table.update_pacientes_list()
            return True

        # self.data_list.append({self.state_machine[self.current_state]["KEY"]:choice})
        self.data[self.state_machine[self.current_state]["KEY"]] = choice
        self.current_state = self.state_machine[self.current_state][NEXT_STATE]
        return True

    def consulta_tratamiento_id(self, stdscr=None):
        self.create_view(stdscr=stdscr,
                    data_list=None,
                    mode=CONFIRM_PICKER,
                    prompt_test="[NUEVA CONSULTA] Desea Agregar un nuevo TRATAMIENTO:",
                    default_text=None,
                    default_data=None,
                    generate_list_func=None)
    
    def start_tratamientos_app(self, choice=None):
        if choice is None:
            return False

        if choice is True:
            tratamiento_app = newTratamientoApp()
            tratamiento_app.run(stdscr=self.stdscr)
            self.data[self.state_machine[self.current_state]["KEY"]] = tratamiento_app.get_data()
        else:
            self.data[self.state_machine[self.current_state]["KEY"]] = None

        self.current_state = self.state_machine[self.current_state][NEXT_STATE]
        return True

    def consulta_dentista_id(self, stdscr=None):
        self.create_view(stdscr=stdscr,
                    data_list=DENTISTAS_LIST,
                    mode=LIST_MODE,
                    prompt_test="[NUEVA CONSULTA] Selecione al Dentista:",
                    default_text=None,
                    default_data=None,
                    generate_list_func=self.function_call)

    def consulta_cobros(self, stdscr=None):
        self.create_view(stdscr=stdscr,
                    data_list=None,
                    mode=CONFIRM_PICKER,
                    prompt_test="[NUEVA CONSULTA] Desea Agregar un COBRO:",
                    default_text=None,
                    default_data=None,
                    generate_list_func=self.function_call)

    def start_cobros_app(self, choice=None):
        if choice is None:
            return False

        if choice is True:
            cobro_app = newCobroApp(default_date=self.data["fecha"])
            cobro_app.run(stdscr=self.stdscr)
            self.data[self.state_machine[self.current_state]["KEY"]] = cobro_app.get_data()
        else:
            self.data[self.state_machine[self.current_state]["KEY"]] = None

        self.current_state = self.state_machine[self.current_state][NEXT_STATE]
        return True
        
    def consulta_pagos(self, stdscr=None):
        self.create_view(stdscr=stdscr,
                    data_list=None,
                    mode=CONFIRM_PICKER,
                    prompt_test="[NUEVA CONSULTA] Desea Agregar un Pago:",
                    default_text=None,
                    default_data=None,
                    generate_list_func=self.function_call)
    
    def start_pagos_app(self, choice=None):
        if choice is None:
            return False

        if choice is True:
            pago_app = newPagoApp(default_date=self.data["fecha"])
            pago_app.run(stdscr=self.stdscr)
            self.data[self.state_machine[self.current_state]["KEY"]] = pago_app.get_data()
        else:
            self.data[self.state_machine[self.current_state]["KEY"]] = None

        self.current_state = self.state_machine[self.current_state][NEXT_STATE]
        return True
    

    def final_state(self, stdscr=None):
        self.create_view(stdscr=stdscr,
                    data_list=None,
                    mode=CONFIRM_PICKER,
                    prompt_test="[NUEVA CONSULTA] Desea crear una nueva consulta?:",
                    default_text=None,
                    default_data=None,
                    generate_list_func=self.function_call)
        pass

if __name__ == '__main__':
    #  test state machine
    import curses

    app = newConsultaApp(debug_mode=True)
    curses.wrapper(app.run)
    data = app.get_data()
    for consulta in data:
        for key in consulta.keys():
            print(f"{key}: {consulta[key]}")
        print("-----------")
    
    