from . import element
from . import enums
import xml.etree.ElementTree as ET
import inspect

def parse(filePath=None, stringXML=None):
    if filePath != None:
        file = open(filePath, "r")
        stringXML = file.read()
        file.close()
    root = ET.fromstring(stringXML)
    return _recursiveParser(root)


def _recursiveParser(parent):
    _, _, tagName = parent.tag.rpartition('}')
    obj = None
    if(tagName == str(element.Alert())):
        obj = element.Alert()
    elif(tagName == str(element.Info())):
        obj = element.Info()
    elif(tagName == str(element.EventCode())):
        obj = element.EventCode()
    elif(tagName == str(element.Parameter())):
        obj = element.Parameter()
    elif(tagName == str(element.Resource())):
        obj = element.Resource()
    elif(tagName == str(element.Area())):
        obj = element.Area()
    elif(tagName == str(element.Geocode())):
        obj = element.Geocode()
    else:
        return None

    for child in parent:
        _, _, childTagName = child.tag.rpartition('}')
        if len(child) == 0:
            for attr in inspect.getmembers(obj):
                if attr[0] == childTagName:
                    if len(parent.findall(child.tag)) == 1:
                        setattr(obj, childTagName, (child.text, attr[1][1]))
                    else:
                        getattr(obj, childTagName)[0].append(child.text)
        else:
            getattr(obj, childTagName)[0].append(_recursiveParser(child))

    return obj

def deparse(alert):
    return ET.tostring(_recursiveDeparser(alert), encoding='utf8')

def writeAlertToFile(alert, filePath):
    root = _recursiveDeparser(alert)
    tree = ET.ElementTree(root)
    with open(filePath, "wb") as files:
        tree.write(files)

def _recursiveDeparser(obj):
    root = ET.Element(str(obj))
    attrs = _filterOrderAttributes(inspect.getmembers(obj))
    
    for attr in attrs:
        if attr[0] == "xmlns":
            root.set(attr[0], attr[1][0])
        elif isinstance(attr[1][0], list):
            for item in attr[1][0]:
                if isinstance(item, element.Alert) or isinstance(item, element.Info) or isinstance(item, element.EventCode) or isinstance(item, element.Parameter) or isinstance(item, element.Resource) or isinstance(item, element.Area) or isinstance(item, element.Geocode):
                    root.append(_recursiveDeparser(item))
                else:
                    child = ET.SubElement(root, attr[0])
                    child.text = str(item)
        else:
            if isinstance(attr[1][0], element.Alert) or isinstance(attr[1][0], element.Info) or isinstance(attr[1][0], element.EventCode) or isinstance(attr[1][0], element.Parameter) or isinstance(attr[1][0], element.Resource) or isinstance(attr[1][0], element.Area) or isinstance(attr[1][0], element.Geocode):
                root.append(_recursiveDeparser(attr[1][0]))
            else:
                child = ET.SubElement(root, attr[0])
                child.text = str(attr[1][0])
                
    return root


def _filterOrderAttributes(attrs):
    result = []
    for attr in attrs:
        if not attr[0].startswith('_') and not inspect.ismethod(attr[1]) and len(attr[1]) == 2 and attr[1][0] != None and attr[0] != []:
            result.append(attr)
    result.sort(key=lambda x: x[1][1])
    return result
