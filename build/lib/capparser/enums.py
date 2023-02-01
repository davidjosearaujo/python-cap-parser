from enum import Enum

# Alert tag 
class Status(Enum):
    Actual = 1
    Exercise = 2
    System = 3
    Test = 4
    Draft = 5

class MsgType(Enum):
    Alert = 1
    Update = 2
    Cancel = 3
    Ack = 4
    Error = 5

class Scope(Enum):
    Public = 1
    Restricted = 2
    Private = 3

# Info tag
class Category(Enum):
    Geo = 1
    Met = 2
    Safety = 3
    Security = 4
    Rescue = 5
    Fire = 6
    Health = 7
    Env = 8
    Transport = 9
    Infra = 10
    CBRNE = 11
    Other = 12

class ResponseType(Enum):
    Shelter = 1
    Evacuate = 2
    Prepare = 3
    Execute = 4
    Avoid = 5
    Monitor = 6
    Assess = 7
    AllClear = 8
    NoResponse = 9

class Urgency(Enum):
    Immediate = 1
    Expected = 2
    Future = 3
    Past = 4
    Unknown = 5

class Severity(Enum):
    Extreme = 1
    Severe = 2
    Moderate = 3
    Minor = 4
    Unknown = 5

class Certainty(Enum):
    Observed = 1
    Likely = 2
    Possible = 3
    Unlikely = 4
    Unknown = 5
