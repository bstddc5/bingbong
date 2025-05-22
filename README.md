# bingbong

# Ford UDS Flash Tool GUI

## Overview

This project is a Python-based GUI tool for **flashing factory Ford PowerPC (Copperhead) ECUs** over **CAN via J2534**, using **UDS (ISO 14229)** and **ISO-TP (ISO 15765-2)**. It is designed for quick testing, seed/key decoding, and partial reflashing using `.bin` firmware files with an **OpenPort 2.0** or other J2534-compatible device.

---

## Current Features

* Simple PyQt5 GUI
* Supports basic UDS flow:

  * `0x10` – Diagnostic Session
  * `0x27` – Security Access (Seed/Key)
  * `0x34` – Request Download
  * `0x36` – Transfer Data
  * `0x37` – Request Transfer Exit
* Logs full UDS traffic to table in real time
* Detects and decodes **negative response codes**
* Plug-and-play support for **Tactrix OpenPort 2.0**

---

## Project Structure

```
ford_uds_flash_gui/
├── main.py                # PyQt5 GUI launcher
├── uds_core.py            # Core UDS flash logic and state machine
├── j2534_can.py           # J2534 interface wrapper for OpenPort or other tools
├── seedkey.py             # Placeholder for Ford seed/key solver
├── example_firmware.bin   # (Optional) Sample firmware file
├── uds_log.csv            # Auto-generated UDS message log (runtime)
├── README.md              # This file
```

---

## Setup Instructions

1. **Install dependencies**:

   ```bash
   pip install pyqt5 pyj2534
   ```

2. **Download OpenPort 2.0 J2534 DLLs** and place them here:

   * Example:
     `C:\Program Files (x86)\OpenECU\J2534\op20pt32.dll`

3. **Run the GUI**:

   ```bash
   python main.py
   ```

---

## Hardware Required

* Ford PCM (Copperhead — e.g., 2011–2014 Mustang GT)
* J2534 interface (tested with Tactrix OpenPort 2.0)
* Bench breakout harness (OBD port + 12V power)

---

## What Still Needs to Be Implemented

| Feature                              | Status      | Notes                                                |
| ------------------------------------ | ----------- | ---------------------------------------------------- |
| ISO-TP segmentation for >7 byte msgs | **Pending** | Basic stub in place; full chunking needed            |
| Real Seed/Key Ford algorithm         | **Pending** | Currently uses a null key                            |
| Full memory segment flashing         | **Partial** | Only flashes first 0xF0 bytes for now                |
| `.VBF` to `.bin` integration         | **Planned** | Already exists separately; integrate via file picker |
| CRC verification                     | **Pending** | Needed after full write to ensure validity           |
| Auto detection of module & layout    | **Pending** | Currently fixed address (0x00800000)                 |
| Error handling / retry mechanism     | **Basic**   | Can improve for robustness                           |

---

## Planned Enhancements

* Export UDS log to `.csv` or `.json`
* Command-line headless mode for batch flashes
* EEPROM support (read/write patches)
* Ford CAN broadcast ID detection (auto-pair to PCM)

---

## License

MIT (TBD)
