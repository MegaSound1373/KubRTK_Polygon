# Polygon

A mobile Android app for tracking points at the “Kub RTK” polygon..
Allows you to place cells, keep track of points for tasks and penalties,
save and load polygon diagrams.

## 📥 Download
.
The ready-made APK file is in the [Releases](../../releases/latest) section.

1. Download the latest APK to your phone..
2. Allow installation from unknown sources if required.
3. Install and launch.

## ✨ Opportunities

- **Game board** with a grid ranging from 3×3 to 50×50 cells.
- **Zoom** from 10% to 100% with auto‑scrolling.
- **Cells with multiple parts** (for example, “Door”, “Mines”, “Slide with pipes”) — displayed as separate mini‑rectangles.
- **Cell stacking** at one position — several cells share one cell.
-**Constructor** — placing and removing cells, saving the diagram to a file.
- **Tasks and penalties** — counters with restrictions, automatic score calculation.
- **Automatic update check** — the app notifies about new releases.

## 🛠 Building from source

Requires Linux (Ubuntu) or WSL with Python 3.11+ and Buildozer installed.

# 1. Clone the repository
git clone https://github.com/MegaSound1373/KubRTK_Polygon.git
cd polygon

# 2. Create a virtual environment
python3 -m venv buildozer-env
source buildozer-env/bin/activate

# 3. Install Buildozer
pip install buildozer cython

# 4. Build the APK (the first time will take 30–60 minutes)
buildozer -v android debug
