import os
from lib.config import UserConfig

ASCII = """
\t\t
        ▄██████     ▄▄▄█▄          
       ▄██▀░░▀██▄    ████████▄      
      ███░░░░░░██      █▀▀▀▀▀██▄▄   
     ▄██▌░░░░░░░██    ▐▌        ▀█▄ 
     ███░░▐█░█▌░██    █▌          ▀▌       :::::::::  :::::::::: :::::::::   ::::::::  :::::::::: ::::::::
    ████░▐█▌░▐█▌██   ██                    :+:    :+: :+:        :+:    :+: :+:    :+: :+:       :+:    :+: 
   ▐████░▐░░░░░▌██   █▌                    +:+    +:+ +:+        +:+    +:+ +:+        +:+       +:+  
    ████░░░▄█░░░██  ▐█                     +#+    +:+ +#++:++#   +#+    +:+ +#++:++#++ +#++:++#  +#+   
    ████░░░██░░██▌  █▌                     +#+    +#+ +#+        +#+    +#+        +#+ +#+       +#+        
    ████▌░▐█░░███   █                      #+#    #+# #+#        #+#    #+# #+#    #+# #+#       #+#    #+#
    ▐████░░▌░███   ██                      #########  ########## #########   ########  ########## ######## 
     ████░░░███    █▌               
   ██████▌░████   ██                
 ▐████████████  ███                 
 █████████████▄████                 
██████████████████      
"""


def clear():
    os.system("cls")


def display_art():
    clear()
    print(ASCII)

def rgb_float(value: int) -> float:
    return value / 255

# service blueprint
class Service():
    def __init__(self) -> None:
        self.raw_name: str

    def is_enabled(self):
        if self.raw_name:
            return bool(UserConfig[self.raw_name]['ENABLED'])
        return False
    
def rgbtohex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)