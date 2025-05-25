import winreg
from ctypes import *

def get_first_j2534_device():
    base_key = r"SOFTWARE\PassThruSupport.04.04"
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, base_key) as root:
            for i in range(0, winreg.QueryInfoKey(root)[0]):
                try:
                    subkey_name = winreg.EnumKey(root, i)
                    with winreg.OpenKey(root, subkey_name) as subkey:
                        name = winreg.QueryValueEx(subkey, "Name")[0]
                        dll = winreg.QueryValueEx(subkey, "FunctionLibrary")[0]
                        return name, dll
                except FileNotFoundError:
                    continue
    except FileNotFoundError:
        print("J2534 registry base key not found.")
    return None, None

class DrewTechJ2534:
    def __init__(self):
        self.device_name, self.DLL_PATH = get_first_j2534_device()
        if not self.device_name or not self.DLL_PATH:
            raise RuntimeError("No valid J2534 device found in registry.")
        print(f"[INIT] Device='{self.device_name}'\n       DLL='{self.DLL_PATH}'")

        self.j2534 = cdll.LoadLibrary(self.DLL_PATH)

        self.j2534.PassThruOpen.argtypes = [c_void_p, POINTER(c_ulong)]
        self.j2534.PassThruOpen.restype = c_long

        self.j2534.PassThruConnect.argtypes = [c_ulong, c_ulong, c_ulong, c_ulong, POINTER(c_ulong)]
        self.j2534.PassThruConnect.restype = c_long

        self.j2534.PassThruClose.argtypes = [c_ulong]
        self.j2534.PassThruClose.restype = c_long

        self.j2534.PassThruReadVersion.argtypes = [c_ulong, c_char_p, c_char_p, c_char_p]
        self.j2534.PassThruReadVersion.restype = c_long

        self.j2534.PassThruGetLastError.argtypes = [c_char_p]
        self.j2534.PassThruGetLastError.restype = c_long

        self.device_id = c_ulong()
        self.channel_id = c_ulong()

    def get_last_error(self):
        buf = create_string_buffer(256)
        self.j2534.PassThruGetLastError(buf)
        return buf.value.decode()

    def read_driver_version_without_device(self):
        print("[DEBUG] Attempting PassThruReadVersion with device_id = 0")
        dll_buf, fw_buf, api_buf = create_string_buffer(80), create_string_buffer(80), create_string_buffer(80)
        result = self.j2534.PassThruReadVersion(0, dll_buf, fw_buf, api_buf)
        print(f"[DEBUG] PassThruReadVersion (pre-open) result={result}")
        print(" DLL:", dll_buf.value.decode())
        print(" FW :", fw_buf.value.decode())
        print(" API:", api_buf.value.decode())
        return result

    def open(self):
        print("[DEBUG] Calling PassThruOpen...")
        result = self.j2534.PassThruOpen(None, byref(self.device_id))
        if result == 0:
            print(f"[OPEN] device_id={self.device_id.value}")
        else:
            error = self.get_last_error()
            raise RuntimeError(f"PassThruOpen failed: {result} → {error}")
        return self.device_id.value

    def connect(self, protocol_id=0x05, flags=0x80, baudrate=500000):
        print("[DEBUG] Calling PassThruConnect...")
        result = self.j2534.PassThruConnect(
            self.device_id,
            protocol_id,
            flags,
            baudrate,
            byref(self.channel_id)
        )
        if result == 0:
            print(f"[CONNECT] channel_id={self.channel_id.value}")
        else:
            error = self.get_last_error()
            raise RuntimeError(f"PassThruConnect failed: {result} → {error}")
        return self.channel_id.value

    def read_version(self):
        dll_buf, fw_buf, api_buf = create_string_buffer(80), create_string_buffer(80), create_string_buffer(80)
        result = self.j2534.PassThruReadVersion(self.device_id, dll_buf, fw_buf, api_buf)
        if result != 0:
            raise RuntimeError(f"PassThruReadVersion failed: {result}")
        return {
            "dll": dll_buf.value.decode(),
            "firmware": fw_buf.value.decode(),
            "api": api_buf.value.decode()
        }

    def close(self):
        self.j2534.PassThruClose(self.device_id)
        print("[CLOSE] Device closed.")

if __name__ == "__main__":
    api = DrewTechJ2534()
    api.read_driver_version_without_device()

    try:
        api.open()
        version = api.read_version()
        print("[VERSION]")
        for k, v in version.items():
            print(f"  {k.upper()}: {v}")
        api.connect()
        api.close()
    except Exception as e:
        print("❌ EXCEPTION:", str(e))
