import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
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
recurrent_stroke = recurrent_stroke.groupby('歸戶代號').apply(pd.DataFrame.sort_values, '住院日期', ascending=True)
# recurrent_stroke.to_csv('see.csv', index=False, encoding='utf-8-sig')
print(recurrent_stroke.shape)

# Get recurrent stroke patient's first time
recurrent_stroke_first = recurrent_stroke[(~recurrent_stroke.duplicated(['歸戶代號'], keep='first'))]
# Get recurrent stroke patients's second (cloud be last) time
temp_df = recurrent_stroke.drop(recurrent_stroke_first.index, axis=0)
recurrent_stroke_second = temp_df[(~temp_df.duplicated(['歸戶代號'], keep='first'))]
recurrent_stroke_first.reset_index(drop=True, inplace=True)
recurrent_stroke_second.reset_index(drop=True, inplace=True)
# recurrent_stroke_first.to_csv('first.csv', index=False, encoding='utf-8-sig')
# second_times_stroke.to_csv('second.csv', index=False, encoding='utf-8-sig')

# Find non-recurrent stroke patients
recurrent_stroke_ID = recurrent_stroke_first['歸戶代號']
non_readmin = icd_statistic.drop_duplicates(subset=['歸戶代號'], keep=False)
non_recurrent_stroke = stroke_df[stroke_df['歸戶代號'].isin(non_readmin['歸戶代號'])]
print(non_recurrent_stroke.shape)

# Prepare the latest version of each discharge
discharge_note = pd.read_csv(os.path.join('csv', '15344_出院病摘_1.csv'))
discharge_note_uniq = discharge_note[(~discharge_note.duplicated(['住院號'], keep=False))]
discharge_note_duplicate = discharge_note[~discharge_note['住院號'].isin(discharge_note_uniq['住院號'])]
discharge_note_duplicate = discharge_note_duplicate.groupby('住院號').apply(pd.DataFrame.sort_values, ['存檔日期', '異動次數'], ascending=True)
discharge_note_duplicate_last = discharge_note_duplicate[~(discharge_note_duplicate.duplicated(['住院號'], keep='last'))]
discharge_note_latest = pd.concat([discharge_note_uniq, discharge_note_duplicate_last])

# Get recurrent and non-recurrent stroke patient's discharge note
recurrent_note = pd.merge(discharge_note_latest, recurrent_stroke_first, how='inner', on=['歸戶代號', '資料年月', '住院號'])
recurrent_note['label'] = 1
non_recurrent_note = pd.merge(discharge_note_latest, non_recurrent_stroke, how='inner', on=['歸戶代號', '資料年月', '住院號'])
non_recurrent_note['label'] = 0

result = pd.concat([recurrent_note, non_recurrent_note])

# Calculate recurrent stroke average time for data period
first_time = pd.to_datetime(recurrent_stroke_first['住院日期'], format='%Y%m%d', errors='coerce')
second_time = pd.to_datetime(recurrent_stroke_second['住院日期'], format='%Y%m%d', errors='coerce')
recurrent_time = second_time - first_time
recurrent_median_days = np.median(recurrent_time.dt.days)
recurrent_median_day = datetime.timedelta(days=recurrent_median_days)
data_last_date = datetime.datetime.strptime(str(max(result['住院日期'])), '%Y%m%d')
recurrent_threshold = data_last_date - recurrent_median_day

# recurrent_threshold2 = np.mean(recurrent_time.dt.days)
# recurrent_time.dt.days.plot.hist(bins=24, alpha=0.5)
# plt.show()



result = result[['歸戶代號', '資料年月', '住院號', '主訴', '病史', '手術日期、方法及發現', '住院治療經過', 'label']]
result.to_csv('recurrent_stroke_ds.csv', index=False, encoding='utf-8-sig')
print('done')