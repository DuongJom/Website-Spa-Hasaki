from enum import Enum

class GenderType(Enum):
    MALE = 0
    FEMALE = 1
    OTHER = 2

class AppointmentStatusType(Enum):
    CANCEL = 0
    COMPLETE = 1
    INCOMPLETE = 2

class DeletedType(Enum):
    AVAILABLE = 0
    DELETED = 1