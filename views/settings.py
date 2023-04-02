from core.config import Config, Toggle, UserConfig
from ttkbootstrap.dialogs.colorchooser import ColorChooserDialog
import lib.utils as utils
import ttkbootstrap as UI

class SettingsTab(UI.Frame):
  def __init__(self):
    super().__init__()
    self.render()


  def render(self):
    self.general_settings()
    self.esp_settings()
    # saving button

  def general_settings(self):
    container = UI.Labelframe(master=self, padding=10, text="General")
    
    self.cb_buttons = [
      {
        'label': "Radar",
        'key': 'RADAR',
        'value':  UI.IntVar(value=UserConfig['RADAR']['ENABLED'])
      },

      {
        'label': "Trigger Bot",
        'key': 'TRIGGER_BOT',
        'value':  UI.IntVar(value=UserConfig['TRIGGER_BOT']['ENABLED'])
      },
      {
        'label': "Bunny Bhop",
        'key': 'BHOP',
        'value':  UI.IntVar(value=UserConfig['BHOP']['ENABLED'])
      },
    ]

    for (i, cb_button) in enumerate(self.cb_buttons):
      def callback(e, btn=cb_button):
        Toggle(btn['key'])

      element = UI.Checkbutton(master=container, text=cb_button['label'], variable=cb_button['value'])
      element.bind("<Button>", callback)
      element.grid(column=0, row=i, sticky=UI.W, pady=5)

    # flash
    self.cb_flash_val = UI.IntVar(value=UserConfig['FLASH']['ENABLED'])
    self.cb_flash_element = UI.Checkbutton(master=container, text="Flash Opacity Override", variable=self.cb_flash_val)
    self.cb_flash_element.grid(column=0, row=4, sticky=UI.W, pady=5)

    self.scale_flash_val = UI.IntVar(value=UserConfig['FLASH']['VALUE'])
    self.scale_flash_element = UI.Scale(master=container, bootstyle="secondary", from_=0, to=100, variable=self.scale_flash_val)
    self.scale_flash_element.grid(column=0, row=5, sticky=UI.W,)


    # fov
    self.cb_fov_val = UI.IntVar(value=UserConfig['FOV']['ENABLED'])
    self.cb_fov_element = UI.Checkbutton(master=container, text="FOV", variable=self.cb_fov_val)
    self.cb_fov_element.grid(column=0, row=6, sticky=UI.W, pady=5)

    self.scale_fov_val = UI.IntVar(value=UserConfig['FOV']['VALUE'])
    self.scale_fov_element = UI.Scale(master=container, bootstyle="secondary", from_=0, to=100, variable=self.scale_fov_val)
    self.scale_fov_element.grid(column=0, row=7, sticky=UI.W)

    # container
    container.pack(fill=UI.Y, side="left", padx=10, pady=10)
    container.rowconfigure((0, 1, 2), minsize=10)

  def esp_settings(self):
    container = UI.Labelframe(master=self, padding=10,text="ESP", width=100)

    self.cb_esp_val = UI.IntVar(value=UserConfig['ESP']['ENABLED'])
    self.cb_esp_enem_val = UI.IntVar(value=UserConfig['ESP']['ENEMY'])
    self.cb_esp_team_val = UI.IntVar(value=UserConfig['ESP']['TEAM'])

    self.cb_esp_element = UI.Checkbutton(master=container, text="Glow", variable=self.cb_esp_val)
    self.cb_esp_team_element = UI.Checkbutton(master=container, text="Team", variable=self.cb_esp_team_val)
    self.cb_esp_enem_element = UI.Checkbutton(master=container, text="Enemies", variable=self.cb_esp_enem_val)
    
    self.cb_esp_element.grid(column=0, row=0, sticky=UI.W, pady=5)
    self.cb_esp_team_element.grid(column=0, row=1, sticky=UI.W, pady=5, padx=(10, 0))
    self.cb_esp_enem_element.grid(column=0, row=2, sticky=UI.W, pady=5, padx=(10, 0))
    
    self.cb_esp_element.bind("<Button>", lambda e: Toggle("ESP"))
    self.cb_esp_team_element.bind("<Button>", lambda e: Toggle("ESP", "TEAM"))
    self.cb_esp_enem_element.bind("<Button>", lambda e: Toggle("ESP", "ENEMY"))

    self.save_button = UI.Button(master=container, text="💾 SAVE", command=Config.save)
    self.save_button.place(x=370, y=235)

    # color pickers
    self.team_hex = utils.rgbtohex(UserConfig['ESP']['TEAM_COLOR'])
    self.enemy_hex = utils.rgbtohex(UserConfig['ESP']['ENEMY_COLOR'])

    # team
    self.tcb = UI.Label(master=container, background=self.team_hex, width=3, cursor="hand2")
    self.tcl = UI.Label(master=container, text=self.team_hex, background="#111111", padding=(20, 0))
    self.tcb.bind("<Button>", lambda e: self.color_setter("TEAM"))

    # enemy
    self.ecb = UI.Label(master=container, background=self.enemy_hex, width=3, cursor="hand2")
    self.ecl = UI.Label(master=container, text=self.enemy_hex, background="#111111", padding=(20, 0))
    self.ecb.bind("<Button>", lambda e: self.color_setter("ENEMY"))

    # render
    self.tcb.grid(column=1, row=1, sticky=UI.E, pady=5, padx=(10, 0))
    self.ecb.grid(column=1, row=2, sticky=UI.E, pady=5, padx=(10, 0))
    self.tcl.grid(column=2, row=1, sticky=UI.W, pady=5)
    self.ecl.grid(column=2, row=2, sticky=UI.W, pady=5)
    container.pack(fill=UI.BOTH, expand=True, padx=(0, 10), pady=10)

  def color_setter(self, side: str):
    tcp = ColorChooserDialog()
    tcp.show()

    if tcp.result:
      UserConfig["ESP"][f"{side}_COLOR"] = list(tcp.result.rgb)
      
      if side == "TEAM":
        self.tcb.config(background=tcp.result.hex)
        self.tcl.config(text=tcp.result.hex)
      if side == "ENEMY":
        self.ecb.config(background=tcp.result.hex)
        self.ecl.config(text=tcp.result.hex)

