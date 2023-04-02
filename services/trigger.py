from lib.utils import Service
from lib.offsets import Offsets
import pymem as mem
import keyboard as kb


class Trigger(Service):
  def __init__(self, process: mem.Pymem, module) -> None:
    super().__init__()
    self.enabled = True
    self.process = process
    self.module = module
    self.raw_name = "TRIGGER_BOT"

  def invoke(self):
    if not self.is_enabled():
      return

    try:
      local_player = self.process.read_uint(self.module + Offsets.signatures.dwLocalPlayer)
      entity_id = self.process.read_int(local_player + Offsets.netvars.m_iCrosshairId)
      entity = self.process.read_int(self.module + Offsets.signatures.dwEntityList + (entity_id - 1) * 0x10)
        
      entity_team = self.process.read_int(entity + Offsets.netvars.m_iTeamNum)
      local_team = self.process.read_int(local_player + Offsets.netvars.m_iTeamNum)
      
      if kb.is_pressed("alt"):
        if entity_id > 0 and entity_id <= 64 and local_team != entity_team:
          self.process.write_int(self.module + Offsets.signatures.dwForceAttack, 6)

    except:
      pass