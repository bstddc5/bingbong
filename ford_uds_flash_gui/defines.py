from ctypes import *

class ProtocolID:
    CAN = 0x00000005

class ConnectFlags:
    CAN_29BIT_ID = 0x00000100
    CAN_ID_BOTH = 0x00000200

class FilterType:
    FLOW_CONTROL_FILTER = 0x00000003

class BaudRate:
    CAN_500K = 500000

class PASSTHRU_MSG(Structure):
    _fields_ = [
        ("ProtocolID", c_ulong),
        ("RxStatus", c_ulong),
        ("TxFlags", c_ulong),
        ("Timestamp", c_ulong),
        ("DataSize", c_ulong),
        ("ExtraDataIndex", c_ulong),
        ("Data", c_ubyte * 4128)
    ]
