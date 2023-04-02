from lib.utils import display_art, Alert
from window import AppWindow
from core.auth import AuthWindow, Auth, TOKEN_SERVICE, ACCOUNT_NAME
import keyring

def main():
  display_art()

  saved_token = keyring.get_password(TOKEN_SERVICE, ACCOUNT_NAME)
  is_valid_user = Auth.validate(saved_token)

  if not is_valid_user:
    if bool(saved_token):
      Alert.err("Saved access token is invalid")

    auth_win = AuthWindow()
    auth_win.mainloop()
  else:
    window = AppWindow()
    window.mainloop()

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    pass
