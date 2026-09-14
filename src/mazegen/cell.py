from dataclasses import dataclass, field


# stream-line classes that exist to store data,
@dataclass
class Cell:
    """
    This class is for Cell metadata
    """

    x: int
    y: int
    north: bool = True
    east: bool = True
    south: bool = True
    west: bool = True
