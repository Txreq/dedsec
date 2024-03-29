import ttkbootstrap as UI

# views
from views.index import MainTab
from views.settings import SettingsTab
from views.user import UserTab

WIN_WIDTH = 600
WIN_HEIGHT = 350
SETTINGS_WINDOW_SHOWN = False

class AppWindow(UI.Window):
  def __init__(self):
    super().__init__(title="dedsec", resizable=(False, False), themename='dedsec')
    self.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
    self.iconbitmap("assets/sec.ico")

    self.tab_container = UI.Notebook(master=self)
    
    self.tab_container.add(MainTab(), text="Home")
    self.tab_container.add(SettingsTab(), text="Settings")
    self.tab_container.add(UserTab(), text="User")

    self.tab_container.pack(fill=UI.BOTH, expand=True)

  