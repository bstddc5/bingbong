from pyj2534 import J2534
from pyj2534.defines import ProtocolID, BaudRate, ConnectFlags, FilterType


class J2534IsoTPChannel:
    def __init__(self, dll_path, can_tx=0x7E0, can_rx=0x7E8):
        self.j = J2534(dll_path)
        self.device = self.j.open()
        self.channel = self.device.connect(
            ProtocolID.CAN,
            BaudRate.CAN_500K,
            ConnectFlags.CAN_29BIT_ID
        )
        self.channel.start_msg_filter(FilterType.FLOW_CONTROL_FILTER, can_tx, can_rx)
        self.can_tx = can_tx
        self.can_rx = can_rx

    def send_raw(self, payload: list):
        msg = [self.can_tx >> 8, self.can_tx & 0xFF] + payload
        msg += [0x55] * (8 - len(msg))  # pad to 8 bytes
        self.channel.write(msg)

    def read(self, timeout=0.5):
        return self.channel.read(timeout=timeout)

    def close(self):
        self.device.close()
