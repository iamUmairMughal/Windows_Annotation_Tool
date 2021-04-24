from xml.etree import ElementTree
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, Comment
import glob

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def create_xml(folder, filename, path, size, cors):
    top = Element('annotation')
    m1 = SubElement(top, 'folder')
    m1.text = folder.split('/')[-1]
    m2 = SubElement(top, 'filename')
    m2.text = filename
    m3 = SubElement(top, 'path')
    m3.text = path
    m4 = SubElement(top, 'source')

    m41 = SubElement(m4, 'database')
    m41.text = 'Unknown'

    m5 = SubElement(top, 'size')
    m51 = SubElement(m5, 'width')
    m51.text = str(size[0])
    m52 = SubElement(m5, 'height')
    m52.text = str(size[1])
    m53 = SubElement(m5, 'depth')
    m53.text = str(size[2])
    m6 = SubElement(top, 'segmented')
    m6.text = '0'
    for cor in cors:
        m7 = SubElement(top, 'object')
        m71 = SubElement(m7, 'name')
        m71.text = cor[4]
        m72 = SubElement(m7, 'pose')
        m72.text = 'Unspecified'
        m73 = SubElement(m7, 'truncated')
        m73.text = '0'
        m74 = SubElement(m7, 'dificult')
        m74.text = '0'
        m75 = SubElement(m7, 'bndbox')
        m751 = SubElement(m75, 'xmin')
        m751.text = str(cor[0])
        m751 = SubElement(m75, 'ymin')
        m751.text = str(cor[1])
        m751 = SubElement(m75, 'xmax')
        m751.text = str(cor[2])
        m751 = SubElement(m75, 'ymax')
        m751.text = str(cor[3])

    save_file = folder+'/' + filename.split('.')[0] + '.xml'
    with open(save_file, 'w') as f:
        f.write(prettify(top))
    print(prettify(top))


