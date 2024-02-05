import os
from config import Config

class Config_Adapt(Config):
    def __init__(self, file_name):
        super().__init__(file_name)
        if file_name not in os.listdir(os.getcwd()):
            self.create_file()
        
    def create_file(self):
        self.add_section("votes")
        self.set_config("votes", "xiaoke", "10")
        self.set_config("votes", "pikaqiu", "9")
        self.set_config("votes", "shengye", "8")
        self.set_config("votes", "natie", "7")
        self.set_config("votes", "naicha", "6")
        self.set_config("votes", "xueding", "5")
        self.set_config("votes", "danta", "4")
        self.set_config("votes", "yuanbao", "3")
        self.set_config("votes", "dudu", "2")

if __name__ == "__main__":
    config = Config_Adapt("config.ini")
    print(config.get_config("input", "suffix"))

                    
