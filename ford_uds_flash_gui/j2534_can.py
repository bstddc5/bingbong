from j2534_drewtech_registry_can_final import DrewTechJ2534

class J2534IsoTPChannel:
    def __init__(self, dll_path=None, can_tx=0x7E0, can_rx=0x7E8):
        self.j = DrewTechJ2534()
        self.can_tx = can_tx
        self.can_rx = can_rx
        self.j.open()
        self.j.connect(protocol_id=0x05, flags=0x80, baudrate=500000)

    def send_raw(self, payload: list):
        msg = [self.can_tx >> 8, self.can_tx & 0xFF] + payload
        msg += [0x55] * (8 - len(msg))  # pad to 8 bytes
        print(f"[TX] {msg} — (write not implemented yet)")

    def read(self, timeout=0.5):
        print("[RX] Read not implemented yet")
        return []

    def close(self):
        self.j.close()
