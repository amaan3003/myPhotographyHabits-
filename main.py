


# folders = [
#     Path("C:/amaan/cameraPhotos/6thFebandGaon/gaon"),
#     Path("C:/amaan/cameraPhotos/9thNov2025/100CANON"),
#     Path()
#     ]


#importing all the libraries we will require, pandas for storing the data in data frames, exifread for reading data from the photos, and matplotlib to show the data visually in charts and diagrams

import pandas as pd
import numpy as np
import exifread
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

#getting the input from the user about the folder their photos are in
folders = [
    Path("C:/amaan/cameraPhotos/6thFebandGaon/gaon"),
    Path("C:/amaan/cameraPhotos/9thNov2025/100CANON"),
    Path("C:/amaan/cameraPhotos/1thNov2025/100CANON"),
]



# making an empty list.
rows = []


# scrapping data from the folder provided, filter as cr2 format(canon raw img format) with info like focal length, iso, data time , aperture etc and storing them all in list - row
for folder in folders:
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




#storing all data of rows in panda data frame because it is significantly more faster to perform any operations on it that the inherit python list.
df = pd.DataFrame(rows)




#all the data stored in rows was in the format of string so adding operations to convert values in their respective form without fail.
df["focalLength"] = pd.to_numeric(df["focalLength"], errors="coerce")
df["iso"] = pd.to_numeric(df["iso"], errors="coerce")
df["datetime"] = pd.to_datetime(df["datetime"], format="%Y:%m:%d %H:%M:%S", errors="coerce")
df["hour"] = df["datetime"].dt.hour
df["month"] = df["datetime"].dt.month
df["year"] = df["datetime"].dt.year


def parse_shutter(val):
    if pd.isna(val):
        return None
    val = str(val)
    if "/" in val:
        num, den = val.split("/")
        return float(num) / float(den)
    return float(val)


def parse_aperture(val):
    if pd.isna(val):
        return None
    val = str(val)
    if "/" in val:
        num,den = val.split("/")
        return float(num)/float(den)
    return float(val)


df["aperture"] = df["aperture"].apply(parse_aperture)
df["shutter"] = df["shutter"].apply(parse_shutter)
print(df["shutter"].dtype)
print(df["aperture"].dtype)


df["exposure_value"] = np.log2((df["aperture"] ** 2) / df["shutter"]) + np.log2(df["iso"] / 100)

df["is_golden_hour"] = df["hour"].isin([6, 7, 8, 17, 18, 19])

def get_season(month):
    if month in [12, 1, 2]: return "winter"
    if month in [3, 4, 5]: return "spring"
    if month in [6, 7, 8]: return "summer"
    return "autumn"

df["season"] = df["month"].apply(get_season)

df["is_low_light"] = df["iso"] > 1600

# print(df["season"].value_counts())
# print(df.shape)
# print(df.isna().sum())



df = df[df["aperture"]>0].reset_index(drop=True)
print(df[["focalLength", "iso", "aperture", "shutter", "exposure_value"]].describe())
print(df.shape)



