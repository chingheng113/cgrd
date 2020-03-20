import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
import os

icd_statistic = pd.read_csv(os.path.join('csv', '15344_疾病分類統計檔_1.csv')) #icd_10_15344
icd_statistic.dropna(axis=0, subset=['診斷類別1', '診斷類別2', '診斷類別3'], inplace=True)
neural_df = icd_statistic.loc[icd_statistic['舊科別名稱'] == '神經內科']
# Find ischemic stroke patients
selected_icd_codes = ('I63', 'I66', '433', '434')
select_diagnosis_1 = neural_df["診斷類別1"].str.startswith(selected_icd_codes)
select_diagnosis_2 = neural_df["診斷類別2"].str.startswith(selected_icd_codes)
select_diagnosis_3 = neural_df["診斷類別3"].str.startswith(selected_icd_codes)
stroke_df = neural_df.loc[select_diagnosis_1 | select_diagnosis_2 | select_diagnosis_3]
# stroke_df = stroke_df.dropna(axis=0, subset=['備註2'])
# stroke_df = stroke_df.loc[stroke_df["備註2"].str.startswith("腦血管疾病")]
# stroke_df.to_csv('see.csv', index=False, encoding='utf-8-sig')

# Find recurrent stroke patients
recurrent_stroke = stroke_df[stroke_df.duplicated(['歸戶代號'], keep=False)]
recurrent_stroke.sort_values(by=['歸戶代號'], inplace=True)
recurrent_stroke = recurrent_stroke.groupby('歸戶代號').apply(pd.DataFrame.sort_values, '住院日期', ascending=True)
# Get recurrent stroke patient's first time
recurrent_stroke_first = recurrent_stroke[(~recurrent_stroke.duplicated(['歸戶代號'], keep='first'))]
# Get recurrent stroke patients's second (cloud be last) time
temp_df = recurrent_stroke.drop(recurrent_stroke_first.index, axis=0)
recurrent_stroke_second = temp_df[(~temp_df.duplicated(['歸戶代號'], keep='first'))]
recurrent_stroke_first.reset_index(drop=True, inplace=True)
recurrent_stroke_second.reset_index(drop=True, inplace=True)
# Calculate recurrent stroke time
first_time_out = pd.to_datetime(recurrent_stroke_first['出院日期'], format='%Y%m%d', errors='coerce')
second_time_in = pd.to_datetime(recurrent_stroke_second['住院日期'], format='%Y%m%d', errors='coerce')
recurrent_time = second_time_in - first_time_out
recurrent_stroke_first['recurrent_day'] = recurrent_time.dt.days
recurrent_stroke_first = recurrent_stroke_first.drop(recurrent_stroke_first[recurrent_stroke_first.recurrent_day == 0].index)

# Find non-recurrent stroke patients
recurrent_stroke_ID = recurrent_stroke_first['歸戶代號']
non_readmin = icd_statistic.drop_duplicates(subset=['歸戶代號'], keep=False)
non_recurrent_stroke = stroke_df[stroke_df['歸戶代號'].isin(non_readmin['歸戶代號'])]
non_recurrent_stroke['recurrent_day'] = 0

# Prepare the latest version of each discharge
discharge_note = pd.read_csv(os.path.join('csv', '15344_出院病摘_1.csv')) #icd_10_15344
discharge_note_uniq = discharge_note[(~discharge_note.duplicated(['住院號'], keep=False))]
discharge_note_duplicate = discharge_note[~discharge_note['住院號'].isin(discharge_note_uniq['住院號'])]
discharge_note_duplicate = discharge_note_duplicate.groupby('住院號').apply(pd.DataFrame.sort_values, ['存檔日期', '異動次數'], ascending=True)
discharge_note_duplicate_last = discharge_note_duplicate[~(discharge_note_duplicate.duplicated(['住院號'], keep='last'))]
discharge_note_latest = pd.concat([discharge_note_uniq, discharge_note_duplicate_last])

# Get recurrent stroke patient's discharge note
recurrent_note = pd.merge(discharge_note_latest, recurrent_stroke_first, how='inner', on=['歸戶代號', '資料年月', '住院號'])
#  Get non-recurrent patient, but excludes patient who has not enough follow-up period
non_recurrent_note = pd.merge(discharge_note_latest, non_recurrent_stroke, how='inner', on=['歸戶代號', '資料年月', '住院號'])
non_recurrent_note_last_date = datetime.datetime.strptime(str(max(non_recurrent_note['住院日期'])), '%Y%m%d')

# === life time ===
followup_threshold = non_recurrent_note_last_date - datetime.timedelta(days=np.median(recurrent_time.dt.days))
non_recurrent_note_cut = non_recurrent_note[pd.to_datetime(non_recurrent_note['出院日期_y'], format='%Y%m%d', errors='coerce') < followup_threshold]
recurrent_note['label'] = 1
non_recurrent_note_cut['label'] = 0
final_data = pd.concat([recurrent_note, non_recurrent_note_cut])
result = final_data[['歸戶代號', '資料年月', '住院號', '主訴', '病史', '手術日期、方法及發現', '住院治療經過', 'label', 'recurrent_day']]
result.to_csv('recurrent_stroke_ds_all.csv', index=False, encoding='utf-8-sig')
result2 = final_data[['歸戶代號', '資料年月', '住院號', '住院日期', 'label', 'recurrent_day']]
result2.to_csv('recurrent_stroke_ds_all_for_statistic.csv', index=False, encoding='utf-8-sig')
#
# # === 365 days ===
# recurrent_note_365 = recurrent_note[recurrent_note['recurrent_day'] < 366]
# recurrent_note_365['label'] = 1
# recurrent_note_365_over = recurrent_note[recurrent_note['recurrent_day'] > 365]
# followup_threshold_365 = non_recurrent_note_last_date - datetime.timedelta(days=365)
# # non_recurrent still includes over 360-days recurrent stroke
# non_recurrent_note_365 = non_recurrent_note[pd.to_datetime(non_recurrent_note['出院日期_y'], format='%Y%m%d', errors='coerce') < followup_threshold_365]
# non_recurrent_note_365 = pd.concat([recurrent_note_365_over, non_recurrent_note_365])
# non_recurrent_note_365['label'] = 0
# result_365 = pd.concat([recurrent_note_365, non_recurrent_note_365])
# result_365 = result_365[['歸戶代號', '資料年月', '住院號', '主訴', '病史', '手術日期、方法及發現', '住院治療經過', 'label', 'recurrent_day']]
# result_365.to_csv('recurrent_stroke_ds_360.csv', index=False, encoding='utf-8-sig')
#
# # === median days ===
# recurrent_note_m = recurrent_note[recurrent_note['recurrent_day'] < np.median(recurrent_time.dt.days)]
# recurrent_note_m['label'] = 1
# recurrent_note_m_over = recurrent_note[recurrent_note['recurrent_day'] > np.median(recurrent_time.dt.days)]
# followup_threshold_m = non_recurrent_note_last_date - datetime.timedelta(days=np.median(recurrent_time.dt.days))
# # non_recurrent still includes over median days recurrent stroke
# non_recurrent_note_m = non_recurrent_note[pd.to_datetime(non_recurrent_note['出院日期_y'], format='%Y%m%d', errors='coerce') < followup_threshold_m]
# non_recurrent_note_m = pd.concat([recurrent_note_m_over, non_recurrent_note_m])
# non_recurrent_note_m['label'] = 0
# result_m = pd.concat([recurrent_note_m, non_recurrent_note_m])
# result_m = result_m[['歸戶代號', '資料年月', '住院號', '主訴', '病史', '手術日期、方法及發現', '住院治療經過', 'label', 'recurrent_day']]
# result_m.to_csv('recurrent_stroke_ds_m.csv', index=False, encoding='utf-8-sig')

print('done')

# just back up
# recurrent_threshold2 = np.mean(recurrent_time.dt.days)
# recurrent_time.dt.days.plot.hist(bins=133, alpha=0.5)
# plt.show()
# recurrent_stroke_first['label'] = 1