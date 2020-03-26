import os, os.path
import zipfile
import xnat as xnatpy

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
    project_name = 'CGRD_test1'
    exp_name = 'stroke'
    file_path = os.path.join('..', '1_100', '0E654727052662F183CE0A56D1030CF21CA06C95',
                             '1.2.528.1.1001.200.10.4021.4317.257665444.20200205201606121',
                             'SDY00000', 'SRS00000')
    session = xnatpy.connect('http://xnat.ninds.nih.gov/', user='linc9', password='linc9')
    xnatpy.connect
    sandbox = session.projects[project_name]
    subject = sandbox.subjects['test1']

    zip_dir_name = 'temp.zip'
    zip_dir(file_path, zip_dir_name)
    prearchive_session = session.services.import_(os.path.join(file_path, zip_dir_name),
                                                  project=project_name,
                                                  destination='/prearchive',
                                                  subject='test1')

    prearchive_session = session.prearchive.sessions()[0]
    # os.remove(os.path.join(file_path, zip_dir_name))
    try:
        prearchive_session.archive(subject='test1', experiment=exp_name)
    except Exception:
        pass
    session.disconnect()
    print('done')