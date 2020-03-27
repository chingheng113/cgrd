import pyxnat
import os

xnat = pyxnat.Interface('http://xnat.ninds.nih.gov/','linc9','linc9')
project = xnat.select.project('CGRD_test1')
subject = project.subject('test1')
experiment = subject.experiment('17BQ36167X01')
files_resource = experiment.resource('radiology reports')
file1 = files_resource.file('README.md')
file1.put('../README.md')
xnat.disconnect()
print('done')