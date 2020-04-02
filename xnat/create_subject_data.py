import pandas as pd
import os

subject = pd.read_csv(os.path.join('..','medical use_CSV','2010-2019stroke_total.csv'))
subject_is_id = subject[subject.diagnosed == 'Ischemic stroke'].idcode
subject_he_id = subject[subject.diagnosed == 'Hemorrhagic stroke'].idcode
subject_both_id = pd.Series(list(set(subject_is_id).intersection(set(subject_he_id))))
subject_only_is_id = subject_is_id[~subject_is_id.isin(subject_both_id)].unique()
subject_only_he_id = subject_he_id[~subject_he_id.isin(subject_both_id)].unique()

subject_both = subject[subject.idcode.isin(subject_both_id)].drop_duplicates(subset='idcode')[['idcode', '性別', '出生日期']]
subject_both['group'] = 'Both'
subject_only_is = subject[subject.idcode.isin(subject_only_is_id)].drop_duplicates(subset='idcode')[['idcode', '性別', '出生日期']]
subject_only_is['group'] = 'Ischemic stroke'
subject_only_he = subject[subject.idcode.isin(subject_only_he_id)].drop_duplicates(subset='idcode')[['idcode', '性別', '出生日期']]
subject_only_he['group'] = 'Hemorrhagic stroke'
result = pd.concat([subject_both, subject_only_is, subject_only_he], axis=0)
result['出生日期'] = pd.to_datetime(result['出生日期'], format='%Y%m%d')
result['yob'] = result['出生日期'].dt.year
result['dob'] = result['出生日期'].dt.strftime('%m/%d/%Y')
result.drop(['出生日期'], axis=1, inplace=True)
result.rename(columns={'idcode': 'ID', '性別': 'gender'}, inplace=True)
result = result[['ID', 'group',	'dob', 'yob', 'gender']]
result.replace({'M':'male', 'F':'female'}, inplace=True)
result.to_csv('upload.csv', index=False)
# result = result[(result.group == 'Ischemic stroke') & (result.gender == 'male')]
# result1 = result.iloc[0:3000,]
# result1.to_csv('upload1.csv', index=False)
# result2 = result.iloc[3000:6000,]
# result2.to_csv('upload2.csv', index=False)
# result3 = result.iloc[6000:,]
# result3.to_csv('upload3.csv', index=False)
print('done')