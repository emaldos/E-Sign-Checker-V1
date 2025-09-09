# ✒️ E-Sign Checker V1

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://python.org)
[![Windows](https://img.shields.io/badge/platform-Windows-0078D6.svg)](https://www.microsoft.com/windows/)
[![GitHub Stars](https://img.shields.io/github/stars/emaldos/E-Sign-Checker-V1.svg)](https://github.com/emaldos/E-Sign-Checker-V1/stargazers)
[![GitHub Issues](https://img.shields.io/github/issues/emaldos/E-Sign-Checker-V1.svg)](https://github.com/emaldos/E-Sign-Checker-V1/issues)

A fast, dark-themed Windows desktop app for capturing, storing, and verifying electronic signatures.  
Clean 3-tab workflow, search with pagination, thumbnails, and similarity-based verification tolerant to small drawing differences.

---

## 🌟 Features

### 🖥️ Modern UI
- Dark mode throughout
- Window opens at 80% of your display and centers itself
- Resizable signature canvases with min/max bounds

### 🗂️ Organized Workflow
- **Home**: search bar + paginated table with thumbnails, auto-loads from DB
- **Add Signature**: owner/title/notes inline + draw area + save
- **Check Signature**: split view Old vs New; load Old from file or select from DB; draw or load New

### 🔐 Smart Verification
- Combined similarity score (pixel difference + perceptual hash)
- Adjustable threshold slider (50–99%, default 90%)
- Clear pass/fail result with percentage

### 💾 Storage & Launch
- SQLite DB `electronic_signatures.db` in project root
- Log file `signature_app.log` in project root
- Windows-only silent launcher `run_app.vbs` (no console window)
- Auto-installs required Python packages on first run

---

## 📦 Requirements (Windows only)

- Windows 10/11 (x64)
- Python 3.10+ installed and available as `py` or `python`
  - The launcher will install: `PyQt6`, `Pillow`, `numpy`

---

## 📥 Installation (Windows)

```bash
git clone https://github.com/emaldos/E-Sign-Checker-V1.git
cd E-Sign-Checker-V1
```

### One-click launch (recommended)
Double-click `run_app.vbs`  
• Launches the app with no console window  
• Installs missing Python packages automatically

### Manual launch (console)
```bash
py -3 Luncher.py
# or
python Luncher.py
```

---

## 🚀 Quick Start

1. Open the app (`run_app.vbs`).
2. Go to **Add Signature**:
   - Fill Owner / Title / Notes
   - Draw the signature
   - Click **Save**
3. Go to **Home**:
   - Search any field
   - Use Prev/Next or enter a page number
   - View signature thumbnails
4. Go to **Check Signature**:
   - Old: Load from file or **Select From DB**
   - New: Draw or load from file
   - Adjust **Threshold** and click **Verify**

---

## 🗃️ Project Structure

```
E-Sign-Checker-V1/
├─ app/
│  ├─ main.py
│  ├─ home_tab.py
│  ├─ add_signature_tab.py
│  ├─ check_signature_tab.py
│  ├─ signature_db.py
│  ├─ signature_canvas.py
│  ├─ styles.py
│  └─ similarity.py
├─ Luncher.py
├─ run_app.vbs
├─ electronic_signatures.db        # created on first save
├─ signature_app.log               # runtime log
└─ README.md
```

---

## 🔧 Configuration

- Pagination size: `PAGE_SIZE` in `app/home_tab.py`
- Canvas min/max size: defaults in `app/signature_canvas.py`
- Theme colors and table styling: `app/styles.py`

---

## 🛠️ Troubleshooting (Windows)

**Python not found**  
Install Python 3.10+ from https://www.python.org/downloads/ and ensure `py` or `python` is on PATH. Then run `run_app.vbs` again.

**Missing packages / import errors**  
Run the launcher once from the console to view messages:
```bash
py -3 Luncher.py
```

**Blank Home table**  
Add a signature first in **Add Signature**, then use search and pagination to navigate.

**No GUI appears**  
Check `signature_app.log` in the project root for errors.

---

## 🤝 Contributing

1. Fork the repo
2. Create a branch: `git checkout -b feat/your-feature`
3. Make changes and test
4. Open a Pull Request with a clear description and screenshots for UI changes

Issues and feature requests:  
https://github.com/emaldos/E-Sign-Checker-V1/issues

---

## 🔗 Links

- Repository: https://github.com/emaldos/E-Sign-Checker-V1
- Python: https://www.python.org/
