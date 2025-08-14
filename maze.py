import numpy as np
import matplotlib.pyplot as plt
import random
from collections import deque

# Maze parameters
size = 31  # Must be odd for maze generation
maze = np.ones((size, size), dtype=int)  # 1 = wall, 0 = path

# Maze generation using recursive division
def divide(x, y, w, h, orientation):
    if w < 3 or h < 3:
        return
    horizontal = orientation == 'H'
    if horizontal:
        wx = x
        wy = y + (random.randrange(0, h // 2) * 2) + 1
        px = wx + (random.randrange(0, w // 2) * 2)
        for dx in range(w):
            maze[wy][wx + dx] = 1
        maze[wy][px] = 0
        divide(x, y, w, wy - y, 'V')
        divide(x, wy + 1, w, y + h - wy - 1, 'V')
    else:
        wx = x + (random.randrange(0, w // 2) * 2) + 1
        wy = y
        py = wy + (random.randrange(0, h // 2) * 2)
        for dy in range(h):
            maze[wy + dy][wx] = 1
        maze[py][wx] = 0
        divide(x, y, wx - x, h, 'H')
        divide(wx + 1, y, x + w - wx - 1, h, 'H')

# Initialize maze with outer walls and inner paths
maze[1:-1, 1:-1] = 0
divide(1, 1, size - 2, size - 2, 'H')

# Place central island 'C'
center = size // 2
maze[center][center] = 2  # 2 = center island

# Place 5 oil wells (value 3) randomly near center
oil_wells = 0
while oil_wells < 5:
    x = random.randint(center - 5, center + 5)
    y = random.randint(center - 5, center + 5)
    if maze[y][x] == 0:
        maze[y][x] = 3
        oil_wells += 1

# Define 10 zombie entry points on the edges
entry_points = []
for i in range(0, size, size // 5):
    entry_points.append((0, i))  # left edge
    entry_points.append((size - 1, i))  # right edge
    if len(entry_points) >= 10:
        break

# BFS to simulate zombie movement
for y, x in entry_points:
    visited = np.zeros_like(maze)
    queue = deque()
    queue.append((y, x, []))
    while queue:
        cy, cx, path = queue.popleft()
        if not (0 <= cy < size and 0 <= cx < size):
            continue
        if visited[cy][cx] or maze[cy][cx] in [1, 3]:
            continue
        visited[cy][cx] = 1
        new_path = path + [(cy, cx)]
        if maze[cy][cx] == 2:
            for py, px in new_path:
                if maze[py][px] == 0:
                    maze[py][px] = 4  # 4 = zombie path
            maze[cy][cx] = 5  # 5 = zombie reached center
            break
        for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
            queue.append((cy + dy, cx + dx, new_path))

# Visualization
colors = {
    0: 'white',   # path
    1: 'gray',    # wall
    2: 'blue',    # center island
    3: 'orange',  # oil well
    4: 'green',   # zombie path
    5: 'red'      # zombie reached center
}
cmap = plt.matplotlib.colors.ListedColormap([colors[i] for i in range(6)])
plt.figure(figsize=(8, 8))
plt.imshow(maze, cmap=cmap)
plt.title("Zombie Maze Invasion")
plt.axis('off')
plt.show()

