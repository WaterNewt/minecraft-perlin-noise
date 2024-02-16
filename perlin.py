#%%
# Imports
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

#%% 
# Perling generation function
def generate_perlin_noise(xpix, ypix, octaves=3, seed=0):
    np.random.seed(seed)
    noise = PerlinNoise(octaves=octaves, seed=seed)
    return np.array([[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)])

#%%
# Constants
xpix = 30
ypix = 30
octaves = 2.5
seed = 0

#%%
# Creating 2D array of Y levels
perlin_map = generate_perlin_noise(xpix, ypix, octaves, seed)
my_map = []
for index,value in enumerate(perlin_map):
    my_map.append([])
    for i in value:
        new_height = i
        new_height = 100 + i * 100
        my_map[index].append(new_height)
my_map = np.array(my_map)
print(my_map)

#%%
# Creating colors for 2D map
noise_colors = [(0.0, 'blue'), (0.5, 'blue'), (0.51, 'green'), (1.0, 'green')]
custom_cmap = LinearSegmentedColormap.from_list('minecraft', noise_colors)

#%%
# Displaying 2D plot
plt.imshow(my_map, cmap=custom_cmap)
plt.colorbar()
plt.xlabel('X')
plt.ylabel('Z')
plt.title('2D Procedural Generation')

#%%
# Draw 3D graph
fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')

x = np.arange(len(my_map))
z = np.arange(len(my_map[0]))
x, z = np.meshgrid(x, z)
x = x.flatten()
z = z.flatten()

y = my_map.flatten()
max_y = max(y)
size = [xpix, max_y, ypix]

for i in range(len(my_map)):
    for j in range(len(my_map[0])):
        x = i
        z = j
        y = my_map[i][j]
        if y <= 100:
            color = 'blue'
        else:
            color = 'green'
        ax.bar3d(x, z, 0, 1, 1, y, color=color)

ax.set_xlabel('X')
ax.set_ylabel('Z')
ax.set_zlabel('Y')
ax.set_title('3D Procedural Generation')

plt.show()
# %%
