import pandas as pd
import os

img_report_set = pd.read_csv('img_report_set.csv')
i = '14AP35902X01'
a = img_report_set[img_report_set.image_no == i].CONTENT.values
with open("Output.txt", "w") as text_file:
    text_file.write(a[0])
print(os.path.realpath(text_file.name))
print('done')