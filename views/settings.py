from core.config import Config, Toggle, UserConfig
from ttkbootstrap.dialogs.colorchooser import ColorChooserDialog
import lib.utils as utils
import ttkbootstrap as UI


# element blue print
class Element:
  def __init__(self, label: str, key: str, row: int=None) -> None:
    self.label = label
    self.key = key
    self.int_var = UI.IntVar(value=UserConfig[key]['ENABLED'])
    try:
      self.double_var = UI.DoubleVar(value=UserConfig[key]['VALUE'])
    except:
      pass
    self.row = row 

class SettingsTab(UI.Frame):
  def __init__(self):
    super().__init__()
    self.render()

  def render(self):
    self.container_one()
    self.container_two()
    self.container_three()

    # saving button
    self.save_button = UI.Button(master=self, text="SAVE", cursor="hand2", command=Config.save)
    self.save_button.place(x=540, y=280)


  def container_one(self):
    container = UI.Frame(master=self, padding=10)
    
    self.cb_buttons = [
      Element(
        label="Radar",
        key="RADAR",
      ),
      Element(
        label="Bunny Bhop",
        key="BHOP",
      ),
      Element(
        label="Trigger Bot",
        key="TRIGGER_BOT",
      ),
    ]

    for (i, element) in enumerate(self.cb_buttons):
      def callback(e, element=element):
        Toggle(element.key)

      item = UI.Checkbutton(master=container, text=element.label, variable=element.int_var)
      item.bind("<Button>", callback)
      item.grid(column=0, row=i, sticky=UI.W, pady=5)

    # container
    container.pack(fill=UI.Y, side="left", padx=10, pady=10)
    container.rowconfigure((0, 1, 2), minsize=10)


  def container_two(self):
    container = UI.Frame(master=self, padding=10)

    self.cb_esp_val = UI.IntVar(value=UserConfig['ESP']['ENABLED'])
    self.cb_esp_element = UI.Checkbutton(master=container, text="Glow", variable=self.cb_esp_val)
    self.cb_esp_element.grid(column=0, row=0, sticky=UI.W, pady=5)
    self.cb_esp_element.bind("<Button>", lambda e: Toggle("ESP"))
    self.enemy_hex = utils.rgbtohex(UserConfig['ESP']['ENEMY_COLOR'])
    self.ecb = UI.Label(master=container, background=self.enemy_hex, width=3, cursor="hand2")
    self.ecl = UI.Label(master=container, text=self.enemy_hex, background="#111111", padding=(20, 0))
    self.ecb.bind("<Button>", lambda e: self.color_picker())
    self.ecb.grid(column=1, row=0, sticky=UI.W, padx=(10, 0), pady=5)
    self.ecl.grid(column=2, row=0, sticky=UI.W, pady=5)
    container.pack(fill=UI.Y, side="left", padx=10, pady=10)

  def container_three(self):
    container = UI.Frame(master=self, padding=10)
    self.elements = [
      Element(
        label="FOV",
        key="FOV",
        row=0
      ),
      Element(
        label="Flash",
        key="FLASH",
        row=2
      ),
    ]

    for (i, element) in enumerate(self.elements):
      item = UI.Checkbutton(master=container, text=element.label, variable=element.int_var)  

      def on_click(e, element=element):
        Toggle(element.key)

      def on_change(e, element=element):
        UserConfig[element.key]['VALUE'] = element.double_var.get()
          

      item_scale = UI.Scale(
        master=container, 
        bootstyle="secondary", 
        from_=0, to=100, 
        variable=element.double_var
      )
      item.bind("<Button>", on_click)
      item_scale.bind("<B1-Motion>", on_change)

      item.grid(column=0, row=element.row, sticky=UI.W, pady=5)
      item_scale.grid(column=0, row=element.row + 1, sticky=UI.W,)
    container.pack(fill=UI.Y, side="left", padx=10, pady=10)

  def color_picker(self):
    tcp = ColorChooserDialog()
    tcp.show()
    if tcp.result:
      UserConfig["ESP"]["ENEMY_COLOR"] = list(tcp.result.rgb)
      self.ecb.config(background=tcp.result.hex)