import os
import pandas as pd
import numpy as np
nat = np.datetime64('NaT')

path = os.path.join('..', 'medical use_CSV')

img_list = pd.read_csv(os.path.join(path, 'imagelist.csv'))
img_list.dropna(axis=0, inplace=True)
img_list.rename(columns={'item': 'ITEM'}, inplace=True)
img_list['EDATE'] = pd.to_datetime(img_list['EDATE'], format='%Y-%m-%d').dt.strftime('%Y%m%d').astype(int)
reports = pd.read_csv(os.path.join(path, 'R16183_RCGRDRPTXRAY.csv'), encoding='iso-8859-1')
img_reports = pd.merge(img_list, reports, how='inner', on=['ITEM', 'IDCODE', 'EDATE'])
# Prepare the latest version of report
img_reports_uniq = img_reports[(~img_reports.duplicated(['image_no'], keep=False))]
img_reports_duplicate = img_reports[~img_reports['image_no'].isin(img_reports_uniq['image_no'])]
img_reports_duplicate = img_reports_duplicate.groupby('image_no').apply(pd.DataFrame.sort_values, ['AMEND'], ascending=True)
img_reports_duplicate_last = img_reports_duplicate[~(img_reports_duplicate.duplicated(['image_no'], keep='last'))]
img_reports_latest = pd.concat([img_reports_uniq, img_reports_duplicate_last])
img_reports_set = img_reports_latest[['image_no', 'CONTENT']]
img_reports_set.to_csv('img_report_set.csv', index=False)
print('done')