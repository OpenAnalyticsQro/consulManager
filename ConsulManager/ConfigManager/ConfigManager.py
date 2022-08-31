from operator import truediv
import yaml
from pathlib import Path
from ConsulManager.Logger import logger as log
from ConsulManager.ConfigManager import CONFIG_DEFINITIONS, MAIN_CONFIG_FILES, INIT_FILE_NAME, INIT_FILE_FORMAT

GENERATOR_ITEMS_VETOR = {}

class ConfigManager(object):
    def __init__(self) -> None:
        self.__sub_config_list = {}
        self.__cwd = None
        self.__main_config = None

    @property
    def cwd(self):
        if self.__cwd is None:
            self.__cwd = Path(__file__).parent.parent
        return self.__cwd

    def generate_config(self):
        for main_config in self.cwd.glob("mainConfig.yaml"):
            self.__main_config = MainConfigYaml(main_config=main_config, cwd=self.cwd)
            return self.__main_config.generate_config()

        log.error(f"mainConfig.yaml not available in : {self.cwd}")


    # def read_main_config(self, f_path=test_file):
    #     """ read the main config file and split in sub config files"""
    #     with open(test_file) as fd:
    #         main_config = yaml.safe_load(fd)
    #         yield main_config

    # def procces_config_files(self, f_path=test_file):
    #     for config in self.read_main_config(f_path=f_path):
    #         # TODO: create a format for config key:
    #         self.__sub_config_list["test"] = ConfigYaml(main=config)

    #     for config in self.__sub_config_list.values():
    #         log.info(f"Generating config for: {config.name}")
    #         # create config definitions
    #         config.create_definitions()

    # def clear(self):
    #     """ method to clear all config files """
    #     for config in self.__sub_config_list.values():
    #         config.clear()

# this class is used for mainConfig.yaml
class MainConfigYaml(object):
    __valid = False
    __main = None
    __name = None
    __cwd = None
    __config_files_list = []

    def __init__(self, main_config=None, cwd=None):
        # mainConfig.yaml not available
        if main_config.exists() is False:
            log.error(f"mainCoinfig.yaml not available")
        else:
            # reading mainConfig.yaml
            log.info(f"Reading : {main_config}")
            try:
                with open(main_config, "r") as fd:
                    self.__main = yaml.safe_load(fd)
                    if len(self.__main) >= 1:
                        self.__name = list(self.__main.keys())[0]
                        self.__main = self.__main[self.__name]
                        self.__cwd = cwd
                        self.__valid = True
                    else:
                        log.error(f"mainCoinfig.yaml invalid name format")
            except:
                log.error(f"mainCoinfig.yaml invalid file")

    def generate_config(self):
        """ generate all configuration from mainConfig"""
        if self.valid is False:
            return False

        # create Definitios if is required for main

        # generate config files
        self.config_files()

        return True

    def config_files(self):
        """ read all config files"""
        if MAIN_CONFIG_FILES in self.__main.keys():
            for item in self.__main[MAIN_CONFIG_FILES]:
                config_available = False
                tmp_path = Path.joinpath(self.cwd, list(item.values())[0])

                for config_yaml in tmp_path.glob("config.yaml"):
                    config_available = True
                    config_manager = ConfigYaml(main_config=config_yaml, cwd=tmp_path)

                    # config manager was no created 
                    if config_manager.generate_config() is False:
                        log.error(f"invalid config.yaml : {config_yaml}")
                        break

                    self.__config_files_list.append(config_manager)
                    break
                
                if config_available is False:
                    log.error(f"config.yaml not available in: {tmp_path}")

    @property
    def valid(self):
        return self.__valid

    @property
    def cwd(self):
        return Path(self.__cwd)


# this class is used for config.yaml files
class ConfigYaml(object):
    __valid = False
    __name = None
    __main = None
    __config_files_list = []
    __process_list = []
    __init_file_dict = {}

    def __init__(self, main_config=None, cwd=None):
        self.__cwd = cwd
        # config.yaml not available
        if main_config.exists() is False:
            log.error(f"mainCoinfig.yaml not available in {self.cwd}")
        else:
            # reading mainConfig.yaml
            log.info(f"Reading : {main_config}")
            try:
                with open(main_config, "r") as fd:
                    self.__main = yaml.safe_load(fd)
                    if len(self.__main) >= 1:
                        self.__name = list(self.__main.keys())[0]
                        self.__main = self.__main[self.__name]
                        self.__valid = True
                        
                        # set definition list process
                        self.__process_list = [
                                                self.create_definitions,        # funtion to generate all constants and definitios from config file
                                                self.create_init_file,          # function to generate init file
                                            ]
                    else:
                        log.error(f"mainCoinfig.yaml invalid name format")
            except:
                log.error(f"mainCoinfig.yaml invalid file")

    @property
    def name(self):
        return self.__name

    @property
    def valid(self):
        return self.__valid

    @property
    def cwd(self):
        return self.__cwd

    def generate_config(self):
        if self.valid is False:
            return False

        # execute process
        for process in self.__process_list:
            process()

        # execute config files
        self.config_files()

        return True

    def create_init_file(self):
        """ this function look for a init file and create it"""
        log.debug(f"    {self.__name} -> generating init file ({self.cwd})")
        init_file = self.cwd / INIT_FILE_NAME

        # create init file
        if init_file.exists() is False:
            log.debug(f"    mkdir {INIT_FILE_NAME}")

        self.__init_file_dict['name'] = self.name
        # print(INIT_FILE_FORMAT.format_map(self.__init_file_dict))
        with open(init_file, "w") as fd:
            fd.write(INIT_FILE_FORMAT.format_map(self.__init_file_dict))


    def create_definitions(self):
        """ create all definition constants in __init__.py files"""
        definition_list = []
        if CONFIG_DEFINITIONS in self.__main.keys():
            log.debug(f"    {self.__name} -> {CONFIG_DEFINITIONS}")
            for definition in self.__main[CONFIG_DEFINITIONS]:
                tmp_list = [f'# {definition}']
                for key, value in [e for e_list in self.__main[CONFIG_DEFINITIONS][definition] for e in e_list.items()]:
                    item = f'{self.name}_{key}'
                    item_value = f'"{value}"' if isinstance(value, str) else value
                    tmp_list.append(f"{item.upper().replace(' ', '_')} = {item_value}")
                definition_list.append('\n'.join(tmp_list))

            # generate definitions
            self.__init_file_dict[CONFIG_DEFINITIONS] = '\n\n'.join(definition_list)
            return True

        # definition failed
        log.warning(f"    {self.__name} -> {CONFIG_DEFINITIONS} (was not generated)")
        self.__init_file_dict[CONFIG_DEFINITIONS] = ''
        return False

    def config_files(self):
        """ read all config files"""
        if MAIN_CONFIG_FILES in self.__main.keys():
            for item in self.__main[MAIN_CONFIG_FILES]:
                config_available = False
                tmp_path = Path.joinpath(self.cwd, list(item.values())[0])

                for config_yaml in tmp_path.glob("config.yaml"):
                    config_available = True
                    config_manager = ConfigYaml(main_config=config_yaml, cwd= tmp_path)

                    # config manager was no created 
                    if config_manager.generate_config() is False:
                        log.error(f"invalid config.yaml : {config_yaml}")
                        break

                    self.__config_files_list.append(config_manager)
                    break
                
                if config_available is False:
                    log.error(f"config.yaml not available in: {tmp_path}")
        else:
            log.warning(f"    {self.name} -> {MAIN_CONFIG_FILES} (was not generated)")


    def clear(self):
        """ method to clear all generated files"""
        pass

    def __str__(self):
        return str(self.__main)


if __name__ == "__main__":
    config_manager = ConfigManager()
    config_manager.generate_config()
    # config_manager.cwd
    # config_manager.procces_config_files()
    pass