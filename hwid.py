import ttkbootstrap as UI
import uuid
import subprocess
import hashlib
import requests

class HardwareSpec:
    MAC_ADDRESS = uuid.getnode()
    UUID = subprocess.run(['wmic', 'csproduct', 'get', 'uuid'], capture_output=True, text=True).stdout.strip().split("\n")[2]

    def hash():
        hash_obj = hashlib.sha256()
        hash_obj.update(f"{HardwareSpec.MAC_ADDRESS}-{HardwareSpec.UUID}".encode("utf-8"))

        return hash_obj.hexdigest()
    
    def ip_info():
        res = requests.get("http://ip-api.com/json/")
        return res.text

window = UI.Window(themename='dedsec')
window.title("HWID Finder")
window.geometry("400x50")
window.resizable(False, False)

hwid = UI.StringVar()

hwid.set(HardwareSpec.hash())

def copy():
    window.clipboard_clear()
    window.clipboard_append(hwid.get())

UI.Entry(master=window, textvariable=hwid, state=UI.READONLY).pack(padx=(20, 5), expand=True, fill=UI.X, side="left")
UI.Button(master=window, text="Copy", cursor="hand2", command=copy).pack(side="left", padx=(5, 20))
window.mainloop()