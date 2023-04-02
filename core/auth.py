import keyring
import ttkbootstrap as UI
import ctypes
import jwt
import requests
import json

from ttkbootstrap.dialogs.dialogs import Messagebox
from lib.utils import HardwareSpec, Alert, API_ENDPOINT
from urllib.parse import urljoin

TOKEN_SERVICE = "DEDSEC_TOKEN"
HWID_SERVICE = "DEDSEC_HWID"
ACCOUNT_NAME = "DEDSEC_CLIENT"

AUTH_WIN_WIDTH = 400
AUTH_WIN_HEIGHT = 250

MONITOR_WIDTH = ctypes.windll.user32.GetSystemMetrics(0)
MONITOR_HEIGHT = ctypes.windll.user32.GetSystemMetrics(1)


X = (MONITOR_WIDTH - AUTH_WIN_WIDTH) / 2
Y = (MONITOR_HEIGHT - AUTH_WIN_HEIGHT) / 2

class AuthWindow(UI.Window):
  def __init__(self):
    super().__init__(themename="dedsec")
    self.iconbitmap("assets/128.ico")
    self.title("dedsec authenticator")
    self.geometry('%dx%d+%d+%d' % (400, 150, X, Y))
    self.resizable(False, False)
      
    self.token_label = UI.Label(master=self, text="Access Token")
    self.token_entry_value = UI.StringVar()
    self.token_entry_element = UI.Entry(master=self, textvariable=self.token_entry_value)
      
    self.submit_button = UI.Button(master=self, text="SUBMIT", cursor='hand2')
    self.submit_button.bind("<Button>", lambda e: self.validate_user())
    
    self.token_label.pack(side=UI.TOP, pady=(20, 5))
    self.token_entry_element.pack(fill=UI.X, padx=20)
    self.submit_button.pack(pady=5)


  def validate_user(self):
    is_valid = Auth.validate(self.token_entry_value.get())

    if is_valid:
      Alert.info("Your account has been saved successfuly, you may need a restart")
    else:
      Alert.err("Invalid access token was provided")

class Auth:
  def __init__(self):
    pass
  
  def validate(token: str):
    if not token:
      return False

    try:
      decoded_token = jwt.decode(token,algorithms=['HS256'], options={ 'verify_signature': False })

      data = { 
        'token': token, 
        'device': {
          'ip_info': HardwareSpec.ip_info(),
          'mac_addr': str(HardwareSpec.MAC_ADDRESS),
          'uuid': HardwareSpec.UUID,
          'hwid': HardwareSpec.hash(),
        }
      }

      url = urljoin(API_ENDPOINT, "validate")
      res = requests.get(url, data=json.dumps(data))

      if res.status_code != 200:
        return False
      else: 
        hwid = res.json()['hwid']
        if hwid == HardwareSpec.hash():
          keyring.set_password(TOKEN_SERVICE, ACCOUNT_NAME, token)
          return True
        else:
          return False
        
    except Exception as err:
      return False