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

class PriorityType(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2

class FeedbackStatusType(Enum):
    PENDING = 0
    PROCESSING = 1
    PROCESSED = 2

