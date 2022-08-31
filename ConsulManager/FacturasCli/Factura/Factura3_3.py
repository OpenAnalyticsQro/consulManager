import re
import xml.etree.ElementTree as ET
from ConsulManager.FacturasCli.Factura import FACTURA_3_3_RECEPTOR, FACTURA_3_3_COMPLEMENTO
from ConsulManager.FacturasCli import log

class Factura3_3_Xml(object):
    def __init__(self, f_path=None) -> None:
        try:
            if f_path.exists() is True:
                tree = ET.parse(f_path)
                self.root = tree.getroot()
                m = re.match(r'\{.*\}', self.root.tag)
                self.name_space = m.group(0) if m else ''
                self.__valid = True

                # xml elements
                self.__receptor = None
                self.__timbre_fiscal = None
        except:
            self.__valid = False

    @property
    def valid(self):
        return self.__valid

    @property
    def Receptor(self):
        """ return recepetor from factura 3.3"""
        if self.__receptor is None:
            receptor = self.root.find(f"{self.name_space}{FACTURA_3_3_RECEPTOR}")
            self.__receptor = receptor.attrib if receptor is not None else None
        return self.__receptor

    @property
    def TimbreFiscal(self):
        """ return timbre fiscal digital 3.3"""
        if self.__timbre_fiscal is None:
            complemento = self.root.find(f"{self.name_space}{FACTURA_3_3_COMPLEMENTO}")
            self.__timbre_fiscal =  complemento[1].attrib if complemento is not None else None
        return self.__timbre_fiscal