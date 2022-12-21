class Alert(object):
    def __init__(self):
        self.xmlns = None
        self.identifier = None
        self.sender = None
        self.sent = None
        self.status = None
        self.msgType = None
        self.source = None
        self.scope = None
        self.restriction = None
        self.addresses = None
        self.code = []
        self.note = None
        self.references = None
        self.incidents = None
        self.info = []

    def __str__(self):
        return "alert"

class Info(object):
    def __init__(self):
        self.language = None
        self.category = []
        self.event = None
        self.responseType = []
        self.urgency = None
        self.severity = None
        self.certainty = None
        self.audience = None
        self.eventCode = []
        self.effective = None
        self.onset = None
        self.expires = None
        self.senderName = None
        self.headline = None
        self.description = None
        self.instruction = None
        self.web = None
        self.contact = None
        self.parameter = []
        self.resource = []
        self.area = []

    def __str__(self):
        return "info"

class EventCode(object):
    def __init__(self):
        self.valueName = None
        self.value = None

    def __str__(self):
        return "eventCode"

class Parameter(object):
    def __init__(self):
        self.valueName = None
        self.value = None

    def __str__(self):
        return "parameter"

class Resource(object):
    def __init__(self):
        self.resourceDesc = None
        self.mimeType = None
        self.size = None
        self.uri = None
        self.derefUri = None
        self.digest = None

    def __str__(self):
        return "resource"

class Area(object):
    def __init__(self):
        self.areaDesc = None
        self.polygon = []
        self.circle = []
        self.geocode = []
        self.altitude = None
        self.ceiling = None

    def __str__(self):
        return "area"

class Geocode(object):
    def __init__(self):
        self.valueName = None
        self.value = None

    def __str__(self):
        return "geocode"
