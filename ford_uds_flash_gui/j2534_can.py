from j2534_drewtech_registry_can_final import DrewTechJ2534

class J2534IsoTPChannel:
    def __init__(self, dll_path=None, can_tx=0x7E0, can_rx=0x7E8):
        self.j = DrewTechJ2534(dll_path)
        self.can_tx = can_tx
        self.can_rx = can_rx
        self.j.open()

        try:
            # Try CAN_29BIT_ID first
            self.j.connect(protocol_id=0x05, flags=0x80, baudrate=500000)
        except Exception as e:
            if "ConnectFlags" in str(e) or "error code: 6" in str(e):
                print("[FALLBACK] Switching to CAN 11-bit mode...")
                self.j.connect(protocol_id=0x05, flags=0x00, baudrate=500000)
            else:
                raise

    def send_raw(self, payload: list):
        msg = [self.can_tx >> 8, self.can_tx & 0xFF] + payload
        msg += [0x55] * (8 - len(msg))  # pad to 8 bytes
        print(f"[TX] {msg} — (write not implemented yet)")

    def read(self, timeout=0.5):
        print("[RX] Read not implemented yet")
        return []

    def close(self):
        self.j.close()
