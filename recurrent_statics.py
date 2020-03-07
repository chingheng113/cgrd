import pandas as pd
import numpy as np
import os

all_patient_info = pd.read_csv(os.path.join('csv', '15344_歸戶個案_1.csv'))
all_patient_info = all_patient_info[(~all_patient_info.duplicated(['歸戶代號'], keep='first'))]
print(all_patient_info.shape)
p_data = pd.read_csv(os.path.join('recurrent_stroke_ds_all_for_statistic.csv'))
print(p_data.shape)
data = p_data.merge(all_patient_info, on='歸戶代號', how='left')
data['生日'] = pd.to_datetime(data['生日'], format='%Y%m%d', errors='coerce')
data['住院日期'] = pd.to_datetime(data['住院日期'], format='%Y%m%d', errors='coerce')
data['age'] = np.floor((data['住院日期'] - data['生日']) / pd.Timedelta(days=365))
print(data.shape)

re_data = data[data.label == 1]
print(re_data[re_data['性別']=='M'].shape[0])
print(re_data[re_data['性別']=='M'].shape[0]/re_data.shape[0])
print(round(np.mean(re_data.age), 1))
print(round(np.std(re_data.age), 1))
print(round(np.mean(re_data.recurrent_day), 1))
print(round(np.std(re_data.recurrent_day), 1))
print(round(np.median(re_data.recurrent_day), 1))
print('---')
no_data = data[data.label == 0]
print(no_data[no_data['性別']=='M'].shape[0])
print(no_data[no_data['性別']=='M'].shape[0]/no_data.shape[0])
print(round(np.mean(no_data.age), 1))
print(round(np.std(no_data.age), 1))


print('done')