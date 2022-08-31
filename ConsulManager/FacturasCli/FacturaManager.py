from glob import glob
from pathlib import Path
import zipfile
import shutil
from ConsulManager.Logger import logger as log
from ConsulManager.FacturasCli.Factura.Factura3_3 import Factura3_3_Xml
from ConsulManager.FacturasCli.Factura import FACTURA_3_3_RFC, FACTURA_3_3_NAME, FACTURA_3_3_UUID

FACTURAS_FOLDER = Path(r"C:\Users\uidk4253\Documents\OpenAnalytics\ConsulManager\consulManager\ConsulManager\FacturasCli\test_sat")

class FacturaManager(object):
    __result_folder = "Facturas_Ordenadas"
    def __init__(self) -> None:
        # list of folders associated to a unique rfc
        self.__rfc_folder_list = {}
        # list of uuid associated to a specific rfc
        self.__fact_uuid_list = {}
        # list of invalid files
        self.__invalid_files_list = []

    def read_facturas_zip(self, f_path=FACTURAS_FOLDER):
        ''' Read all facturas in zip format
            1. simple files (no zip) yield
            2. folder yield'''
        if f_path.exists() is False:
            log.error(f"Invalid Factura Path: {f_path}")

        for file in f_path.glob("*"):
            # this could be a pdf or a xml file
            if file.is_file() and file.suffix != ".zip":
                yield file
                continue
            # this is a folder
            if file.is_dir():
                yield file
                continue
            
            # extract all files
            log.debug(f"Unzip file: {file}")
            tmp_folder = file.parent / (file.stem + "_tmp")
            with zipfile.ZipFile(file, mode='r') as archive:
                archive.extractall(path=tmp_folder)
                yield tmp_folder
            log.debug(f"Removing Folder: {tmp_folder}")
            shutil.rmtree(tmp_folder)

    def read_facturas_folder(self, f_path=FACTURAS_FOLDER):
        ''' read facturas folders
            1. simple files are yield'''
        if f_path.exists() is False:
            log.error(f"Invalid Factura Path: {f_path}")

        for folder in self.read_facturas_zip(f_path=f_path):
            # is not a folder
            if folder.is_file():
                yield folder
                continue

            # read first xml format: to generate all requiered folders
            for file in folder.glob("*.xml"):
                if file.is_file():
                    if file.suffix == ".xml":
                        yield file
                        continue

            # read all reminder files
            for file in folder.glob("*"):
                if file.is_file():
                    if file.suffix == ".pdf":
                        yield file
                        continue

    def arrange_facturas(self, f_path=FACTURAS_FOLDER, remove_folder=True, result_path=None):
        ''' arrange facturas folder in xml or pdf format:
            1. extra files are no arranged and are notified trough result.txt'''
        if f_path.exists() is False:
            log.error(f"Invalid Factura Path: {f_path}")
        
        # create and remove result folder
        if result_path is None:
            result_folder = f_path / self.__result_folder
        else:
            result_folder = result_folder / self.__result_folder

        if (result_folder.exists() is False):
            result_folder.mkdir()
        elif remove_folder is True:
            shutil.rmtree(result_folder)
            result_folder.mkdir()

        for file in self.read_facturas_folder(f_path=f_path):
            if file.suffix == ".xml":
                self.arrange_facturas_xml(file, path=result_folder)
            elif file.suffix == ".pdf":
                self.arrange_facturas_pdf(factura=file)
            else:
                # invalid files
                self.__invalid_files_list.append(f"[INVALID FORMAT]- {file}")

        # Process invalid files
        if self.__invalid_files_list:
            log.debug(f"Generating Result file in: {result_folder/'result.txt'}")
            with open(result_folder/'result.txt', "w+") as fd:
                for invalid in self.__invalid_files_list:
                    log.error(f"Invalid: {invalid}")
                    fd.writelines(f"{invalid}\n")

    def arrange_facturas_pdf(self, factura=None):
        """ arrange facturas in pdf format"""
        folder = self.__fact_uuid_list.get(factura.name.replace(".pdf",'').upper())
        if folder is not None:
            aux = folder / factura.name
            # avoid to duplicate facturas
            if aux.exists() is False:
                log.info(f"movig: {factura.name} -> {folder.name}")
                factura.rename(aux)
        else:
            self.__invalid_files_list.append(f"[INVALID UUID] - {factura}")

    def arrange_facturas_xml(self, factura=None, path=None):
        """ arrange facturas in xml format"""
        if factura is None:
            return False

        fact = Factura3_3_Xml(f_path=factura)

        # check for valid xml format
        if fact.valid is False:
            self.__invalid_files_list.append(f"[INVALID XML] - {factura}")
            return False

        if fact.Receptor is None:
            self.__invalid_files_list.append(f"[INVALID XML] - {factura}")
            return False

        rfc_folder = self.get_folder_for_rfc(rfc=fact.Receptor[FACTURA_3_3_RFC], name=fact.Receptor[FACTURA_3_3_NAME], path=path)
        aux = rfc_folder / factura.name

        # avoid to duplicate facturas
        if aux.exists() is False:
            log.info(f"Moving {factura.name} -> {rfc_folder.name}")
            factura.rename(aux)

        # update uuid list with rfc_folder
        if fact.TimbreFiscal is not None:
            self.__fact_uuid_list[fact.TimbreFiscal[FACTURA_3_3_UUID].upper()] = rfc_folder
        else:
            self.__invalid_files_list.append(f"[INVALID XML] - {factura}")
            return False
        return True

    def get_folder_for_rfc(self, rfc=None, name=None, path=None):
        """ returns folder for specific rfc, if folder does not exit then create a new one"""
        if self.__rfc_folder_list.get(rfc) is None:
            rfc_path = path / f"{name.replace(' ','_')}_{rfc}"
            log.debug(f"Mkdir Folder:{rfc_path}")
            if rfc_path.exists() is False:
                rfc_path.mkdir()
            self.__rfc_folder_list[rfc] = rfc_path

        return self.__rfc_folder_list.get(rfc)









if __name__ == "__main__":
    f_manager = FacturaManager()
    f_manager.arrange_facturas(f_path=FACTURAS_FOLDER)
