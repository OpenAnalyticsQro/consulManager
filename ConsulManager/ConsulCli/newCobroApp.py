from ConsulManager.ConsulCli.ConsulLayoutBase import consulLayoutBase, INITIAL_STATE, FINAL_STATE, NEXT_STATE, FUNC_STATE, KEY_EVENT
from ConsulManager.ConsulCli import LIST_MODE, DATE_PICKER, DINAMIC_LIST, CONFIRM_PICKER, FLOAT_NUMBER
from ConsulManager.AirTable import PAGOS_ESTATUS_LIST, VALID_CUENTAS_LIST, FACTURA_STATUS_LIST

class newCobroApp(consulLayoutBase):
    def __init__(self,init_state=INITIAL_STATE, debug_mode=False, default_date="11/03/2022"):
        super().__init__(init_state, debug_mode)
        self.default_date = default_date

    def set_state_machine(self):
        self.state_machine = {
            INITIAL_STATE:{
                NEXT_STATE:"GET_COBRO_MONTO_ST",
                FUNC_STATE:self.inital_state,
                KEY_EVENT:self.update_choice_from_view,
                "KEY":"fecha"
                },
            "GET_COBRO_MONTO_ST":{
                NEXT_STATE:"GET_COBRO_CUENTA_ST",
                FUNC_STATE:self.cobro_monto_state,
                KEY_EVENT:self.update_choice_from_view,
                "KEY":"monto"
            },
            "GET_COBRO_CUENTA_ST":{
                NEXT_STATE:"GET_COBRO_ESTATUS_ST",
                FUNC_STATE:self.cobro_cuenta_state,
                KEY_EVENT:self.update_choice_from_view,
                "KEY":"cuenta"
            },
            "GET_COBRO_ESTATUS_ST":{
                NEXT_STATE:"GET_COBROS_FACTURA_ST",
                FUNC_STATE:self.estado_cuenta_state,
                KEY_EVENT:self.update_choice_from_view,
                "KEY":"estatus"
            },
            "GET_COBROS_FACTURA_ST":{
                NEXT_STATE:FINAL_STATE,
                FUNC_STATE:self.cobro_factura_estatus,
                KEY_EVENT:self.update_choice_from_view,
                "KEY":"factura"
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
            prompt_test="[NUEVO COBRO] Selecione la fecha del COBRO:",
            default_data=self.default_date)
    
    def cobro_monto_state(self, stdscr=None):
        self.create_view(stdscr=stdscr,
            mode=FLOAT_NUMBER,
            prompt_test="[NUEVO COBRO] Escriba el monto:")

    def cobro_cuenta_state(self, stdscr=None):
        self.create_view(stdscr=stdscr,
                    data=VALID_CUENTAS_LIST,
                    mode=LIST_MODE,
                    prompt_test="[NUEVO COBRO] seleccione la cuenta:",
                    default_text=None,
                    default_data=None,
                    generate_list_func=self.function_call)

    def estado_cuenta_state(self, stdscr=None):
        self.create_view(stdscr=stdscr,
                    data=PAGOS_ESTATUS_LIST,
                    mode=LIST_MODE,
                    prompt_test="[NUEVO COBRO] seleccione el estado del COBRO:",
                    default_text=None,
                    default_data=None,
                    generate_list_func=self.function_call)

    def cobro_factura_estatus(self, stdscr=None):
        self.create_view(stdscr=stdscr,
                    data=FACTURA_STATUS_LIST,
                    mode=LIST_MODE,
                    prompt_test="[NUEVO COBRO] seleccione el estado de la Factura:",
                    default_text=None,
                    default_data=None,
                    generate_list_func=self.function_call)

    def final_state(self, stdscr=None):
        self.create_view(stdscr=stdscr,
                    data=None,
                    mode=CONFIRM_PICKER,
                    prompt_test="[NUEVO COBRO] Desea crear un COBRO nuevo?:",
                    default_text=None,
                    default_data=None,
                    generate_list_func=self.function_call)
        pass

if __name__ == '__main__':
    #  test state machine
    import curses

    app = newCobroApp(debug_mode=True)
    curses.wrapper(app.run)
    data = app.get_data()
    for consulta in data:
        for key in consulta.keys():
            print(f"{key}: {consulta[key]}")
        print("-----------")
    
    