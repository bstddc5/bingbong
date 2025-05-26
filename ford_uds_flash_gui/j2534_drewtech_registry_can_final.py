from ctypes import *
from defines import *
import time

class DrewTechJ2534:
    def __init__(self, dll_path):
        self.DLL_PATH = dll_path
        self.j2534 = cdll.LoadLibrary(self.DLL_PATH)

        self.j2534.PassThruOpen.argtypes = [c_void_p, POINTER(c_ulong)]
        self.j2534.PassThruOpen.restype = c_long

        self.j2534.PassThruConnect.argtypes = [c_ulong, c_ulong, c_ulong, c_ulong, POINTER(c_ulong)]
        self.j2534.PassThruConnect.restype = c_long

        self.j2534.PassThruWriteMsgs.argtypes = [c_ulong, POINTER(PASSTHRU_MSG), POINTER(c_ulong), c_ulong]
        self.j2534.PassThruWriteMsgs.restype = c_long

        self.j2534.PassThruReadMsgs.argtypes = [c_ulong, POINTER(PASSTHRU_MSG), POINTER(c_ulong), c_ulong]
        self.j2534.PassThruReadMsgs.restype = c_long

        self.j2534.PassThruClose.argtypes = [c_ulong]
        self.j2534.PassThruClose.restype = c_long

        self.device_id = c_ulong()
        self.channel_id = c_ulong()

    def open(self):
        result = self.j2534.PassThruOpen(None, byref(self.device_id))
        if result != 0:
            raise RuntimeError(f"PassThruOpen failed: {result}")
        print(f"[OPEN] device_id={self.device_id.value}")

    def connect(self, protocol_id, flags, baudrate):
        result = self.j2534.PassThruConnect(
            self.device_id, protocol_id, flags, baudrate, byref(self.channel_id))
        if result != 0:
            raise RuntimeError(f"PassThruConnect failed: {result}")
        print(f"[CONNECT] channel_id={self.channel_id.value}")

    def send_raw(self, data):
        msg = PASSTHRU_MSG()
        msg.ProtocolID = ProtocolID.CAN
        msg.TxFlags = 0
        msg.DataSize = len(data)
        msg.Data = (c_ubyte * 4128)(*data)
        msg.Timeout = 1000
        msg.ExtraDataIndex = 0

        num_msgs = c_ulong(1)
        result = self.j2534.PassThruWriteMsgs(self.channel_id, byref(msg), byref(num_msgs), 1000)
        if result != 0:
            raise RuntimeError(f"WriteMsgs failed: {result}")
        print(f"[TX] {list(msg.Data[:msg.DataSize])}")

    def read(self, timeout=1000):
        msg = PASSTHRU_MSG()
        msg.ProtocolID = ProtocolID.CAN
        msg.DataSize = 4128
        msg.Data = (c_ubyte * 4128)()

        num_msgs = c_ulong(1)
        result = self.j2534.PassThruReadMsgs(self.channel_id, byref(msg), byref(num_msgs), timeout)
        if result != 0 or num_msgs.value == 0:
            return []
        return list(msg.Data[:msg.DataSize])

    def close(self):
        if self.device_id:
            self.j2534.PassThruClose(self.device_id)
            print("[CLOSE] Device closed.")
