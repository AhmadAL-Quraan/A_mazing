from dataclasses import dataclass


# stream-line classes that exist to store data,
@dataclass
class Cell:
    """This class is for Cell metadata

    Args:
        x: the x-axis of the cell (the row the cell exists in)
        y: The y-axis of the cell (the col the cell exists in)
        north: the cell's upper wall
        east: the cell's right wall
        south: the cell's lower wall
        west: the cell's left wall

    """

    x: int
    y: int
    north: bool = True
    east: bool = True
    south: bool = True
    west: bool = True
