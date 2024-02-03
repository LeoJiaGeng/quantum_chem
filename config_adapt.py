import os
from config import Config

class Config_Adapt(Config):
    def __init__(self, file_name):
        super().__init__(file_name)
        if file_name not in os.listdir(os.getcwd()):
            self.create_file()
        
    def create_file(self):
        self.add_section("votes")
        self.set_config("votes", "xiaoke", "0")
        self.set_config("votes", "pikaqiu", "0")
        self.set_config("votes", "shengye", "0")
        self.set_config("votes", "natie", "0")
        self.set_config("votes", "naicha", "0")
        self.set_config("votes", "xueding", "0")


if __name__ == "__main__":
    config = Config_Adapt("config.ini")
    print(config.get_config("input", "suffix"))

                    
