from sys import exit
from random import randint
from math import sin, pi

import pygame as pg
from functions import seconds_to_frames
from consts import *
from animatronics import Bonnie, Chica, Freddy, Foxy, Office

pg.mixer.pre_init()
pg.init()

perspective_surface = pg.Surface((W, H))
hs = [(0, 0)] * W
for x in range(W):
    k = 0.5 * (1 - sin(x * pi / (W - 1))) + 1
    h = H / k
    hs[x] = (H - h) / 2, h


def redraw_as_perspective(surface, screen):
    for x in range(W):
        y0, h = hs[x]
        stripe = surface.subsurface(x, y0, 1, h)
        stripe_dst = screen.subsurface(x, 0, 1, H)
        pg.transform.scale(stripe, (1, H), stripe_dst)


class Sprite:
    def __init__(self, image_path=None, pos=(0, 0), width=None, height=None, visible=True, speed=0):
        if image_path is None:
            self.image = pg.Surface((width, height))
        else:
            self.image = pg.image.load(image_path).convert_alpha()
        self.pos = pos
        self.w = width
        if width is None:
            self.w = self.image.get_width()
        self.h = self.image.get_height()

        self.alpha_tick = 0
        self.alpha = 255

        self.frame = 0
        self.n_frames = self.image.get_width() // self.w
        self.tick = 0

        self.visible = visible
        self.loop = True
        self.speed = speed
        self.animate = True

    def draw(self, surface):
        if self.visible:
            display_image = self.image.subsurface(self.w * self.frame, 0, self.w, self.h)
            display_image.set_alpha(self.alpha, pg.SRCALPHA)
            surface.blit(display_image, self.pos)

    def update(self):
        self.tick += 1
        self.alpha_tick += 1
        if self.n_frames == 1:
            return
        if self.tick * self.speed // 100:
            self.tick = self.tick % (self.speed / 100)
            if self.animate:
                self.frame += 1
            if self.loop:
                self.frame %= self.n_frames
            elif self.frame >= self.n_frames:
                self.visible = False


class Game:
    def __init__(self):
        self.w, self.h = W, H
        self.frame = WAIT
        self.tick = 1  # заменить на 0
        self.start_frame = True
        self.selected_item = 1
        self.previous_item = 1

        self.beat_game = 3
        self.last_night = 1
        self.night = self.last_night
        self.office = Office()

        self.load_sounds()

        self.screen = pg.display.set_mode((W, H))
        self.clock = pg.time.Clock()

        self.load_data()

        self.__run__ = True
        self.main()

    def main(self):
        while self.__run__:
            pressed_keys = []
            mouse_pressed = False
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.__run__ = False
                    else:
                        pressed_keys.append(event.key)
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pressed = True

            self.draw()
            self.update(pressed_keys, mouse_pressed)
            self.clock.tick(FPS)
            # pg.display.set_caption(f'fps: {self.clock.get_fps():.0f}')
        pg.quit()

    def load_sounds(self):
        # channels
        self.channel1 = pg.mixer.Channel(0)
        self.channel2 = pg.mixer.Channel(1)
        self.channel3 = pg.mixer.Channel(2)

        # sounds
        self.ambience2 = pg.mixer.Sound('data/sounds/ambience2.wav')
        self.ballast_hummedium2 = pg.mixer.Sound('data/sounds/Ballast HumMedium2.wav')
        self.blip3 = pg.mixer.Sound('data/sounds/blip3.wav')
        self.buzz_fan_florescent_2 = pg.mixer.Sound('data/sounds/Buzz_Fan_Florescent 2.wav')
        self.camera_video_load = pg.mixer.Sound('data/sounds/CAMERA_VIDEO_LOAD.wav')
        self.chimes_2 = pg.mixer.Sound('data/sounds/chimes 2.wav')
        self.circus = pg.mixer.Sound('data/sounds/circus.wav')
        self.coldpresc_b = pg.mixer.Sound('data/sounds/ColdPresc B.wav')
        self.computer_digital = pg.mixer.Sound('data/sounds/COMPUTER_DIGITAL.wav')
        self.crowd_small_children = pg.mixer.Sound('data/sounds/CROWD_SMALL_CHILDREN.wav')
        self.darkness_music = pg.mixer.Sound('data/sounds/darkness music.wav')
        self.deep_steps = pg.mixer.Sound('data/sounds/deep steps.wav')
        self.door_pounding_message = pg.mixer.Sound('data/sounds/DOOR_POUNDING_MESSAGE.wav')
        self.eerieambiencelargescary = pg.mixer.Sound('data/sounds/EerieAmbienceLargeScary.wav')
        self.error = pg.mixer.Sound('data/sounds/error.wav')
        self.garble1 = pg.mixer.Sound('data/sounds/garble1.wav')
        self.garble2 = pg.mixer.Sound('data/sounds/garble2.wav')
        self.garble3 = pg.mixer.Sound('data/sounds/garble3.wav')
        self.knock2 = pg.mixer.Sound('data/sounds/knock2.wav')
        self.laugh_giggle_girl_1 = pg.mixer.Sound('data/sounds/Laugh_Giggle_Girl_1.wav')
        self.laugh_giggle_girl_1d = pg.mixer.Sound('data/sounds/Laugh_Giggle_Girl_1d.wav')
        self.laugh_giggle_girl_2d = pg.mixer.Sound('data/sounds/Laugh_Giggle_Girl_2d.wav')
        self.laugh_giggle_girl_8d = pg.mixer.Sound('data/sounds/Laugh_Giggle_Girl_8d.wav')
        self.minidv_tape_eject_1 = pg.mixer.Sound('data/sounds/MiniDV_Tape_Eject_1.wav')
        self.music_box = pg.mixer.Sound('data/sounds/music box.wav')
        self.oven_1 = pg.mixer.Sound('data/sounds/OVEN_1.wav')
        self.oven_2 = pg.mixer.Sound('data/sounds/OVEN_2.wav')
        self.oven_3 = pg.mixer.Sound('data/sounds/OVEN_3.wav')
        self.oven_4 = pg.mixer.Sound('data/sounds/OVEN_4.wav')
        self.partyfavorraspypart = pg.mixer.Sound('data/sounds/PartyFavorraspyPart.wav')
        self.pirate_song2 = pg.mixer.Sound('data/sounds/pirate song2.wav')
        self.powerdown = pg.mixer.Sound('data/sounds/powerdown.wav')
        self.put_down = pg.mixer.Sound('data/sounds/put down.wav')
        self.robotvoice = pg.mixer.Sound('data/sounds/robotvoice.wav')
        self.run = pg.mixer.Sound('data/sounds/run.wav')
        self.sfxbible = pg.mixer.Sound('data/sounds/SFXBible.wav')
        self.static = pg.mixer.Sound('data/sounds/static.wav')
        self.static2 = pg.mixer.Sound('data/sounds/static2.wav')
        self.voiceover1 = pg.mixer.Sound('data/sounds/voiceover1.wav')
        self.voiceover2 = pg.mixer.Sound('data/sounds/voiceover2.wav')
        self.voiceover3 = pg.mixer.Sound('data/sounds/voiceover3.wav')
        self.voiceover4 = pg.mixer.Sound('data/sounds/voiceover4.wav')
        self.voiceover5 = pg.mixer.Sound('data/sounds/voiceover5.wav')
        self.windowscare = pg.mixer.Sound('data/sounds/windowscare.wav')
        self.xscream = pg.mixer.Sound('data/sounds/XSCREAM.wav')
        self.xscream2 = pg.mixer.Sound('data/sounds/XSCREAM2.wav')

    def load_data(self):
        if self.frame == FRAME_17:
            self.warning = Sprite('data/textures/warning.png', WARNING_POS)

        elif self.frame == TITLE:
            class WhiteStripe(Sprite):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.alpha = 255 - 200
                    self.image.fill(WHITE)

                def update(self):
                    super().update()
                    x, y = self.pos
                    if y == H:
                        self.pos = WHITE_STRIPE_POS
                    else:
                        self.pos = x, y + 1

            self.white_stripe = WhiteStripe(pos=WHITE_STRIPE_POS, width=1280, height=32)

            class TitleWhiteStripes(Sprite):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.speed = 10
                    self.visible_tick = 0

                def update(self):
                    super().update()
                    self.visible_tick += 1
                    if self.alpha_tick // seconds_to_frames(0.08):
                        self.alpha_tick %= seconds_to_frames(0.08)
                        self.alpha = 255 - (randint(0, 100) + 100)
                    if self.visible_tick // seconds_to_frames(0.3):
                        self.visible_tick %= seconds_to_frames(0.3)
                        n = randint(0, 3)
                        if n % 2:
                            self.visible = True
                        else:
                            self.visible = False

            self.title_white_stripes = TitleWhiteStripes('data/textures/title_white_stripes.png', WHITE_STRIPES_POS,
                                                         1280)

            class TitleFreddy(Sprite):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.animate = False
                    self.speed = 0

                def update(self):
                    super().update()
                    if self.tick // seconds_to_frames(0.08):
                        self.tick %= seconds_to_frames(0.08)
                        n = randint(0, 100)
                        if n == 0:
                            self.frame = 1
                        elif n == 1:
                            self.frame = 2
                        elif n == 2:
                            self.frame = 3
                        else:
                            self.frame = 0
                    if self.alpha_tick // seconds_to_frames(0.3):
                        self.alpha_tick %= seconds_to_frames(0.3)
                        self.alpha = 255 - randint(0, 250)

            self.title_freddy = TitleFreddy('data/textures/title_freddy.png', TITLE_FREDDY_POS, 1280)

            class Noise(Sprite):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.speed = 99

                def update(self):
                    super().update()
                    if self.alpha_tick // seconds_to_frames(0.09):
                        self.alpha_tick %= seconds_to_frames(0.09)
                        self.alpha = 255 - (50 + randint(0, 100))

            self.noise = Noise('data/textures/noise.png', NOISE_POS, 1280)
            self.title = Sprite('data/textures/title.png', TITLE_POS)
            self.star1 = Sprite('data/textures/star.png', STAR1_POS)
            self.star2 = Sprite('data/textures/star.png', STAR2_POS)
            self.star3 = Sprite('data/textures/star.png', STAR3_POS)

            class Pointer(Sprite):
                def update(self, selected_item=0):
                    x, y = POINTER_POS
                    self.pos = x, y + selected_item * POINTER_DH

            self.pointer = Pointer('data/textures/pointer.png', POINTER_POS)

            class Button(Sprite):
                def update(self, mouse_pos=(0, 0)):
                    super().update()
                    x, y = mouse_pos
                    x1, y1 = self.pos
                    x2, y2 = x1 + self.w, y1 + self.h

                    if x1 <= x <= x2 and y1 <= y <= y2:
                        return True
                    return False

            self.new_game = Button('data/textures/new_game.png', NEW_GAME_POS)
            self.continue_ = Button('data/textures/continue.png', CONTINUE_POS)
            self.title_night = Sprite('data/textures/night.png', TITLE_NIGHT_POS)
            self.night_counter = Sprite('data/textures/night_counter.png', NIGHT_COUNTER_POS, 14)
            self.night_6 = Button('data/textures/6th night.png', NIGHT_6_POS)
            self.custom_night = Button('data/textures/custom_night.png', CUSTOM_NIGHT_POS)
            self.version = Sprite('data/textures/version.png', VERSION_POS)
            self.scott = Sprite('data/textures/scott.png', SCOTT_POS)

        elif self.frame == WAIT:
            self.loading = Sprite('data/textures/loading.png', LOADING_POS)

        elif self.frame == FRAME_1:
            class OfficeSprite(Sprite):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.offset = 0
                    self.speed = 0

                def draw(self, surface):
                    if self.visible:
                        surface.blit(self.image, self.pos, (self.frame * self.w + self.offset, 0, W, H))

                def update(self, mouse_pos=(0, 0)):
                    super().update()
                    x = mouse_pos[0]
                    if x >= 739:
                        self.offset += 2
                    if x >= 988:
                        self.offset += 5
                    if x >= 1046:
                        self.offset += 5
                    if x <= 519:
                        self.offset -= 2
                    if x <= 303:
                        self.offset -= 5
                    if x <= 146:
                        self.offset -= 5
                    self.offset = max(0, min(self.w - W, self.offset))

            class OfficeObject(Sprite):
                def draw(self, surface, offset=0):
                    if self.visible:
                        display_image = self.image.subsurface(self.frame * self.w, 0, self.w, self.h)
                        display_image.set_alpha(self.alpha, pg.SRCALPHA)
                        x, y = self.pos
                        surface.blit(display_image, (x - offset, y))

            self.office_sprite = OfficeSprite('data/textures/office.png', OFFICE_SPRITE_POS, 1600)
            self.fan = OfficeObject('data/textures/fan.png', FAN_POS, 138, speed=99)
            self.power_left = Sprite('data/textures/power_left.png', POWER_LEFT_POS)

            class Counter(Sprite):
                def __init__(self, image_path=None, pos=(0, 0), width=None, height=None, visible=True, speed=0,
                             init_value=0):
                    super().__init__(image_path, pos, width, height, visible, speed)
                    self.value = init_value

                def draw(self, surface):
                    if self.visible:
                        x, y = self.pos
                        for i, digit in enumerate(str(self.value)):
                            digit = int(digit)
                            display_image = self.image.subsurface(self.w * digit, 0, self.w, self.h)
                            surface.blit(display_image, (x + i * self.w, y))

            self.power_counter = Counter('data/textures/power_counter.png', POWER_COUNTER_POS, 18, init_value=100)
            self.percent = Sprite('data/textures/percent.png', PERCENT_POS)
            self.usage = Sprite('data/textures/usage.png', USAGE_POS)

            class UsageSprite(Sprite):
                def __init__(self, image_path=None, pos=(0, 0), width=None, height=None, visible=True, speed=0):
                    super().__init__(image_path, pos, width, height, visible, speed)

            self.usage_sprite = UsageSprite('data/textures/usage_sprite.png', USAGE_SPRITE_POS)

            class CameraButton(Sprite):
                def __init__(self, image_path=None, text_image_path=None, pos=(0, 0), width=None, height=None,
                             visible=True, speed=3, id=0):
                    super().__init__(image_path, pos, width, height, visible, speed)
                    self.text = pg.image.load(text_image_path).convert_alpha()
                    self.frame = 1
                    self.id = id

                def draw(self, surface):
                    x, y = self.pos
                    surface.blit(self.image, self.pos, (self.w * self.frame, 0, self.w, self.h))
                    surface.blit(self.text, (x + 8, y + 8))

                def update(self, mouse_pos=(0, 0), id=0):
                    if self.id == id:
                        super().update()
                    else:
                        self.frame = 1
                        self.tick = 0
                    x, y = mouse_pos
                    x1, y1 = self.pos
                    x2, y2 = x1 + self.w, y1 + self.h

                    if x1 <= x <= x2 and y1 <= y <= y2:
                        return True
                    return False

            self.cam_btn_1a = CameraButton('data/textures/cam_btn.png', 'data/textures/cam_1a.png', CAM_1A_POS, 60,
                                           id=CAM_1A)
            self.cam_btn_1b = CameraButton('data/textures/cam_btn.png', 'data/textures/cam_1b.png', CAM_1B_POS, 60,
                                           id=CAM_1B)
            self.cam_btn_1c = CameraButton('data/textures/cam_btn.png', 'data/textures/cam_1c.png', CAM_1C_POS, 60,
                                           id=CAM_1C)
            self.cam_btn_2a = CameraButton('data/textures/cam_btn.png', 'data/textures/cam_2a.png', CAM_2A_POS, 60,
                                           id=CAM_2A)
            self.cam_btn_2b = CameraButton('data/textures/cam_btn.png', 'data/textures/cam_2b.png', CAM_2B_POS, 60,
                                           id=CAM_2B)
            self.cam_btn_3 = CameraButton('data/textures/cam_btn.png', 'data/textures/cam_3.png', CAM_3_POS, 60,
                                           id=CAM_3)
            self.cam_btn_4a = CameraButton('data/textures/cam_btn.png', 'data/textures/cam_4a.png', CAM_4A_POS, 60,
                                           id=CAM_4A)
            self.cam_btn_4b = CameraButton('data/textures/cam_btn.png', 'data/textures/cam_4b.png', CAM_4B_POS, 60,
                                           id=CAM_4B)
            self.cam_btn_5 = CameraButton('data/textures/cam_btn.png', 'data/textures/cam_5.png', CAM_5_POS, 60,
                                           id=CAM_5)
            self.cam_btn_6 = CameraButton('data/textures/cam_btn.png', 'data/textures/cam_6.png', CAM_6_POS, 60,
                                           id=CAM_6)
            self.cam_btn_7 = CameraButton('data/textures/cam_btn.png', 'data/textures/cam_7.png', CAM_7_POS, 60,
                                           id=CAM_7)

            class Button(Sprite):
                def __init__(self, image_path=None, pos=(0, 0), width=None, height=None, visible=True, speed=0,
                             rect=None):
                    if rect is not None:
                        pos = rect[:2]
                        width = rect[2]
                        height = rect[3]
                    super().__init__(image_path, pos, width, height, visible, speed)

                def update(self, mouse_pos=(0, 0)):
                    super().update()
                    x, y = mouse_pos
                    x1, y1 = self.pos
                    x2, y2 = x1 + self.w, y1 + self.h

                    if x1 <= x <= x2 and y1 <= y <= y2:
                        return True
                    return False

            class FlipButton(Sprite):
                def __init__(self, image_path=None, pos=(0, 0), width=None, height=None, visible=True, speed=0,
                             rect=None):
                    if rect is not None:
                        pos = rect[:2]
                        width = rect[2]
                        height = rect[3]
                    super().__init__(image_path, pos, width, height, visible, speed)
                    self.touch_able = True

                def update(self, mouse_pos=(0, 0)):
                    super().update()
                    x, y = mouse_pos
                    x1, y1 = self.pos
                    x2, y2 = x1 + self.w, y1 + self.h

                    if x1 <= x <= x2 and y1 <= y <= y2 and self.touch_able:
                        self.touch_able = False
                        return True
                    return False

            self.flip_panel = Sprite('data/textures/flip_panel.png', FLIP_PANEL_POS)
            self.open_cameras = FlipButton(visible=False, rect=FLIP_UP_RECT)
            self.show_open = Button(visible=False, rect=FLIP_DOWN_RECT)

            class Cameras(Sprite):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.frame = 4
                    self.offset = 0
                    self.a = 0
                    self.b = 0

                def draw(self, surface):
                    if self.visible:
                        surface.blit(self.image, self.pos, (self.frame * self.w + self.offset, 0, W, H))

                def update(self):
                    self.b += 1
                    if self.a == 0:
                        self.offset += 1
                        if self.b >= 320:
                            self.a = 1
                            self.b = 0
                    elif self.a == 1:
                        if self.b >= 100:
                            self.a = 2
                            self.b = 0
                    elif self.a == 2:
                        self.offset -= 1
                        if self.b >= 320:
                            self.a = 3
                            self.b = 0
                    elif self.a == 3:
                        if self.b >= 100:
                            self.a = 0
                            self.b = 0

            self.cameras = Cameras('data/textures/cameras.png', CAMERAS_POS, 1600)
            self.camera_map = Sprite('data/textures/camera_map.png', CAMERA_MAP_POS, 400)

        elif self.frame == WHAT_DAY:
            class WhiteStripes(Sprite):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.speed = 75
                    self.loop = False

            self.what_day = Sprite('data/textures/what_day.png', WHAT_DAY_POS, 240)
            self.white_stripes = WhiteStripes('data/textures/white_stripes.png', WHITE_STRIPES_POS, 1280)

        elif self.frame == DIED:
            self.died_noise = Sprite('data/textures/noise.png', DIED_NOISE_POS, 1280, speed=99)

        elif self.frame == FREDDY:
            class FreddyJumpscarePowerDown(Sprite):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.speed = 60
                    self.loop = False

                def update(self):
                    super(FreddyJumpscarePowerDown, self).update()

            self.freddy_jumpscare_power_down = FreddyJumpscarePowerDown('data/textures/freddy_jumpscare_power_down.png',
                                                                        FREDDY_JUMPSCARE_POWER_DOWN_POS, 1280)
            self.freddy_noise = Sprite('data/textures/noise.png', FREDDY_NOISE_POS, 1280, speed=99)

        elif self.frame == NEXT_DAY:
            class FinalHourNumber(Sprite):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.stopped = False
                    self.init_pos = self.pos

                def update(self):
                    super().update()
                    if self.tick < 300:
                        x, y = self.init_pos
                        self.pos = x, y - self.tick * 112 / 300
                    elif self.tick == 300:
                        self.stopped = True
                    else:
                        self.stopped = False

            self.am = Sprite('data/textures/AM.png', AM_POS)
            self.five = FinalHourNumber('data/textures/5.png', FIVE_POS)
            self.six = FinalHourNumber('data/textures/6.png', SIX_POS)

        elif self.frame == GAME_OVER:
            self.game_over_backdrop = Sprite('data/textures/game_over_backdrop.png', GAME_OVER_BACKDROP_POS)
            self.game_over_backdrop2 = Sprite('data/textures/game_over_backdrop2.png', GAME_OVER_BACKDROP2_POS)

        elif self.frame == THE_END:
            self.the_end = Sprite('data/textures/the_end.png', THE_END_POS)

        elif self.frame == AD:
            self.ad = Sprite('data/textures/ad.png', AD_POS)

        elif self.frame == THE_END_2:
            self.the_end_2 = Sprite('data/textures/the_end_2.png', THE_END_2_POS)

        elif self.frame == CUSTOMIZE:
            self.customize_night = Sprite('data/textures/customize_night.png', CUSTOMIZE_NIGHT_POS)
            self.customize_freddy = Sprite('data/textures/customize_freddy.png', CUSTOMIZE_FREDDY_POS)
            self.customize_bonnie = Sprite('data/textures/customize_bonnie.png', CUSTOMIZE_BONNIE_POS)
            self.customize_chica = Sprite('data/textures/customize_chica.png', CUSTOMIZE_CHICA_POS)
            self.customize_foxy = Sprite('data/textures/customize_foxy.png', CUSTOMIZE_FOXY_POS)
            self.customize_backdrop1 = Sprite('data/textures/customize_backdrop_1.png', CUSTOMIZE_BACKDROP1_POS)
            self.customize_backdrop2 = Sprite('data/textures/customize_backdrop_2.png', CUSTOMIZE_BACKDROP2_POS)
            self.customize_backdrop3 = Sprite('data/textures/customize_backdrop_3.png', CUSTOMIZE_BACKDROP3_POS)
            self.customize_backdrop4 = Sprite('data/textures/customize_backdrop_4.png', CUSTOMIZE_BACKDROP4_POS)
            self.customize_backdrop5_1 = Sprite('data/textures/customize_backdrop_5.png', CUSTOMIZE_BACKDROP5_1_POS)
            self.customize_backdrop5_2 = Sprite('data/textures/customize_backdrop_5.png', CUSTOMIZE_BACKDROP5_2_POS)
            self.customize_backdrop5_3 = Sprite('data/textures/customize_backdrop_5.png', CUSTOMIZE_BACKDROP5_3_POS)
            self.customize_backdrop5_4 = Sprite('data/textures/customize_backdrop_5.png', CUSTOMIZE_BACKDROP5_4_POS)
            self.customize_backdrop6 = Sprite('data/textures/customize_backdrop_6.png', CUSTOMIZE_BACKDROP6_POS)

            class AICounter(Sprite):
                def __init__(self, image_path=None, pos=(0, 0), width=None, height=None, visible=True, speed=0,
                             init_value=0):
                    super().__init__(image_path, pos, width, height, visible, speed)
                    self.value = init_value

                def draw(self, surface):
                    if self.visible:
                        x, y = self.pos
                        for i, digit in enumerate(str(self.value)[::-1]):
                            digit = int(digit)
                            display_image = self.image.subsurface(self.w * digit, 0, self.w, self.h)
                            surface.blit(display_image, (x - i * self.w, y))

                def add_value(self, value):
                    self.value = max(0, min(20, self.value + value))

            class Button(Sprite):
                def update(self, mouse_pos=(0, 0)):
                    super().update()
                    x, y = mouse_pos
                    x1, y1 = self.pos
                    x2, y2 = x1 + self.w, y1 + self.h

                    if x1 <= x <= x2 and y1 <= y <= y2:
                        return True
                    return False

            self.decrease_btn1 = Button('data/textures/decrease_button.png', DECREASE_BUTTON1_POS)
            self.decrease_btn2 = Button('data/textures/decrease_button.png', DECREASE_BUTTON2_POS)
            self.decrease_btn3 = Button('data/textures/decrease_button.png', DECREASE_BUTTON3_POS)
            self.decrease_btn4 = Button('data/textures/decrease_button.png', DECREASE_BUTTON4_POS)
            self.increase_btn1 = Button('data/textures/increase_button.png', INCREASE_BUTTON1_POS)
            self.increase_btn2 = Button('data/textures/increase_button.png', INCREASE_BUTTON2_POS)
            self.increase_btn3 = Button('data/textures/increase_button.png', INCREASE_BUTTON3_POS)
            self.increase_btn4 = Button('data/textures/increase_button.png', INCREASE_BUTTON4_POS)
            self.ai_counter1 = AICounter('data/textures/ai_counter.png', AI_COUNTER1_POS, 35, init_value=1)
            self.ai_counter2 = AICounter('data/textures/ai_counter.png', AI_COUNTER2_POS, 35, init_value=3)
            self.ai_counter3 = AICounter('data/textures/ai_counter.png', AI_COUNTER3_POS, 35, init_value=3)
            self.ai_counter4 = AICounter('data/textures/ai_counter.png', AI_COUNTER4_POS, 35, init_value=1)
            self.ready = Button('data/textures/ready.png', READY_POS)

        elif self.frame == THE_END_3:
            self.the_end_3 = Sprite('data/textures/the_end_3.png', THE_END_3_POS)

        elif self.frame == CREEPY_START:
            self.creepy_start = Sprite('data/textures/creepy_start_backdrop.png', CREEPY_START_POS)
            self.eye1 = Sprite('data/textures/eye.png', EYE1_POS)
            self.eye2 = Sprite('data/textures/eye.png', EYE2_POS)

        elif self.frame == CREEPY_END:
            self.creepy_end = Sprite('data/textures/creepy_end_backdrop.png', CREEPY_END_POS)

    def draw(self):
        if self.frame == FRAME_17:
            self.warning.draw(self.screen)

        elif self.frame == TITLE:
            self.title_freddy.draw(self.screen)
            self.noise.draw(self.screen)
            self.title.draw(self.screen)
            self.star1.draw(self.screen)
            self.star2.draw(self.screen)
            self.star3.draw(self.screen)
            self.pointer.draw(self.screen)
            self.new_game.draw(self.screen)
            self.continue_.draw(self.screen)
            self.title_night.draw(self.screen)
            self.night_counter.draw(self.screen)
            self.night_6.draw(self.screen)
            self.custom_night.draw(self.screen)
            self.version.draw(self.screen)
            self.scott.draw(self.screen)
            self.white_stripe.draw(self.screen)
            self.title_white_stripes.draw(self.screen)

        elif self.frame == FRAME_1:
            if self.office.opened_camera is None:
                self.office_sprite.draw(perspective_surface)
                offset = self.office_sprite.offset
                self.fan.draw(perspective_surface, offset)
            else:
                self.cameras.draw(perspective_surface)

            redraw_as_perspective(perspective_surface, self.screen)

            if self.office.opened_camera is None:
                pass
            else:
                self.camera_map.draw(self.screen)
                self.cam_btn_1a.draw(self.screen)
                self.cam_btn_1b.draw(self.screen)
                self.cam_btn_1c.draw(self.screen)
                self.cam_btn_2a.draw(self.screen)
                self.cam_btn_2b.draw(self.screen)
                self.cam_btn_3.draw(self.screen)
                self.cam_btn_4a.draw(self.screen)
                self.cam_btn_4b.draw(self.screen)
                self.cam_btn_5.draw(self.screen)
                self.cam_btn_6.draw(self.screen)
                self.cam_btn_7.draw(self.screen)

            self.power_left.draw(self.screen)
            self.power_counter.draw(self.screen)
            self.percent.draw(self.screen)
            self.usage.draw(self.screen)
            self.flip_panel.draw(self.screen)

        elif self.frame == WHAT_DAY:
            self.screen.fill(BLACK)
            self.what_day.draw(self.screen)
            self.white_stripes.draw(self.screen)

        elif self.frame == DIED:
            self.died_noise.draw(self.screen)

        elif self.frame == FREDDY:
            self.freddy_jumpscare_power_down.draw(self.screen)
            if self.freddy_jumpscare_power_down.frame >= self.freddy_jumpscare_power_down.n_frames:
                self.freddy_noise.draw(self.screen)

        elif self.frame == NEXT_DAY:
            self.screen.fill(BLACK)
            self.am.draw(self.screen)
            self.five.draw(self.screen)
            self.six.draw(self.screen)
            pg.draw.rect(self.screen, BLACK, RECT_1)
            pg.draw.rect(self.screen, BLACK, RECT_2)

        elif self.frame == WAIT:
            self.loading.draw(self.screen)

        elif self.frame == GAME_OVER:
            self.game_over_backdrop.draw(self.screen)
            self.game_over_backdrop2.draw(self.screen)

        elif self.frame == THE_END:
            self.the_end.draw(self.screen)

        elif self.frame == AD:
            self.ad.draw(self.screen)

        elif self.frame == THE_END_2:
            self.the_end_2.draw(self.screen)

        elif self.frame == CUSTOMIZE:
            self.screen.fill(BLACK)
            self.customize_night.draw(self.screen)
            self.customize_freddy.draw(self.screen)
            self.customize_bonnie.draw(self.screen)
            self.customize_chica.draw(self.screen)
            self.customize_foxy.draw(self.screen)
            self.customize_backdrop1.draw(self.screen)
            self.customize_backdrop2.draw(self.screen)
            self.customize_backdrop3.draw(self.screen)
            self.customize_backdrop4.draw(self.screen)
            self.customize_backdrop5_1.draw(self.screen)
            self.customize_backdrop5_2.draw(self.screen)
            self.customize_backdrop5_3.draw(self.screen)
            self.customize_backdrop5_4.draw(self.screen)
            self.customize_backdrop6.draw(self.screen)
            self.decrease_btn1.draw(self.screen)
            self.decrease_btn2.draw(self.screen)
            self.decrease_btn3.draw(self.screen)
            self.decrease_btn4.draw(self.screen)
            self.increase_btn1.draw(self.screen)
            self.increase_btn2.draw(self.screen)
            self.increase_btn3.draw(self.screen)
            self.increase_btn4.draw(self.screen)
            self.ai_counter1.draw(self.screen)
            self.ai_counter2.draw(self.screen)
            self.ai_counter3.draw(self.screen)
            self.ai_counter4.draw(self.screen)
            self.ready.draw(self.screen)

        elif self.frame == THE_END_3:
            self.the_end_3.draw(self.screen)

        elif self.frame == CREEPY_START:
            self.creepy_start.draw(self.screen)
            if self.tick >= seconds_to_frames(9.5):
                self.eye1.draw(self.screen)
                self.eye2.draw(self.screen)

        elif self.frame == CREEPY_END:
            self.creepy_end.draw(self.screen)

        pg.display.flip()

    def next_frame(self):
        self.change_frame(self.frame + 1)

    def change_frame(self, frame):
        self.frame = frame
        self.tick = 0
        self.start_frame = True
        self.load_data()

    def update(self, pressed_keys, mouse_pressed):
        keys = pg.key.get_pressed()
        mouse_pos = pg.mouse.get_pos()

        if self.frame == FRAME_17:
            if self.tick >= seconds_to_frames(2) or keys[pg.K_RETURN] or pg.mouse.get_pressed()[0]:
                self.next_frame()
            self.warning.update()

        elif self.frame == TITLE:
            if self.start_frame:
                if randint(0, 1000) == 1:
                    self.change_frame(CREEPY_START)
                pg.mixer.stop()
                self.channel1.play(self.static2)
                self.channel2.play(self.darkness_music, -1)
                self.channel1.set_volume(100)
                self.channel2.set_volume(100)
                self.channel3.set_volume(100)
            for key in pressed_keys:
                if key == pg.K_UP:
                    self.selected_item = (self.selected_item - 1) % min(4, self.beat_game + 2)
                    self.channel3.play(self.blip3)
                elif key == pg.K_DOWN:
                    self.selected_item = (self.selected_item + 1) % min(4, self.beat_game + 2)
                    self.channel3.play(self.blip3)
                elif key == pg.K_RETURN:
                    if self.selected_item == 0:
                        self.change_frame(AD)
                        self.night = 1
                        self.last_night = 1
                    elif self.selected_item == 1:
                        self.change_frame(WHAT_DAY)
                        self.night = self.last_night
                    elif self.selected_item == 2:
                        self.change_frame(WHAT_DAY)
                        self.night = 6
                    elif self.selected_item == 3:
                        self.change_frame(CUSTOMIZE)
                        self.night = 7

            self.white_stripe.update()
            self.title_white_stripes.update()
            self.title_freddy.update()
            self.noise.update()
            if self.new_game.update(mouse_pos):
                self.selected_item = 0
                if self.selected_item != self.previous_item:
                    self.channel3.play(self.blip3)
                if mouse_pressed:
                    self.last_night = 1
                    self.night = 1
                    self.change_frame(AD)

            if self.continue_.update(mouse_pos):
                self.selected_item = 1
                if self.selected_item != self.previous_item:
                    self.channel3.play(self.blip3)
                if mouse_pressed:
                    self.night = self.last_night
                    self.change_frame(WHAT_DAY)

            if self.beat_game > 0:
                self.night_6.visible = True
                self.star1.visible = True
                if self.night_6.update(mouse_pos):
                    self.selected_item = 2
                    if self.selected_item != self.previous_item:
                        self.channel3.play(self.blip3)
                    if mouse_pressed:
                        self.night = 6
                        self.change_frame(WHAT_DAY)
            else:
                self.night_6.visible = False
                self.star1.visible = False

            if self.beat_game > 1:
                self.custom_night.visible = True
                self.star2.visible = True
                if self.custom_night.update(mouse_pos):
                    self.selected_item = 3
                    if self.selected_item != self.previous_item:
                        self.channel3.play(self.blip3)
                    if mouse_pressed:
                        self.night = 7
                        self.change_frame(CUSTOMIZE)
            else:
                self.custom_night.visible = False
                self.star2.visible = False

            if self.beat_game > 2:
                self.star3.visible = True
            else:
                self.star3.visible = False

            self.night_counter.frame = self.last_night - 1
            self.pointer.update(self.selected_item)
            self.previous_item = self.selected_item

        elif self.frame == WHAT_DAY:
            if self.start_frame:
                pg.mixer.stop()
                self.channel1.play(self.blip3)
            self.what_day.frame = self.night - 1
            self.white_stripes.update()
            if self.tick >= seconds_to_frames(2):
                self.change_frame(WAIT)

        elif self.frame == FRAME_1:
            if self.office.opened_camera is None:
                self.office_sprite.update(mouse_pos)
                self.fan.update()
                if self.open_cameras.update(mouse_pos):
                    self.office.open_cameras()
                    self.flip_panel.visible = False
            else:
                if self.open_cameras.update(mouse_pos):
                    self.office.close_cameras()
                    self.flip_panel.visible = False
                if self.cam_btn_1a.update(mouse_pos, self.office.opened_camera) and mouse_pressed:
                    self.cameras.frame = 4
                    self.office.change_camera(CAM_1A)
                elif self.cam_btn_1b.update(mouse_pos, self.office.opened_camera) and mouse_pressed:
                    self.cameras.frame = 1
                    self.office.change_camera(CAM_1B)
                elif self.cam_btn_1c.update(mouse_pos, self.office.opened_camera) and mouse_pressed:
                    self.cameras.frame = 11
                    self.office.change_camera(CAM_1C)
                elif self.cam_btn_2a.update(mouse_pos, self.office.opened_camera) and mouse_pressed:
                    self.cameras.frame = 3
                    self.office.change_camera(CAM_2A)
                elif self.cam_btn_2b.update(mouse_pos, self.office.opened_camera) and mouse_pressed:
                    self.cameras.frame = 5
                    self.office.change_camera(CAM_2B)
                elif self.cam_btn_3.update(mouse_pos, self.office.opened_camera) and mouse_pressed:
                    self.cameras.frame = 9
                    self.office.change_camera(CAM_3)
                elif self.cam_btn_4a.update(mouse_pos, self.office.opened_camera) and mouse_pressed:
                    self.cameras.frame = 10
                    self.office.change_camera(CAM_4A)
                elif self.cam_btn_4b.update(mouse_pos, self.office.opened_camera) and mouse_pressed:
                    self.cameras.frame = 8
                    self.office.change_camera(CAM_4B)
                elif self.cam_btn_5.update(mouse_pos, self.office.opened_camera) and mouse_pressed:
                    self.cameras.frame = 7
                    self.office.change_camera(CAM_5)
                elif self.cam_btn_6.update(mouse_pos, self.office.opened_camera) and mouse_pressed:
                    self.cameras.frame = 4
                    self.office.change_camera(CAM_6)
                elif self.cam_btn_7.update(mouse_pos, self.office.opened_camera) and mouse_pressed:
                    self.cameras.frame = 6
                    self.office.change_camera(CAM_7)
            if self.show_open.update(mouse_pos):
                self.open_cameras.touch_able = True
                self.flip_panel.visible = True
            self.cameras.update()

        elif self.frame == DIED:
            if self.start_frame:
                pg.mixer.stop()
                self.channel1.play(self.static)
                self.channel1.set_volume(100)
            self.died_noise.update()
            if self.tick >= seconds_to_frames(10):
                self.change_frame(GAME_OVER)

        elif self.frame == FREDDY:
            if self.start_frame:
                pg.mixer.stop()
                self.channel1.play(self.xscream)
                self.channel1.set_volume(100)
            if self.tick >= seconds_to_frames(12):
                self.change_frame(GAME_OVER)
            if self.freddy_jumpscare_power_down.frame == self.freddy_jumpscare_power_down.n_frames:
                pg.mixer.stop()
                self.channel1.play(self.static)
            self.freddy_jumpscare_power_down.update()
            self.freddy_noise.update()

        elif self.frame == NEXT_DAY:
            self.five.update()
            self.six.update()
            if self.start_frame:
                pg.mixer.stop()
                self.channel1.play(self.chimes_2)
                self.channel1.set_volume(100)
                self.channel2.set_volume(100)
            if self.five.stopped:
                self.channel2.play(self.crowd_small_children)
            if self.tick == seconds_to_frames(9):
                self.night += 1
                if self.night == 6:
                    self.change_frame(THE_END)
                elif self.night == 7:
                    self.change_frame(THE_END_2)
                elif self.night == 8:
                    self.change_frame(THE_END_3)
                else:
                    self.change_frame(WHAT_DAY)

        elif self.frame == WAIT:
            if self.tick >= seconds_to_frames(0.1):
                self.change_frame(FRAME_1)

        elif self.frame == GAME_OVER:
            if self.start_frame:
                pg.mixer.stop()
            if self.tick >= seconds_to_frames(10):
                n = randint(0, 10000)
                if n == 1:
                    self.change_frame(CREEPY_END)
                else:
                    self.change_frame(TITLE)

        elif self.frame == THE_END:
            if self.start_frame:
                pg.mixer.stop()
                self.channel1.play(self.music_box, -1)
                self.channel1.set_volume(100)
            if self.tick >= seconds_to_frames(15):
                self.change_frame(TITLE)

        elif self.frame == AD:
            if keys[pg.K_RETURN] or mouse_pressed or self.tick >= seconds_to_frames(5):
                self.change_frame(WHAT_DAY)

        elif self.frame == THE_END_2:
            if self.start_frame:
                pg.mixer.stop()
                self.channel1.play(self.music_box, -1)
                self.channel1.set_volume(100)
            if self.tick >= seconds_to_frames(15):
                self.change_frame(TITLE)

        elif self.frame == CUSTOMIZE:
            if self.decrease_btn1.update(mouse_pos) and mouse_pressed:
                self.ai_counter1.add_value(-1)
            if self.decrease_btn2.update(mouse_pos) and mouse_pressed:
                self.ai_counter2.add_value(-1)
            if self.decrease_btn3.update(mouse_pos) and mouse_pressed:
                self.ai_counter3.add_value(-1)
            if self.decrease_btn4.update(mouse_pos) and mouse_pressed:
                self.ai_counter4.add_value(-1)
            if self.increase_btn1.update(mouse_pos) and mouse_pressed:
                self.ai_counter1.add_value(1)
            if self.increase_btn2.update(mouse_pos) and mouse_pressed:
                self.ai_counter2.add_value(1)
            if self.increase_btn3.update(mouse_pos) and mouse_pressed:
                self.ai_counter3.add_value(1)
            if self.increase_btn4.update(mouse_pos) and mouse_pressed:
                self.ai_counter4.add_value(1)
            if self.ready.update(mouse_pos) and mouse_pressed:
                if self.ai_counter1.value == 1 and \
                        self.ai_counter2.value == 9 and \
                        self.ai_counter3.value == 8 and \
                        self.ai_counter4.value == 7:
                    self.change_frame(CREEPY_END)
                else:
                    self.change_frame(WHAT_DAY)

        elif self.frame == THE_END_3:
            if self.start_frame:
                pg.mixer.stop()
                self.channel1.play(self.music_box, -1)
                self.channel1.set_volume(100)
            if self.tick >= seconds_to_frames(15):
                self.change_frame(TITLE)

        elif self.frame == CREEPY_START:
            if self.start_frame:
                pg.mixer.stop()
            if self.tick >= seconds_to_frames(10):
                self.change_frame(TITLE)

        elif self.frame == CREEPY_END:
            if self.start_frame:
                pg.mixer.stop()
                self.channel3.play(self.xscream2)
                self.channel3.set_volume(100)
            if self.tick >= seconds_to_frames(1):
                self.__run__ = False

        if self.tick != 0:
            self.start_frame = False
        self.tick += 1


if __name__ == '__main__':
    game = Game()
