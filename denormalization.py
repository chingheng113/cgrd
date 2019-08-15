import pandas as pd
import numpy as np


def de_er_diagnosis():
    df = pd.read_csv('14653_急診診斷檔_1.csv')
    df = df[['院區', '資料年月', '歸戶代號', '輸入日期', '門診號', '掛號科別', '疾病序號', '疾病碼']]
    df.dropna(subset=['輸入日期', '疾病序號'], axis=0, inplace=True)
    # df = df.loc[0:100, :]
    sep = df['疾病序號'].unique()
    inx = 0
    sub_df = pd.DataFrame
    for num in sep:
        if inx == 0:
            sub_df = df[df['疾病序號'] == num]
        else:
            temp_df = df[df['疾病序號'] == num]
            temp_df = temp_df[['歸戶代號', '輸入日期', '疾病碼']]
            temp_df.rename(columns={'疾病碼': '疾病碼_'+str(inx+1)}, inplace=True)
            sub_df = pd.merge(sub_df, temp_df, how='left', on=['歸戶代號', '輸入日期'])
        inx = inx+1
    sub_df.drop(['疾病序號'], axis=1, inplace=True)
    sub_df.to_csv('14653_急診診斷檔_1(demoralized).csv', index=False, encoding='utf-8-sig')
    print('done')


if __name__ == '__main__':
    de_er_diagnosis()

