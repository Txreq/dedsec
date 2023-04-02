from lib.utils import Service
from lib.offsets import Offsets
from time import sleep
import pymem as mem
import keyboard as kb

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