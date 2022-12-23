from datetime import datetime, timezone
from enums import enums
import random
import re

# FEATURE - Convert class attributes to private
# FEATURE - Edit __str__ and create __tag__ for each class
# FEATURE - Add docstrings
# FEATURE - Add type hints

class Alert(object):
    def __init__(self, identifier=None, sender="CAPParser", sent=None, status=enums.Status.Actual, msgType=enums.MsgType.Alert, scope=enums.Scope.Public):
        # Check if the identifier is None and if it is, generate a random one
        if identifier == None:
            identifier = datetime.now().strftime("%Y%m%d%H%M%S")
        # Check if the sent is None and if it is, generate a random one
        if sent == None:
            sent = datetime.now().astimezone(timezone.utc).isoformat(timespec='seconds')

        self.xmlns = ("urn:oasis:names:tc:emergency:cap:1.2",0)
        self.identifier = (identifier, 1)  # Obligatory
        self.sender = (sender, 2)  # Obligatory
        self.sent = (sent, 3)  # Obligatory
        self.status = (status, 4)  # Obligatory
        self.msgType = (msgType, 5)  # Obligatory
        self.source = (None, 6)
        self.scope = (scope, 7)  # Obligatory
        self.restriction = (None, 8)
        self.addresses = (None, 9)
        self.code = ([], 10)
        self.note = (None, 11)
        self.references = (None, 12)
        self.incidents = (None, 13)
        self.info = ([], 14)

    def setIdentifier(self, identifier):
        self.identifier = (identifier, 1)

    def setSender(self, sender):
        self.sender = (sender, 2)

    def setSent(self, sent):
        if sent == None:
            sent = datetime.now()
        self.sent = (sent.astimezone(
            timezone.utc).isoformat(timespec='seconds'), 3)
        
    def setStatus(self, status):
        if not isinstance(status, enums.Status):
            return None
        self.status = (status, 4)

    def setMsgType(self, msgType):
        if not isinstance(msgType, enums.MsgType):
            return None
        self.msgType = (msgType, 5)

    def setSource(self, source):
        self.source = (source, 6)

    def setScope(self, scope):
        if not isinstance(scope, enums.Scope):
            return None
        self.scope = (scope, 7)

    def setRestriction(self, restriction):
        self.restriction = (restriction, 8)

    def addAddress(self, address):
        if ' ' in address and  "\"" not in address:
            address = "\"" + address + "\""
        self.addresses[0].concat(" " + address).strip()

    def removeAddress(self, address):
        if ' ' in address:
            address = "\"" + address + "\""
        self.addresses[0].replace(address, "")
        self.addresses[0].strip()

    def addCode(self, code):
        if ' ' in code:
            return None
        self.code[0].append(code)

    def removeCode(self, code):
        self.code[0].remove(code)

    def setNote(self, note):
        self.note = (note, 11)

    def addReference(self, sender, identifier, sent):
        self.references[0].concat(" " + sender + "," + identifier + "," + sent)
        self.references[0].strip()

    def removeReference(self, sender, identifier, sent):
        self.references[0].replace(sender + "," +
                                identifier + "," + sent, "")
        self.references[0].strip()

    def addIncident(self, incident):
        if ' ' in incident:
            incident = "\"" + incident + "\""
        self.incidents[0].concat(" " + incident)
        self.incidents[0].strip()

    def removeIncidnet(self, incident):
        if ' ' in incident:
            incident = "\"" + incident + "\""
        self.incidents[0].replace(incident, "")
        self.incidents[0].strip()

    def addInfo(self, info):
        self.info[0].append(info)

    def removeInfo(self, info):
        self.info[0].remove(info)

    def __str__(self):
        return "alert"


class Info(object):
    def __init__(self, language="en-US", category=enums.Category.Fire, event="CAPParser Default Event", urgency=enums.Urgency.Immediate, severity=enums.Severity.Severe, certainty=enums.Certainty.Observed):
        self.language = (language, 0)
        self.category = (category, 1)  # Obligatory
        self.event = (event, 2)  # Obligatory
        self.responseType = ([], 3)
        self.urgency = (urgency, 4)    # Obligatory
        self.severity = (severity, 5)   # Obligatory
        self.certainty = (certainty, 6)  # Obligatory
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
        self.language = (language, 0)

    def addCategory(self, category):
        if not isinstance(category, enums.Category):
            return None
        self.category[0].append(category)

    def removeCategory(self, category):
        if not isinstance(category, enums.Category):
            return None
        self.category[0].remove(category)

    def setEvent(self, event):
        if isinstance(event, str):
            return None
        self.event = (event, 2)

    def addResponseType(self, responseType):
        if not isinstance(responseType, enums.ResponseType):
            return None
        self.responseType[0].append(responseType)

    def removeResponseType(self, responseType):
        if not isinstance(responseType, enums.ResponseType):
            return None
        self.responseType[0].remove(responseType)

    def setUrgency(self, urgency):
        if not isinstance(urgency, enums.Urgency):
            return None
        self.urgency = (urgency, 4)

    def setSeverity(self, severity):
        if not isinstance(severity, enums.Severity):
            return None
        self.severity = (severity, 5)

    def setCertainty(self, certainty):
        if not isinstance(certainty, enums.Certainty):
            return None
        self.certainty = (certainty, 6)

    def setAudience(self, audience):
        self.audience = (audience, 7)

    def addEventCode(self, eventName, eventValue):
        self.eventCode[0].append(EventCode(eventName, eventValue))

    def removeEventCode(self, eventCode):
        self.eventCode[0].remove(eventCode)

    def setEffective(self, dateTime):
        self.effective = dateTime.astimezone(
            timezone.utc).isoformat(timespec='seconds')

    def setOnset(self, dateTime):
        self.onset = dateTime.astimezone(
            timezone.utc).isoformat(timespec='seconds')

    def setExpires(self, dateTime):
        self.expires = dateTime.astimezone(
            timezone.utc).isoformat(timespec='seconds')

    def setSenderName(self, senderName):
        self.senderName = (senderName, 12)

    def setHeadline(self, headline):
        self.headline = (headline[:160], 13)

    def setDescription(self, description):
        self.description = (description, 14)

    def setInstruction(self, instruction):
        self.instruction = (instruction, 15)

    def setWeb(self, url):
        if not re.match('^https?://.+$', url):
            return None
        self.web = (url, 16)

    def setContact(self, contact):
        self.contact = (contact, 17)

    def addParameter(self, parameterName, parameterValue):
        self.parameter[0].append(Parameter(parameterName, parameterValue))

    def removeParameter(self, parameter):
        self.parameter[0].remove(parameter)

    def addResource(self, resource):
        self.resource[0].append(Resource(resource))

    def removeResource(self, resource):
        self.resource[0].remove(resource)

    def addArea(self, areaDesc):
        self.area[0].append(Area(areaDesc))

    def removeArea(self, area):
        self.area[0].remove(area)

    def __str__(self):
        return "info"


class EventCode(object):
    def __init__(self, eventName, eventValue):
        self.valueName = (eventName, 0)
        self.value = (eventValue, 1)

    def setEventName(self, eventName):
        self.eventName = (eventName, 0)

    def setEventValue(self, eventValue):
        self.eventValue = (eventValue, 1)

    def __str__(self):
        return "eventCode"


class Parameter(object):
    def __init__(self, parameterName, parameterValue):
        self.valueName = (parameterName, 0)
        self.value = (parameterValue, 1)

    def setParameterName(self, parameterName):
        self.parameterName = (parameterName, 0)

    def setParameterValue(self, parameterValue):
        self.parameterValue = (parameterValue, 1)

    def __str__(self):
        return "parameter"


class Resource(object):
    def __init__(self, resourceDesc, resourceMimeType):
        self.resourceDesc = (resourceDesc, 0)   # Obligatory
        self.mimeType = (resourceMimeType, 1)   # Obligatory
        self.size = (None, 2)
        self.uri = (None, 3)
        self.derefUri = (None, 4)
        self.digest = (None, 5)

    def setResourceDesc(self, resourceDesc):
        self.resourceDesc = (resourceDesc, 0)

    def setMimeType(self, resourceMimeType):
        self.mimeType = (resourceMimeType, 1)

    def setSize(self, size):
        self.size = (size, 2)

    def setUri(self, uri):
        self.uri = (uri, 3)

    def setDerefUri(self, derefUri):
        self.derefUri = (derefUri, 4)

    def setDigest(self, digest):
        self.digest = (digest, 5)

    def __str__(self):
        return "resource"


class Area(object):
    def __init__(self, areaDesc):
        self.areaDesc = (areaDesc, 0)   # Obligatory
        self.polygon = ([], 1)
        self.circle = ([], 2)
        self.geocode = ([], 3)
        self.altitude = (None, 4)
        self.ceiling = (None, 5)

    def setAreaDesc(self, areaDesc):
        self.areaDesc = (areaDesc, 0)

    def addPolygon(self, polygon):
        self.polygon[0].append(polygon)

    def removePolygon(self, polygon):
        self.polygon[0].remove(polygon)

    def addCircle(self, circle):
        self.circle[0].append(circle)

    def removeCircle(self, circle):
        self.circle[0].remove(circle)

    def addGeocode(self, geocodeName, geocodeValue):
        self.geocode[0].append(Geocode(geocodeName, geocodeValue))

    def removeGeocode(self, geocode):
        self.geocode[0].remove(geocode)

    def setAltitude(self, altitude):
        self.altitude = (altitude, 4)

    def setCeiling(self, ceiling):
        self.ceiling = (ceiling, 5)

    def __str__(self):
        return "area"

class Geocode(object):
    def __init__(self, geocodeName, geocodeValue):
        self.valueName = (geocodeName, 0)
        self.value = (geocodeValue, 1)

    def setGeocodeName(self, geocodeName):
        self.geocodeName = (geocodeName, 0)

    def setGeocodeValue(self, geocodeValue):
        self.geocodeValue = (geocodeValue, 1)

    def __str__(self):
        return "geocode"
