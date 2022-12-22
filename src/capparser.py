from structures import classes, enums
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
    if(tagName == str(classes.Alert())):
        obj = classes.Alert()
    elif(tagName == str(classes.Info())):
        obj = classes.Info()
    elif(tagName == str(classes.EventCode())):
        obj = classes.EventCode()
    elif(tagName == str(classes.Parameter())):
        obj = classes.Parameter()
    elif(tagName == str(classes.Resource())):
        obj = classes.Resource()
    elif(tagName == str(classes.Area())):
        obj = classes.Area()
    elif(tagName == str(classes.Geocode())):
        obj = classes.Geocode()
    else:
        return None
        
    for child in parent:
        _, _, childTagName = child.tag.rpartition('}')
        if len(child) == 0:
            for attr in inspect.getmembers(obj):
                if attr[0] == childTagName:
                    if len(parent.findall(child.tag)) == 1:
                        setattr(obj, childTagName, child.text)
                    else:
                        getattr(obj, childTagName).append(child.text)          
        else:
            getattr(obj, childTagName).append(_recursiveParser(child))

    return obj

#TODO: Add support for writing to XML string