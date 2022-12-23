from datetime import datetime, timezone
import enums
import random
import re

class Alert(object):
    def __init__(self, identifier=None, sender="CAPParser", sent=None, status=enums.Status.Actual, msgType=enums.MsgType.Alert, scope=enums.Scope.Public):
        '''Create a new Alert object, with the following obligatory parameters: identifier, sender, sent, status, msgType and scope. The identifier and sent parameters can be None, in which case they will be generated automatically.'''
        # Check if the identifier is None and if it is, generate a random one
        if identifier == None:
            identifier = datetime.now().strftime("%Y%m%d%H%M%S")
        # Check if the sent is None and if it is, generate a random one
        if sent == None:
            sent = datetime.now().astimezone(timezone.utc).isoformat(timespec='seconds')

        self.xmlns = ("urn:oasis:names:tc:emergency:cap:1.2",0)
        self.identifier = (identifier, 1)
        self.sender = (sender, 2)
        self.sent = (sent, 3)
        self.status = (status, 4)
        self.msgType = (msgType, 5)
        self.source = (None, 6)
        self.scope = (scope, 7)
        self.restriction = (None, 8)
        self.addresses = (None, 9)
        self.code = ([], 10)
        self.note = (None, 11)
        self.references = (None, 12)
        self.incidents = (None, 13)
        self.info = ([], 14)

    def setIdentifier(self, identifier):
        '''Set the identifier of the alert. This must be a string.'''
        if not isinstance(identifier, str):
            return None
        self.identifier = (identifier, 1)

    def getIdentifier(self):
        '''Get the identifier of the alert.'''
        return self.identifier[0]

    def setSender(self, sender):
        '''Set the sender of the alert. This must be a string.'''
        if not isinstance(sender, str):
            return None
        self.sender = (sender, 2)

    def getSender(self):
        '''Get the sender of the alert.'''
        return self.sender[0]

    def setSent(self, sent):
        '''Set the sent of the alert. This must be a datetime object, if it is None, it will be set to the current time.'''
        if sent == None:
            sent = datetime.now()
        self.sent = (sent.astimezone(
            timezone.utc).isoformat(timespec='seconds'), 3)

    def getSent(self):
        '''Get the sent of the alert.'''
        return self.sent[0]
        
    def setStatus(self, status):
        '''Set the status of the alert. This must be a enums.Status object.'''
        if not isinstance(status, enums.Status):
            return None
        self.status = (status, 4)

    def getStatus(self):
        '''Get the status of the alert.'''
        return self.status[0]

    def setMsgType(self, msgType):
        '''Set the msgType of the alert. This must be a enums.MsgType object.'''
        if not isinstance(msgType, enums.MsgType):
            return None
        self.msgType = (msgType, 5)

    def getMsgType(self):
        '''Get the msgType of the alert'''
        return self.msgType[0]

    def setSource(self, source):
        '''Set the source of the alert. This must be a string.'''
        if not isinstance(source, str):
            return None
        self.source = (source, 6)

    def getSource(self):
        '''Get the source of the alert.'''
        return self.source[0]

    def removeSource(self):
        '''Remove the source of the alert.'''
        self.source = (None, 6)

    def setScope(self, scope):
        '''Set the scope of the alert. This must be a enums.Scope object.'''
        if not isinstance(scope, enums.Scope):
            return None

        if scope == enums.Scope.Private and self.addresses[0] == None:
            self.addresses = ("\"CAP Default Address\"", 9)

        self.scope = (scope, 7)

    def getScope(self):
        '''Get the scope of the alert.'''
        return self.scope[0]

    def setRestriction(self, restriction):
        '''Set the restriction of the alert. This must be a string.'''
        if not isinstance(restriction, str):
            return None
        self.restriction = (restriction, 8)

    def getRestriction(self):
        '''Get the restriction of the alert.'''
        return self.restriction[0]

    def removeRestriction(self):
        '''Remove the restriction of the alert.'''
        self.restriction = (None, 8)

    def addAddress(self, address):
        '''Add an address to the alert. This must be a string.'''
        if not isinstance(address, str) and "\"" not in address:
            return None

        if self.addresses[0] == None:
            self.addresses = ("", 9)

        if ' ' in address:
            address = "\"" + address.strips() + "\""

        if "\"CAP Default Address\"" in self.addresses[0]:
            self.addresses = (self.addresses[0].replace("\"CAP Default Address\"", ""),9)

        self.addresses = ((self.addresses[0] + " " + address).strip(), 9)

    def removeAddress(self, address):
        '''Remove an address of the alert. This must be a string. If the scope is Private and no addresses are left, the address will be set to default value'''
        if not isinstance(address, str):
            return None

        if ' ' in address:
            address = "\"" + address + "\""
        self.addresses = (self.addresses[0].replace(address, "").strip(), 9)

        if self.scope[0] == enums.Scope.Private and self.addresses[0] == "":
            self.addresses = ("\"CAP Default Address\"", 9)
        elif self.addresses[0] == "":
            self.addresses = (None, 9)

    def getAddresses(self):
        '''Get the addresses of the alert.'''
        return self.addresses[0]

    def removeAllAddresses(self):
        '''Remove all addresses of the alert. If the scope is Private, the address will be set to default value'''
        self.addresses = ("\"CAP Default Address\"",9) if self.scope[0] == enums.Scope.Private else (None,9)
            
    def addCode(self, code):
        '''Add a code to the alert. This must be a string.'''
        if not isinstance(code, str) or ' ' in code:
            return None
        self.code[0].append(code)

    def removeCode(self, code):
        '''Remove a code of the alert. This must be a string.'''
        if not isinstance(code, str):
            return None
        self.code[0].remove(code)

    def getCodes(self):
        '''Get the codes of the alert.'''
        return self.code[0]

    def setNote(self, note):
        '''Set the note of the alert. This must be a string.'''

        if not isinstance(note, str):
            return None
        self.note = (note, 11)

    def getNote(self):
        '''Get the note of the alert.'''
        return self.note[0]

    def addReference(self, sender, identifier, sent):
        '''Add a reference to the alert. Each must be a string.'''

        if not isinstance(sender, str) or not isinstance(identifier, str) or not isinstance(sent, str):
            return None

        ref = sender + "," + identifier + "," + sent
        if ' ' in ref:
            ref = "\"" + ref + "\""

        self.references = (self.references[0] + ref.strip(), 12)

    def removeReference(self, sender, identifier, sent):
        '''Remove a reference of the alert. Each must be a string.'''

        if not isinstance(sender, str) or not isinstance(identifier, str) or not isinstance(sent, str):
            return None

        ref = sender + "," + identifier + "," + sent
        if ' ' in ref:
            ref = "\"" + ref + "\""

        self.references = (self.references[0].replace(ref, "").strip(), 12)

    def getReferences(self):
        '''Get the references of the alert.'''
        return self.references[0]

    def addIncident(self, incident):
        '''Add an incident to the alert. This must be a string.'''

        if not isinstance(incident, str):
            return None

        if ' ' in incident:
            incident = "\"" + incident + "\""
        self.incidents = (self.incidents[0] + " " + incident, 13)

    def removeIncidnet(self, incident):
        '''Remove an incident of the alert. This must be a string.'''

        if not isinstance(incident, str):
            return None

        if ' ' in incident:
            incident = "\"" + incident + "\""
        self.incidents = (self.incidents[0].replace(incident, "").strip() , 13)

    def getIncidents(self):
        '''Get the incidents of the alert.'''
        return self.incidents[0]

    def addInfo(self, info):
        '''Add an info to the alert. This must be an element.Info object.'''
        
        if not isinstance(info, Info):
            return None
        self.info[0].append(info)

    def removeInfo(self, info):
        '''Remove an info of the alert. This must be an element.Info object.'''

        if not isinstance(info, Info):
            return None
        self.info[0].remove(info)

    def getInfos(self):
        '''Get the infos of the alert.'''
        return self.info[0]

    def __str__(self):
        return "alert"


class Info(object):
    def __init__(self, category=[enums.Category.Other], event="CAPParser Default Event", urgency=enums.Urgency.Immediate, severity=enums.Severity.Severe, certainty=enums.Certainty.Observed):
        '''Initialize an Info object. The language must be a string. The category, urgency, severity, and certainty must be enums. If no parameters are given, the default values will be used.'''
        self.language = (None, 0)
        self.category = ([], 1)  
        self.event = (event, 2)  
        self.responseType = ([], 3)
        self.urgency = (urgency, 4)    
        self.severity = (severity, 5)   
        self.certainty = (certainty, 6)  
        self.audience = (None, 7)
        self.eventCode = ([], 8)
        self.effective = (None, 9)
        self.onset = (None, 10)
        self.expires = (None, 11)
        self.senderName = (None, 12)
        self.headline = (None, 13)
        self.description = (None, 14)
        self.instruction = (None, 15)
        self.web = (None, 16)
        self.contact = (None, 17)
        self.parameter = ([], 18)
        self.resource = ([], 19)
        self.area = ([], 20)

    def setLanguage(self, language):
        '''Set the language of the info. This must be a string.'''
        if not isinstance(language, str):
            return None
        self.language = (language, 0)

    def getLanguage(self):
        '''Get the language of the info.'''
        return self.language[0]

    def addCategory(self, category):
        '''Add a category to the info. This must be an enum.Category object.'''
        if not isinstance(category, enums.Category):
            return None
        self.category[0].append(category)

    def removeCategory(self, category):
        '''Remove a category of the info. This must be an enum.Category object. If the category is the only one, it will be replaced with "Other".'''
        if not isinstance(category, enums.Category):
            return None
        self.category[0].remove(category)
        if len(self.category[0]) == 0:
            self.category[0].append(enums.Category.Other)
        
    def getCategories(self):
        '''Get the categories of the info.'''
        return self.category[0]

    def setEvent(self, event):
        '''Set the event of the info. This must be a string.'''
        if isinstance(event, str):
            return None
        self.event = (event, 2)

    def getEvent(self):
        '''Get the event of the info.'''
        return self.event[0]

    def addResponseType(self, responseType):
        '''Add a responseType to the info. This must be an enum.ResponseType object.'''
        if not isinstance(responseType, enums.ResponseType):
            return None
        self.responseType[0].append(responseType)

    def removeResponseType(self, responseType):
        '''Remove a responseType of the info. This must be an enum.ResponseType object.'''
        if not isinstance(responseType, enums.ResponseType):
            return None
        self.responseType[0].remove(responseType)

    def getResponseTypes(self):
        '''Get the responseTypes of the info.'''
        return self.responseType[0]

    def setUrgency(self, urgency):
        '''Set the urgency of the info. This must be an enum.Urgency object.'''
        if not isinstance(urgency, enums.Urgency):
            return None
        self.urgency = (urgency, 4)

    def getUrgency(self):
        '''Get the urgency of the info.'''
        return self.urgency[0]

    def setSeverity(self, severity):
        '''Set the severity of the info. This must be an enum.Severity object.'''
        if not isinstance(severity, enums.Severity):
            return None
        self.severity = (severity, 5)

    def getSeverity(self):
        '''Get the severity of the info.'''
        return self.severity[0]

    def setCertainty(self, certainty):
        '''Set the certainty of the info. This must be an enum.Certainty object.'''
        if not isinstance(certainty, enums.Certainty):
            return None
        self.certainty = (certainty, 6)

    def getCertainty(self):
        '''Get the certainty of the info.'''
        return self.certainty[0]

    def setAudience(self, audience):
        '''Set the audience of the info. This must be a string.'''
        self.audience = (audience, 7)

    def getAudience(self):
        '''Get the audience of the info.'''
        return self.audience[0]

    def addEventCode(self, eventName, eventValue):
        '''Add an eventCode to the info. These must be strings.'''
        self.eventCode[0].append(EventCode(eventName, eventValue))

    def removeEventCode(self, eventCode):
        '''Remove an eventCode of the info. This must be an element.EventCode object.'''
        self.eventCode[0].remove(eventCode)

    def getEventCodes(self):
        '''Get the eventCodes of the info.'''
        return self.eventCode[0]

    def setEffective(self, dateTime):
        '''Set the effective of the info. This must be a datetime object.'''
        self.effective = dateTime.astimezone(
            timezone.utc).isoformat(timespec='seconds')

    def getEffective(self):
        '''Get the effective of the info.'''
        return self.effective[0]

    def setOnset(self, dateTime):
        '''Set the onset of the info. This must be a datetime object.'''
        self.onset = dateTime.astimezone(
            timezone.utc).isoformat(timespec='seconds')

    def getOnset(self):
        '''Get the onset of the info.'''
        return self.onset[0]

    def setExpires(self, dateTime):
        '''Set the expires of the info. This must be a datetime object.'''
        self.expires = dateTime.astimezone(
            timezone.utc).isoformat(timespec='seconds')

    def getExpires(self):
        '''Get the expires of the info.'''
        return self.expires[0]

    def setSenderName(self, senderName):
        '''Set the senderName of the info. This must be a string.'''
        self.senderName = (senderName, 12)

    def getSenderName(self):
        '''Get the senderName of the info.'''
        return self.senderName[0]

    def setHeadline(self, headline):
        '''Set the headline of the info. This must be a string. The headline will be truncated to 160 characters.'''
        self.headline = (headline[:160], 13)

    def getHeadline(self):
        return self.headline[0]

    def setDescription(self, description):
        '''Set the description of the info. This must be a string.'''
        self.description = (description, 14)

    def getDescription(self):
        '''Get the description of the info.'''
        return self.description[0]

    def setInstruction(self, instruction):
        '''Set the instruction of the info. This must be a string.'''
        self.instruction = (instruction, 15)

    def getInstruction(self):
        '''Get the instruction of the info.'''
        return self.instruction[0]

    def setWeb(self, url):
        '''Set the web of the info. This must be a string. It must start with http:// or https://'''
        if not re.match('^https?://.+$', url):
            return None
        self.web = (url, 16)

    def getWeb(self):
        '''Get the web of the info.'''
        return self.web[0]

    def setContact(self, contact):
        '''Set the contact of the info. This must be a string.'''
        self.contact = (contact, 17)

    def getContact(self):
        '''Get the contact of the info.'''
        return self.contact[0]

    def addParameter(self, parameter):
        '''Add a parameter to the info. This must be an element.Parameter object.'''
        self.parameter[0].append(parameter)

    def removeParameter(self, parameter):
        '''Remove a parameter of the info. This must be an element.Parameter object.'''
        self.parameter[0].remove(parameter)

    def getParameters(self):
        '''Get the parameters of the info.'''
        return self.parameter[0]

    def addResource(self, resource):
        '''Add a resource to the info. This must be an element.Resource object.'''
        self.resource[0].append(resource)

    def removeResource(self, resource):
        '''Remove a resource of the info. This must be an element.Resource object.'''
        self.resource[0].remove(resource)

    def getResources(self):
        '''Get the resources of the info.'''
        return self.resource[0]

    def addArea(self, areaareaDesc):
        '''Add an area to the info. This must be an element.Area object.'''
        self.area[0].append(area)

    def removeArea(self, area):
        '''Remove an area of the info. This must be an element.Area object.'''
        self.area[0].remove(area)

    def getAreas(self):
        '''Get the areas of the info.'''
        return self.area[0]

    def __str__(self):
        return "info"


class EventCode(object):
    def __init__(self, eventName=None, eventValue=None):
        '''Initialize an eventCode object. These must be strings.'''
        self.valueName = (eventName, 0)
        self.value = (eventValue, 1)

    def setEventName(self, eventName):
        '''Set the eventName of the eventCode. This must be a string.'''
        self.eventName = (eventName, 0)

    def getEventName(self):
        '''Get the eventName of the eventCode.'''
        return self.eventName[0]

    def setEventValue(self, eventValue):
        '''Set the eventValue of the eventCode. This must be a string.'''
        self.eventValue = (eventValue, 1)

    def getEventValue(self):
        '''Get the eventValue of the eventCode.'''
        return self.eventValue[0]

    def __str__(self):
        return "eventCode"


class Parameter(object):
    def __init__(self, parameterName=None, parameterValue=None):
        '''Initialize a parameter object. These must be strings.'''
        self.valueName = (parameterName, 0)
        self.value = (parameterValue, 1)

    def setParameterName(self, parameterName):
        '''Set the parameterName of the parameter. This must be a string.'''
        self.parameterName = (parameterName, 0)

    def getParameterName(self):
        '''Get the parameterName of the parameter.'''
        return self.parameterName[0]

    def setParameterValue(self, parameterValue):
        '''Set the parameterValue of the parameter. This must be a string.'''
        self.parameterValue = (parameterValue, 1)

    def getParameterValue(self):
        '''Get the parameterValue of the parameter.'''
        return self.parameterValue[0]

    def __str__(self):
        return "parameter"


class Resource(object):
    def __init__(self, resourceDesc=None, resourceMimeType=None):
        '''Initialize a resource object. These must be strings.'''
        self.resourceDesc = (resourceDesc, 0)   
        self.mimeType = (resourceMimeType, 1)   
        self.size = (None, 2)
        self.uri = (None, 3)
        self.derefUri = (None, 4)
        self.digest = (None, 5)

    def setResourceDesc(self, resourceDesc):
        '''Set the resourceDesc of the resource. This must be a string.'''
        self.resourceDesc = (resourceDesc, 0)

    def getResourceDesc(self):
        '''Get the resourceDesc of the resource.'''
        return self.resourceDesc[0]

    def setMimeType(self, resourceMimeType):
        '''Set the mimeType of the resource. This must be a string.'''
        self.mimeType = (resourceMimeType, 1)

    def getMimeType(self):
        '''Get the mimeType of the resource.'''
        return self.mimeType[0]

    def setSize(self, size):
        '''Set the size of the resource. This must be a integer.'''
        self.size = (size, 2)

    def getSize(self):
        '''Get the size of the resource.'''
        return self.size[0]

    def setUri(self, uri):
        '''Set the uri of the resource. This must start with http:// or https://'''
        if not re.match('^https?://.+$', uri):
            return None
        self.uri = (uri, 3)

    def getUri(self):
        '''Get the uri of the resource.'''
        return self.uri[0]

    def setDerefUri(self, derefUri):
        '''Set the derefUri of the resource. This must be a string'''
        self.derefUri = (derefUri, 4)

    def getDerefUri(self):
        '''Get the derefUri of the resource.'''
        return self.derefUri[0]

    def setDigest(self, digest):
        '''Set the digest of the resource. This must be a string'''
        self.digest = (digest, 5)

    def getDigest(self):
        '''Get the digest of the resource.'''
        return self.digest[0]

    def __str__(self):
        return "resource"


class Area(object):
    def __init__(self, areaDesc=None):
        '''Initialize an area object with a areaDesc. This must be a string.'''
        self.areaDesc = (areaDesc, 0)
        self.polygon = ([], 1)
        self.circle = ([], 2)
        self.geocode = ([], 3)
        self.altitude = (None, 4)
        self.ceiling = (None, 5)

    def setAreaDesc(self, areaDesc):
        '''Set the areaDesc of the area. This must be a string.'''
        self.areaDesc = (areaDesc, 0)

    def addPolygon(self, polygon):
        '''Add a polygon to the area. This must be a string.'''
        self.polygon[0].append(polygon)

    def removePolygon(self, polygon):
        '''Remove a polygon from the area. This must be a string.'''
        self.polygon[0].remove(polygon)

    def addCircle(self, circle):
        '''Add a circle to the area. This must be a string.'''
        self.circle[0].append(circle)

    def removeCircle(self, circle):
        '''Remove a circle from the area. This must be a string.'''
        self.circle[0].remove(circle)

    def addGeocode(self, geocodeName, geocodeValue):
        '''Add a geocode to the area. These must be strings.'''
        self.geocode[0].append(Geocode(geocodeName, geocodeValue))

    def removeGeocode(self, geocode):
        '''Remove a geocode from the area. This must be a element.Geocode object.'''
        self.geocode[0].remove(geocode)

    def setAltitude(self, altitude):
        '''Set the altitude of the area. This must be a float.'''
        self.altitude = (altitude, 4)

    def setCeiling(self, ceiling):
        '''Set the ceiling of the area. This must be a float.'''
        self.ceiling = (ceiling, 5)

    def __str__(self):
        return "area"

class Geocode(object):
    def __init__(self, geocodeName=None, geocodeValue=None):
        '''Initialize a geocode object with a geocodeName and geocodeValue. These must be strings.'''
        self.valueName = (geocodeName, 0)
        self.value = (geocodeValue, 1)

    def setGeocodeName(self, geocodeName):
        '''Set the geocodeName of the geocode. This must be a string.'''
        self.geocodeName = (geocodeName, 0)

    def setGeocodeValue(self, geocodeValue):
        '''Set the geocodeValue of the geocode. This must be a string.'''
        self.geocodeValue = (geocodeValue, 1)

    def __str__(self):
        return "geocode"
