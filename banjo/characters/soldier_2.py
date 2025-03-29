from __future__ import annotations

__all__ = ["Soldier2"]

import arcade

# Constants
RIGHT_FACING = 0
LEFT_FACING = 1

# Soldier 2 Constants
WALKING_VELOCITY = 100
RUNNING_VELOCITY = 200
HEALTH_POINTS = 30
ACCURACY = 0.7
VISION_RANGE = 800

# FAMAS Constants
FAMAS_DAMAGE = 10
FAMAS_MAG = 20
BULLET_MOVE_FORCE = 4500
BULLET_MASS = 0.1
BULLET_GRAVITY = 300

SHOOTING_SOUND = arcade.load_sound("sounds/snd_shooting.wav")
SHELL_SOUND = arcade.load_sound("sounds/snd_bullet_shell.wav")

PATH_CONSTANT = "sprites/soldier_2/"
IDLE = PATH_CONSTANT + "Idle.png"
WALK = PATH_CONSTANT + "Walk.png"
RUN = PATH_CONSTANT + "Run.png"
MELEE = PATH_CONSTANT + "Melee.png"
CROUCH_FIRE = PATH_CONSTANT + "Crouched_shooting.png"
AIM_FIRE = PATH_CONSTANT + "Aimed_down_shooting.png"
RELOAD = PATH_CONSTANT + "Reload.png"
HURT = PATH_CONSTANT + "Hurt.png"
DEATH = PATH_CONSTANT + "Death.png"

IDLE_SPRITESHEET = arcade.load_spritesheet(IDLE)
WALK_SPRITESHEET = arcade.load_spritesheet(WALK)
RUN_SPRITESHEET = arcade.load_spritesheet(RUN)
MELEE_SPRITESHEET = arcade.load_spritesheet(MELEE)
CROUCH_FIRE_SPRITESHEET = arcade.load_spritesheet(CROUCH_FIRE)
AIM_FIRE_SPRITESHEET = arcade.load_spritesheet(AIM_FIRE)
RELOAD_SPRITESHEET = arcade.load_spritesheet(RELOAD)
HURT_SPRITESHEET = arcade.load_spritesheet(HURT)
DEATH_SPRITESHEET = arcade.load_spritesheet(DEATH)

TEXTURE_CANVAS = (256, 128)
IDLE_TEXTURE_GRID = IDLE_SPRITESHEET.get_texture_grid(TEXTURE_CANVAS, 9, 9)
WALK_TEXTURE_GRID = WALK_SPRITESHEET.get_texture_grid(TEXTURE_CANVAS, 8, 8)
RUN_TEXTURE_GRID = RUN_SPRITESHEET.get_texture_grid(TEXTURE_CANVAS, 8, 8)
MELEE_TEXTURE_GRID = MELEE_SPRITESHEET.get_texture_grid(TEXTURE_CANVAS, 4, 4)
CROUCHED_FIRE_TEXTURE_GRID = CROUCH_FIRE_SPRITESHEET.get_texture_grid(TEXTURE_CANVAS, 7, 7)
AIM_FIRE_TEXTURE_GRID = AIM_FIRE_SPRITESHEET.get_texture_grid(TEXTURE_CANVAS, 7, 7)
RELOAD_TEXTURE_GRID = RELOAD_SPRITESHEET.get_texture_grid(TEXTURE_CANVAS, 8, 8)
HURT_TEXTURE_GRID = HURT_SPRITESHEET.get_texture_grid(TEXTURE_CANVAS, 3, 3)
DEATH_TEXTURE_GRID = DEATH_SPRITESHEET.get_texture_grid(TEXTURE_CANVAS, 9, 9)

IDLE_TEXTURES = [(texture, texture.flip_left_right()) for texture in IDLE_TEXTURE_GRID]
WALK_TEXTURES = [(texture, texture.flip_left_right()) for texture in WALK_TEXTURE_GRID]
RUN_TEXTURES = [(texture, texture.flip_left_right()) for texture in RUN_TEXTURE_GRID]
MELEE_TEXTURES = [(texture, texture.flip_left_right()) for texture in MELEE_TEXTURE_GRID]
CROUCHED_FIRE_TEXTURES = [(texture, texture.flip_left_right()) for texture in CROUCHED_FIRE_TEXTURE_GRID]
AIM_FIRE_TEXTURES = [(texture, texture.flip_left_right()) for texture in AIM_FIRE_TEXTURE_GRID]
RELOAD_TEXTURES = [(texture, texture.flip_left_right()) for texture in RELOAD_TEXTURE_GRID]
HURT_TEXTURES = [(texture, texture.flip_left_right()) for texture in HURT_TEXTURE_GRID]
DEATH_TEXTURES = [(texture, texture.flip_left_right()) for texture in DEATH_TEXTURE_GRID]


class Soldier2(arcade.Sprite):
    """ `banjo.Soldier2` is the class that represents the Soldier 2 NPC
    character in the game. It is a subclass of `arcade.Sprite` and has
    additional functionality to handle walking, running, melee attacks,
    shooting, grenade throwing, taking damage, and dying.

    Soldier 2 is the tactical mid-range soldier NPC in the game. They
    are equipped with a 5.56mm FAMAS F1 with a 25 round magazine. They
    are trained to take cover and shoot from a distance. They will keep
    their distance from Banjo and shoot at him from a distance. Due to
    crouching and aiming down sights, they are more accurate than the
    other NPCs.

    Notes
    -----
    Lt. Riley is a seasoned soldier who has been in the field for a
    while. He's a calm and collected soldier who knows how to handle
    himself in a firefight. He's a bit of a perfectionist and likes to
    take his time to line up his shots.

    Lt. Riley has 30 health points and deals 10 damage with each round
    he hits Banjo with. He rocks a 5.56mm FAMAS F1 with a 25 round magazine.
    He only carries a smoke grenade which he can throw at Banjo to obscure
    his vision.

    Lt. Riley is part of TF141 and is a member of the Bravo Team.
    Due to how cold and calculated he is, he is also known as "Ghost".

    Attributes
    ----------
    `texture_dict` : dict
        A dictionary containing the texture grids for each animation
        state of the soldier.
    `is_run` : bool
        A boolean representing whether the soldier is running or not.
    `hp` : int
        The health points of the soldier.
    `attack` : int
        The damage dealt by the soldier's weapon.
    `magazine` : int
        The maximum number of rounds in the soldier's magazine.
    `current_mag` : int
        The current number of rounds in the soldier's magazine.
    `accuracy` : float
        The accuracy of the soldier's weapon.
    `range` : int
        The range of the soldier's weapon.
    `texture` : arcade.Texture
        The current texture of the soldier.
    `character_face_direction` : int
        The direction the soldier is facing. 0 for right, 1 for left.
    `current_animation` : str
        The current animation state of the soldier.
    `current_texture_index` : int
        The index of the current texture in the animation state.
    `time_since_last_frame` : float
        The time since the last frame was updated.
    `animation_fps` : dict
        A dictionary containing the frames per second for each
        animation state of the soldier.

    Usage
    -----
    >>> soldier_2 = Soldier2()
    """
    def __init__(self) -> None:
        """ Initialize the Soldier 2 NPC.
        """
        super().__init__(scale=1.5)

        self.texture_dict = {
            "idle": IDLE_TEXTURES,
            "walk": WALK_TEXTURES,
            "run": RUN_TEXTURES,
            "melee": MELEE_TEXTURES,
            "aim_fire": AIM_FIRE_TEXTURES,
            "crouch_fire": CROUCHED_FIRE_TEXTURES,
            "reload": RELOAD_TEXTURES,
            "hurt": HURT_TEXTURES,
            "death": DEATH_TEXTURES
        }

        self.is_run = False
        self.hp = HEALTH_POINTS
        self.attack = FAMAS_DAMAGE
        self.magazine = FAMAS_MAG
        self.current_mag = FAMAS_MAG
        self.accuracy = ACCURACY
        self.range = VISION_RANGE

        self.texture = self.texture_dict["walk"][0][0]
        self.character_face_direction = RIGHT_FACING
        self.current_animation = "idle"
        self.current_texture_index = 0

        # FPS control variables
        self.time_since_last_frame = 0.0
        self.animation_fps = {
            "idle": 1/6,
            "walk": 1/8,
            "run": 1/12,
            "turn": 1/2,
            "melee": 1/6,
            "hip_fire": 1/16,
            "aim_fire": 1/16,
            "crouch_fire": 1/16,
            "reload": 1/3,
            "hurt": 1/4,
            "death": 1/2
        }

    def idle(self) -> None:
        """ Play the idle animation.

        Usage
        -----
        >>> soldier_1.idle()
        """
        current_texture = self.texture_dict[self.current_animation]

        if self.current_texture_index > len(current_texture) - 1:
            self.current_texture_index = 0

        self.texture = current_texture[self.current_texture_index][self.character_face_direction]
        self.current_texture_index += 1

    def walk(self) -> None:
        """ Play the walking animation.

        Usage
        -----
        >>> soldier_1.walk()
        """
        current_texture = self.texture_dict[self.current_animation]

        if self.current_texture_index > len(current_texture) - 1:
            self.current_texture_index = 0

        self.texture = current_texture[self.current_texture_index][self.character_face_direction]
        self.current_texture_index += 1

    def run(self) -> None:
        """ Play the running animation.

        Usage
        -----
        >>> soldier_1.run()
        """
        current_texture = self.texture_dict[self.current_animation]

        if self.current_texture_index > len(current_texture) - 1:
            self.current_texture_index = 0

        self.texture = current_texture[self.current_texture_index][self.character_face_direction]
        self.current_texture_index += 1

    def turn(self) -> None:
        """ Play the turning animation.

        Parameters
        ----------
        `direction` : int
            The direction the player is turning. 0 for right, 1 for left.

        Usage
        -----
        >>> player.turn(0)
        """
        self.character_face_direction = abs(self.character_face_direction - 1)
        self.texture = IDLE_TEXTURES[0][self.character_face_direction]

    def melee(self) -> None:
        """ Play the melee attack animation.

        Usage
        -----
        >>> soldier_1.melee()
        """
        current_texture = self.texture_dict[self.current_animation]

        if self.current_texture_index > len(current_texture) - 1:
            self.current_texture_index = 0

        self.texture = current_texture[self.current_texture_index][self.character_face_direction]
        self.current_texture_index += 1

    def aim_fire(self) -> None:
        """ Play the aim fire shooting animation.

        Usage
        -----
        >>> soldier_1.aim_fire()
        """
        current_texture = self.texture_dict[self.current_animation]

        if self.current_texture_index > len(current_texture) - 1:
            self.current_mag -= 1
            if self.current_mag == 0:
                self.reload()
                return
            self.current_texture_index = 0

        self.texture = current_texture[self.current_texture_index][self.character_face_direction]

        if self.current_texture_index == 2:
            arcade.play_sound(SHOOTING_SOUND)
        if self.current_texture_index == 4:
            arcade.play_sound(SHELL_SOUND)
        if self.current_texture_index == 5:
            arcade.play_sound(SHELL_SOUND, volume=0.8)

        self.current_texture_index += 1

    def crouch_fire(self) -> None:
        """ Play the crouched fire shooting animation.

        Usage
        -----
        >>> soldier_1.crouch_fire()
        """
        current_texture = self.texture_dict[self.current_animation]

        if self.current_texture_index > len(current_texture) - 1:
            self.current_mag -= 1
            if self.current_mag == 0:
                self.reload()
                return
            self.current_texture_index = 0

        self.texture = current_texture[self.current_texture_index][self.character_face_direction]

        if self.current_texture_index == 2:
            arcade.play_sound(SHOOTING_SOUND)
        if self.current_texture_index == 4:
            arcade.play_sound(SHELL_SOUND)
        if self.current_texture_index == 5:
            arcade.play_sound(SHELL_SOUND, volume=0.8)

        self.current_texture_index += 1

    def reload(self) -> None:
        """ Reload the magazine.

        Usage
        -----
        >>> soldier_1.reload()
        """
        current_texture = self.texture_dict[self.current_animation]

        if self.current_texture_index > len(current_texture) - 1:
            self.current_mag = self.magazine
            return

        self.texture = current_texture[self.current_texture_index][self.character_face_direction]
        self.current_texture_index += 1

    def hurt(self) -> None:
        """ Play the hurt animation.

        Usage
        -----
        >>> soldier_1.hurt()
        """
        current_texture = self.texture_dict[self.current_animation]

        if self.current_texture_index > len(current_texture) - 1:
            self.current_texture_index = 0

        self.texture = current_texture[self.current_texture_index][self.character_face_direction]
        self.current_texture_index += 1

    def death(self) -> None:
        """ Play the death animation.

        Usage
        -----
        >>> soldier_1.death()
        """
        current_texture = self.texture_dict[self.current_animation]

        self.hp = 0

        if self.current_texture_index > len(current_texture) - 1:
            return

        self.texture = current_texture[self.current_texture_index][self.character_face_direction]
        self.current_texture_index += 1

    def update_animation(
            self,
            delta_time: float=1/60,
            *args,
            **kwargs
        ) -> None:

        if self.hp == 0:
            return

        self.time_since_last_frame += delta_time

        if self.time_since_last_frame >= self.animation_fps[self.current_animation]:
            getattr(self, self.current_animation)()
            self.time_since_last_frame = 0