class UDSFlashSession:
    def __init__(self, dll_path, debug_func=None):
        self.debug = debug_func or print
        self.dll_path = dll_path
        self.connected = False

    def connect(self):
        self.debug("[CONNECT] Simulated connect")
        self.connected = True

    def close(self):
        self.debug("[CLOSE] Device closed.")
        self.connected = False

    def read_data_by_identifier(self, did):
        self.debug(f"[0x22] Requesting DID 0x{did:04X}")
        dummy = {
            0xF190: "1FTFX1CF9BKD38144",
            0xF187: "KTC3C65.H32",
            0xF188: "88E1CE09",
            0xF194: "PCM-PowertrainCtrl"
        }
        return dummy.get(did, "N/A")
