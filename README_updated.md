# Ford UDS Flash Tool

A Python GUI application to flash Ford ECUs using the UDS protocol over a J2534-compatible device.

---

## ✅ Current Features

- [x] PyQt5 GUI with load, flash, and logging interface
- [x] Real-time UDS request/response log table
- [x] Basic UDS flashing (0x10, 0x27, 0x34, 0x36, 0x37)
- [x] Negative response code decoding
- [x] DrewTech Mongoose-Plus Ford2 support via registry-based J2534 loading
- [x] Correct CAN protocol support (ISO15765-2, 500Kbps, 29-bit ID)
- [x] `PassThruOpen`, `PassThruConnect`, and `PassThruReadVersion` wrapped via `ctypes`
- [x] Debug logging and J2534 error string decoding
- [x] Registry-based automatic device detection
- [x] Stubbed seed/key function
- [x] Configurable TX/RX CAN IDs

---

## ⚠️ In Progress

- [ ] Full flash block upload support (only small initial block sent now)
- [ ] Flash progress bar and status feedback
- [ ] VBF → BIN integration using existing tool
- [ ] VIN and part number UDS tab (`0x22 F190`, `0x22 F187`)
- [ ] Save log data to CSV/JSON
- [ ] Retry/recovery logic for failed UDS exchanges

---

## ❌ Not Yet Implemented

- [ ] ISO-TP segmentation for full-length BIN files
- [ ] CRC32 or checksum verification of flashed data
- [ ] EEPROM read/write or calibration data support
- [ ] CAN address auto-detection / discovery
- [ ] Headless CLI mode for batch operations

---

## 🔧 Requirements

- Python 3.10 (32-bit only, for DrewTech DLL compatibility)
- PyQt5
- A valid `.bin` file for your Ford ECU
- Drew Technologies Mongoose-Plus Ford2 + driver + J2534 Toolbox 3

---

## 🛠 Architecture Overview

```
main.py                → GUI logic and layout
uds_core.py            → UDS flash session (0x10/0x27/0x34/0x36/0x37)
j2534_can.py           → Wrapper around real J2534 driver backend
j2534_drewtech_*.py    → Real DLL interaction using ctypes
seedkey.py             → Stubbed security access logic (placeholder)
```

---

## 🧠 Next Steps

- [ ] Wire in `PassThruWriteMsgs` + `ReadMsgs`
- [ ] Add UDS query tab for VIN, SWPN, calibration ID
- [ ] Implement `0x22`/`0x2E`/`0x31` logic for diagnostics and config
- [ ] Connect VBF loader and auto-convert `.vbf` to `.bin`

---

## ✉️ Notes

This tool is **for development and educational use only**. Flashing Ford ECUs incorrectly can brick the module. Always back up data and confirm compatibility.

