import perlin
from ursina import *
from ursina import color as colors
import numpy as np
from ursina.prefabs.first_person_controller import FirstPersonController

terrain = perlin.getInfo()

BEDROCK = 'assets/rock.png'
GRASS_BLOCK = 'assets/grass.png'
DIRT_BLOCK = 'assets/dirt.png'
WATER_BLOCK = 'assets/water.png'

def update():
    if player.Y<=terrain['min_y']-10:
        player.position = terrain['spawn']

class Voxel(Button):
    def __init__(self, text='', parent=camera.ui, model=..., radius=0.1, origin=..., text_origin=..., text_size=1, color=..., collider='box', highlight_scale=1, pressed_scale=1, disabled=False, **kwargs):
        self.kwargs = kwargs
        super().__init__(
            parent=scene,
            position=kwargs['position'],
            model='cube',
            origin_y=0.5,
            texture=kwargs['texture'],
            color=colors.white,
            highlight_color=colors.gray
        )
    def input(self, key):
        if self.hovered:
            if key == 'right mouse down':
                voxel = Voxel(position=(self.position+mouse.normal), texture=self.kwargs['texture'])
            elif key == 'left mouse down':
                destroy(self)

app = Ursina()
level_parent = Entity(model=Mesh(vertices=[], uvs=[]))
terrain_map = np.array(terrain['map'])

for z in range(terrain['size'][2]):
    for x in range(terrain['size'][0]):
        y = terrain_map[x][z]
        if [x, y, z] in terrain['blocks']['grass_block']:
            texture = GRASS_BLOCK
        else:
            texture = WATER_BLOCK
        layer1 = Voxel(position=(x, y, z), texture=texture)
        level_parent.combine().vertices.extend(layer1.combine().vertices)

level_parent.collider = 'mesh'
camera = EditorCamera()
player = FirstPersonController(position=terrain['spawn'])
app.run()