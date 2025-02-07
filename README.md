# MIDI-humanizer

The MIDI Humanizer is a tool that allows you to humanize MIDI files by adding random variations to note timing, duration, and velocity. It provides a graphical user interface (GUI) built with PySide6, making it easy to select MIDI files, adjust humanization parameters, and save the processed files.

## Features

- **Select MIDI File:** Choose a MIDI file using a file dialog.
- **Adjust Humanization Parameters:**
  - **Time Offset:** Randomly shift note start times within a specified range.
  - **Duration Offset:** Randomly adjust note durations within a specified range.
  - **Velocity Offset:** Randomly change note velocities within a specified range.
  - **Duration Percentage:** Reduce note durations by a specified percentage before applying offsets.
- **Multiple Track Processing:** Humanize each track individually while considering notes from all tracks to prevent overlapping.
- **Save Processed File:** Save the humanized MIDI file with a `_humanized` suffix in the same directory.

## Usage

### Linux

```bash
python venv .venv
./.venv/Scripts/activate
pip install -r requirements.txt
python main.py
```

### Windows (Powershell)

```powershell
python -m venv .venv
/.venv/Scripts/activate
pip install requirements.txt
python main.py
```
