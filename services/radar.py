from lib.utils import Service
from lib.offsets import Offsets
import pymem as mem
import keyboard as kb


class Radar(Service):
  def __init__(self, process: mem.Pymem, module) -> None:
    super().__init__()
    self.process = process
    self.module = module
    self.raw_name = "RADAR"

  def invoke(self):
    if not self.is_enabled():
      return

    try:
      for i in range(1, 32 + 1):
        entity = self.process.read_int(self.module + Offsets.signatures.dwEntityList + i * 0x10)
      
        if entity:
          self.process.write_uchar(entity + Offsets.netvars.m_bSpotted, 1)

    except:
      pass