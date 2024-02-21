#%%
# Imports
import random
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

#%% Perling generation function
def generate_perlin_noise(xpix, ypix, octaves=3, seed=0):
    np.random.seed(seed)
    noise = PerlinNoise(octaves=octaves, seed=seed)
    return np.array([[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)])

#%% Function to convert mesh data to .obj format
def save_obj(filename, vertices, faces):
    with open(filename, 'w') as f:
        for vertex in vertices:
            f.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
        for face in faces:
            f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")

#%%
# Constants
xpix = 30
ypix = 30
octaves = 1
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

# colors = []
# for index,value in enumerate(my_map):
#     for i in value:
#         if i<=100:
#             colors.append('blue')
#         else:
#             colors.append('green')

x = np.arange(len(my_map))
z = np.arange(len(my_map[0]))
x, z = np.meshgrid(x, z)
x = x.flatten()
z = z.flatten()

y = my_map.flatten()
#ax.scatter(x,z,y, c=colors)
max_y = max(y)
size = [xpix, max_y, ypix]

if __name__ == '__main__':
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
    # Displaying 3D plot
    fig = plt.figure()

    ax = fig.add_subplot(111, projection='3d')

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
elif __name__ == 'perlin':
    blocks = {"grass_block": [], "water": []}
    positions_y = []
    # colors = []
    for x in range(len(my_map)):
        for z in range(len(my_map[0])):
            y:np.float64 = my_map[x][z]
            if y <= 70:
                blocks['water'].append([x, y, z])
            else:
                blocks['grass_block'].append([x, y, z])
            positions_y.append(y)
                
    def getInfo():
        info = {"size": size, "blocks": blocks, "map": my_map, "spawn": (random.randint(0, xpix), size[1], random.randint(0, ypix)), "min_y": min(positions_y)}
        return info