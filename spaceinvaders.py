import pygame, sys, os
#os.environ['SDL_AUDIODRIVER'] = 'pulse ' # possible fix to underrun
class Shield(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('images/shield.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.mask = pygame.mask.from_surface(self.image)

class Invader(pygame.sprite.Sprite):
    def __init__(self, path, points):
        super().__init__()
        self.image1 = pygame.image.load(path).convert_alpha()
        self.image2 = pygame.image.load(path[:-5]+'2'+path[-4:]).convert_alpha()
        self.blank = pygame.image.load('images/blank.png')
        self.rect = None
        self.points = points

        self.images = [self.image1, self.image2]
        self.image = self.images[1]

        self.state = 1
        self.mask = pygame.mask.from_surface(self.image)

        self.ani_num = 0
        self.ref = None

    def update(self, speed):
        if self.state == 0:
             self.image = self.blank
        else:
            self.rect.x += speed
            self.ani_state()

        hit_list = pygame.sprite.spritecollide(self, shield_group, False)
        for hit in hit_list:
            result = pygame.sprite.collide_mask(hit, self)
            if result:
                hit_array = pygame.surfarray.array2d(hit.image)
                hit_array[result[0], result[1]:result[1]+8] = 0
                hit.image = pygame.surfarray.make_surface(hit_array)
                hit.image.set_colorkey((0,0,0))
                hit.mask = pygame.mask.from_surface(hit.image)

    def ani_state(self):
        if self.ani_num == 0:
            self.ani_num = 1
        else:
            self.ani_num = 0
        self.image = self.images[self.ani_num]

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        path2 = 'images/player_explode1.png'
        self.image = pygame.image.load('images/cannon.png').convert_alpha()
        self.explosion = [pygame.image.load(path2[:-5]+str(i)+path2[-4:]) for i in range(1,3)]
        self.rect = self.image.get_rect(x=18,y=216)
        self.shooting = False
        self.shot_count = 0
        self.alive = True
        self.lives = 3

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= 1
        if keys[pygame.K_d]:
            self.rect.x += 1

        if self.rect.x <= 18:
            self.rect.x = 18
        if self.rect.x >= 190:
            self.rect.x = 190

        if pygame.sprite.spritecollide(self, alien_shot_group, True):
            self.alive = False
            self.lives -= 1

    def shoot(self):
        self.shooting = True
        self.shot_count += 1
        if self.shot_count == 16:
            self.shot_count = 0
        return PlayerShot(self.rect.midtop)

class PlayerShot(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('images/player_shot.png').convert_alpha()
        self.rect = self.image.get_rect(midtop = pos)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        # Player Shot hitting 'top'
        if self.rect.y < 40:
            self.kill()
            player.shooting = False
            explode_group.add(Explosion('top', self.rect.midtop ))
        else: self.rect.y -= 4

        # Player Shot hitting shield
        hit_list = pygame.sprite.spritecollide(self, shield_group, False)
        for hit in hit_list:
            result = pygame.sprite.collide_mask(hit, self)
            if result:
                explode_group.add(Explosion('shield', self.rect.midtop, hit, result ))
                self.kill()
                player.shooting = False

        # Player Shot hitting Alien
        hit_list = pygame.sprite.spritecollide(self, alien_group, False)
        for hit in hit_list:
            result = pygame.sprite.collide_mask(hit, self)
            if result:
                explode_group.add(Explosion('alien', hit.rect.topleft, hit, result ))
                score.score += hit.points
                hit.state = 0
                hit.mask = pygame.mask.from_surface(hit.blank)
                hit.image = hit.blank
                alien_blowup.play()
                self.kill()
                player.shooting = False

class Explosion(pygame.sprite.Sprite):
    def __init__(self, type, pos, hit = None, result = None ):
        super().__init__()
        self.explode_timer = 0
        # Player shot explodes at top
        if type == 'top' or type == 'shield':
            self.image = pygame.image.load('images/player_shot_explode.png').convert_alpha()
            self.rect = self.image.get_rect(midtop = pos)
            if type == 'shield':
                explo_array = pygame.surfarray.array2d(self.image)
                shot_mask = explo_array != 0
                hit_array = pygame.surfarray.array2d(hit.image)
                hit_array[result[0]-3:result[0]+5, result[1] - self.rect.h + 6 :result[1] + 6 ][shot_mask] = 0
                hit.image = pygame.surfarray.make_surface(hit_array)
                hit.image.set_colorkey((0,0,0))
                hit.mask = pygame.mask.from_surface(hit.image)
                self.rect.x += 1
                self.rect.y -= 2

        # Alien shot explodes at bottom
        if type == 'bottom' or type == 'ashield' or type == 'xshot':
            self.image = pygame.image.load('images/alien_shot_explode.png').convert_alpha()
            self.rect = self.image.get_rect(midbottom = pos)
            if type == 'ashield':
                explo_array = pygame.surfarray.array2d(self.image)
                shot_mask = explo_array != 0
                hit_array = pygame.surfarray.array2d(hit.image)
                hit_array[result[0]-2:result[0]+4, result[1] - 2 :result[1] + self.rect.h - 2][shot_mask] = 0
                hit.image = pygame.surfarray.make_surface(hit_array)
                hit.image.set_colorkey((0,0,0))
                hit.mask = pygame.mask.from_surface(hit.image)
                self.rect.x += 1
                self.rect.y += 2

        # PLayer shot explodes alien/invader
        if type == 'alien':
            self.image = pygame.image.load('images/alien_explode.png')
            self.rect = self.image.get_rect(topleft = pos)

        # Player shot hits UFO
        if type == 'ufo':
            self.image = pygame.image.load('images/ufo_explode.png').convert_alpha()
            self.rect = self.image.get_rect(midtop = pos)

    def update(self):
        if self.explode_timer < 16:
            self.explode_timer += 1
        if self.explode_timer == 16:
            self.kill()

class InvaderShots(pygame.sprite.Sprite):
    def __init__(self, path):
        super().__init__()
        self.images = [pygame.image.load(path[:-5]+str(i)+path[-4:]).convert_alpha() for i in range(1,5)]
        self.rect = self.images[0].get_rect()
        self.masks = [pygame.mask.from_surface(self.images[i]) for i in range(len(self.images))]
        self.image = self.images[0]
        self.mask = self.masks[0]
        self.ani_num = 0
        self.start_time = 0
        self.ufo_ok = True

    def ani_state(self):
        self.ani_num = 0 if self.ani_num == len(self.images)-1 else self.ani_num + 1
        self.image = self.images[self.ani_num]
        self.mask = self.masks[self.ani_num]

    def fire(self, col, ufo = True):
        self.rect.center = alien_group.sprites()[col].rect.midbottom
        self.start_time = pygame.time.get_ticks()
        self.ufo_ok = ufo

    def update(self, speed):
        # Hit bottom
        if self.rect.y >= 231:
            self.kill()
            explode_group.add(Explosion('bottom', self.rect.midbottom ))
        elif pygame.time.get_ticks() - self.start_time > 1000/60 * 3:
            self.rect.y += speed
            self.start_time = pygame.time.get_ticks()
            self.ani_state()

        # Alien Shot hitting shield
        hit_list = pygame.sprite.spritecollide(self, shield_group, False)
        for hit in hit_list:
            result = pygame.sprite.collide_mask(hit, self)
            if result:
                explode_group.add(Explosion('ashield', self.rect.midbottom, hit, result ))
                self.kill()

        hit_list = pygame.sprite.spritecollide(self, player_shot_group, False)
        for hit in hit_list:
            explode_group.add(Explosion('xshot', self.rect.midbottom ))
            hit.kill()
            self.kill()
            player.shooting = False

class UFO(pygame.sprite.Sprite):
    # Animation, timer to check, point, values, direction
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/ufo.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.point_table = [100, 50, 50, 100, 150, 100, 100, 50, 300, 100, 100, 100, 50, 150, 100]
        self.ufo_ok = False
        self.speed = 1

    def update(self, speed):
        self.rect.x += self.speed

        if self.rect.x > 224 or self.rect.x < 0 :
            self.ufo_ok = True
            self.kill()

        hit_list = pygame.sprite.spritecollide(self, player_shot_group, False)
        for hit in hit_list:
            explode_group.add(Explosion('ufo', self.rect.midtop))
            score.score += self.point_table[player.shot_count]
            ufo_blowup.play()
            hit.kill()
            self.kill()
            player.shooting = False

    def fire(self):
        self.rect.y = 39
        if player.shot_count % 2 == 0:
            self.rect.x = 5
            self.speed = 1
        if player.shot_count % 2 != 0:
            self.rect.x = 219
            self.speed = -1
        #print('ufo fire')

class ShotHandler():
    def __init__(self):
        self.speed = 4
        self.aliens_alive = 55
        self.reload_rates = [48*3,16*3,11*3,8*3,7*3]
        self.ok_to_fire = False

        self.plunger_table = [1,7,1,1,1,4,11,1,6,3,1,1,11,9,2,8]
        self.p_pointer = 0

        self.squigly_table = [11,1,6,3,1,1,11,9,2,8,2,11,4,7,10]
        self.s_pointer = 0

        self.type_time = 0
        self.shot1_time = 0
        self.shot2_time = 0
        self.shot3_time = 0
        self.ufo_time = 0
        self.ufo_ok = False

    def fire_ufo(self):
        shot = UFO()
        shot.fire()
        alien_shot_group.add(shot)
        self.ufo_ok = False
        self.ufo_time = 0
        ufo_sound.play()

    def fire_plunger(self):
            path = 'images/plunger1.png'
            shot = InvaderShots(path)
            col = self.plunger_table[self.p_pointer]-1
            # check if alive
            while True:
                if alien_group.sprites()[col].state == 0:
                    col += 11
                    if col > 54:
                        self.p_pointer = 0 if self.p_pointer == len(self.plunger_table)-1 else self.p_pointer + 1
                        col = self.plunger_table[self.p_pointer] - 1
                        return
                else: break
            shot.fire(col)
            self.p_pointer = 0 if self.p_pointer == len(self.plunger_table)-1 else self.p_pointer + 1
            alien_shot_group.add(shot)
            self.shot1_time = 0
            self.ok_to_fire = False

    def fire_squigly(self):
        path = 'images/squigly1.png'
        shot = InvaderShots(path)
        col = self.squigly_table[self.s_pointer]-1
        # check if alive
        while True:
            if alien_group.sprites()[col].state == 0:
                col += 11
                if col > 54:
                    self.s_pointer = 0 if self.s_pointer == len(self.squigly_table)-1 else self.s_pointer + 1
                    col = self.squigly_table[self.s_pointer]-1
                    return
            else: break
        shot.fire(col, ufo = False)
        self.s_pointer = 0 if self.s_pointer == len(self.squigly_table)-1 else self.s_pointer + 1
        alien_shot_group.add(shot)
        self.shot2_time = 0
        self.ok_to_fire = False

    def fire_rolling(self): # to fix bug, use other chot code to get the row
        path = 'images/rolling1.png'
        shot = InvaderShots(path)
        for col, alien in enumerate(alien_group.sprites()): # Bug: if it gets past row of alive aliens, will shot form next row
            if alien.state == 1 and alien.rect.left < player.rect.center[0] and alien.rect.right > player.rect.center[0]:
                shot.fire(col)
                alien_shot_group.add(shot)
                self.shot3_time = 0
                self.ok_to_fire = False
                break

    def check_reload(self):
        if score.score >= 3000:
            reload_index = 4
        if score.score < 3000:
            reload_index = 3
        if score.score < 2000:
            reload_index = 2
        if score.score < 1000:
            reload_index = 1
        if score.score < 200:
            reload_index = 0

        if min(self.shot1_time, self.shot2_time, self.shot3_time) > self.reload_rates[reload_index]:
            self.ok_to_fire = True
        else: self.ok_to_fire = False

        self.aliens_alive = sum([x.state for x in alien_group.sprites()])

        self.ufo_time += 1
        if self.ufo_time >= 600:
            count = 0
            for shot in alien_shot_group.sprites():
                count += shot.ufo_ok
            if count == len(alien_shot_group.sprites()):
                self.ufo_ok = True

    def update(self):
        self.check_reload()

        if self.aliens_alive <= 8:
            self.speed = 5
        else: self.speed = 4

        if self.type_time == 0 and self.ok_to_fire and self.aliens_alive > 1:
            self.fire_rolling()

        if self.type_time == 1 and self.ok_to_fire:
            self.fire_plunger()

        if self.type_time == 2 and self.ok_to_fire:
            if self.ufo_ok and self.aliens_alive > 8:
                self.fire_ufo()
            else: self.fire_squigly()

        self.shot1_time += 1
        self.shot2_time += 1
        self.shot3_time += 1
        self.type_time = 0 if self.type_time == 2 else self.type_time + 1

class ScoreStash():
    def __init__(self):
        self.scores_text = pygame.image.load('images/scores_text.png')
        self.scores_text_rect = self.scores_text.get_rect(topleft = (9,8))
        self.credit = pygame.image.load('images/credit2.png')
        self.c_rect = self.credit.get_rect(topleft = (137,240))

        with open('hiscore.txt') as f:
            self.hiscore = f.read()
        self.hiscore = int(self.hiscore)

        nums = os.listdir( os.getcwd()+'/images/numbers_text/')
        self.num_list = [pygame.image.load('images/numbers_text/' + x) for x in nums]
        self.score = 0
        self.extra_life = 0

    def update(self):
        if self.score >= 1500 and self.extra_life == 0:
            extra_life.play()
            self.extra_life = 1
            player.lives += 1

        if self.score > self.hiscore:
            self.hiscore = self.score

        self.lives_text = player.lives
        self.score_to_text = list(f'{self.score:0>4}')
        self.hiscore_to_text = list(f'{self.hiscore:0>4}')

        self.make_score()

    def make_score(self):
        digits = [self.num_list[int(x)] for x in self.score_to_text]
        score_board = pygame.Surface((32,8))
        for i, digit in enumerate(digits):
            score_board.blit(digit, (0+8*i,0,8,8))

        digits2 = [self.num_list[int(x)] for x in self.hiscore_to_text]
        hiscore_board = pygame.Surface((32,8))
        for i, digit in enumerate(digits2):
            hiscore_board.blit(digit, (0+8*i,0,8,8))

        self.draw(score_board, hiscore_board)

    def draw(self,score, hiscore):
        for i in range(player.lives-1):
            screen.blit(player.image, (27+i*16,240,8,13))
        screen.blit(self.num_list[self.lives_text], (9,240,8,8))
        screen.blit(self.scores_text, self.scores_text_rect)
        screen.blit(self.credit, self.c_rect)
        screen.blit(score, (25,24,8,32))
        screen.blit(hiscore, (89,24,8,32))

class GameManager():
    # should have all these variables and objexts set internally to work..
    def __init__(self):
        self.state = 0
        self.gameover = pygame.image.load('images/game_over.png').convert_alpha()
        self.go_rect = self.gameover.get_rect(topleft= (73,48))
        self.intro_run = True

    def intro(self):
        alpha = 5
        run = True
        while self.intro_run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.intro_run = False

            screen.fill((0,0,0))

            if alpha < 255:
                alpha += 1
            else: alpha = 255

            intro_image.set_alpha(alpha)
            screen.blit(intro_image, intro_rect)
            if alpha == 255:
                screen.blit(press_to_play, press_rect)

            DSURF.blit(pygame.transform.scale(screen,(224*3,256*3) ), (0,0))
            pygame.display.update()
            clock.tick(60)
        return

    def reset(self):
        self.state = 0
        score.__init__()
        player.__init__()

        player_shot_group.empty()
        alien_shot_group.empty()
        shot_hanlder.__init__()

        aliens = make_invaders(self.state)
        alien_group.empty()
        for alien in aliens:
            alien_group.add(alien)

        shield_group.empty()
        for i in [29,74,118,164]:
            shield_group.add(Shield((i,187)))

    def check_state(self):
        if not player.alive:
            self.blow_up()
        for a in alien_group:
            if a.rect.bottom >= 223 and a.state == 1:
                GM.game_over()
        if shot_hanlder.aliens_alive == 0:
            self.next_rack()

    def next_rack(self):
        self.state = 1 if self.state == 8 else self.state + 1
        player.shooting = False

        player_shot_group.empty()
        alien_shot_group.empty()
        shot_hanlder.__init__()

        aliens = make_invaders(self.state)
        alien_group.empty()
        for alien in aliens:
            alien_group.add(alien)

        shield_group.empty()
        for i in [29,74,118,164]:
            shield_group.add(Shield((i,187)))

        alien_group.draw(screen)
        shield_group.draw(screen)

        DSURF.blit(pygame.transform.scale(screen,(224*3,256*3) ), (0,0))
        pygame.display.update()
        pygame.time.delay(2000)
        pygame.event.pump()

    def blow_up(self):
        player_blowup.play()
        blow_up_list = [0,1,0,1,0,1,0,1,0,1,0,1,0,1]
        player.shooting = False
        for shot in player_shot_group.sprites():
            shot.kill()
        for shot in alien_shot_group.sprites(): # Fix UFO
            shot.kill()
        while not player.alive:
            for i in blow_up_list:
                screen.fill((0,0,0))
                pygame.draw.line(screen, (32,255,32), (3,239), (219, 239))
                score.update()

                shield_group.draw(screen)
                alien_group.draw(screen)
                screen.blit(player.explosion[i], player.rect)

                DSURF.blit(pygame.transform.scale(screen,(224*3,256*3) ), (0,0))
                pygame.display.update()
                clock.tick(10)
            # add blit blank player and update player stash, reomve reset all shots
            if player.lives == 0:
                self.game_over()
            pygame.time.delay(2000)
            player.alive = True
            player.rect.y = 216
            player.rect.x = 18

    def game_over(self):
        self.intro_run = True
        with open('hiscore.txt') as f:
            self.hiscore = f.read()
        if score.score > int(self.hiscore):
            with open('hiscore.txt','w') as f:
                f.write(str(score.score))
        cycle = 0
        while cycle < 300:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill((0,0,0))
            pygame.draw.line(screen, (32,255,32), (3,239), (219, 239))
            score.update()

            shield_group.draw(screen)
            alien_group.draw(screen)
            screen.blit(self.gameover, self.go_rect)

            DSURF.blit(pygame.transform.scale(screen,(224*3,256*3) ), (0,0))
            pygame.display.update()
            cycle += 1
            clock.tick(60)

        self.reset()

def make_invaders(state = 0):
    r = [120, 144, 160, 168, 168, 168, 176, 176, 176 ]
    aliens = []
    invader_parms = [ ['images/octo_1.png', 10], ['images/octo_1.png', 10],
                      ['images/crab_1.png', 20], ['images/crab_1.png', 20],
                      ['images/squid_1.png', 30] ]

    for parms in invader_parms:
        for x in range(11):
            aliens.append(Invader(parms[0], parms[1]))

    aliens_rects = [pygame.Rect((24+16*x, r[state]-16*y, 16, 16)) for y in range(5) for x in range(11)]

    for i in range(55):
        aliens[i].rect = aliens_rects[i]
        aliens[i].ref = i

    return aliens

# Game variables / Objects
pygame.mixer.pre_init(buffer=512)
pygame.mixer.init()
pygame.init()
DSURF = pygame.display.set_mode((224*3,256*3))
screen = pygame.Surface((224,256))
clock = pygame.time.Clock()

icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('Space Invaders')
# Intro images
intro_image = pygame.image.load('images/si_logo.png').convert()
intro_rect = intro_image.get_rect()
press_to_play = pygame.image.load('images/press_to_play.png').convert()
press_rect = press_to_play.get_rect(topleft = (36,180))

# Sounds
player_fire = pygame.mixer.Sound('sounds/1.wav')
player_blowup = pygame.mixer.Sound('sounds/2.wav')
extra_life = pygame.mixer.Sound('sounds/9.wav')
alien_blowup = pygame.mixer.Sound('sounds/3.wav')
ufo_sound = pygame.mixer.Sound('sounds/8.wav')
ufo_blowup = pygame.mixer.Sound('sounds/0.wav')
inv_sound = ['4.wav', '5.wav', '6.wav', '7.wav']
invader_move = [pygame.mixer.Sound('sounds/'+ x) for x in inv_sound]

# Sound tables
inv_table = [50, 43, 36, 28, 22, 17, 13, 10,  8,  7,  6,  5,  4, 3, 2, 1]
inv_delay_table = [52, 46, 39, 34, 28, 24, 21, 19, 16, 14, 13, 12, 11, 9, 7, 5]
inv_pointer = 0
snd_ref = 1

# Aliens
aliens = make_invaders()
alien_group = pygame.sprite.Group()
for alien in aliens:
    alien_group.add(alien)

ref = 1
max_ref = len(aliens)
speed = 2
inv_pointer = 0
snd_ref = 1
# Player
player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)

# Shots
player_shot_group = pygame.sprite.Group()
alien_shot_group = pygame.sprite.Group()
shot_hanlder = ShotHandler()
explode_group = pygame.sprite.Group()

# Shields
shield_group = pygame.sprite.Group()
for i in [29,74,118,164]:
    shield_group.add(Shield((i,187)))

#  Managers
score = ScoreStash()
GM = GameManager()

# Game Loop
while True:
    if GM.intro_run == True:
        ref = 1
        max_ref = len(aliens)
        speed = 2
        inv_pointer = 0
        snd_ref = 1
        GM.intro()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not player.shooting:
                player_fire.play()
                player_shot_group.add(player.shoot())

    for i, val in enumerate(inv_table):
        if val <= shot_hanlder.aliens_alive:
            inv_snd_delay = inv_delay_table[i]
            break

    screen.fill((0,0,0))
    pygame.draw.line(screen, (32,255,32), (3,239), (219, 239))

    score.update()
    player_group.update()

    if ref >= max_ref:
        alien_group.update(speed)
        for alien in alien_group:
            if (alien.state == 1 and alien.rect.right > 219) or (alien.state == 1 and alien.rect.left < 3):
                speed *= -1
                for a in alien_group:
                    a.rect.y += 8
                break
        ref = 1
    else: ref += 1

    if snd_ref >= inv_snd_delay:
        invader_move[inv_pointer].play()
        inv_pointer = 0 if inv_pointer == 3 else inv_pointer + 1
        snd_ref = 1
    else: snd_ref += 1

    player_shot_group.update()
    shot_hanlder.update()
    alien_shot_group.update(shot_hanlder.speed)
    explode_group.update()

    shield_group.draw(screen)
    alien_group.draw(screen)
    player_group.draw(screen)
    player_shot_group.draw(screen)
    alien_shot_group.draw(screen)
    explode_group.draw(screen)

    if shot_hanlder.aliens_alive == 0:
        ref = 1
        speed = 2

    GM.check_state()
    max_ref = sum([x.state for x in alien_group.sprites()])

    DSURF.blit(pygame.transform.scale(screen,(224*3,256*3) ), (0,0))
    pygame.display.update()
    clock.tick(60)
