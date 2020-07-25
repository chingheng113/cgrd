import pandas as pd
import os


patient_img = pd.read_csv(os.path.join('radiology_id_1.csv'))
print(patient_img.shape)
patient_img = patient_img.drop_duplicates(subset='IDCODE')
patient_img = patient_img.rename(columns={'IDCODE': 'ID'})
print(patient_img.shape)
patient = pd.read_csv('upload.csv')

result = pd.merge(patient_img, patient, on='ID')
isc = result[result.group == 'Ischemic stroke'].head(200)
print(isc.shape)
hem = result[result.group == 'Hemorrhagic stroke'].head(200)
print(hem.shape)
patient_img_diagnosis = pd.concat([isc, hem])
print(patient_img_diagnosis.shape)
patient_img_diagnosis.to_csv('patient_img_diagnosis.csv', index=False)
print('done')