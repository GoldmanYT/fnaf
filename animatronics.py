from functions import seconds_to_frames
from consts import *
from random import randint, choice, random


class Animatronic:
    def __init__(self, ai_level, office):
        self.ai_level = ai_level
        self.ways = {}
        self.increase_hours = []
        self.pos = CAM_1A
        self.tick = 0
        self.frequency = 1
        self.office = office
        self.attacking = False
        self.previous_hour = 0

    def attack(self):
        self.attacking = True

    def update(self):
        self.tick += 1
        if self.tick // seconds_to_frames(self.frequency):
            self.tick %= seconds_to_frames(self.frequency)
            self.move()
        if self.pos == OFFICE:
            self.attack()
        if self.previous_hour != self.office.hour:
            self.previous_hour = self.office.hour
            if self.office.hour in self.increase_hours:
                self.ai_level += 1

    def move(self):
        x = randint(1, 20)
        if self.ai_level >= x:
            ways = self.ways.get(self.pos).copy()
            if OFFICE in ways:
                if self.pos == LEFT_DOOR and self.office.left_door or \
                        self.pos in (RIGHT_DOOR, CAM_4B) and self.office.right_door:
                    ways.remove(OFFICE)
                else:
                    ways = [OFFICE]
            self.pos = choice(ways)

    def set_ai_level(self, ai_level):
        self.ai_level = ai_level

    def raise_ai_level(self):
        self.ai_level += 1


class Bonnie(Animatronic):
    def __init__(self, ai_level, office):
        super().__init__(ai_level, office)
        self.frequency = 4.97
        self.ways = {
            CAM_1A: [CAM_1B],
            CAM_1B: [CAM_5, CAM_2A],
            CAM_2A: [CAM_3, CAM_2B],
            CAM_2B: [CAM_3, LEFT_DOOR],
            CAM_3: [CAM_2A, CAM_2B, LEFT_DOOR],
            CAM_5: [CAM_2A],
            LEFT_DOOR: [CAM_1B, OFFICE]
        }
        self.increase_hours = [2, 3, 4]


class Chica(Animatronic):
    def __init__(self, ai_level, office):
        super().__init__(ai_level, office)
        self.frequency = 4.98
        self.ways = {
            CAM_1A: [CAM_1B],
            CAM_1B: [CAM_7],
            CAM_7: [CAM_6],
            CAM_6: [CAM_4A],
            CAM_4A: [CAM_4B],
            CAM_4B: [RIGHT_DOOR],
            RIGHT_DOOR: [CAM_1B, OFFICE]
        }
        self.increase_hours = [3, 4]


class Freddy(Animatronic):
    def __init__(self, ai_level, office):
        super().__init__(ai_level, office)
        self.frequency = 3.02
        self.counter = -1
        self.ways = {
            CAM_1A: [CAM_1B],
            CAM_1B: [CAM_7],
            CAM_7: [CAM_6],
            CAM_6: [CAM_4A],
            CAM_4A: [CAM_4B],
            CAM_4B: [CAM_4A, OFFICE]
        }

    def update(self):
        self.tick += 1
        if self.counter != -1:
            self.counter -= 1
        if self.counter == 0:
            ways = self.ways.get(self.pos).copy()
            if OFFICE in ways:
                if self.pos == CAM_4B and self.office.right_door:
                    ways.remove(OFFICE)
                else:
                    ways = [OFFICE]
            self.pos = choice(ways)
        if self.pos == OFFICE:
            self.attack()

    def move(self):
        x = randint(1, 20)
        if self.ai_level >= x and self.office.opened_camera != self.pos:
            self.counter = max(0, 1000 - self.ai_level * 100)


class Foxy(Animatronic):
    def __init__(self, ai_level, office):
        super().__init__(ai_level, office)
        self.frequency = 5.01
        self.stage = 0
        self.blocked = False
        self.unblocking_in = 0
        self.attacking_in = seconds_to_frames(25)
        self.increase_hours = [3, 4]

    def update(self):
        self.tick += 1
        if self.stage == 3:
            self.attacking_in -= 1
            if self.office.opened_camera == CAM_2A:
                self.attacking_in = 0
            if self.attacking_in <= 0:
                self.pos = LEFT_DOOR
        if self.blocked:
            self.unblocking_in -= 1
            self.tick = 0
        else:
            super().update()
        if self.office.opened_camera is not None:
            self.blocked = True
            self.unblocking_in = seconds_to_frames(random() * (16.67 - 0.83) + 0.83)
        if self.pos == LEFT_DOOR:
            if self.office.left_door:
                self.pos = CAM_1C
                self.stage = choice((0, 1))
            else:
                self.attack()

    def move(self):
        x = randint(1, 20)
        if self.ai_level >= x and not self.blocked:
            self.stage += 1


class Office:
    def __init__(self):
        self.left_door = False
        self.right_door = False
        self.opened_camera = None
        self.last_camera = CAM_1A
        self.hour = 0

    def toggle_left_door(self):
        self.left_door = not self.left_door

    def toggle_right_door(self):
        self.right_door = not self.right_door

    def open_cameras(self):
        self.opened_camera = self.last_camera

    def close_cameras(self):
        self.opened_camera = None

    def change_camera(self, camera):
        self.last_camera = camera
        self.opened_camera = camera
