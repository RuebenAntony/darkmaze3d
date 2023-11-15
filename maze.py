from panda3d.core import GeomNode, NodePath, CardMaker
import random

class Maze:
    def __init__(self, size):
        self.size = size
        self.maze = self.generate_maze()
        self.ground = self.generate_ground()

    def set_color(self, r, g, b):
        for row in self.maze:
            for cell in row:
                if cell is not None:
                    cell.setColor(r, g, b, 1)  # Set the color to the provided RGB values

    def generate_maze(self):
        # Initialize all cells as isolated sets
        sets = [[(i, j)] for i in range(self.size) for j in range(self.size)]
        walls = []

        # Create walls and associate them with adjacent cells
        for i in range(self.size):
            for j in range(self.size):
                if i < self.size - 1:
                    walls.append(((i, j), (i + 1, j)))
                if j < self.size - 1:
                    walls.append(((i, j), (i, j + 1)))

        # Randomly select walls and merge cells
        random.shuffle(walls)
        while walls:
            cell1, cell2 = walls.pop()
            set1 = [s for s in sets if cell1 in s][0]
            set2 = [s for s in sets if cell2 in s][0]
            if set1 != set2:
                set1.extend(set2)
                sets.remove(set2)

        # Generate the maze based on the sets
        maze = [[None]*self.size for _ in range(self.size)]
        for s in sets:
            row = [None]*self.size
            for cell in s:
                i, j = cell
                # Create a square
                cm = CardMaker('cell')
                cm.setFrame(-0.5, 0.5, -0.5, 0.5)  # Set the size of the square

                # Generate the geometry for the square
                geom = cm.generate()

                # Create a node path for the cell
                node_path = NodePath(geom)

                # Extrude the square to create a cube with random height
                node_path.setScale(1, 1, random.uniform(0.1, 1.0))  # Set the size of the cube

                # Check if the wall is isolated
                if i > 0 and maze[i-1][j] is not None or \
                   i < self.size - 1 and maze[i+1][j] is not None or \
                   j > 0 and maze[i][j-1] is not None or \
                   j < self.size - 1 and maze[i][j+1] is not None:
                    # Set the position and orientation of the cube
                    node_path.setPos(i, j, 0)  # Set the position of the cube
                    node_path.setHpr(random.randint(0, 360), 0, 0)  # Rotate randomly around the Z-axis

                    # Set the color of the cube to grey
                    node_path.setColor(0.5, 0.5, 0.5, 1)  # Set the color to grey
                    row[j] = node_path
            maze[i] = row
        return maze

    def generate_ground(self):
        # Create a square
        cm = CardMaker('ground')
        cm.setFrame(-self.size / 2, self.size / 2, -self.size / 2, self.size / 2)  # Set the size of the square

        # Generate the geometry for the square
        geom = cm.generate()

        # Create a node path for the ground
        node_path = NodePath(geom)

        # Set the position of the ground
        node_path.setPos(self.size / 2, self.size / 2, -0.1)  # Set the position of the ground

        # Rotate the ground to make it horizontal
        node_path.setHpr(90, 90, 0)  # Rotate 90 degrees around the X-axis and Y-axis

        # Set the color of the ground to black
        node_path.setColor(0, 0, 0, 1)  # Set the color to black

        # Make the ground visible from both sides
        node_path.setTwoSided(True)

        return node_path
