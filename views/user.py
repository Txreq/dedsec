from core.auth import TOKEN_SERVICE, ACCOUNT_NAME
from lib.utils import API_ENDPOINT
from urllib.parse import urljoin
from io import BytesIO
from PIL import Image, ImageTk


import ttkbootstrap as UI
import keyring
import jwt
import requests

class UserTab(UI.Frame):
  def __init__(self):
    super().__init__(padding=(15, 10))
    self.render()

  def render(self):
    self.token = keyring.get_password(TOKEN_SERVICE, ACCOUNT_NAME)
    self.loading = True
    try:
      self.decoded_token = jwt.decode(self.token, algorithms=['HS256'], options={ 'verify_signature': False })
      self.user_res = requests.get(urljoin(API_ENDPOINT, "user"), data=self.decoded_token['id'])
      self.data = self.user_res.json()

      UI.Label(master=self, text=self.data['name'], font=("Calibri", 20, "bold")).grid(column=0, row=0, sticky=UI.W)
      UI.Label(master=self, text="EMAIL", font=("Arial", 10, "bold")).grid(column=0, row=1, sticky=UI.W)
      UI.Label(master=self, text=self.data['email']).grid(column=1, row=1, sticky=UI.W)

      UI.Label(master=self, text="HWID", font=("Arial", 10, "bold")).grid(column=0, row=2, sticky=UI.W)
      UI.Label(master=self, text=self.data['hwid']).grid(column=1, row=2, sticky=UI.W)

    except Exception as err:
      pass