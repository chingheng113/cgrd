import pandas as pd
import pydicom
import glob
import os
import csv
# path = '//nindsdirfs//shares//BIS//Amar//Stroke_Shared_Folder//2019_07_02_CGRD_Stroke/Images//STROKE_IMAGENO.csv'
# a = pd.read_csv(path)
# path example
# \\nindsdirfs\shares\BIS\Amar\Stroke_Shared_Folder\2019_07_02_CGRD_Stroke\Images\1.2.528.1.1001.200.10.4573.2021.3754721344.20190923031720119\SDY00000\SRS00000

dicom_keywords = ['ImageType', 'PatientID', 'PatientBirthDate', 'PatientSex', 'StudyDate', 'SeriesDate', 'PatientWeight',
                  'ContentDate', 'StudyTime', 'SeriesTime', 'ContentTime', 'AccessionNumber', 'RequestAttributesSequence',
                  'PerformedProcedureStepID', 'requestid', 'StudyID', 'Modality', 'Manufacturer']


root_dir = '//nindsdirfs//shares//BIS//Amar//Stroke_Shared_Folder//2019_07_02_CGRD_Stroke/Images//'
with open('dicom_header.csv', mode='w', newline='') as dicom_header_file:
    csv_writer = csv.writer(dicom_header_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    field_name = ['dir'] + dicom_keywords
    csv_writer.writerow(field_name)
    patients_dirs = os.listdir(root_dir)
    for patients_dir in patients_dirs:
        sdy_dirs = os.listdir(os.path.join(root_dir, patients_dir))
        for sdy_dir in sdy_dirs:
            if sdy_dir != 'DICOMDIR':
                srs_dirs = os.listdir(os.path.join(root_dir, patients_dir, sdy_dir))
                for srs_dir in srs_dirs:
                    image_files = glob.glob(os.path.join(root_dir, patients_dir, sdy_dir, srs_dir, '*.DCM'))
                    for image_file in image_files:
                        head_info = pydicom.filereader.dcmread(image_file, stop_before_pixels=True, force=True)
                        head_info_list = [image_file]
                        # M1: iterate all of elements
                        # for elem in head_info:
                        #     if elem.keyword != '':
                        #         # print(elem.keyword, elem.value)
                        # M2: get specific tag
                        for dicom_keyword in dicom_keywords:
                            try:
                                elem = head_info.data_element(dicom_keyword)
                            except KeyError as e:
                                pass
                            if elem is None:
                                head_info_list.append('')
                            else:
                                head_info_list.append(elem.value)
                        csv_writer.writerow(head_info_list)
        print(patients_dir)


# By folloing code, we find out that '1.2.528.1.1001.200.10.4573.10409.3754721344.20190926025013594' and
# '1.2.528.1.1001.200.10.4573.10409.3754721344.20190926021755157' are bad data.
# so the number of patient is 7148, not 7150
# df = pd.read_csv('dicom_header.csv')
# dir = df['dir'].str.split('\\').str[0].str.split('//').str[-1]
# uniq = list(dict.fromkeys(dir))
# print(len(uniq))
# patients_dirs = os.listdir(root_dir)
# uniq_p = list(dict.fromkeys(patients_dirs))
# print(len(uniq_p))
# print(list(set(uniq_p)-set(uniq)))
print('done')