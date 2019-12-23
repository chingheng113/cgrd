import pandas as pd
import os


icd_statistic = pd.read_csv(os.path.join('csv', '15344_疾病分類統計檔_1.csv')) #icd_10
icd_statistic.dropna(axis=0, subset=['診斷類別1', '診斷類別2', '診斷類別3'], inplace=True)
neural_df = icd_statistic.loc[icd_statistic['舊科別名稱'] == '神經內科']

# Find stroke patients
selected_icd_codes = ('I60', 'I61', 'I62', 'I63', 'I64', 'I65', 'I66', 'I67', 'I68', 'I69',
                      '430', '431', '432', '433', '434', '435', '436', '437', '438')
select_diagnosis_1 = neural_df["診斷類別1"].str.startswith(selected_icd_codes)
select_diagnosis_2 = neural_df["診斷類別2"].str.startswith(selected_icd_codes)
select_diagnosis_3 = neural_df["診斷類別3"].str.startswith(selected_icd_codes)
stroke_df = neural_df.loc[select_diagnosis_1 | select_diagnosis_2 | select_diagnosis_3]
print(stroke_df.shape)
# Find recurrent stroke patients
recurrent_stroke = stroke_df[stroke_df.duplicated(['歸戶代號'], keep=False)]
recurrent_stroke.sort_values(by=['歸戶代號'], inplace=True)
recurrent_stroke = recurrent_stroke.groupby('歸戶代號').apply(pd.DataFrame.sort_values, '資料年月', ascending=True)
# recurrent_stroke.to_csv('see.csv', index=False, encoding='utf-8-sig')

# Get recurrent stroke patient's first time
recurrent_stroke_first = recurrent_stroke[(~recurrent_stroke.duplicated(['歸戶代號'], keep='first'))]
# recurrent_stroke_first.to_csv('see2.csv', index=False, encoding='utf-8-sig')
print(recurrent_stroke.shape)

# Find non-recurrent stroke patients
recurrent_stroke_ID = recurrent_stroke_first['歸戶代號']
non_recurrent_stroke = stroke_df[~stroke_df['歸戶代號'].isin(recurrent_stroke_ID)]
# non_recurrent_stroke.to_csv('see3.csv', index=False, encoding='utf-8-sig')
print(non_recurrent_stroke.shape)


discharge_note = pd.read_csv(os.path.join('csv', '15344_出院病摘_1.csv'))
q = stroke_df['歸戶代號'].isin(recurrent_stroke_ID)
z = stroke_df['資料年月'].isin(recurrent_stroke_first['資料年月'])
# a = discharge_note.loc[]

print('done')