from idna import check_initial_combiner
from ConsulManager.ConsulCli import DINAMIC_LIST_AIR, LIST_MODE, DINAMIC_LIST, DATE_PICKER, MONTHS_DICT, CONFIRM_PICKER, FLOAT_NUMBER, INT_NUMBER, STR_BOX, PHONE_NUMBER
# from ConsulManager.ConsulCli.ConsulLayoutBase import View
from datetime import date
import re
import curses





class DataPad(object):
    __select_index = -1
    def __init__(self, curses=None, heigth=150, width=30, data=[], max_width=0,
                max_heigth=0, start_x=67, start_y=1, mode=LIST_MODE,
                generate_list_func=None,
                default_text=""):
        self.__heigth = heigth
        self.__width = width
        self.__startx = start_x
        self.__starty = start_y
        self.__curses = curses
        self.__generate_list_func = generate_list_func
        self.__default_text = default_text
        self.update_mode(mode=mode)
        self.__update_max_dsp(width=width + start_x, heigth=heigth + start_y, max_width=max_width, max_heigth=max_heigth)
        self.__pad = self.__curses.newpad(self.__heigth, self.__width)
        self.__proccess_key = {}

        # text area
        self.update_area(x=0, y=0)

        # display area
        self.__update_dsp_area_ul(start_x=self.__startx, start_y=self.__starty)
        self.__update_dsp_area_lr(end_x=self.__dsp_area_ul_x + self.__width, end_y=self.__dsp_area_ul_y + self.__heigth)

        # data
        # self.set_data_list(data=data)
        self.init_selected_mode(data=data)
        self.update_data_screen()

        # init
        self.__init_procces_key()

    def update_mode(self, mode=LIST_MODE):
        self.__mode = mode

    # rewrite this functions
    def init_selected_mode(self, data=[]):
        if self.__mode == LIST_MODE:
            self.set_data_list(data=data)
        if self.__mode == DATE_PICKER:
            self.set_data_picker()
        if self.__mode == DINAMIC_LIST:
            self.set_dinamic_list()

    def update_data_screen(self):
        if self.__mode == LIST_MODE:
            self.update_data_list()
        if self.__mode == DATE_PICKER:
            self.update_date_picker()
        if self.__mode == DINAMIC_LIST:
            self.update_dinamic_list()

    def get_choice(self):
        if self.__select_index == -1:
            return None
        if self.__select_index >= len(self.__data):
            return None
        return self.__data[self.__select_index]

    def __init_procces_key(self):
        if self.__mode == LIST_MODE:
            self.__proccess_key = {
                "KEY_C2" : self.index_move_down,        # DOWN_KEY
                "KEY_DOWN" : self.index_move_down,      # DOWN_KEY
                "KEY_A2": self.index_move_up,           # UP_KEY
                "KEY_UP": self.index_move_up,           # UP_KEY
                chr(10): self.get_choice                # ENTER_KEY
            }
        if self.__mode == DATE_PICKER:
            self.__proccess_key = {
                "KEY_B3" : self.move_index_rigth_date_picker,       # KEY_RIGHT
                "KEY_RIGHT": self.move_index_rigth_date_picker,     # KEY_RIGTH
                "KEY_B1" : self.move_index_left_date_picker,        # KEY_LEFT
                "KEY_LEFT": self.move_index_left_date_picker,       # KEY_LEFT
                "KEY_A2" : self.move_index_up_date_picker,          # KEY_UP
                "KEY_UP" : self.move_index_up_date_picker,          # KEY_UP
                "KEY_C2" : self.move_index_down_date_picker,        # KEY_DOWN
                "KEY_DOWN": self.move_index_down_date_picker,       # KEY_DOWN
                chr(10): self.get_choice_data_picker,               # KEY_ENTER
            }
        if self.__mode == DINAMIC_LIST:
            self.__proccess_key = {
                chr(8): self.remove_last_chr_dinamic,
                "KEY_C2" : self.move_index_down_d_list,        # KEY_DOWN
                "KEY_DOWN": self.move_index_down_d_list,       # KEY_DOWN
                "KEY_A2" : self.move_index_up_d_list,          # KEY_UP
                "KEY_UP" : self.move_index_up_d_list,          # KEY_UP
                chr(10): self.get_dinamic_list_choice,               # KEY_ENTER
            }

    # Basic functions
    def update_area(self, x=0, y=0):
        self.__text_area_x = x
        self.__text_area_y = y

    def __update_max_dsp(self, heigth=0, width=0, max_width=0, max_heigth=0):
        if heigth >= max_heigth:
            self.__max_dsp_heigth = max_heigth - 1
        else:
            self.__max_dsp_heigth = heigth
        
        if width >= max_width:
            self.__max_dsp_width = max_width - 1
        else:
            self.__max_dsp_width = width

    def __update_dsp_area_lrx(self, end_x=0):
        if end_x < 0:
            self.__dsp_area_lr_x = 0
            return True
        if end_x > self.__max_dsp_width:
            self.__dsp_area_lr_x = self.__max_dsp_width
            return True
        self.__dsp_area_lr_x = end_x
    
    def __update_dsp_area_lry(self, end_y=0):
        if end_y < 0:
            self.__dsp_area_lr_y = 0
            return True
        if end_y > self.__max_dsp_heigth:
            self.__dsp_area_lr_y = self.__max_dsp_heigth
            return True
        self.__dsp_area_lr_y = end_y
    
    def __update_dsp_area_lr(self, end_x=0, end_y=0):
        self.__update_dsp_area_lrx(end_x=end_x)
        self.__update_dsp_area_lry(end_y=end_y)

    def __update_dsp_area_ulx(self, start_x=0):
        if start_x < 0:
            self.__dsp_area_ul_x = 0
            return True
        if start_x > self.__max_dsp_width:
            self.__dsp_area_ul_x = self.__max_dsp_width
            return True
        self.__dsp_area_ul_x = start_x
        return True

    def __update_dsp_area_uly(self, start_y=0):
        if start_y < 0:
            self.__dsp_area_ul_y = 0
            return True
        if start_y > self.__max_dsp_heigth:
            self.__dsp_area_ul_y = self.__max_dsp_heigth
            return True
        self.__dsp_area_ul_y = start_y
        return True

    def __update_dsp_area_ul(self, start_x=0, start_y=0):
        self.__update_dsp_area_ulx(start_x=start_x)
        self.__update_dsp_area_uly(start_y=start_y)

    # Extra function
    def process_key(self, key=None):
        if key is None:
            return None
        if key in self.__proccess_key.keys():
            return self.__proccess_key[key]()

        # Update this function
        # process letter and numbers
        # subtitute this for only process_key_alpha_numeric (rewrited)
        if self.__mode == DINAMIC_LIST:
            return self.process_key_dinamic(key=key)
        if self.__mode == DATE_PICKER:
            return self.process_key_date_picker(key=key)

    # DATA LIST MODE
    def set_data_list(self, data=[]):   #ported
        self.__data = data

    def update_data_list(self, data=None):  #ported
        if data is not None:
            self.__data = data
        
        index = 0
        self.__pad.clear()
        for line in self.__data:
            if self.__select_index == index:
                self.__pad.addstr(index,0, line, self.__curses.A_STANDOUT)
            else:
                self.__pad.addstr(index,0, line)
            index += 1

    def index_move_down(self): #ported
        if self.__select_index >= len(self.__data) - 1:
            pass
        elif self.__select_index < self.__max_dsp_heigth - 1:
            self.__select_index += 1
        else:
            self.__text_area_y +=1
            self.__select_index +=1
        self.update_data_screen()
        self.refresh_data()
        return None

    def index_move_up(self):    # ported
        if self.__select_index == -1:
            return None

        if self.__text_area_y >= 1:
            self.__text_area_y -= 1
            self.__select_index -= 1
        elif self.__select_index == 0:
            pass
        else:
            self.__select_index += -1
        self.update_data_screen()
        self.refresh_data()
        return None

    
    def refresh_data(self, data=[]):
    # Displays a section of the pad in the middle of the screen.
    # (0,0) : coordinate of upper-left corner of pad area to display.
    # (5,5) : coordinate of upper-left corner of window area to be filled
    #         with pad content.
    # (20, 75) : coordinate of lower-right
        self.__pad.refresh(self.__text_area_y,
                            self.__text_area_x,
                            self.__dsp_area_ul_y,
                            self.__dsp_area_ul_x,
                            self.__dsp_area_lr_y,
                            self.__dsp_area_lr_x)
    
    # DATE PICKER MODE
    def move_index_rigth_date_picker(self): # ported
        if self.__select_index < 2:
            self.__select_index +=1
        self.update_date_picker()
        self.refresh_data()
        return None

    def move_index_left_date_picker(self): # ported
        if self.__select_index >= 1:
            self.__select_index -= 1
        self.update_date_picker()
        self.refresh_data()
        return None

    def move_index_up_date_picker(self):    # ported
        if self.__select_index == 0:
            if self.__selected_day >= 1:
                self.__selected_day -= 1
        if self.__select_index == 1:
            if self.__selected_month >= 2:
                self.__selected_month -= 1
        if self.__select_index == 2:
            if self.__selected_year >= 2011:
                self.__selected_year -= 1
        self.set_data_picker(   day=self.__selected_day,
                                month=self.__selected_month,
                                year=self.__selected_year,
                                index=self.__select_index)
        self.update_date_picker()
        self.refresh_data()
        return None

    def move_index_down_date_picker(self): #reported
        if self.__select_index == 0:
            if self.__selected_day < 31:
                self.__selected_day += 1
        if self.__select_index == 1:
            if self.__selected_month < 12:
                self.__selected_month += 1
        if self.__select_index == 2:
            if self.__selected_year < 2050:
                self.__selected_year += 1
        self.set_data_picker(   day=self.__selected_day,
                                month=self.__selected_month,
                                year=self.__selected_year,
                                index=self.__select_index)
        self.update_date_picker()
        self.refresh_data()
        return None

    def update_date_picker(self):   # ported
        self.__pad.clear()
        x_index = 0
        index = 0
        for line in self.__data:
            if line == "/":
                self.__pad.addstr(0, x_index, line)
            elif self.__select_index == index:
                self.__pad.addstr(0, x_index, line, self.__curses.A_STANDOUT)
                index += 1
            else:
                self.__pad.addstr(0, x_index, line)
                index += 1
            x_index += len(line)

    def set_data_picker(self, day=None, month=None, year=None, index = 0): #ported
        today = date.today()

        self.__select_index = index
        self.__buffer_date = ""

        # select day
        if day is None:
            self.__selected_day = today.day
        else:
            self.__selected_day = day

        # select month
        if month is None:
            self.__selected_month = today.month
        else:
            self.__selected_month = month

        # select year
        if year is None:
            self.__selected_year = today.year
        else:
            self.__selected_year = year


        self.__data = [f"{self.__selected_day:02}", "/", f"{MONTHS_DICT[self.__selected_month]}", f"/", f"{self.__selected_year}"]

    def get_choice_data_picker(self): # ported
        return f"{self.__selected_day:02}/{self.__selected_month:02}/{self.__selected_year}"

    def process_key_date_picker(self, key=None): # ported
        if key is None:
            return None
        
        if len(key) > 1:
            return None
        
        if key < '0' or key > '9':
            return None

        # change selected day
        if self.__select_index == 0:
            if len(self.__buffer_date) < 2:
                if int(self.__buffer_date + key) == 0:
                    return None
                if int(self.__buffer_date + key) > 31:
                    self.__buffer_date = key
                else:
                    self.__buffer_date += key
            else:
                if int(key) == 0:
                    return None
                self.__buffer_date = key

            self.__data[0] = f"{int(self.__buffer_date):02}"
            self.__selected_day = int(self.__data[0])
        
        self.update_date_picker()
        self.refresh_data
        return None
        


    # Dinamic List
    def get_dinamic_list_choice(self):  #porte
        if self.__select_index < 1:
            return None
        return self.__data[self.__select_index]

    def move_index_up_d_list(self):  #ported
        if self.__select_index == -1:
            return None

        if self.__text_area_y >= 1:
            self.__text_area_y -= 1
            self.__select_index -= 1
        else:
            self.__select_index += -1
        
        if self.__select_index == 0:
            self.__select_index = -1

        self.update_data_screen()
        self.refresh_data()
        return None

    def move_index_down_d_list(self): # ported
        if self.__select_index >= len(self.__data) - 1:
            return None
        if self.__select_index < self.__max_dsp_heigth - 1:
            self.__select_index += 1
        else:
            self.__text_area_y +=1
            self.__select_index +=1
        
        # skip index 0
        if self.__select_index == 0:
            self.__select_index = 1
        
        # self.__select_index += 1

        self.update_data_screen()
        self.refresh_data()
        return None

    def set_dinamic_list(self, generate_list_func=None):  # ported
        self.__select_index = -1
        self.__valid_text = False
        self.__data = [self.__default_text]
    
    def update_dinamic_list(self): # ported
        self.__pad.clear()
        # self.__pad.addstr(0,0, self.__d_text)
        
        index = 0
        # self.__pad.clear()
        for line in self.__data:
            if self.__select_index == index:
                self.__pad.addstr(index,0, line, self.__curses.A_STANDOUT)
            else:
                self.__pad.addstr(index,0, line)
            index += 1

    def process_key_dinamic(self, key=None): # ported
        if key is None:
            return None
        
        if self.__data[0] == self.__default_text:
            self.__data[0] = ""
        
        if len(key) > 1:
            return None


        if self.__valid_text is False:
            # self.__d_text = ""
            # self.__data[0] = ""
            text = ""
            self.__valid_text = True
        
        text = self.__data[0] + key
        # self.__d_text += key

        # update dianamic list
        # x = ["1","2", "3"]
        self.__data.clear()
        if self.__generate_list_func is not None:
            self.__data = [text] + self.__generate_list_func(text)
        else:
            self.__data = [text]

        self.update_dinamic_list()
        self.refresh_data()

        return None
    
    def remove_last_chr_dinamic(self):
        # self.__d_text = self.__d_text[:-1]
        if self.__data[0] == self.__default_text:
            return None
        if self.__data[0] != "":
            text = self.__data[0][:-1]
            if text == "":
                self.__data.clear()
                self.__data = [self.__default_text]
            else:
                # pass
                self.__data.clear()
                self.__data = [text] + self.__generate_list_func(text)
        else:
            # self.__data.clear()
            self.__data = [self.__default_text]

        self.update_dinamic_list()
        self.refresh_data()
        return None



class DataPadBase(object):
    def __init__(self, curses=None, heigth=150, width=30, data=[], max_width=0,
                max_heigth=0, start_x=67, start_y=1,
                generate_list_func=None,
                default_text="",
                default_data=None):
        # common initialization
        self.curses = curses
        
        self.heigth = heigth
        self.width = width
        self.startx = start_x
        self.starty = start_y

        self.select_index = -1
        self.proccess_key = {}
        self.generate_list_func = None
        self.default_text = ""
        self.data = None

        # common functions
        self.pad = self.curses.newpad(self.heigth, self.width)
        # print("Data created")
        self.update_max_dsp(width=width + start_x, heigth=heigth + start_y, max_width=max_width, max_heigth=max_heigth)
        self.update_area(x=0, y=0)


        # display area
        self.update_dsp_area_ul(start_x=self.startx, start_y=self.starty)
        self.update_dsp_area_lr(end_x=self.dsp_area_ul_x + self.width, end_y=self.dsp_area_ul_y + self.heigth)

        # rewrite this specific function
        self.init()
        # self.update_data_screen()
        self.init_procces_key()

    # rewrite this functions
    def init(self):
        pass

    def update_data_screen(self):
        pass

    def index_move_down(self):
        return None

    def index_move_up(self):
        return None

    def index_move_rigth(self):
        return None
    
    def index_move_left(self):
        return None

    def get_choice(self):
        return None

    def process_key_alpha_numeric(self, key=None):
        return None

    def init_procces_key(self):
        pass

    # Basic functions
    def update_area(self, x=0, y=0):
        self.text_area_x = x
        self.text_area_y = y

    def update_max_dsp(self, heigth=0, width=0, max_width=0, max_heigth=0):
        if heigth >= max_heigth:
            self.max_dsp_heigth = max_heigth - 1
        else:
            self.max_dsp_heigth = heigth
        
        if width >= max_width:
            self.max_dsp_width = max_width - 1
        else:
            self.max_dsp_width = width

    def update_dsp_area_lrx(self, end_x=0):
        if end_x < 0:
            self.dsp_area_lr_x = 0
            return True
        if end_x > self.max_dsp_width:
            self.dsp_area_lr_x = self.max_dsp_width
            return True
        self.dsp_area_lr_x = end_x
    
    def update_dsp_area_lry(self, end_y=0):
        if end_y < 0:
            self.dsp_area_lr_y = 0
            return True
        if end_y > self.max_dsp_heigth:
            self.dsp_area_lr_y = self.max_dsp_heigth
            return True
        self.dsp_area_lr_y = end_y
    
    def update_dsp_area_lr(self, end_x=0, end_y=0):
        self.update_dsp_area_lrx(end_x=end_x)
        self.update_dsp_area_lry(end_y=end_y)

    def update_dsp_area_ulx(self, start_x=0):
        if start_x < 0:
            self.dsp_area_ul_x = 0
            return True
        if start_x > self.max_dsp_width:
            self.dsp_area_ul_x = self.max_dsp_width
            return True
        self.dsp_area_ul_x = start_x
        return True

    def update_dsp_area_uly(self, start_y=0):
        if start_y < 0:
            self.dsp_area_ul_y = 0
            return True
        if start_y > self.max_dsp_heigth:
            self.dsp_area_ul_y = self.max_dsp_heigth
            return True
        self.dsp_area_ul_y = start_y
        return True

    def update_dsp_area_ul(self, start_x=0, start_y=0):
        self.update_dsp_area_ulx(start_x=start_x)
        self.update_dsp_area_uly(start_y=start_y)

    # Extra function
    def process_key(self, key=None):
        if key is None:
            return None
        if key in self.proccess_key.keys():
            return self.proccess_key[key]()

        # Update this function
        # process letter and numbers
        # subtitute this for only process_key_alpha_numeric (rewrited)
        return self.process_key_alpha_numeric(key=key)
        # if self.__mode == DINAMIC_LIST:
        #     return self.process_key_dinamic(key=key)
        # if self.__mode == DATE_PICKER:
        #     return self.process_key_date_picker(key=key)
    
    def refresh_data(self):
    # Displays a section of the pad in the middle of the screen.
    # (0,0) : coordinate of upper-left corner of pad area to display.
    # (5,5) : coordinate of upper-left corner of window area to be filled
    #         with pad content.
    # (20, 75) : coordinate of lower-right
        self.pad.refresh(self.text_area_y,
                            self.text_area_x,
                            self.dsp_area_ul_y,
                            self.dsp_area_ul_x,
                            self.dsp_area_lr_y,
                            self.dsp_area_lr_x)

class DataPadList(DataPadBase):
    def __init__(self, curses=None, heigth=150, width=30, data=[], max_width=0, max_heigth=0, start_x=67, start_y=1, generate_list_func=None, default_text="", default_data=None):
        super(DataPadList, self).__init__(curses=curses, heigth=heigth, width=width, data=data, max_width=max_width, max_heigth=max_heigth, start_x=start_x, start_y=start_y, generate_list_func=generate_list_func, default_text=default_text)
        self.data = data
        self.update_data_screen()
        self.refresh_data()

    def update_data_screen(self):
        index = 0
        self.pad.clear()
        for line in self.data:
            if self.select_index == index:
                self.pad.addstr(index,0, line, self.curses.A_STANDOUT)
            else:
                self.pad.addstr(index,0, line)
            index += 1

    def index_move_down(self):
        if self.select_index >= len(self.data) - 1:
            return None
        if self.select_index < self.max_dsp_heigth - 1:
            self.select_index += 1
        else:
            self.text_area_y +=1
            self.select_index +=1

        self.update_data_screen()
        self.refresh_data()
        return None

    def index_move_up(self):
        if self.select_index == -1:
            return None
        if self.select_index == 0:
            return None

        if self.text_area_y >= 1:
            self.text_area_y -= 1
            self.select_index -= 1
        else:
            self.select_index += -1

        self.update_data_screen()
        self.refresh_data()
        return None

    def get_choice(self):
        if self.select_index == -1:
            return None
        if self.select_index >= len(self.data):
            return None
        return self.data[self.select_index]

    def init_procces_key(self):
        self.proccess_key = {
            "KEY_C2" : self.index_move_down,        # DOWN_KEY
            "KEY_DOWN" : self.index_move_down,      # DOWN_KEY
            "KEY_A2": self.index_move_up,           # UP_KEY
            "KEY_UP": self.index_move_up,           # UP_KEY
            chr(10): self.get_choice                # ENTER_KEY
        }

class DataPadConfirm(DataPadBase):
    def __init__(self, curses=None, heigth=150, width=30, data=[], max_width=0, max_heigth=0, start_x=67, start_y=1, generate_list_func=None, default_text="", default_data=None):
        super(DataPadConfirm, self).__init__(curses=curses, heigth=heigth, width=width, data=data, max_width=max_width, max_heigth=max_heigth, start_x=start_x, start_y=start_y, generate_list_func=generate_list_func, default_text=default_text)
        self.data = ["SI", "NO"]
        self.select_index = 0
        self.update_data_screen()
        self.refresh_data()

    def update_data_screen(self):
        index = 0
        self.pad.clear()
        for line in self.data:
            if self.select_index == index:
                self.pad.addstr(index,0, line, self.curses.A_STANDOUT)
            else:
                self.pad.addstr(index,0, line)
            index += 1

    def index_move_down(self):
        if self.select_index >= len(self.data) - 1:
            return None
        if self.select_index < self.max_dsp_heigth - 1:
            self.select_index += 1
        else:
            self.text_area_y +=1
            self.select_index +=1

        self.update_data_screen()
        self.refresh_data()
        return None

    def index_move_up(self):
        if self.select_index == -1:
            return None
        if self.select_index == 0:
            return None

        if self.text_area_y >= 1:
            self.text_area_y -= 1
            self.select_index -= 1
        else:
            self.select_index += -1

        self.update_data_screen()
        self.refresh_data()
        return None

    def get_choice(self):
        if self.select_index == 0:
            return True
        return False

    def init_procces_key(self):
        self.proccess_key = {
            "KEY_C2" : self.index_move_down,        # DOWN_KEY
            "KEY_DOWN" : self.index_move_down,      # DOWN_KEY
            "KEY_A2": self.index_move_up,           # UP_KEY
            "KEY_UP": self.index_move_up,           # UP_KEY
            chr(10): self.get_choice                # ENTER_KEY
        }

class DataPadDinamicList(DataPadBase):
    def __init__(self, curses=None, heigth=150, width=30, data=[], max_width=0, max_heigth=0, start_x=67, start_y=1, generate_list_func=None, default_text="", default_data=None):
        super(DataPadDinamicList, self).__init__(curses=curses, heigth=heigth, width=width, data=data, max_width=max_width, max_heigth=max_heigth, start_x=start_x, start_y=start_y, generate_list_func=generate_list_func, default_text=default_text)
        self.select_index = -1
        self.valid_text = False
        self.default_text = default_text
        self.data = [self.default_text]
        self.generate_list_func = generate_list_func

        self.update_data_screen()
        self.refresh_data()

    def update_data_screen(self):
        self.pad.clear()
        
        index = 0
        for line in self.data:
            if self.select_index == index:
                self.pad.addstr(index,0, line, self.curses.A_STANDOUT)
            else:
                self.pad.addstr(index,0, line)
            index += 1

    def index_move_down(self):
        if self.select_index >= len(self.data) - 1:
            return None
        if self.select_index < self.max_dsp_heigth - 1:
            self.select_index += 1
        else:
            self.text_area_y +=1
            self.select_index +=1
        
        if self.select_index == 0:
            self.select_index = 1

        self.update_data_screen()
        self.refresh_data()
        return None

    def index_move_up(self):
        if self.select_index == -1:
            return None

        if self.text_area_y >= 1:
            self.text_area_y -= 1
            self.select_index -= 1
        else:
            self.select_index += -1
        
        if self.select_index == 0:
            self.select_index = -1

        self.update_data_screen()
        self.refresh_data()
        return None

    def get_choice(self):
        if self.select_index < 1:
            return None
        return self.data[self.select_index]


    def process_key_alpha_numeric(self, key=None):
        if key is None:
            return None
        
        if self.data[0] == self.default_text:
            self.data[0] = ""
        
        if len(key) > 1:
            return None


        if self.valid_text is False:
            text = ""
            self.valid_text = True
        
        text = self.data[0] + key
        self.data.clear()
        if self.generate_list_func is not None:
            self.data = [text] + self.generate_list_func(text)
        else:
            self.data = [text]

        self.update_data_screen()
        self.refresh_data()

        return None
    
    def remove_last_chr(self):
        if self.data[0] == self.default_text:
            return None
        if self.data[0] != "":
            text = self.data[0][:-1]
            if text == "":
                self.data.clear()
                self.data = [self.default_text]
            else:
                self.data.clear()
                self.data = [text] + self.generate_list_func(text)
        else:
            self.data = [self.default_text]

        self.update_data_screen()
        self.refresh_data()
        return None

    def init_procces_key(self):
        self.proccess_key = {
            chr(8): self.remove_last_chr,
            "KEY_C2" : self.index_move_down,        # KEY_DOWN
            "KEY_DOWN": self.index_move_down,       # KEY_DOWN
            "KEY_A2" : self.index_move_up,          # KEY_UP
            "KEY_UP" : self.index_move_up,          # KEY_UP
            chr(10): self.get_choice,               # KEY_ENTER
        }

class DataPadDinamicListAir(DataPadBase):
    def __init__(self, curses=None, heigth=150, width=30, data=[], max_width=0, max_heigth=0, start_x=67, start_y=1, generate_list_func=None, default_text="", default_data=None):
        super(DataPadDinamicListAir, self).__init__(curses=curses, heigth=heigth, width=width, data=data, max_width=max_width, max_heigth=max_heigth, start_x=start_x, start_y=start_y, generate_list_func=generate_list_func, default_text=default_text)
        self.select_index = -1
        self.valid_text = False
        self.default_data = default_data
        self.default_text = default_text
        self.data = [{"id":None, "data":self.default_text}]
        self.generate_list_func = generate_list_func

        self.update_data_screen()
        self.refresh_data()

    def update_data_screen(self):
        self.pad.clear()
        
        index = 0
        for line in self.data:
            if self.select_index == index:
                self.pad.addstr(index,0, line["data"], self.curses.A_STANDOUT)
            else:
                self.pad.addstr(index,0, line["data"])
            index += 1

    def index_move_down(self):
        if self.select_index >= len(self.data) - 1:
            return None
        if self.select_index < self.max_dsp_heigth - 1:
            self.select_index += 1
        else:
            self.text_area_y +=1
            self.select_index +=1
        
        if self.select_index == 0:
            self.select_index = 1

        self.update_data_screen()
        self.refresh_data()
        return None

    def index_move_up(self):
        if self.select_index == -1:
            return None

        if self.text_area_y >= 1:
            self.text_area_y -= 1
            self.select_index -= 1
        else:
            self.select_index += -1
        
        if self.select_index == 0:
            self.select_index = -1

        self.update_data_screen()
        self.refresh_data()
        return None

    def get_choice(self):
        if self.select_index < 1:
            return None
        return self.data[self.select_index]["id"]


    def process_key_alpha_numeric(self, key=None):
        if key is None:
            return None
        
        if self.data[0]["data"] == self.default_text:
            self.data[0]["data"] = ""
        
        if len(key) > 1:
            return None


        if self.valid_text is False:
            text = ""
            self.valid_text = True
        
        text = self.data[0]["data"] + key
        self.data.clear()
        if self.generate_list_func is not None:
            self.data = [{"id":None, "data":text}] + self.generate_list_func(text)
            if self.default_data is not None:
                self.data.append({"id":0, "data":self.default_data})

        else:
            self.data = [{"id":None, "data":text}]
            if self.default_data is not None:
                self.data.append({"id":0, "data":self.default_data})

        self.update_data_screen()
        self.refresh_data()

        return None
    
    def remove_last_chr(self):
        if self.data[0]["data"] == self.default_text:
            return None
        if self.data[0]["data"] != "":
            text = self.data[0]["data"][:-1]
            if text == "":
                self.data.clear()
                self.data = [{"id":None, "data":self.default_text}]
            else:
                self.data.clear()
                self.data = [{"id":None, "data":text}] + self.generate_list_func(text)
                if self.default_data is not None:
                    self.data.append({"id":0, "data":self.default_data})
        else:
            self.data = [{"id":None, "data":self.default_text}]

        self.update_data_screen()
        self.refresh_data()
        return None

    def init_procces_key(self):
        self.proccess_key = {
            chr(8): self.remove_last_chr,
            "KEY_C2" : self.index_move_down,        # KEY_DOWN
            "KEY_DOWN": self.index_move_down,       # KEY_DOWN
            "KEY_A2" : self.index_move_up,          # KEY_UP
            "KEY_UP" : self.index_move_up,          # KEY_UP
            chr(10): self.get_choice,               # KEY_ENTER
        }

class DataPadFloat(DataPadBase):
    def __init__(self, curses=None, heigth=150, width=30, data=[], max_width=0, max_heigth=0, start_x=67, start_y=1, generate_list_func=None, default_text="", default_data=None):
        super(DataPadFloat, self).__init__(curses=curses, heigth=heigth, width=width, data=data, max_width=max_width, max_heigth=max_heigth, start_x=start_x, start_y=start_y, generate_list_func=generate_list_func, default_text=default_text)
        self.select_index = -1
        self.valid_text = False
        self.default_text = "0.0"
        self.data = [self.default_text]

        self.update_data_screen()
        self.refresh_data()

    def update_data_screen(self):
        self.pad.clear()
        
        index = 0
        for line in self.data:
            self.pad.addstr(index,0, line)
            index += 1

    def get_choice(self):
        try:
            val = float(self.data[0])
            return val
        except:
            self.data[0] = "<El numero no es valido>"
            self.valid_text = False
            self.update_data_screen()
            self.refresh_data()
            pass
        return None


    def process_key_alpha_numeric(self, key=None):
        if key is None:
            return None
        
        if self.data[0] == self.default_text:
            self.data[0] = ""
        
        if len(key) > 1:
            return None


        if self.valid_text is False:
            self.data[0] = ""
            self.valid_text = True

        if key < '0' or key > '9':
            if key != '.':
                return None
        
        text = self.data[0] + key
        self.data.clear()
        if self.generate_list_func is not None:
            self.data = [text] + self.generate_list_func(text)
        else:
            self.data = [text]

        self.update_data_screen()
        self.refresh_data()

        return None
    
    def remove_last_chr(self):
        # if self.data[0] == self.default_text:
        #     return None
            
        if self.data[0] != "":
            text = self.data[0][:-1]
            if text == "":
                text = self.default_text
            self.data = [text]
        else:
            self.data = [self.default_text]

        self.update_data_screen()
        self.refresh_data()
        return None

    def init_procces_key(self):
        self.proccess_key = {
            chr(8): self.remove_last_chr,
            chr(10): self.get_choice,               # KEY_ENTER
        }

class DataPadInt(DataPadBase):
    def __init__(self, curses=None, heigth=150, width=30, data=[], max_width=0, max_heigth=0, start_x=67, start_y=1, generate_list_func=None, default_text="", default_data=None):
        super(DataPadInt, self).__init__(curses=curses, heigth=heigth, width=width, data=data, max_width=max_width, max_heigth=max_heigth, start_x=start_x, start_y=start_y, generate_list_func=generate_list_func, default_text=default_text)
        self.select_index = -1
        self.valid_text = False
        self.default_text = "0"
        self.data = [self.default_text]

        self.update_data_screen()
        self.refresh_data()

    def update_data_screen(self):
        self.pad.clear()
        
        index = 0
        for line in self.data:
            self.pad.addstr(index,0, line)
            index += 1

    def get_choice(self):
        try:
            val = int(self.data[0])
            return val
        except:
            self.data[0] = "<El numero no es valido>"
            self.valid_text = False
            self.update_data_screen()
            self.refresh_data()
            pass
        return None


    def process_key_alpha_numeric(self, key=None):
        if key is None:
            return None
        
        if self.data[0] == self.default_text:
            self.data[0] = ""
        
        if len(key) > 1:
            return None


        if self.valid_text is False:
            self.data[0] = ""
            self.valid_text = True

        if key < '0' or key > '9':
            return None
        
        text = self.data[0] + key
        self.data.clear()
        if self.generate_list_func is not None:
            self.data = [text] + self.generate_list_func(text)
        else:
            self.data = [text]

        self.update_data_screen()
        self.refresh_data()

        return None
    
    def remove_last_chr(self):
        # if self.data[0] == self.default_text:
        #     return None
            
        if self.data[0] != "":
            text = self.data[0][:-1]
            if text == "":
                text = self.default_text
            self.data = [text]
        else:
            self.data = [self.default_text]

        self.update_data_screen()
        self.refresh_data()
        return None

    def init_procces_key(self):
        self.proccess_key = {
            chr(8): self.remove_last_chr,
            chr(10): self.get_choice,               # KEY_ENTER
        }

class DataPadStr(DataPadBase):
    def __init__(self, curses=None, heigth=150, width=30, data=[], max_width=0, max_heigth=0, start_x=67, start_y=1, generate_list_func=None, default_text="", default_data=None, upper=False):
        super(DataPadStr, self).__init__(curses=curses, heigth=heigth, width=width, data=data, max_width=max_width, max_heigth=max_heigth, start_x=start_x, start_y=start_y, generate_list_func=generate_list_func, default_text=default_text)
        self.select_index = -1
        self.valid_text = False
        self.default_text = default_text
        self.data = [self.default_text]
        self.upper = upper

        self.update_data_screen()
        self.refresh_data()

    def update_data_screen(self):
        self.pad.clear()
        
        index = 0
        for line in self.data:
            self.pad.addstr(index,0, line)
            index += 1

    def get_choice(self):
        # try:
        # val = int(self.data[0])
        if self.data[0] == self.default_text:
            return None
        if self.upper:
            return self.data[0].upper()
        return self.data[0]
        # except:
        #     self.data[0] = "<El texto no es valido>"
        #     self.valid_text = False
        #     self.update_data_screen()
        #     self.refresh_data()
        #     pass
        # return None


    def process_key_alpha_numeric(self, key=None):
        if key is None:
            return None
        
        if self.data[0] == self.default_text:
            self.data[0] = ""
        
        if len(key) > 1:
            return None


        if self.valid_text is False:
            self.data[0] = ""
            self.valid_text = True
        
        text = self.data[0] + key
        self.data.clear()
        if self.generate_list_func is not None:
            self.data = [text] + self.generate_list_func(text)
        else:
            self.data = [text]

        self.update_data_screen()
        self.refresh_data()

        return None
    
    def remove_last_chr(self):
        # if self.data[0] == self.default_text:
        #     return None

        if self.data[0] == self.default_text:
            return None
            
        if self.data[0] != "":
            text = self.data[0][:-1]
            if text == "":
                text = self.default_text
            self.data = [text]
        else:
            self.data = [self.default_text]

        self.update_data_screen()
        self.refresh_data()
        return None

    def init_procces_key(self):
        self.proccess_key = {
            chr(8): self.remove_last_chr,
            chr(10): self.get_choice,               # KEY_ENTER
        }

class DataPadPhone(DataPadBase):
    def __init__(self, curses=None, heigth=150, width=30, data=[], max_width=0, max_heigth=0, start_x=67, start_y=1, generate_list_func=None, default_text="", default_data=None):
        super(DataPadPhone, self).__init__(curses=curses, heigth=heigth, width=width, data=data, max_width=max_width, max_heigth=max_heigth, start_x=start_x, start_y=start_y, generate_list_func=generate_list_func, default_text=default_text)
        self.select_index = -1
        self.valid_text = False
        self.default_text = default_text
        self.data = [self.default_text]

        self.update_data_screen()
        self.refresh_data()

    def update_data_screen(self):
        self.pad.clear()
        
        index = 0
        for line in self.data:
            if line == self.default_text:
                phone = line
            elif len(line) < 3:
                phone = f"({line[:3]})"
            elif len(line) < 7:
                phone = f"({line[:3]}) {line[3:6]}"
            elif len(line) < 10:
                phone = f"({line[:3]}) {line[3:6]}-{line[6:]}"
            else:
                check_mark = u'\u2713'
                phone = f"({line[:3]}) {line[3:6]}-{line[6:]} {check_mark}"

            self.pad.addstr(index,0, phone)
            index += 1

    def get_choice(self):
        # try:
        # val = int(self.data[0])
        if self.data[0] == self.default_text:
            return None
        if len(self.data[0]) < 10:
            return None
        return self.data[0]
        # except:
        #     self.data[0] = "<El texto no es valido>"
        #     self.valid_text = False
        #     self.update_data_screen()
        #     self.refresh_data()
        #     pass
        # return None


    def process_key_alpha_numeric(self, key=None):
        if key is None:
            return None
        
        if self.data[0] == self.default_text:
            self.data[0] = ""
        
        if len(key) > 1:
            return None


        if self.valid_text is False:
            self.data[0] = ""
            self.valid_text = True

        if key < '0' or key > '9':
            return None
        
        if len(self.data[0]) > 9:
            return None
        
        text = self.data[0] + key
        self.data.clear()
        if self.generate_list_func is not None:
            self.data = [text] + self.generate_list_func(text)
        else:
            self.data = [text]

        self.update_data_screen()
        self.refresh_data()

        return None
    
    def remove_last_chr(self):
        # if self.data[0] == self.default_text:
        #     return None
        if self.data[0] == self.default_text:
            return None
            
        if self.data[0] != "":
            text = self.data[0][:-1]
            if text == "":
                text = self.default_text
            self.data = [text]
        else:
            self.data = [self.default_text]



        self.update_data_screen()
        self.refresh_data()
        return None

    def init_procces_key(self):
        self.proccess_key = {
            chr(8): self.remove_last_chr,
            chr(10): self.get_choice,               # KEY_ENTER
        }


class DataPadDatePicker(DataPadBase):
    def __init__(self, curses=None, heigth=150, width=30, data=[], max_width=0, max_heigth=0, start_x=67, start_y=1, generate_list_func=None, default_text="", default_data=None):
        super(DataPadDatePicker, self).__init__(curses=curses, heigth=heigth, width=width, data=data, max_width=max_width, max_heigth=max_heigth, start_x=start_x, start_y=start_y, generate_list_func=generate_list_func, default_text=default_text)
        self.select_index = -1
        self.valid_text = False
        self.data = [self.default_text]
        self.generate_list_func = generate_list_func

        if default_data is None:
            self.set_data_picker()
        else:
            d_date = re.compile(r"(\d\d)\/(\d\d)\/(\d\d\d\d)")
            d_match = d_date.match(default_data)
            if d_match is None:
                self.set_data_picker()
            else:
                self.set_data_picker(day=int(d_match.groups()[0]),
                                    month=int(d_match.groups()[1]),
                                    year=int(d_match.groups()[2]))

        self.update_data_screen()
        self.refresh_data()

    def update_data_screen(self):
        self.pad.clear()
        x_index = 0
        index = 0
        for line in self.data:
            if line == "/":
                self.pad.addstr(0, x_index, line)
            elif self.select_index == index:
                self.pad.addstr(0, x_index, line, self.curses.A_STANDOUT)
                index += 1
            else:
                self.pad.addstr(0, x_index, line)
                index += 1
            x_index += len(line)

    def index_move_down(self):
        if self.select_index == 0:
            if self.selected_day < 31:
                self.selected_day += 1
        if self.select_index == 1:
            if self.selected_month < 12:
                self.selected_month += 1
        if self.select_index == 2:
            if self.selected_year < 2050:
                self.selected_year += 1
        self.set_data_picker(   day=self.selected_day,
                                month=self.selected_month,
                                year=self.selected_year,
                                index=self.select_index)
        self.update_data_screen()
        self.refresh_data()
        return None

    def index_move_up(self):
        if self.select_index == 0:
            if self.selected_day >= 1:
                self.selected_day -= 1
        if self.select_index == 1:
            if self.selected_month >= 2:
                self.selected_month -= 1
        if self.select_index == 2:
            if self.selected_year >= 2011:
                self.selected_year -= 1
        self.set_data_picker(   day=self.selected_day,
                                month=self.selected_month,
                                year=self.selected_year,
                                index=self.select_index)
        self.update_data_screen()
        self.refresh_data()
        return None


    def index_move_rigth(self):
        if self.select_index < 2:
            self.select_index +=1
        self.update_data_screen()
        self.refresh_data()
        return None
    
    def index_move_left(self):
        if self.select_index >= 1:
            self.select_index -= 1
        self.update_data_screen()
        self.refresh_data()
        return None

    def get_choice(self):
        return f"{self.selected_day:02}/{self.selected_month:02}/{self.selected_year}"

    def process_key_alpha_numeric(self, key=None):
        if key is None:
            return None
        
        if len(key) > 1:
            return None
        
        if key < '0' or key > '9':
            return None

        # change selected day
        if self.select_index == 0:
            if len(self.buffer_date) < 2:
                if int(self.buffer_date + key) == 0:
                    return None
                if int(self.buffer_date + key) > 31:
                    self.buffer_date = key
                else:
                    self.buffer_date += key
            else:
                if int(key) == 0:
                    return None
                self.buffer_date = key

            self.data[0] = f"{int(self.buffer_date):02}"
            self.selected_day = int(self.data[0])
        
        self.update_date_picker()
        self.refresh_data
        return None


    def set_data_picker(self, day=None, month=None, year=None, index = 0, default_data=None): #ported
        today = date.today()

        self.select_index = index
        self.buffer_date = ""

        # select day
        if day is None:
            self.selected_day = today.day
        else:
            self.selected_day = day

        # select month
        if month is None:
            self.selected_month = today.month
        else:
            self.selected_month = month

        # select year
        if year is None:
            self.selected_year = today.year
        else:
            self.selected_year = year


        self.data = [f"{self.selected_day:02}", "/", f"{MONTHS_DICT[self.selected_month]}", f"/", f"{self.selected_year}"]

    def init_procces_key(self):
        
        self.proccess_key = {
            "KEY_B3" : self.index_move_rigth,                   # KEY_RIGHT
            "KEY_RIGHT": self.index_move_rigth,                 # KEY_RIGTH
            "KEY_B1" : self.index_move_left,                    # KEY_LEFT
            "KEY_LEFT": self.index_move_left,                   # KEY_LEFT
            "KEY_A2" : self.index_move_up,                      # KEY_UP
            "KEY_UP" : self.index_move_up,                      # KEY_UP
            "KEY_C2" : self.index_move_down,                    # KEY_DOWN
            "KEY_DOWN": self.index_move_down,                   # KEY_DOWN
            chr(10): self.get_choice,                           # KEY_ENTER
        }


# DATAPAD TYPES
DATAPAD_DICT = {LIST_MODE:DataPadList,
                DINAMIC_LIST:DataPadDinamicList,
                DINAMIC_LIST_AIR:DataPadDinamicListAir,
                DATE_PICKER:DataPadDatePicker,
                CONFIRM_PICKER:DataPadConfirm,
                FLOAT_NUMBER:DataPadFloat,
                INT_NUMBER:DataPadInt,
                STR_BOX:DataPadStr,
                PHONE_NUMBER:DataPadPhone}

# GENERIC VIEW

# testing

def main(stdscr):
    from ConsulManager.AirTable.PacientesAir.Pacientes import PacientesAir
    from ConsulManager.AirTable.ListaTratamientos.ListaTratamientosAir import ListaTratamientosAir
    from ConsulManager.ConsulCli.ConsulLayoutBase import View

    # pacientes = PacientesAir()
    # pacientes.update_pacientes_list()
    trata = ListaTratamientosAir()
    trata.update_tratamientos_list()

    MAX_HEIGTH, MAX_WIDTH = stdscr.getmaxyx()
    S1 = int(MAX_WIDTH / 12)

    test_data = []
    for i in range(15):
        test_data.append(f"test campo {i}")
    stdscr.clear()
    stdscr.refresh()
    main_view = View(
        data_list=test_data,
        s1=S1,
        max_heigth=MAX_HEIGTH,
        max_width=MAX_WIDTH,
        mode=DINAMIC_LIST_AIR,
        # generate_list_func=test_func,
        # generate_list_func=pacientes.find_paciente,
        generate_list_func=trata.find_tratamiento,
        prompt_test="Example Test 2",
        default_text="<< Telefono >>",
        default_data="<< NUEVO TRATAMIENTO >>"
    )
    # main_view.refresh()


    # get Key
    while True:
        key = stdscr.getkey()
        choice = None
        # Escape key
        if key == chr(27):
            break
        # CTRL + C
        if key == chr(3):
            break

        choice = main_view.process_key(key=key)
        
        stdscr.clear()
        stdscr.addstr(4,0, f'key:: {key}')
        stdscr.addstr(5,0, f'choice:: {choice}')

        stdscr.refresh()
        main_view.refresh()

if __name__ == '__main__':
    curses.wrapper(main)
    # l