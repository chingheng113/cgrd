import os, os.path
import zipfile
import xnat
import pydicom
import pandas as pd
import glob

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
    try:
        return img_reports[img_reports.image_no == image_No].CONTENT.values[0]
    except Exception:
        return ''


def report_uploader(session, experiment, img_report_set, image_No):
    report_text = get_img_report(img_report_set, image_No)
    if report_text != '':
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
    # errors
    # 4689770029AF324755F5E84267FDFCA0BA4948C4
    # DEEBF652E69FD1EF3F6D291E1C3BDE6A4791181A
    # F1D36B632A4136F3022DCA408889A2FB805066F7
    # D8039D0E66E373D5679DB36EC1F311F6FF042870
    # FDE4265345F936C505C4670DBC266A06A08F8DAA
    # E9D7D8AA5029CD9AEA2AA6AC921C8D4C6BAA7F45
    # B5F171F041F7DF4867140F7D3CCE7EE0CDEA8949
    # D2B28AD1EE7D736D8980D42884350581F7BA5D8D
    # 87F54C021BABE9BC174DECE79BBDEB77060EF4DE
    # A8D1A62FC0C1EB86F5628DD91B824D59528050A8
    # 45268D51D3BA31762B2363A937A5D143A060C934
    img_report_set = pd.read_csv('img_report_set.csv')
    project_name = 'CGRD_test1'
    session = xnat.connect('http://xnat.ninds.nih.gov/', user='linc9', password='linc9')
    root_path = os.path.join('..', '1_100')
    for subdir_name in glob.glob(os.path.join(root_path, '*', '')):
        patient_ID = subdir_name.split('/')[2]
        try:
            image_No = get_DICOM_info(root_path, patient_ID)
            experiment = img_uploader(root_path, session, project_name, patient_ID, image_No)
            report_uploader(session, experiment, img_report_set, image_No)
        except Exception:
            print(patient_ID)
            pass
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