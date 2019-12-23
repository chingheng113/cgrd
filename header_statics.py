import pandas as pd
import numpy as np

df = pd.read_csv('dicom_header.csv')
df.drop(df[df['PatientID'] == 'Philips Medical Systems'].index, inplace=True)
print(df['StudyDate'].astype(int).min(), df['StudyDate'].astype(int).max())
df = df[(~df.duplicated(['PatientID'], keep='first'))]
b_day = pd.to_datetime(df['PatientBirthDate'], format='%Y%m%d', errors='coerce')
s_day = pd.to_datetime(df['StudyDate'], format='%Y%m%d', errors='coerce')
df['AGE'] = np.floor((s_day - b_day) / pd.Timedelta(days=365))
df_f = df[df['PatientSex'] == 'F']
print(df_f.shape)
print(df_f['AGE'].mean())
df_m = df[df['PatientSex'] == 'M']
print(df_m.shape)
print(df_m['AGE'].mean())
print('done')