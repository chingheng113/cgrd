import pandas as pd
import os
import xnat
import glob

# project_name = 'CGRD_test1'
# # session = xnat.connect('http://xnat.ninds.nih.gov/', user='linc9', password='linc9')
# # a = session.subjects['aaa']
# # print(a)

root_path = os.path.join('..', '1_100','*','')
for a in glob.glob(root_path):
    print(a.split('/')[2])
print('done')