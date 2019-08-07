import pandas as pd
import numpy as np

# discharge = pd.read_csv('出院病摘_CSV.csv')
# selected_dischrge = discharge[discharge['歸戶代號'] == 'BBF3583A3B53DCE0AEF62FC8CB9488995FF21795']

icd_codes = ['430', '431', '432', '4320', '4321', '4329', '433', '4330', '4331', '4332', '4333', '4338', '4339']


icd = pd.read_csv('14653_疾病分類統計檔_1.csv')
selected_icd = icd[['歸戶代號', '資料年月', '輸入日期', '診斷類別1', '診斷類別名稱1', '診斷類別2','診斷類別名稱2',
                    '診斷類別3', '診斷類別名稱3', '診斷類別4', '診斷類別名稱4', '診斷類別5', '診斷類別名稱5',
                    '診斷類別6', '診斷類別名稱6', '診斷類別7', '診斷類別名稱7', '診斷類別8', '診斷類別名稱8',
                    '診斷類別9', '診斷類別名稱9']]

er_diagnosis = pd.read_csv('14653_急診診斷檔_1.csv')
selected_er = er_diagnosis[['歸戶代號', '資料年月', '輸入日期', '疾病碼']]

result = pd.merge(selected_er, selected_icd, on=['歸戶代號', '資料年月'])
result = result[result['歸戶代號'] == 'E8C293D4D36EA95D7A350B4F3ECDBB1BD7610F37']

result.to_csv('look.csv', index=False, encoding='utf-8-sig')

print('done')