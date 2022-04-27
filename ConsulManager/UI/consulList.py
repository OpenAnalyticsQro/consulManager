import sys

from ConsulManager.UI.ui_listConsultas import Ui_consulList
from ConsulManager.UI.ui_optionListWidget import Ui_optionListWidget
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGraphicsDropShadowEffect, QLabel
from PySide6.QtCore import QFile, QPropertyAnimation, QEasingCurve, Signal, QSize, QParallelAnimationGroup, QPoint, QRect, Property, QSequentialAnimationGroup
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, Signal

# CONSTANS
EXPAND_TO_LEFT = 0
EXPAND_TO_RIGHT = 1
EXPAND_TO_LEFT_UP = 2

# CONSTANS MESSAGE
NEW_PX_MSG = "Nuevo Paciente"
NEW_PHONE_MSG = "###"


# Base Widget
class ConsulWidget(QWidget):
    def __init__(self, parent=None, x=0, y=0):
        super().__init__(parent)
        self.update_xy(init_x=x, init_y=y)

        # init Widgets
        self.initWidgets()
        # set init configuration
        self.initConfig()
        # set slot Configuration
        self.initSlots()
        # update animations
        self.setupAnimation()

    # internal functions
    def update_xy(self, init_x=None, init_y=None):
        """ updates initial position of ConsulWidget"""
        if init_x is None:
            x = self.x()
        else:
            x = init_x
        if init_y is None:
            y = self.y()
        else:
            y = init_y

        self.move(x, y)

    def initSlots(self):
        pass

    def initWidgets(self):
        pass

    def initConfig(self):
        pass

    # animations
    def setupAnimation(self):
        pass

    def animation_expand_widget(self, widget=None, animation=None, duration=800, type=EXPAND_TO_RIGHT):
        """ animation to expand widget"""
        min_w = widget.minimumWidth()
        min_h = widget.minimumHeight()
        max_w = widget.maximumWidth()
        max_h = widget.maximumHeight()

        pos = widget.geometry()

        if animation is None:
            animation_group = QParallelAnimationGroup()
        else:
            animation_group = animation

        animation = QPropertyAnimation(widget, b'geometry')
        animation.setDuration(duration)
        # heigth keeps equal
        if type == EXPAND_TO_RIGHT:
            animation.setEndValue(QRect(pos.x(), pos.y(), max_w, max_h))
        # heigth keeps equal
        elif type == EXPAND_TO_LEFT:
            animation.setEndValue(QRect(pos.x()-max_w+min_w, pos.y(), max_w, max_h))
        elif type == EXPAND_TO_LEFT_UP:
            animation.setEndValue(QRect(pos.x()-max_w+min_w, pos.y()-max_h+min_h, max_w, max_h))
        animation.setEasingCurve(QEasingCurve.OutQuart)

        animation_group.addAnimation(animation)
        return animation_group

    def animation_collapse_widget(self, widget=None, animation=None, duration=800):
        """ Animation to collapse widget"""
        min_w = widget.minimumWidth()
        min_h = widget.minimumHeight()
        pos = widget.geometry()

        if animation is None:
            animation_group = QParallelAnimationGroup()
        else:
            animation_group = animation

        animation = QPropertyAnimation(widget, b'geometry')
        animation.setDuration(duration)
        animation.setEndValue(QRect(pos.x(), pos.y(), min_w, min_h))
        animation.setEasingCurve(QEasingCurve.OutQuart)

        animation_group.addAnimation(animation)
        return animation_group

# Option List Widget
class optionListWidget(ConsulWidget):
    def __init__(self, parent=None, x=0, y=0, name=NEW_PX_MSG, phone=NEW_PHONE_MSG):
        self.__name = name
        self.__phone = phone
        super().__init__(parent, x, y)


    def initWidgets(self):
        self.__main = Ui_optionListWidget()
        self.__main.setupUi(self)
    
    def initConfig(self):
        self.__main.optionName.setText(self.__name)
        self.__main.optionPhone.setText(self.__phone)

# ConsulList Widget
class ConsulList(ConsulWidget):
    expand_widget = Signal()
    collapse_widget = Signal()
    search_mode = Signal()
    clear_options = Signal()
    set_options_list = Signal(list)
    def __init__(self, parent=None, x=0, y=0):
        super().__init__(parent, x=x, y=y)

        # internal variables
        self.__is_extended = False
        self.__search_mode_enable = False
        self.__options_list = []
        # remove this
        self.set_options_list.emit(["hirvin","diana", "x2", "x3", "x4", "x5", "x6", "x7"])

    def initWidgets(self):
        self.__listW = Ui_consulList()
        self.__listW.setupUi(self)

    def initSlots(self):
        self.__listW.buttonFrame.mousePressEvent = self.buttonFramemousePressEvent
        self.__listW.searchEdit.mousePressEvent = self.buttonFramemousePressEvent
        self.__listW.dataFrame.mousePressEvent = self.dataFramemousePressEvent

        self.expand_widget.connect(self.__expand_widget)
        self.collapse_widget.connect(self.__collapse_widget)
        self.search_mode.connect(self.__search_mode)
        self.clear_options.connect(self.__clear_options_list)
        self.set_options_list.connect(self.__set_options_list)
        self.__listW.searchEdit.editingFinished.connect(self.searchEditFocusOutEvent)

    def initConfig(self):
        # list Widget
        self.__listW.FrameBase.resize(self.__listW.FrameBase.minimumSize())
        self.__listW.FrameBase.move(self.__listW.FrameBase.maximumWidth() - self.__listW.FrameBase.minimumWidth(),
                                    self.__listW.FrameBase.maximumHeight() - self.__listW.FrameBase.minimumHeight())
        # efect 1
        self.efect = QGraphicsDropShadowEffect()
        self.efect.setXOffset(0)
        self.efect.setYOffset(1)
        self.efect.setBlurRadius(2)
        self.efect.setColor(QColor(0, 0, 0, 30))
        self.__listW.FrameBase.setGraphicsEffect(self.efect)
        # efect 2
        self.efect2 = QGraphicsDropShadowEffect()
        self.efect2.setXOffset(0)
        self.efect2.setYOffset(2)
        self.efect2.setBlurRadius(2)
        self.efect2.setColor(QColor(0, 0, 0, 15))
        self.__listW.FrameBase.setGraphicsEffect(self.efect2)

        self.__listW.dataButtonFrame.resize(self.__listW.dataButtonFrame.minimumSize())
        
        
    def setupAnimation(self):
        # Expand animations
        self.__expand_animation = self.animation_expand_widget(widget=self.__listW.FrameBase,
                                                                type=EXPAND_TO_LEFT_UP)
        self.__expand_animation = self.animation_expand_widget(widget=self.__listW.dataButtonFrame,
                                                                animation=self.__expand_animation,
                                                                type=EXPAND_TO_RIGHT)
        # Collapse animations
        self.__collapse_animations = self.animation_collapse_widget(widget=self.__listW.FrameBase,
                                                                    duration=200)
        self.__collapse_animations = self.animation_collapse_widget(widget=self.__listW.dataButtonFrame,
                                                                    duration=200,
                                                                    animation=self.__collapse_animations)

    # itnernal functions
    def __clear_options_list(self):
        for w in self.__options_list:
            w.deleteLater()
        self.__options_list.clear()

    def __set_options_list(self, recv_list=[]):
        for index, option in enumerate(recv_list):
            tmp_w = self.__create_option_widget(name=option, index=index)
            self.__options_list.append(tmp_w)
            # self.__listW.optionsLayout.addWidget(label,0)
            self.__listW.optionsLayout.insertWidget(index, tmp_w)

    def __create_option_widget(self, name="", index=0):
        return optionListWidget(self.__listW.listScroll, name=name)


    def buttonFramemousePressEvent(self, event):
        if self.__search_mode_enable is False:
            self.setFocus()

    def dataFramemousePressEvent(self, event):
        pass


    def searchEditFocusInEvent(self, event):
        if self.__is_extended is False:
            return False

        if self.__search_mode_enable:
            return True

        print("enable")
        self.__search_mode_enable = True

    def searchEditFocusOutEvent(self):
        if self.__search_mode_enable is True:
            print("Edited comple")
            self.__search_mode_enable = False
            self.collapse_widget.emit()

    def __expand_widget(self):
        # if self.__is_extended:
        #     return True
        if self.__is_extended is False:
            print("Expanded")
            self.__is_extended = True
            self.__expand_animation.start()
            # self.__listW.searchEdit.setTextInteractionFlags(Qt.TextBrowserInteraction|Qt.TextEditorInteraction)
            self.__listW.searchEdit.setReadOnly(False)
            self.__listW.searchEdit.setCursorPosition(0)

            # enable search mode
            self.__search_mode_enable = True
            self.search_mode.emit()

    def __collapse_widget(self):
        if self.__search_mode_enable is False:
            print("Collapse")
            self.__is_extended = False
            # self.__listW.searchEdit.setTextInteractionFlags(Qt.NoTextInteraction)
            self.__listW.searchEdit.setReadOnly(True)
            self.__listW.searchEdit.setCursorPosition(0)
            self.__listW.searchEdit.setText("Nueva")
            self.__listW.iconLabel.setText("")
            self.__collapse_animations.start()

            # clean all options
            self.clear_options.emit()

    def __search_mode(self):
        self.__listW.searchEdit.setFocus()
        self.__listW.searchEdit.setText("")
        self.__listW.iconLabel.setText("")
        self.__search_mode_enable = True





    # # slots
    # def mousePressEvent(self, event):
    #     print("Mouse press event")
    # #     self.setFocus()
    
    def focusInEvent(self, event):
        self.expand_widget.emit()
    
    def focusOutEvent(self, event):
        self.collapse_widget.emit()
        




# Test
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.consulLisW = ConsulList(self, x=0, y=0)
        self.resize(800,800)

        # remove this line
        self.option = optionListWidget(self, 0, 500)

        self.setStyleSheet(u"QWidget\n"
"{\n"
"background:#FFFBFF;\n"
"}\n")

    # internal events
    def mousePressEvent(self, e):
        print("Focus windows")
        self.setFocus()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())