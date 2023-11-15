from direct.showbase.ShowBase import ShowBase
from maze import Maze


class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        self.maze = Maze(20)
        self.maze.set_color(1, 1, 1)  # Set the maze color to white

        # Attach the maze and the ground to the render node
        for row in self.maze.maze:
            for cell in row:
                if cell is not None:
                    cell.reparentTo(self.render)
        self.maze.ground.reparentTo(self.render)

        # No texture is applied to the maze, it will just be grey

        # Define the key mappings
        self.keyMap = {"left":0, "right":0, "forward":0, "backward":0, "up":0, "down":0}

        # Add the key event handlers
        self.accept("w", self.setKey, ["forward", 1])
        self.accept("w-up", self.setKey, ["forward", 0])
        self.accept("s", self.setKey, ["backward", 1])
        self.accept("s-up", self.setKey, ["backward", 0])
        self.accept("a", self.setKey, ["left", 1])
        self.accept("a-up", self.setKey, ["left", 0])
        self.accept("d", self.setKey, ["right", 1])
        self.accept("d-up", self.setKey, ["right", 0])
        self.accept("space", self.setKey, ["up", 1])
        self.accept("space-up", self.setKey, ["up", 0])
        self.accept("shift", self.setKey, ["down", 1])
        self.accept("shift-up", self.setKey, ["down", 0])

        # Add a task to update the camera
        self.taskMgr.add(self.update_camera, "update_camera")

    def setKey(self, key, value):
        self.keyMap[key] = value

    def update_camera(self, task):
        if self.mouseWatcherNode.hasMouse():
            # Get the mouse position
            x = self.mouseWatcherNode.getMouseX()
            y = self.mouseWatcherNode.getMouseY()

            # Update the camera orientation
            self.camera.lookAt(x * 10, y * -10, 0)

        # Update the camera position
        if self.keyMap["left"]:
            self.camera.setX(self.camera, -10 * globalClock.getDt())
        if self.keyMap["right"]:
            self.camera.setX(self.camera, 10 * globalClock.getDt())
        if self.keyMap["forward"]:
            self.camera.setY(self.camera, 10 * globalClock.getDt())
        if self.keyMap["backward"]:
            self.camera.setY(self.camera, -10 * globalClock.getDt())
        if self.keyMap["up"]:
            self.camera.setZ(self.camera, 10 * globalClock.getDt())
        if self.keyMap["down"]:
            self.camera.setZ(self.camera, -10 * globalClock.getDt())

        return task.cont


app = MyApp()
app.run()
