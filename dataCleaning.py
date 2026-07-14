import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler

df = pd.read_excel(r"C:\Development\myPhotoHabits\Videos\customer_call_list_messy.xlsx")
df = df.drop_duplicates()

df = df.drop('Not_Useful_Column', axis=1)

df['Last_Name'] = df['Last_Name'].str.replace('[^a-zA-Z]','',regex=True)
df['Phone_Number'] = df['Phone_Number'].str.replace('[^0-9]','',regex=True)
df["Phone_Number"] = df["Phone_Number"].replace("", np.nan)
df[['Street','City','State']] = df['Address'].str.split(',', expand=True,n=2)
df["Street"] = df["Street"].str.strip()
df["City"] = df["City"].str.strip()
df["State"] = df["State"].str.strip()
df['Do_Not_Contact'] = df['Do_Not_Contact'].replace({'Y':'Yes','N':'No'})
df['Paying Customer'] = df['Paying Customer'].replace({'Y':'Yes','N':'No','N/a':np.nan})
df = df.dropna(subset='Paying Customer')
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
df = df[df['Do_Not_Contact'] != 'Yes']
df = df.dropna(subset='Phone_Number')
df = df.reset_index(drop=True)
df = df.drop('Address', axis=1)
df.drop("State", axis=1)
print(df)