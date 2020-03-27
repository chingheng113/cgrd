import os, os.path
import zipfile
import xnat
import pydicom
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


if __name__ == '__main__':
    file_path = os.path.join('..', '1_100', '0E654727052662F183CE0A56D1030CF21CA06C95',
                             '1.2.528.1.1001.200.10.4021.4317.257665444.20200205201606121',
                             'SDY00000', 'SRS00000')
    image_files = glob.glob(os.path.join(file_path, '*.DCM'))
    head_info = pydicom.filereader.dcmread(image_files[0], stop_before_pixels=True, force=True)
    patient_ID = head_info.data_element('PatientID').value
    image_No = head_info.data_element('AccessionNumber').value
    if image_No is None:
        image_No = head_info.data_element('StudyID').value

    project_name = 'CGRD_test1'

    session = xnat.connect('http://xnat.ninds.nih.gov/', user='linc9', password='linc9')
    project = session.projects[project_name]
    subject = session.subjects['test1']
    file_path2 = os.path.join('..', '1_100', '0E654727052662F183CE0A56D1030CF21CA06C95')
    zip_dir_name = 'temp.zip'
    # file_path2
    zip_dir(file_path2, zip_dir_name)
    experiment = session.services.import_(os.path.join(file_path2, zip_dir_name),
                                          project=project_name,
                                          subject='test1',
                                          experiment=image_No)
    os.remove(os.path.join(file_path2, zip_dir_name))

    # report
    ext = session.create_object(experiment.uri)
    resource = ext.resources.get('Report', None)
    # If resource doesn't exist, just create it
    if resource is None:
        resource = session.classes.ResourceCatalog(parent=ext, label='Report')
    resource.upload('../README.md', 'README.md')
    # resource.upload_dir('/output/currsub')
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