import pandas as pd
import os

# discharge_note = pd.read_csv(os.path.join('csv', '14653_出院病摘_1.csv'))
# a = discharge_note['歸戶代號'].loc[0]
icd_statistic = pd.read_csv(os.path.join('csv', '14653_疾病分類統計檔_1.csv'))
duplicateRows = icd_statistic[icd_statistic.duplicated(['歸戶代號'])]
duplicateRows.sort_values(by=['歸戶代號'], inplace=True)
duplicateRows.to_csv('see.csv', index=False, encoding='utf-8-sig')
print('done')