import ttkbootstrap as UI
import pymem as mem
from threading import Thread
from PIL import Image, ImageTk

# services
from services.bhop import Bhop
from services.radar import Radar
from services.trigger import Trigger
from services.esp import ESP

class MainTab(UI.Frame):
  def __init__(self) -> None:
    super().__init__()
    self.render()
    self.init()

    
  def render(self):
    # main
    self.banner_image = ImageTk.PhotoImage(Image.open("assets/banner.png"))
    self.banner = UI.Label(master=self, image=self.banner_image)
    self.banner.pack(side=UI.TOP)

    self.attach_btn = UI.Button(
      master=self, 
      bootstyle=UI.SECONDARY, 
      text="ATTACH", 
      cursor="hand2",
      width=30,
      command=self.start,
      state=UI.NORMAL
    )

    self.process_status_str = UI.StringVar(master=self)
    self.process_status_label = UI.Label(master=self, textvariable=self.process_status_str)

    # footer
    self.version_label = UI.Label(text="vesion 2.0 (closed beta)", style="light", font="Inter 8").place(x=5, y=(25))
    self.copyrights_label = UI.Label(text="made by Txreq", style="light", font="Inter 8").place(x=5, y=(45))
    
    # settings window
    self.settings_button = UI.Button(
      text="⚙", 
      bootstyle=(UI.SECONDARY, UI.OUTLINE),
      cursor="hand2",
    )

  def init(self):
    self.attach_btn.pack()
    self.process_status_label.pack(pady=10)

    try:
      self.proc = mem.Pymem("csgo.exe")
      self.module = mem.pymem.process.module_from_name(self.proc.process_handle, "client.dll").lpBaseOfDll
      self.process_status_str.set(f"CSGO ({self.proc.process_id})")

    except:
      self.process_status_str.set(f"CSGO process was not found")
      self.attach_btn.config(state=UI.DISABLED)

  def start(self):
      # threads
      ESP(self.proc, self.module).thread().start()

      self.attach_btn.config(text="ATTACHED", state=UI.ACTIVE, bootstyle=UI.SUCCESS, command=None)
      self.loop()

  # client loop
  def loop(self):
    try:
      Radar(self.proc, self.module).invoke()
      Bhop(self.proc, self.module).invoke()
      Trigger(self.proc, self.module).invoke()
      self.after(ms=1, func=self.loop)
    except Exception as err:
      self.attach_btn.config(text="ERROR", state=UI.DISABLED, bootstyle=UI.DANGER)
      self.process_status_str.set("An error occured during execution")
      print(err)

