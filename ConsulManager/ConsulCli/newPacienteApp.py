from tarfile import RECORDSIZE
from ConsulManager.ConsulCli.ConsulLayoutBase import consulLayoutBase, INITIAL_STATE, FINAL_STATE, NEXT_STATE, FUNC_STATE, KEY_EVENT
from ConsulManager.ConsulCli import LIST_MODE, DATE_PICKER, DINAMIC_LIST, CONFIRM_PICKER, FLOAT_NUMBER, STR_BOX, PHONE_NUMBER
from ConsulManager.AirTable import PAGOS_ESTATUS_LIST, VALID_CUENTAS_LIST, FACTURA_STATUS_LIST
from ConsulManager.AirTable.PacientesAir.Pacientes import PacientesAir

class newPacienteApp(consulLayoutBase):
    def __init__(self,init_state=INITIAL_STATE, debug_mode=False, default_date="11/03/2022"):
        super().__init__(init_state, debug_mode)
        self.default_date = default_date
        self.record = None
        self.pacientes_table = PacientesAir()

    def set_state_machine(self):
        self.state_machine = {
            INITIAL_STATE:{
                NEXT_STATE:"GET_PACIENTE_APELLIDO_ST",
                FUNC_STATE:self.inital_state,
                KEY_EVENT:self.update_choice_from_view,
                "KEY":"name"
                },
            "GET_PACIENTE_APELLIDO_ST":{
                NEXT_STATE:"GET_PACIENTE_PHONE_ST",
                FUNC_STATE:self.paciente_apellido_state,
                KEY_EVENT:self.update_choice_from_view,
                "KEY":"apellidos"
            },
            "GET_PACIENTE_PHONE_ST":{
                NEXT_STATE:FINAL_STATE,
                FUNC_STATE:self.paciente_phone_state,
                KEY_EVENT:self.update_choice_from_view,
                "KEY":"telefono"
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
            mode=STR_BOX,
            prompt_test="[NUEVO PACIENTE] Escriba el/los Nombre(s):",
            default_text="<< NOMBRE(S) >>")
    
    def paciente_apellido_state(self, stdscr=None):
        self.create_view(stdscr=stdscr,
            mode=STR_BOX,
            prompt_test="[NUEVO PACIENTE] Escriba el/los APELLIDO(s):",
            default_text="<< APELLIDO(S) >>")

    def paciente_phone_state(self, stdscr=None):
        self.create_view(stdscr=stdscr,
            mode=PHONE_NUMBER,
            prompt_test="[NUEVO PACIENTE] Escriba el numero telefonico:",
            default_text="<< NUMERO DE TELEFONO >>")

    def final_state(self, stdscr=None):
        self.create_view(stdscr=stdscr,
                    data_list=None,
                    mode=CONFIRM_PICKER,
                    prompt_test="[NUEVO PACIENTE] Desea crear al nuevo PACIENTE?:",
                    default_text=None,
                    default_data=None,
                    generate_list_func=self.function_call)

    def comfirn_exit_choice(self, choice=None):
        if choice is None:
            return False

        if choice is True:
            self.current_state = None
            self.record = self.pacientes_table.create_paciente(**self.data)
            # print(f"data: {self.data}")
            # print(f"se creo paciente: {self.record['id']}")
            self.data_list.append(self.data)
            self.data = {}
        else:
            self.current_state = INITIAL_STATE
        return True
    
    def get_recor_id(self):
        return self.record

if __name__ == '__main__':
    #  test state machine
    import curses

    app = newPacienteApp(debug_mode=True)
    curses.wrapper(app.run)
    data = app.get_data()
    for consulta in data:
        for key in consulta.keys():
            print(f"{key}: {consulta[key]}")
        print("-----------")
    record = app.get_recor_id()
    print(f"record id: {record}")
    
    