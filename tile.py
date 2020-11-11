class Tile:
    def __init__(self, pos, indices, angle=0):
        self.x = pos[0]
        self.y = pos[1]
        self.angle = angle
        self.row = indices[0]
        self.col = indices[1]

    def get_pos(self):
        return self.x, self.y

    def get_indices(self):
        return self.row, self.col
