import pandas as pd
import exifread
from pathlib import Path
from itertools import chain


folders = [
    Path("C:/amaan/cameraPhotos/6thFebandGaon/gaon"),
    Path("C:/amaan/cameraPhotos/9thNov2025/100CANON"),
    Path("C:/amaan/cameraPhotos/1thNov2025/100CANON")
    ]


all_files = chain(folders[0].glob("*.CR2"), folders[1].glob("*.CR2"))

rows = []

for img_path in all_files:
    try:
        with open(img_path,"rb") as f:
            tags = exifread.process_file(f, details=False)

            focal = tags.get("EXIF FocalLength")
            iso = tags.get("EXIF ISOSpeedRatings")
            dt = tags.get("EXIF DateTimeOriginal")

            rows.append({
                "filename":img_path.name,
                "focalLength" : str(focal) if focal else None,
                "iso": str(iso) if iso else None,
                "datetime": str(dt) if dt else None,

            })
    except Exception as e:
        print(f"Skipped {img_path.name}: {e}")


        
df = pd.DataFrame(rows)

df["focalLength"] = df["focalLength"].apply(
    lambda x:float(x) if x is not None else None
)


df["iso"] = df["iso"].apply(
    lambda x: int(x) if x is not None else None
)


print(df.groupby(["focalLength", "iso"]).size())
