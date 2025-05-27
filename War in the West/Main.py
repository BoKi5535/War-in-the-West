###########################
# Pygames Project
# War In The West
# by Yannik
###########################

#####################################################################
# Hey There, Use Headphones for the best experience!
# This is a game where you have to shoot the enemies and dodge their attacks.
# You can move left and right, jump, duck, and shoot.
# The game has a time limit of 3 minutes, and you have to survive until the end.
# And has a story mode, where you can learn more about the game.
# And a title screen, where you can start the game or view the story.
#####################################################################

# Importing things
import pygame as py
from random import randint

# Initialising
py.init()
py.mixer.init()
win_size = (800,600)                                
screen = py.display.set_mode(win_size)              
py.display.set_caption("War in the West")

# Hintergrund Bild
bg_image = py.image.load("backrounds/titlesite.png")
title_pic = py.image.load("backrounds/title.png")
start_pic = py.image.load("backrounds/Start.png")
title_sch = py.image.load("backrounds/titlesch.png")
story_pic = py.image.load("backrounds/story.png")
end_pic = py.image.load("backrounds/end.png")
ending = py.image.load("backrounds/ending.png")

# Load sounds
background_music = py.mixer.music.load("sounds/battlefield.mp3")
jump_sound = py.mixer.Sound("sounds/jump.mp3")
rifle_sound = py.mixer.Sound("sounds/riflesound.wav")
rocket_sound = py.mixer.Sound("sounds/rocket.mp3")
start_music = py.mixer.Sound("sounds/startmusic.mp3")
battlefield = py.mixer.Sound("sounds/battlefield.mp3")
heartbeat = py.mixer.Sound("sounds/heartbeat.mp3")

# Load channels
music_channel = py.mixer.Channel(0)
sound_effect_channel = py.mixer.Channel(1)
walking_channel = py.mixer.Channel(3)
title_music_channel = py.mixer.Channel(2)  
battlefield_music_channel = py.mixer.Channel(4)

# Clock
font = py.font.Font(None, 50)
text_color = (0,0,0)
start_time = 0  
duration = 3 * 60 * 1000  

# KLASSENDEFINITIONEN #

###################
# Bullet-Klasse
###################
class Bullet(py.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = py.image.load("bullets/rifle.bullet.png")
        self.mask = py.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = soldier.rect.x + 150
        self.rect.y = soldier.rect.y + 40
        self.speed = -80 * direction
        self.shoot_sound = py.mixer.Sound("sounds/riflesound.wav")
        self.has_played = False
        self.channel = py.mixer.find_channel()
        if self.channel:
            self.channel.play(self.shoot_sound)
            self.has_played = True

    def update(self):
        self.rect.x -= self.speed
        if not self.has_played:
            self.shoot_sound.play()
            self.has_played = True
        if self.rect.x > win_size[0] or self.rect.right < 0:
            self.kill()

################
# Rocket-Klasse
################
class Rocket(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = py.image.load("bullets/tank.bullet.png")
        self.mask = py.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = tank.rect.x
        self.rect.y = tank.rect.y+25
        self.speed = 12
        self.rocketsound = py.mixer.Sound("sounds/rocket.mp3")

    def reset_position(self):
        self.rect.x = tank.rect.x
        self.rect.y = tank.rect.y+25

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.x -= self.speed
        if self.rect.x == 300:
            self.rocketsound.play()
        if self.rect.x < 50:
            self.rocketsound.stop()
        if self.rect.x < -150:
            self.rect.x = tank.rect.x

#################
# Bomb-Klasse
##################
class Bomb(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = py.image.load("bullets/bomb.png")
        self.mask = py.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = jet.rect.x
        self.rect.y = jet.rect.y+100
        self.speed = -10

    def reset_position(self):
        self.rect.x = randint(0,350)
        self.rect.y = -100

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y > 450:
            self.reset_position()

##################
# Tank-Klasse
##################
class Tank(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = py.image.load("Tank/Tank2.png")
        self.mask = py.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = 800
        self.rect.y = 340
        self.speed = 4

    def reset_position(self):
        self.rect.x = 800
        self.rect.y = 340

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.x -= self.speed

#################
# Jet-Klasse
#################
class Jet(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = py.image.load("Plane/jet.png")
        self.rect = self.image.get_rect()
        self.rect.x = 600
        self.rect.y = -60
        self.speed = 10

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < -500:
            self.rect.x = randint(900,1100)

####################
# Floor-Klasse
###################
class Floor(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = py.image.load("elements/Floor.png")
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 500

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

######################
# Story-Klasse
######################
class Story(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = py.image.load("backrounds/story.png")
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 500

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

#############################
# Soldier-Klasse (vollständig)
##############################
class Soldier(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animation = [py.image.load(f"SRW/soldierwalkrifle{i}.png") for i in range(5)]
        self.image = self.animation[0]
        self.mask = py.mask.from_surface(self.image)
        self.flipped_image = py.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x = 25
        self.rect.y = 350
        self.costume = 0
        self.speed = 12
        self.not_moving = True
        self.jump = False
        self.starth = -40
        self.floor = 350
        self.dy = 10
        self.height = self.starth
        self.jumpsound = py.mixer.Sound("sounds/jump.mp3")
        self.battlefield_music = py.mixer.Sound("sounds/battlefield.mp3")
        self.aim = 0
        self.is_shooting = False
        self.shoot_animation_done = True
        self.animation2 = [py.image.load(f"SCS/aim{i}.png") for i in range(4)]
        self.last_aim_change_time = 0
        self.aim_change_cooldown = 50
        self.alarm = False
        self.music = py.mixer.Sound("sounds/soldier_walk.wav")
        self.sound_playing = False
        self.last_shot_time = 0
        self.shoot_cooldown = 500  
        self.duck = False
        self.collision_animation = [py.image.load(f"death/death{i}.png") for i in range(9)]
        self.collision_costume = 0
        self.in_collision = False
        self.collided = False
        self.deathspeed = 60

    def refresh(self):
        global end
        if not self.in_collision:
            if not self.not_moving and not self.duck:
                self.costume = (self.costume + 1) % len(self.animation)
                self.image = self.animation[self.costume]
            elif self.alarm:
                current_time = py.time.get_ticks()
                if current_time - self.last_aim_change_time > self.aim_change_cooldown:
                    if self.aim < len(self.animation2) - 1:
                        self.aim += 1
                        self.image = self.animation2[self.aim]
                        self.last_aim_change_time = current_time
                    else:
                        self.alarm = False
                        self.shoot_animation_done = True
                        self.is_shooting = False
                        self.last_shot_time = current_time
            
            else:
                self.sound_playing = False
                py.mixer.Sound.stop(self.music)
        else:
            self.collision_costume = (self.collision_costume + 1) % len(self.collision_animation)
            self.image = self.collision_animation[self.collision_costume]
            self.rect.y += 10  
            if self.collision_costume == 0:
                end = True

    def draw(self, direction):
        if direction == 1:
            screen.blit(self.image, (self.rect.x, self.rect.y))
        else:
            self.flipped_image = py.transform.flip(self.image, True, False)
            screen.blit(self.flipped_image, (self.rect.x, self.rect.y))

    def update(self):
        if not self.in_collision:
            if self.jump:
                self.height += self.dy
                self.rect.y += self.height
                if self.rect.y >= self.floor:
                    self.rect.y = self.floor
                    self.jump = False
            if self.duck:
                self.rect.y = 400
                self.image = py.image.load("duck/duck.png")
            if not py.key.get_pressed()[py.K_DOWN]:
                self.duck = False
                if self.jump:
                    self.rect.y += self.height
                else:
                    self.rect.y = 350


def key_handler():


    if soldier.alarm:
        current_time = py.time.get_ticks()
        if current_time - soldier.last_aim_change_time > soldier.aim_change_cooldown:
            soldier.last_aim_change_time = current_time
            if soldier.aim < len(soldier.animation2) - 1:
                soldier.aim += 1
                soldier.image = soldier.animation2[soldier.aim]
            else:
                soldier.alarm = False
                soldier.shoot_animation_done = True
                soldier.is_shooting = False
                soldier.last_shot_time = py.time.get_ticks()
    global direction
    key = py.key.get_pressed()

    if key[py.K_LEFT]:
        direction = -1
        if not soldier.sound_playing and not soldier.duck:
            walking_channel.play(soldier.music, loops=-1)
            soldier.sound_playing = True
        if soldier.rect.x > 10:
            soldier.rect.x -= soldier.speed
            soldier.not_moving = False
            if not soldier.sound_playing and not soldier.duck:
                walking_channel.play(soldier.music, loops=-1)
                soldier.sound_playing = True

    elif key[py.K_RIGHT]:
        direction = 1
        if not soldier.sound_playing and not soldier.duck:
            walking_channel.play(soldier.music, loops=-1)
            soldier.sound_playing = True
        if soldier.rect.x < win_size[0] - soldier.rect.width - 10:
            soldier.rect.x += soldier.speed
        soldier.not_moving = False

    elif key[py.K_UP]:
        if not soldier.jump:
            soldier.jump = True
            soldier.height = soldier.starth
            py.mixer.Sound.play(soldier.jumpsound)

    elif key[py.K_DOWN]:
        soldier.duck = True
        walking_channel.stop()

    elif key[py.K_SPACE]:
        current_time = py.time.get_ticks()
        if current_time - soldier.last_shot_time > soldier.shoot_cooldown and soldier.shoot_animation_done:
            soldier.not_moving = True
            soldier.alarm = True
            soldier.shoot_animation_done = False
            soldier.is_shooting = True
            soldier.aim = 0
            soldier.last_aim_change_time = current_time
            bullet = Bullet(soldier.rect.x + 25, soldier.rect.y)
            bullets.add(bullet)
            soldier.last_shot_time = current_time

    else:
        soldier.not_moving = True
        soldier.alarm = soldier.alarm 
        soldier.sound_playing = False
        py.mixer.Sound.stop(soldier.music)

def check_collision_BT():
    global tank_lives
    for bullet in bullets:
        offset = (bullet.rect.x - tank.rect.x), (bullet.rect.y - tank.rect.y)
        if tank.mask.overlap(bullet.mask, offset):
            bullets.remove(bullet)
            tank_lives -= 1
            if tank_lives == 0:
                tank.rect.x = randint(800, 900)
                tank_lives = 2

def check_collision_SR():
    offset =  (rocket.rect.x - soldier.rect.x), (rocket.rect.y - soldier.rect.y)
    if soldier.mask.overlap(rocket.mask,offset):
        if soldier.collision_costume == 8:
            soldier.rect.y += soldier.deathspeed
            soldier.rect.x = 10000
            rocket.rect.x = 10000
            global end
            end = True

def check_collision_BS():
    offset =  (bomb.rect.x - soldier.rect.x), (bomb.rect.y - soldier.rect.y)
    if soldier.mask.overlap(bomb.mask,offset):
        soldier.rect.x = 10000
        bomb.rect.x = 10000
        global end
        end = True

# Globale Variabeln:
title_shown = False
show_story = False
game_is_running = True
direction = 1
soldier = Soldier()
shoot_animation_length = len(soldier.animation2) * soldier.aim_change_cooldown
clock = py.time.Clock()
floor = Floor()
bullets = py.sprite.Group()
tank = Tank()
rocket = Rocket()
story = Story()
jet = Jet()
bomb = Bomb()
explosions = py.sprite.Group()
end = False
tank_lives = 2

##############
# Hauptschleife:
last_animation_tick = 0
##############

while game_is_running:
    key = py.key.get_pressed()
    for event in py.event.get():                    
        if event.type == py.QUIT:                   
            game_is_running = False

        elif event.type == py.KEYDOWN:
            if event.key == py.K_RETURN:
                if not title_shown:
                    title_shown = True
                    start_time = py.time.get_ticks()
                    title_music_channel.stop()
                    if not battlefield_music_channel.get_busy():
                        battlefield_music_channel.play(battlefield)
                elif show_story:
                    show_story = False

            elif event.key == py.K_SPACE:
                pass  

        mods = py.key.get_mods()
        if mods & py.KMOD_RSHIFT and not title_shown:
            show_story = True

        if soldier.collision_costume == 8:
            end = True

    if title_shown == False:
        if not title_music_channel.get_busy():
            title_music_channel.play(start_music) 
        screen.blit(title_pic, (0, 0))
        screen.blit(start_pic, (150, 50))
        screen.blit(title_sch, (150, -184))

    if title_shown == True:
        if not battlefield_music_channel.get_busy():
            battlefield_music_channel.play(battlefield)

    if show_story == True:
        screen.blit(story_pic, (0, 0))
        py.display.update()
        continue

    if py.sprite.collide_rect(soldier, rocket):
        soldier.in_collision = True

    if end == True:
        py.mixer.stop()
        heartbeat.play()
        screen.blit(end_pic, (0, 0))
        py.display.update()

        while True:
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    exit()
            clock.tick(10)

    if title_shown == True:
        screen.blit(bg_image, (0, 0))
        title_music_channel.stop()

    key_handler()

    if title_shown == True:
        floor.draw()

    if title_shown == True:
        bullets.update()
        bullets.draw(screen)

    check_collision_BT()

    if title_shown == True:
        bomb.update()
        bomb.draw()

        rocket.update()
        rocket.draw()

        check_collision_SR()

        soldier.draw(direction)
        soldier.refresh()
        soldier.update()

        check_collision_BS()

        explosions.update()
        explosions.draw(screen)

        tank.update()
        tank.draw()

        jet.update()
        jet.draw()

        elapsed_time = py.time.get_ticks() - start_time
        remaining_time = max(duration - elapsed_time, 0)
        minutes = remaining_time // 60000
        seconds = (remaining_time % 60000) // 1000
        time_str = f"{minutes:02}:{seconds:02}"

        text_surface = font.render(time_str, True, text_color)
        text_rect = text_surface.get_rect(topleft = (10, 10))
        screen.blit(text_surface, text_rect)

        if remaining_time == 0:
            screen.blit(ending,(0,0))
            game_is_running = False


    py.display.update()
    clock.tick(10)


py.quit()

# hope you enjoyed the game! :)
