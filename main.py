


# folders = [
#     Path("C:/amaan/cameraPhotos/6thFebandGaon/gaon"),
#     Path("C:/amaan/cameraPhotos/9thNov2025/100CANON"),
#     Path("C:/amaan/cameraPhotos/1thNov2025/100CANON")
#     ]


import pandas as pd
import exifread
from pathlib import Path
import matplotlib.pyplot as plt

folder = Path(input("Enter the path to your photos folder: ").strip())

rows = []
for img_path in folder.glob("*.CR2"):
    try:
        with open(img_path, "rb") as f:
            tags = exifread.process_file(f, details=False)
            focal = tags.get("EXIF FocalLength")
            iso = tags.get("EXIF ISOSpeedRatings")
            dt = tags.get("EXIF DateTimeOriginal")
            aperture = tags.get("EXIF FNumber")
            shutter = tags.get("EXIF ExposureTime")

            rows.append({
                "filename": img_path.name,
                "focalLength": str(focal) if focal else None,
                "iso": str(iso) if iso else None,
                "datetime": str(dt) if dt else None,
                "aperture": str(aperture) if aperture else None,
                "shutter": str(shutter) if shutter else None,
            })
    except Exception as e:
        print(f"Skipped {img_path.name}: {e}")

df = pd.DataFrame(rows)

df["focalLength"] = pd.to_numeric(df["focalLength"], errors="coerce")
df["iso"] = pd.to_numeric(df["iso"], errors="coerce")
df["datetime"] = pd.to_datetime(df["datetime"], format="%Y:%m:%d %H:%M:%S", errors="coerce")
df["hour"] = df["datetime"].dt.hour
df["month"] = df["datetime"].dt.month
df["year"] = df["datetime"].dt.year

print(f"\nTotal photos analysed: {len(df)}")
print(f"Most used focal length: {df['focalLength'].mode()[0]}mm")
print(f"Most used ISO: {df['iso'].mode()[0]}")
print(f"Peak shooting hour: {df['hour'].value_counts().idxmax()}:00")
print(f"Most active month: {df['month'].value_counts().idxmax()}")

print("\n=== ISO vs FOCAL LENGTH (avg by hour) ===")
print(df.groupby("hour")[["iso", "focalLength"]].mean().round(1))

print("\n=== SHOT DISTRIBUTION BY HOUR ===")
print(df["hour"].value_counts().sort_index())

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle("Photography Pattern Analysis", fontsize=14, fontweight="bold")

df["hour"].value_counts().sort_index().plot(kind="bar", ax=axes[0, 0], color="steelblue")
axes[0, 0].set_title("Shots by Hour of Day")
axes[0, 0].set_xlabel("Hour")
axes[0, 0].set_ylabel("Count")

df["iso"].dropna().plot(kind="hist", bins=15, ax=axes[0, 1], color="coral")
axes[0, 1].set_title("ISO Distribution")
axes[0, 1].set_xlabel("ISO")

df["focalLength"].dropna().plot(kind="hist", bins=15, ax=axes[1, 0], color="mediumseagreen")
axes[1, 0].set_title("Focal Length Distribution")
axes[1, 0].set_xlabel("Focal Length (mm)")

axes[1, 1].scatter(df["focalLength"], df["iso"], alpha=0.4, color="mediumpurple")
axes[1, 1].set_title("ISO vs Focal Length")
axes[1, 1].set_xlabel("Focal Length (mm)")
axes[1, 1].set_ylabel("ISO")

plt.tight_layout()
plt.savefig("photography_analysis.png", dpi=150)
plt.show()

print("\nChart saved as photography_analysis.png")