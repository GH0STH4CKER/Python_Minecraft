from ursina.prefabs.first_person_controller import FirstPersonController
from ursina import *
import ursina

app = Ursina()

player_enabled = True
p_key_held = False
world_size = 25 # x and y
world_depth = 5 # z

grass_texture = load_texture('assets/grass_block2.png')
stone_texture = load_texture('assets/stone_block2.png')
wood_texture = load_texture('assets/wood_block.png')
brick_texture = load_texture('assets/brick_block.png')
dirt_texture = load_texture('assets/dirt_block.png')
sky_texture = load_texture('assets/skybox.png')
arm_texture = load_texture('assets/arm_texture2.png')
punch_sound = Audio('assets/punch_sound', loop=False, autoplay=False)
block_pick = 1

window.fps_counter.enabled = True
window.exit_button.visible = True



def toggle_player_visibility():
    global player_enabled
    player_enabled = not player_enabled
    player.enabled = player_enabled

def update(self):
    global block_pick
    global p_key_held
    
    if held_keys['p'] and not p_key_held:
        toggle_player_visibility()
        p_key_held = True
    elif not held_keys['p'] and p_key_held:
        p_key_held = False

    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
    else:
        hand.passive()

    if held_keys['1']: block_pick = 1
    if held_keys['2']: block_pick = 2
    if held_keys['3']: block_pick = 3
    if held_keys['4']: block_pick = 4
    if held_keys['5']: block_pick = 5



class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture=grass_texture):
        super().__init__(
            parent=scene,
            position=position,
            model='assets/block',
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, 1),
            scale=0.5
        )
        self.default_color = self.color

    def on_mouse_enter(self):
        self.color = color.color(19, 0.03, 0.7)

    def on_mouse_exit(self):
        self.color = self.default_color

    def input(self, key):
        if key == 'escape':
            application.quit()

        if self.hovered:
            if key == 'right mouse down':
                punch_sound.play()
                if block_pick == 1: voxel = Voxel(position=self.position + mouse.normal, texture=grass_texture)
                if block_pick == 2: voxel = Voxel(position=self.position + mouse.normal, texture=stone_texture)
                if block_pick == 3: voxel = Voxel(position=self.position + mouse.normal, texture=brick_texture)
                if block_pick == 4: voxel = Voxel(position=self.position + mouse.normal, texture=dirt_texture)
                if block_pick == 5: voxel = Voxel(position=self.position + mouse.normal, texture=wood_texture)

            if key == 'left mouse down':
                punch_sound.play()
                destroy(self)
#ursina.EditorCamera()
class NonInteractiveButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.highlight_color = self.color
        self.collision = False

class TableUI(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui)

        cell_size = 0.08  # Size of each cell
        spacing = 0.02  # Spacing between cells

        self.cells = []
        for i in range(9):

            if i <= 4:   
                cell = NonInteractiveButton(               
                parent=self,
                model='quad',
                color=color.rgba(1, 1, 1, 0.9),
                texture=["assets/grass3d.png","assets/Stone3d.png","assets/Brick3d.png","assets/Dirt3d.png","assets/plank3d.png"][i],
                border=0.02,
                scale=(cell_size, cell_size),  # Cells are square now
                origin=(-0.5, 0),
                position=(-0.43 + i * (cell_size + spacing), -0.42)) , # Adjust positions
                text_entity = Text(parent=cell, text=str(i + 1), position=(-0.43 + i * (cell_size + spacing), -0.382))
            else:
                cell = NonInteractiveButton(    
                parent=self,
                model='quad',
                border=0.02,
                scale=(cell_size, cell_size),  # Cells are square now
                origin=(-0.5, 0),
                position=(-0.43 + i * (cell_size + spacing), -0.42))  ,# Adjust positions
                text_entity = Text(parent=cell, text=str(i + 1), position=(-0.43 + i * (cell_size + spacing), -0.382))

            self.cells.append(cell)
            


class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='sphere',
            texture=sky_texture,
            scale=150,
            double_sided=True
        )

class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model='assets/arm',
            texture=arm_texture,
            scale=0.2,
            rotation=Vec3(150, -10, 0),
            position=Vec2(0.4, -0.6)
        )

    def active(self):
        self.position = Vec2(0.3, -0.5)

    def passive(self):
        self.position = Vec2(0.4, -0.6)

for z in range(world_size):
    for x in range(world_size):
        for y in range(world_depth):
            if y == 4: # Top grass layer
                voxel = Voxel(position=(x, y, z), texture=grass_texture)  # Create ground layer
            elif y == 0:  # Bottom stone layer
                voxel = Voxel(position=(x, y, z), texture=stone_texture)
            else:  # Middle other dirt layer
                voxel = Voxel(position=(x, y, z), texture=dirt_texture)

player = FirstPersonController(position=(12,12,5))
table = TableUI()
sky = Sky()
hand = Hand()
window.fullscreen = True
app.run()
