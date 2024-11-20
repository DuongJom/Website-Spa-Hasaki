from enum import Enum

class GenderType(Enum):
    MALE = 0
    FEMALE = 1
    OTHER = 2

class AppointmentStatus(Enum):
    CANCEL = 0
    COMPLETE = 1
    INCOMPLETE = 2