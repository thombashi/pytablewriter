from enum import Enum, unique


@unique
class FontSize(Enum):
    NONE = "none"
    TINY = "tiny"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


@unique
class FontStyle(Enum):
    NORMAL = "normal"
    ITALIC = "italic"
    TYPEWRITER = "typewriter"


@unique
class FontWeight(Enum):
    NORMAL = "normal"
    BOLD = "bold"
