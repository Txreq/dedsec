from core.config import UserConfig

import os
import uuid
import subprocess
import hashlib
import requests
import ctypes

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

# retuns some hardware specifications
class HardwareSpec:
    MAC_ADDRESS = uuid.getnode()
    UUID = subprocess.run(['wmic', 'csproduct', 'get', 'uuid'], capture_output=True, text=True).stdout.strip().split("\n")[2]

    def hash():
        hash_obj = hashlib.sha256()
        hash_obj.update(f"{HardwareSpec.MAC_ADDRESS}-{HardwareSpec.UUID}".encode("utf-8"))

        return hash_obj.hexdigest()
    
    def ip_info():
        res = requests.get("http://ip-api.com/json/")
        return res.text
    

# native os alert

class Alert:
    msg = ctypes.windll.user32.MessageBoxW
    MB_ICONEXCLAMATION = 0x00000030
    MB_ICONWARNING = 0x00000030
    MB_ICONINFORMATION = 0x00000040 
    MB_ICONASTERISK = 0x00000040
    MB_ICONQUESTION = 0x00000020
    MB_ICONSTOP = 0x00000010
    MB_ICONERROR = 0x00000010
    MB_ICONHAND = 0x00000010

    def warn(message: str, title: str="Warning"):
        Alert.msg(None, message, title, Alert.MB_ICONWARNING)

    def err(message: str, title: str="Error"):
        Alert.msg(None, message, title, Alert.MB_ICONERROR)

    def info(message: str, title: str="Success"):
        Alert.msg(None, message, title, Alert.MB_ICONINFORMATION)
