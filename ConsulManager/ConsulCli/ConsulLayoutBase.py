from typing import Tuple
from ConsulManager.AirTable.PacientesAir.Pacientes import PacientesAir
import curses
from ConsulManager.ConsulCli.ConsulDataPad import DATAPAD_DICT
from ConsulManager.ConsulCli import LIST_MODE, DATE_PICKER, DINAMIC_LIST, CONFIRM_PICKER, FLOAT_NUMBER
# from ConsulManager.ConsulCli import STATE_TYPE_BASE, STATE_TYPE_EXIT_CONFIRMATION, STATE_TYPE_NEW_MACHINE

# DEFINE MACROS
INITIAL_STATE = "INITIAL_STATE"
FINAL_STATE = "FINAL_STATE"
NEXT_STATE = "NEXT_STATE"
FUNC_STATE = "FUNC_STATE"
KEY_EVENT= "KEY_EVENT"

# GENERIC VIEW
class View(object):
    def __init__(self, data_list=[], s1=1, max_heigth=1, max_width=1,
                mode=LIST_MODE,
                prompt_test="Example Test",
                default_text="< Nombre y/o telefono >",
                default_data=None,
                generate_list_func=None,
                upper=False):

        # TODO: change in % values
        self.data_pad = DATAPAD_DICT[mode](
            curses=curses,
            data = data_list,
            width = s1*5,
            max_heigth = max_heigth,
            max_width = max_width,
            start_y = 1,
            start_x= s1*7,
            generate_list_func=generate_list_func,
            default_text=default_text,
            default_data=default_data,
        )

        # set prompt_windows
        self.__max_x_prompt_window = (s1*7)-1
        self.__max_y_prompt_window = max_heigth - 1
        self.__prompt = curses.newwin(self.__max_y_prompt_window, self.__max_x_prompt_window, 1, 0)
        self.__prompt_text = prompt_test
        self.refresh()
    
    def process_key(self, key=None):
        return self.data_pad.process_key(key=key)
    
    def refresh_prompt(self):
        self.__prompt.clear()

        # get the chunks in the prompt
        n = self.__max_x_prompt_window - 1
        chunks = [self.__prompt_text[i:i+n] for i in range(0, len(self.__prompt_text), n)]
        index = 0

        # split the string in chunk of the size of the windows
        for chunk in chunks[:self.__max_y_prompt_window]:
            self.__prompt.addstr(index, 0, chunk)
            index += 1
        self.__prompt.refresh()

    def refresh(self):
        self.refresh_prompt()
        self.data_pad.refresh_data()


class consulLayoutBase(object):
    # define init values
    # size variables
    max_heigth = 0
    max_width = 0
    S1 = 0
    # view
    # view = None
    # function_call = None
    # logic variables
    # exit_app = False
    # # store info
    # data_list = []
    # data = {}
    # state machine
    state_machine = {}
    def __init__(self, init_state=INITIAL_STATE, debug_mode=False):
        # basci variables
        
        # self.state_machine = state_machine
        self.current_state = init_state
        self.debug_mode = debug_mode
        self.stdscr = None
        self.data={}
        self.data_list=[]

        
        self.state_machine = {}
        self.exit_app = False
        self.view=None
        self.function_call = None

        self.external_init()
        self.set_state_machine()
    
    # Rewrite functions
    def external_init(self):
        """ this function will be used to adicional intialization"""
        # self.__pacientes_table = PacientesAir()
        # self.__pacientes_table.update_pacientes_list()
        # self.function_call = self.__pacientes_table.find_paciente
        pass

    def set_state_machine(self):
        self.state_machine = {
            INITIAL_STATE:{
                NEXT_STATE:FINAL_STATE,
                FUNC_STATE:self.inital_state,
                KEY_EVENT:self.update_choice_from_view,
                "KEY":"CONSULTA_DATE"
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
            prompt_test="[NUEVA CONSULTA] Selecione la fecha de la consulta:")
        pass

    def final_state(self, stdscr=None):
        self.create_view(stdscr=stdscr,
                    data_list=None,
                    mode=CONFIRM_PICKER,
                    prompt_test="[NUEVA CONSULTA] Desea crear una nueva consulta?:",
                    default_text=None,
                    default_data=None,
                    generate_list_func=self.function_call)
        pass

    def update_choice_from_view(self, choice=None):
        if choice is None:
            return False

        self.data[self.state_machine[self.current_state]["KEY"]] = choice
        self.current_state = self.state_machine[self.current_state][NEXT_STATE]
        return True

    def comfirn_exit_choice(self, choice=None):
        if choice is None:
            return False

        self.data_list.append(self.data)
        self.data = {}
        if choice is True:
            self.current_state = INITIAL_STATE
        else:
            self.current_state = None
        return True

    # based functions
    def update_screen_size(self, stdscr=None):
        if stdscr is not None:
            self.max_heigth, self.max_width = stdscr.getmaxyx()
            self.S1 = int(self.max_width / 12)

    def clean_layout(self, stdscr=None):
        stdscr.clear()
        if self.debug_mode:
            stdscr.addstr(0, 0, f"[DEBUG MODE]{self.current_state}")

    def get_data(self):
        return self.data_list

    def create_view(self,
                    stdscr=None,
                    data=None,
                    mode=None,
                    prompt_test=None,
                    default_text=None,
                    default_data=None,
                    generate_list_func=None):
        # create view
        self.view = View(s1=self.S1,
                            max_heigth=self.max_heigth,
                            max_width=self.max_width,
                            # editable
                            data_list=data,
                            mode=mode,
                            prompt_test=prompt_test,
                            default_text=default_text,
                            default_data=default_data,
                            generate_list_func=generate_list_func
                        )
        stdscr.refresh()
        self.view.refresh()


    
    def run(self, stdscr):
        self.stdscr = stdscr
        self.update_screen_size(stdscr=stdscr)

        while self.exit_app is False:
            if self.state_machine is None:
                return False

            self.clean_layout(stdscr=stdscr)

            # create view
            if self.current_state in self.state_machine.keys():
                self.state_machine[self.current_state][FUNC_STATE](stdscr=stdscr)
            else:
                return True
            self.proccess_key_event(stdscr=stdscr)

            

    def proccess_key_event(self, stdscr=None):
        if stdscr is None:
            return False

        while True:
            key = stdscr.getkey()
            # Escape key
            if key == chr(27):
                self.exit_app = True
                return True
            # CTRL + C
            if key == chr(3):
                self.exit_app = True
                return True
            
            stdscr.clear()

            if self.state_machine[self.current_state][KEY_EVENT] is None:
                return True

            choice = self.view.process_key(key=key)
            if self.state_machine[self.current_state][KEY_EVENT](choice):
                return True
            # self.choice = self.view.process_key(key=key)

            # if self.view is not None:
            #     self.choice = self.view.process_key(key=key)

            #     if self.choice is not None:
                    
            #         # CONFIRM EXIT 
            #         if self.state_machine[self.current_state]["type"] == STATE_TYPE_EXIT_CONFIRMATION:
            #             self.data_list.append(self.data)
            #             self.data = {}
            #             self.current_state = self.state_machine[self.current_state]["confirm_options"][self.choice]
            #             return True

            #         # NEW MACHINE
            #         if self.state_machine[self.current_state]["type"] == STATE_TYPE_NEW_MACHINE:
            #             if self.choice is False:
            #                 self.current_state = self.state_machine[self.current_state]["next_state"]
            #                 return True

            #             # overwrite date
            #             if self.state_machine[self.current_state]["set_default_data"] is not None:
            #                 state_machine = self.state_machine[self.current_state]["state_machine"]
            #                 print(f"xxx: {self.data[self.state_machine[self.current_state]['set_default_data']]}")
            #                 for state in state_machine.values():
            #                     state["default_data"] = self.data[self.state_machine[self.current_state]["set_default_data"]]

            #             new_machine = consulLayoutBase(state_machine=self.state_machine[self.current_state]["state_machine"],
            #                                     init_state=self.state_machine[self.current_state]["init_state"],
            #                                     pacientes_table=False)
            #             new_machine.run(self.stdscr)
            #             self.data[self.state_machine[self.current_state]["key"]] = new_machine.get_data()
            #             self.current_state = self.state_machine[self.current_state]["next_state"]
            #             return True

            #         # BASE STATE
            #         if self.state_machine[self.current_state]["type"] == STATE_TYPE_BASE:
            #             self.data[self.state_machine[self.current_state]["key"]] = self.choice
            #             # update next state
            #             self.current_state = self.state_machine[self.current_state]["next_state"]
            #             return True

            if self.debug_mode:
                stdscr.addstr(4,0, f'key:: {key}')
                stdscr.addstr(5,0, f'choice:: {choice}')
            stdscr.refresh()
            self.view.refresh()

if __name__ == '__main__':
    #  test state machine
    app = consulLayoutBase(debug_mode=True)
    curses.wrapper(app.run)
    data = app.get_data()
    for consulta in data:
        for key in consulta.keys():
            print(f"{key}: {consulta[key]}")
        