import pandas as pd
import numpy as np

# discharge = pd.read_csv('出院病摘_CSV.csv')
# selected_dischrge = discharge[discharge['歸戶代號'] == 'BBF3583A3B53DCE0AEF62FC8CB9488995FF21795']

stroke_icd = ['430', '431', '432', '4320', '4321', '4329', '433', '4330', '4331', '4332', '4333', '4338', '4339',
             '434', '4340', '4341', '4349', '43491', '435', '4350', '4351', '4352', '4353', '4358', '4359', '436', '437',
             '4370', '4371', '4372', '4373', '4374', '4375', '4376', '4377', '4378', '4379']

cerebrovascular_icd = ['4389', '85226', '85205', '85225', '43811', '43820', '43889', '43310']

icd_codes = stroke_icd+cerebrovascular_icd

# not stroke when being hospitalized
icd = pd.read_csv('14653_疾病分類統計檔_1.csv')
selected_icd = icd[['歸戶代號', '資料年月', '輸入日期', '診斷類別1', '診斷類別名稱1', '診斷類別2','診斷類別名稱2',
                    '診斷類別3', '診斷類別名稱3', '診斷類別4', '診斷類別名稱4', '診斷類別5', '診斷類別名稱5',
                    '診斷類別6', '診斷類別名稱6', '診斷類別7', '診斷類別名稱7', '診斷類別8', '診斷類別名稱8',
                    '診斷類別9', '診斷類別名稱9']]

selected_icd = selected_icd.loc[~(
    selected_icd['診斷類別1'].isin(icd_codes) | selected_icd['診斷類別2'].isin(icd_codes) |
    selected_icd['診斷類別3'].isin(icd_codes) | selected_icd['診斷類別4'].isin(icd_codes) |
    selected_icd['診斷類別5'].isin(icd_codes) | selected_icd['診斷類別6'].isin(icd_codes) |
    selected_icd['診斷類別7'].isin(icd_codes) | selected_icd['診斷類別8'].isin(icd_codes) |
    selected_icd['診斷類別9'].isin(icd_codes)
)]

# is stroke at emergency
er_diagnosis = pd.read_csv('14653_急診診斷檔_1(demoralized).csv')
diagnosis_col = list(er_diagnosis.columns)
diagnosis_col = [e for e in diagnosis_col if e not in ('院區', '資料年月', '歸戶代號', '輸入日期', '門診號', '掛號科別')]
#selected_er = er_diagnosis.loc[er_diagnosis[diagnosis_col].isin(icd_codes)]
loc_fl = []
inx = 0
for d in diagnosis_col:
    if inx == 0:
        loc_fl = er_diagnosis[d].isin(icd_codes)
    else:
        temp_fl = er_diagnosis[d].isin(icd_codes)
        loc_fl = loc_fl | temp_fl
    inx = inx+1
selected_er = er_diagnosis.loc[loc_fl]

result = pd.merge(selected_er, selected_icd, on=['歸戶代號', '資料年月'])
# result = result[result['歸戶代號'] == 'E8C293D4D36EA95D7A350B4F3ECDBB1BD7610F37']

result.to_csv('look.csv', index=False, encoding='utf-8-sig')

print('done')