# 📷 Photography Habit Analyser

> Analyse your shooting patterns from RAW photo metadata — understand how, when, and how you shoot.

---

## What It Does

This tool reads EXIF metadata from your Canon RAW (`.CR2`) files and turns them into actionable insights about your photography habits.

**You'll find out:**
- 🕐 What time of day you shoot the most
- 📏 Your most used focal lengths
- 🔆 Your ISO preferences
- 📅 Your most active months
- 📊 How ISO and focal length relate across your shoots

---

## Example Output

```
Total photos analysed: 312
Most used focal length: 50.0mm
Most used ISO: 400
Peak shooting hour: 17:00
Most active month: 11
```

Plus a chart saved as `photography_analysis.png`:

| Chart | Description |
|-------|-------------|
| Shots by Hour | When during the day you shoot most |
| ISO Distribution | Your ISO usage patterns |
| Focal Length Distribution | Which focal lengths you reach for |
| ISO vs Focal Length | How these two settings relate |

---

## Getting Started

### 1. Install dependencies

```bash
pip install pandas exifread matplotlib
```

### 2. Run the script

```bash
python photo_analyser.py
```

### 3. Enter your folder path when prompted

```
Enter the path to your photos folder: C:/photos/100CANON
```

That's it. Results print to terminal and a chart is saved automatically.

---

## Requirements

- Python 3.8+
- Canon `.CR2` RAW files with EXIF data
- Libraries: `pandas`, `exifread`, `matplotlib`

---

## Built By

**Mohammad Amaan** — [@chaiaurcamera](https://www.instagram.com/chaiaurcamera/) · [Portfolio](https://photography-portfolio-one-tan.vercel.app/)

> CS student at UCD · Photography enthusiast · Built this to understand my own shooting habits better.
