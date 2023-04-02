from core.auth import TOKEN_SERVICE, ACCOUNT_NAME
from lib.utils import API_ENDPOINT
from urllib.parse import urljoin

import ttkbootstrap as UI
import keyring
import jwt
import requests

class UserTab(UI.Frame):
  def __init__(self):
    super().__init__()
    self.render()

  def render(self):
    self.token = keyring.get_password(TOKEN_SERVICE, ACCOUNT_NAME)
    self.loading = True
    try:
      self.decoded_token = jwt.decode(self.token, algorithms=['HS256'], options={ 'verify_signature': False })
      self.response = requests.get(urljoin(API_ENDPOINT, "/user"), data={ 'uid': self.decoded_token['id'] })
      self.loading = False

      UI.Label(master=self, text=self.response.status_code).pack()
    except:
      pass