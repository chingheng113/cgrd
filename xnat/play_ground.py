from pyxnat import Interface
import os
# https://wiki.xnat.org/workshop-2016/files/29034956/29034952/1/1465403228621/Pyxnat+101.pdf


file_path = os.path.join('..','1_100', '0E654727052662F183CE0A56D1030CF21CA06C95',
                                    '1.2.528.1.1001.200.10.4021.4317.257665444.20200205201606121',
                                    'SDY00000', 'SRS00000')

xnat = Interface(server='http://xnat.ninds.nih.gov/', user='linc9', password='linc9')
print(list(xnat.select.projects()))
# Using pyxnat's object methods to walk down the path.
subject_pyxnat2016 = xnat.select.project('CGRD_test1').subject('test1')

experiment = subject_pyxnat2016.experiment('stroke')
experiment.create(experiments='xnat:mrSessionData')
# experiment.attrs.mset({'xnat:mrSessionData/fieldstrength': '3.0',
#                        'xnat:mrSessionData/coil': 'head',
#                        'xnat:mrSessionData/marker': "right"
#                        })
scan = experiment.scan('ScanOne')
scan.create(scans='xnat:mrScanData')
scan.attrs.mset({'xnat:mrScanData/parameters/imageType':'t1_fl2d_tra_4mm',
                 'xnat:mrScanData/series_description': 't1_fl2d_tra_4mm',
                 'xnat:mrScanData/quality' : 'usable'
                 })

dicom_resource = scan.resource('DICOM')

dicom_resource.put_dir(file_path)
the_files = dicom_resource.files()
for f in the_files:
    print(f)

print('done')