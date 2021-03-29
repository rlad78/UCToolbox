class Coordinate:    
    def __init__(self, x: int, y: int) -> None:
        """Initializes a 2d POSITIVE ONLY coordinate, with some maths useful for
        working in xlwings

        Args:
            x (int): x-coord
            y (int): y-coord
        """
        self.x = x
        self.y = y
        
    def pos(self) -> tuple[int, int]:
        return self.x, self.y
    
    def __add__(self, other):
        if type(other) == object:
            return tuple(map(sum, zip(other.pos, self.pos())))
        elif type(other) == int:
            self.x += other
            self.y += other
        elif type(other) == tuple:
            self.x, self.y = tuple(map(sum, zip(other.pos, self.pos())))
        else:
            raise Exception(f'[Coordinate] addition with type {type(other)} is not supported')
    
    def inc_x(self, x=1) -> None:
        self.x += x
        
    def inc_y(self, y=1) -> None:
        self.y += y
