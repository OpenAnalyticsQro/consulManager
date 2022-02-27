from ConsulManager.ConsulCli.ConsulLayoutBase import consulLayoutBase, INITIAL_STATE, FINAL_STATE, NEXT_STATE, FUNC_STATE, KEY_EVENT
from ConsulManager.ConsulCli import DINAMIC_LIST_AIR, LIST_MODE, DATE_PICKER, DINAMIC_LIST, CONFIRM_PICKER, FLOAT_NUMBER, INT_NUMBER
from ConsulManager.AirTable import PAGOS_ESTATUS_LIST, VALID_CUENTAS_LIST, FACTURA_STATUS_LIST, DENTISTAS_LIST
from ConsulManager.AirTable.ListaTratamientos.ListaTratamientosAir import ListaTratamientosAir



class newTratamientoApp(consulLayoutBase):
    def __init__(self,init_state=INITIAL_STATE, debug_mode=False, default_date="11/03/2022"):
        super().__init__(init_state, debug_mode)
        self.__tartamientos_table = ListaTratamientosAir()
        self.__tartamientos_table.update_tratamientos_list()
        self.function_call = self.__tartamientos_table.find_tratamiento
        self.default_date = default_date

    def set_state_machine(self):
        self.state_machine = {
            INITIAL_STATE:{
                NEXT_STATE:"SET_DATE_ST",
                FUNC_STATE:self.inital_state,
                KEY_EVENT:self.update_choice_from_view,
                "KEY":"tratamiento"
                },

            "SET_DATE_ST":{
                NEXT_STATE:"GET_CANTIDAD_ST",
                FUNC_STATE:self.set_date,
                KEY_EVENT:self.update_choice_from_view,
                "KEY":"fecha"
                },

            
            "GET_CANTIDAD_ST":{
                NEXT_STATE:"GET_COSTO_FINAL_ST",
                FUNC_STATE:self.tratamiento_get_cantidad_id,
                KEY_EVENT:self.update_choice_from_view,
                "KEY":"cantidad"
            },
            "GET_COSTO_FINAL_ST":{
                NEXT_STATE:None,
                FUNC_STATE:self.tratamiento_get_costo_final_id,
                KEY_EVENT:self.exit_choice_from_view,
                "KEY":"costo_final"
            },
            FINAL_STATE:{
                NEXT_STATE:None,
                FUNC_STATE:self.final_state,
                KEY_EVENT:None,
                "KEY":None,
            }
        }
        pass
    
    def inital_state(self, stdscr=None):
        self.create_view(stdscr=stdscr,
            mode=DINAMIC_LIST_AIR,
            prompt_test="[NUEVA TRATAMIENTO] Selecione el TRATAMIENTO:",
            default_text="<< Seleccione el Tratamiento >>",
            default_data=None,
            generate_list_func=self.function_call
            )

    def set_date(self, stdscr=None):
        self.create_view(stdscr=stdscr,
            mode=DATE_PICKER,
            prompt_test="[NUEVO TRATAMIENTO] Selecione la fecha del inicio del TRATAMIENTO:",
            default_data=self.default_date)
    
    def tratamiento_get_cantidad_id(self, stdscr=None):
        self.create_view(stdscr=stdscr,
            mode=INT_NUMBER,
            prompt_test="[NUEVA TRATAMIENTO] Selecione la cantidad de tratamientos:",
            default_text=None,
            generate_list_func=self.function_call
            )

    def tratamiento_get_costo_final_id(self, stdscr=None):
        costo_sugerido = self.__tartamientos_table.get_costo_sugerido(self.data["tratamiento"])
        if costo_sugerido is None:
            costo_sugerido = 0
        cantidad = self.data["cantidad"]
        self.create_view(stdscr=stdscr,
            mode=FLOAT_NUMBER,
            prompt_test=f"[NUEVA TRATAMIENTO] Selecione el COSTO FINAL: ",
            default_data=costo_sugerido*cantidad,
            generate_list_func=self.function_call
            )
    
    def exit_choice_from_view(self, choice=None):
        if choice is None:
            return False

        # self.data_list.append({self.state_machine[self.current_state]["KEY"]:choice})
        self.data[self.state_machine[self.current_state]["KEY"]] = choice
        self.current_state = self.state_machine[self.current_state][NEXT_STATE]
        self.data_list.append(self.data)
        return True
        pass

    def final_state(self, stdscr=None):
        # self.create_view(stdscr=stdscr,
        #             data_list=None,
        #             mode=CONFIRM_PICKER,
        #             prompt_test="[NUEVA TRATAMIENTO] Desea crear un nuevo Tratamiento?:",
        #             default_text=None,
        #             default_data=None,
        #             generate_list_func=self.function_call)
        self.current_state=None
        pass

if __name__ == '__main__':
    #  test state machine
    import curses

    app = newTratamientoApp(debug_mode=True)
    curses.wrapper(app.run)
    data = app.get_data()
    for consulta in data:
        for key in consulta.keys():
            print(f"{key}: {consulta[key]}")
        print("-----------")
    
    