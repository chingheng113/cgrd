import os, os.path
import zipfile
import xnat
import pydicom
import pandas as pd

# https://xnat.readthedocs.io/en/latest/static/tutorial.html

def zip_dir(dirname, zipfilename):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else:
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))

    zf = zipfile.ZipFile(os.path.join(dirname, zipfilename), "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        # print arcname
        zf.write(tar, arcname)
    zf.close()


def img_uploader(root_path, session, project_name, patient_ID, image_No):
    file_path = os.path.join(root_path, patient_ID)
    zip_dir_name = 'temp.zip'
    # file_path2
    zip_dir(file_path, zip_dir_name)
    experiment = session.services.import_(os.path.join(file_path, zip_dir_name),
                                          project=project_name,
                                          subject=patient_ID,
                                          experiment=image_No)
    os.remove(os.path.join(file_path, zip_dir_name))
    return experiment


def get_DICOM_info(root_path, patient_ID):
    for root, dirs, files in os.walk(os.path.join(root_path, patient_ID)):
        if files:
            if files[0].endswith('.DCM'):
                head_info = pydicom.filereader.dcmread(os.path.join(root, files[0]), stop_before_pixels=True, force=True)
                p_ID = head_info.data_element('PatientID').value
                image_No = head_info.data_element('AccessionNumber').value
                if image_No is None:
                    image_No = head_info.data_element('StudyID').value
                return image_No


def get_img_report(img_reports, image_No):
    return img_reports[img_reports.image_no == image_No].CONTENT.values[0]


def report_uploader(session, experiment, img_report_set, image_No):
    report_text = get_img_report(img_report_set, image_No)
    with open("report.txt", "w") as text_file:
        text_file.write(report_text)
    ext = session.create_object(experiment.uri)
    resource = ext.resources.get('Report', None)
    # If resource doesn't exist, just create it
    if resource is None:
        resource = session.classes.ResourceCatalog(parent=ext, label='Report')
    resource.upload(os.path.realpath(text_file.name), 'report.txt')
    # resource.upload_dir('/output/currsub')
    os.remove(os.path.realpath(text_file.name))


if __name__ == '__main__':
    img_report_set = pd.read_csv('img_report_set.csv')
    project_name = 'CGRD_test1'
    session = xnat.connect('http://xnat.ninds.nih.gov/', user='linc9', password='linc9')
    root_path = os.path.join('..', '1_100')
    patient_ID = '0E654727052662F183CE0A56D1030CF21CA06C95'
    image_No = get_DICOM_info(root_path, patient_ID)
    experiment = img_uploader(root_path, session, project_name, patient_ID, image_No)
    report_uploader(session, experiment, img_report_set, image_No)
    session.disconnect()
    print('done')




    # Prearchive first and then archive it, so buggyyy...
    # prearchive_session = session.services.import_(os.path.join(file_path2, zip_dir_name),
    #                                               project=project_name,
    #                                               destination='/prearchive',
    #                                               subject='test1')
    # prearchive_session = session.prearchive.sessions()[0]
    # try:
    #     prearchive_session.archive(subject='test1', experiment=image_No)
    # except Exception:
    #     pass