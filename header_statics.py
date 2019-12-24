import pandas as pd
import os
import numpy as np

df = pd.read_csv('dicom_header.csv')
df.drop(df[df['PatientID'] == 'Philips Medical Systems'].index, inplace=True)
print(df['StudyDate'].astype(int).min(), df['StudyDate'].astype(int).max())
df = df[(~df.duplicated(['AccessionNumber'], keep='first'))]

# don't care X-reports
# b_day = pd.to_datetime(df['PatientBirthDate'], format='%Y%m%d', errors='coerce')
# s_day = pd.to_datetime(df['StudyDate'], format='%Y%m%d', errors='coerce')
# df['AGE'] = np.floor((s_day - b_day) / pd.Timedelta(days=365))
# df_f = df[df['PatientSex'] == 'F']
# print(df_f.shape)
# print(df_f['AGE'].mean())
# df_m = df[df['PatientSex'] == 'M']
# print(df_m.shape)
# print(df_m['AGE'].mean())


# have x reports
df_img = pd.read_csv(os.path.join('csv', 'STROKE_IMAGENO.csv'))
df_img.rename(columns={'item': '檢查項目', 'EDATE':'收件日期'}, inplace=True)
df_img['收件日期'] = pd.to_datetime(df_img['收件日期'], format='%Y-%m-%d', errors='coerce')
df.rename(columns={'AccessionNumber': 'image_no', 'PatientID': '歸戶代號', 'item': '檢查項目'}, inplace=True)
result = pd.merge(df, df_img, how='inner', on=['image_no', '歸戶代號'])

x_df_1 = pd.read_csv(os.path.join('csv', '14653_X光科報告_1.csv'))
x_df_2 = pd.read_csv(os.path.join('csv', '15344_X光科報告_1.csv'))
x_df = pd.concat([x_df_1, x_df_2])
x_df['收件日期'] = pd.to_datetime(x_df['收件日期'], format='%Y%m%d', errors='coerce')
x_df['檢查項目'] = x_df['檢查項目'].str.replace(' ', '')
result = pd.merge(result, x_df, how='inner', on=['收件日期', '歸戶代號', '檢查項目'])
print(result.shape)
#
result_by_p = result[(~result.duplicated(['歸戶代號'], keep='first'))]
b_day = pd.to_datetime(result_by_p['PatientBirthDate'], format='%Y%m%d', errors='coerce')
s_day = pd.to_datetime(result_by_p['StudyDate'], format='%Y%m%d', errors='coerce')
result_by_p['AGE'] = np.floor((s_day - b_day) / pd.Timedelta(days=365))
result_by_p_f = result_by_p[result_by_p['PatientSex'] == 'F']
print(result_by_p_f.shape)
print(result_by_p_f['AGE'].mean())
result_by_p_m = result_by_p[result_by_p['PatientSex'] == 'M']
print(result_by_p_m.shape)
print(result_by_p_m['AGE'].mean())
#
print(result.groupby(['Modality']).size())
print(result.groupby(['Manufacturer']).size())
print(result.groupby(['檢查項目']).size())


print('done')