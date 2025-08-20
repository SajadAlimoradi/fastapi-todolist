from enum import Enum


class PriorityEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class CategoryEnum(str, Enum):
    WORK = "work"
    PERSONAL = "personal"
    SHOPPING = "shopping"
