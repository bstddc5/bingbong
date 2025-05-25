from j2534_can import J2534IsoTPChannel
from seedkey import solve_key

NEG_CODES = {
    0x10: "General Reject",
    0x11: "Service Not Supported",
    0x12: "SubFunction Not Supported",
    0x33: "Security Access Denied",
    0x35: "Invalid Key",
    0x36: "Exceeded Attempts",
    0x78: "Response Pending",
    0x22: "Conditions Not Correct",
    0x31: "Request Out of Range",
}

class UDSFlashSession:
    def __init__(self, logger=print, dll_path=None):
        self.log = logger
        self.dll_path = dll_path or r"C:\Program Files (x86)\OpenECU\J2534\op20pt32.dll"
        self.channel = None

    def decode_negative(self, resp):
        if len(resp) >= 3 and resp[0] == 0x7F:
            service = resp[1]
            code = resp[2]
            meaning = NEG_CODES.get(code, "Unknown Error")
            return f"NEG: Service 0x{service:02X}, Code 0x{code:02X} → {meaning}"
        return ""

    def log_rx(self, resp):
        decoded = self.decode_negative(resp)
        self.log("RX", resp, decoded)

    def run(self, bin_data):
        self.channel = J2534IsoTPChannel(dll_path=self.dll_path)

        def send(data):
            self.log("TX", data)
            self.channel.send_raw(data)

        def recv():
            msgs = self.channel.read()
            for msg in msgs:
                data = msg.Data
                self.log_rx(data)
                return data
            self.log("RX", [], "No response")
            return []

        try:
            send([0x10, 0x03])
            recv()

            send([0x27, 0x01])
            resp = recv()
            seed = resp[2:] if len(resp) > 2 else b'\x00\x00\x00\x00'
            key = solve_key(bytes(seed))

            send([0x27, 0x02] + list(key))
            recv()

            addr = 0x00800000
            size = min(len(bin_data), 0xF0)

            send([0x34, 0x00, 0x44] + list(addr.to_bytes(4, 'big')) + list(size.to_bytes(4, 'big')))
            recv()

            send([0x36, 0x01] + list(bin_data[:size]))
            recv()

            send([0x37])
            recv()

        finally:
            self.channel.close()

    def test_session(self):
        self.channel = J2534IsoTPChannel(dll_path=self.dll_path)
        self.channel.send_raw([0x10, 0x03])
        resp = self.channel.read()
        for msg in resp:
            self.log("RX", msg.Data, "Test session response")
        self.channel.close()
