import pandas as pd
import glob
import sys, os
current_path = os.path.dirname(__file__)

def xlsx_to_csv_pd():
    read_path = glob.glob(os.path.join(current_path, 'xls', '*.xlsx'))
    for p in  read_path:
        output_filename = str(os.path.basename(p)).replace('.xlsx', '')
        data_xls = pd.read_excel(p, index_col=0, encoding='utf-8')
        data_xls.to_csv(os.path.join('csv', output_filename+'.csv'), encoding='utf_8_sig')
        print(output_filename)


if __name__ == '__main__':
    xlsx_to_csv_pd()