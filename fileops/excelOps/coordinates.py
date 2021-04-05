class Coordinate:    
    def __init__(self, y: int, x: int) -> None:
        """Initializes a 2d POSITIVE ONLY coordinate, with some maths useful for
        working in xlwings

        Args:
            y (int): y-coord, first in excel land
            x (int): x-coord
        """
        if x < 0 or y < 0:
            raise Exception('Coordinate values not allowed to be non-positive or zero')
        self.y = y
        self.x = x
        
    def pos(self) -> tuple[int, int]:
        return self.y, self.x
    
    def __add__(self, other):
        if type(other).__name__ == 'Coordinate':
            return tuple(map(sum, zip(other.pos(), self.pos())))
        elif type(other) == int:
            return self.y + other, self.x + other
        elif type(other) == tuple:
            return tuple(map(sum, zip(other, self.pos())))
        else:
            raise TypeError(f'[Coordinate] addition with type {type(other)} is not supported')
                
    def __sub__(self, other):
        if type(other).__name__ == 'Coordinate':
            return tuple(map(lambda t: abs(t[0]-t[1]), zip(self.pos(), other.pos())))
        elif type(other) == int:
            return self.y - other, self.x - other
        elif type(other) == tuple:
            return tuple(map(lambda t: abs(t[0]-t[1]), zip(self.pos(), other)))
        else:
            raise TypeError(f'[Coordinate] subtraction with type {type(other)} is not supported')

    def inc_y(self, y=1) -> None:
        self.y += y
    
    def inc_x(self, x=1) -> None:
        self.x += x

    def dec_y(self, y=1) -> None:
        self.y -= y
        
    def dec_x(self, x=1) -> None:
        self.x -= x
