from pyxnat import Interface

interface = Interface(server='http://xnat.ninds.nih.gov/', user='linc9', password='linc9')

print(list(interface.select.projects()))