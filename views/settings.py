from core.config import Config, Toggle, UserConfig
from ttkbootstrap.dialogs.colorchooser import ColorChooserDialog
import lib.utils as utils
import ttkbootstrap as UI


# element blue print
class Element:
  def __init__(self, label: str, key: str, scale: bool=False, row: int=None) -> None:
    self.label = label
    self.key = key
    self.scale = scale
    self.int_var = UI.IntVar(value=UserConfig[key]['ENABLED'])
    if scale:
      self.double_var = UI.DoubleVar(value=UserConfig[key]['VALUE'])

    self.row = row 

class SettingsTab(UI.Frame):
  def __init__(self):
    super().__init__()
    self.render()

  def render(self):
    self.container_one()
    self.container_two()

    # saving button
    self.save_button = UI.Button(master=self, text="SAVE", cursor="hand2", command=Config.save)
    self.save_button.place(x=540, y=280)


  def container_one(self):
    container = UI.Frame(master=self, padding=10)
    
    self.cb_buttons = [
      Element(
        label="Radar",
        key="RADAR",
        row=0
      ),
      Element(
        label="Bunny Bhop",
        key="BHOP",
        row=1
      ),
      Element(
        label="Trigger Bot",
        key="TRIGGER_BOT",
        row=2
      ),
      Element(
        label="Flash",
        key="FLASH",
        row=3,
        scale=True
      ),
    ]

    for (element) in self.cb_buttons:
      def callback(e, element=element):
        Toggle(element.key)

      def on_change(e, element=element):
        if str(UserConfig[element.key]['VALUE']):
          UserConfig[element.key]['VALUE'] = element.double_var.get()

      
      if element.scale:
        item_scale = UI.Scale(
          master=container, 
          bootstyle="secondary", 
          from_=0, to=100, 
          variable=element.double_var
        )
        item_scale.bind("<B1-Motion>", on_change)
        item_scale.grid(column=0, row=element.row + 1)

      item = UI.Checkbutton(master=container, text=element.label, variable=element.int_var)
      item.bind("<Button>", callback)
      item.grid(column=0, row=element.row, sticky=UI.W, pady=5)

    # container
    container.pack(fill=UI.Y, side="left", padx=10, pady=10)
    container.rowconfigure((0, 1, 2), minsize=10)


  def container_two(self):
    container = UI.Frame(master=self, padding=10)

    self.cb_esp_val = UI.IntVar(value=UserConfig['ESP']['ENABLED'])
    self.cb_esp_element = UI.Checkbutton(master=container, text="Glow", variable=self.cb_esp_val)
    self.cb_esp_element.grid(column=0, row=0, sticky=UI.W, pady=5)
    
    self.cb_hb_val = UI.IntVar(value=UserConfig['ESP']['HEALTH_BASED'])
    self.cb_hb_element = UI.Checkbutton(master=container, text="Health Based", variable=self.cb_hb_val)
    self.cb_hb_element.grid(column=0, row=2, sticky=UI.W, pady=5)

    self.enemy_hex = utils.rgbtohex(UserConfig['ESP']['ENEMY_COLOR'])
    self.ecb = UI.Label(master=container, background=self.enemy_hex, width=3, cursor="hand2")
    self.ecl = UI.Label(master=container, text=self.enemy_hex, background="#111111", padding=(20, 0))
    
    self.cb_esp_element.bind("<Button>", lambda e: Toggle("ESP"))
    self.cb_hb_element.bind("<Button>", lambda e: Toggle("ESP", field="HEALTH_BASED"))
    self.ecb.bind("<Button>", lambda e: self.color_picker())
    
    self.ecb.grid(column=1, row=0, sticky=UI.W, padx=(10, 0), pady=5)
    self.ecl.grid(column=2, row=0, sticky=UI.W, pady=5)
    container.pack(fill=UI.Y, side="left", padx=10, pady=10)
      

  def color_picker(self):
    tcp = ColorChooserDialog()
    tcp.show()
    if tcp.result:
      UserConfig["ESP"]["ENEMY_COLOR"] = list(tcp.result.rgb)
      self.ecb.config(background=tcp.result.hex)