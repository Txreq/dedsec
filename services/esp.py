from lib.utils import Service, rgb_float
from lib.offsets import Offsets
from core.config import UserConfig
from threading import Thread
from time import sleep
import pymem as mem

class ESP(Service):
  def __init__(self, process: mem.Pymem, module) -> None:
    super().__init__()
    self.process = process
    self.module = module
    self.raw_name = "ESP"

  def invoke(self):
    if not self.is_enabled():
      return
    class Color:
      Red = rgb_float(UserConfig['ESP']['ENEMY_COLOR'][0])
      Green = rgb_float(UserConfig['ESP']['ENEMY_COLOR'][1])
      Blue = rgb_float(UserConfig['ESP']['ENEMY_COLOR'][2])
      Alpha = UserConfig['ESP']['OPACITY'] / 100

    glow_manager = self.process.read_int(self.module + Offsets.signatures.dwGlowObjectManager)
    local_player = self.process.read_int(self.module + Offsets.signatures.dwLocalPlayer)
    local_team = self.process.read_int(local_player + Offsets.netvars.m_iTeamNum)
  
    for i in range(1, 32 + 1):
      entity = self.process.read_int(self.module + Offsets.signatures.dwEntityList + i * 0x10)

      if entity:
        entity_team = self.process.read_int(entity + Offsets.netvars.m_iTeamNum)
        entity_glow = self.process.read_int(entity + Offsets.netvars.m_iGlowIndex)

        if entity_team != local_team and bool(UserConfig['ESP']['ENABLED']):
          self.process.write_float(glow_manager + entity_glow * 0x38 + 0x8, Color.Red)
          self.process.write_float(glow_manager + entity_glow * 0x38 + 0xC, Color.Green)
          self.process.write_float(glow_manager + entity_glow * 0x38 + 0x10, Color.Blue)
          self.process.write_float(glow_manager + entity_glow * 0x38 + 0x14, Color.Alpha)
          self.process.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)

  def t_invoke(self) -> None:
    while True:
      self.invoke()
      sleep(0.001)

  def thread(self) -> Thread:
    t = Thread(target=self.t_invoke)
    t.setDaemon(True)
    return t