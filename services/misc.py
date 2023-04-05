from lib.utils import Service
from lib.offsets import Offsets
from core.config import UserConfig
from time import sleep
import pymem as mem
import keyboard as kb

# flash opacity override
class Flash(Service):
  def __init__(self, process: mem.Pymem, module) -> None:
    super().__init__()
    self.process = process
    self.module = module
    self.raw_name = "FLASH"


  def invoke(self):
    local_player = self.process.read_uint(self.module + Offsets.signatures.dwLocalPlayer)
    flash_addr = local_player + Offsets.netvars.m_flFlashMaxAlpha

    if not self.is_enabled():
      if flash_addr:
        curr_alpha = self.process.read_float(flash_addr)
        if curr_alpha < float(255):
          self.process.write_float(flash_addr, float(255))
      return

    if local_player:
      try:
        flash_alpha = UserConfig['FLASH']['VALUE'] / 100 * 255
        if flash_addr:
          self.process.write_float(flash_addr, flash_alpha)
      except:
        pass


class Bhop(Service):
  def __init__(self, process: mem.Pymem, module) -> None:
    super().__init__()
    self.process = process
    self.module = module
    self.raw_name = "BHOP"
    
  def invoke(self):
    try:
      if not self.is_enabled():
        return

      if kb.is_pressed("space"):
        force_jump = self.module + Offsets.signatures.dwForceJump
        local_player = self.process.read_int(self.module + Offsets.signatures.dwLocalPlayer)

      if local_player:
        is_grounded = self.process.read_int(local_player + Offsets.netvars.m_fFlags)

        if is_grounded and is_grounded == 257:
          self.process.write_int(force_jump, 5)
          sleep(0.07)
          self.process.write_int(force_jump, 4)
    except:
      pass