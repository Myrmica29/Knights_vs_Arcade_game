import pygame
import random
import sys

from buttons import EditButton, ConfigButton
from fog import Fog
from monsters import Monster
from player import Player


class Game:

    def __init__(self):

        # importer l'icon du jeu
        icon = pygame.image.load('ressources/helmet_black.png')

        # Screen
        self.screen = pygame.display.set_mode((1080, 720), pygame.FULLSCREEN)
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Joystick Game !")

        # Game over
        self.game_over_image = pygame.image.load('ressources/game_over.png')
        pos = (self.screen.get_width()/2, self.screen.get_height()/2)
        self.game_over_rect = self.game_over_image.get_rect(center=pos)

        # Press to start text
        self.press_text_image = pygame.image.load('ressources/press_to_start.png')
        pos = (self.screen.get_width() / 2, self.screen.get_height() / 2 + 30)
        self.press_text_rect = self.press_text_image.get_rect(center=pos)

        # Knight helmet
        self.knight_helmet_image = pygame.image.load('ressources/helmet_gray.png')
        pos = (self.screen.get_width() / 2, self.screen.get_height() / 2 - 180)
        self.knight_helmet_rect = self.knight_helmet_image.get_rect(center=pos)

        # Selector
        self.selector_image = pygame.image.load("ressources/selector.png")
        self.selector_rect = self.selector_image.get_rect()

        # Text
        self.font = pygame.font.Font('ressources/Pacifico-Regular.ttf', 32)
        self.font_2 = pygame.font.Font('ressources/Pacifico-Regular.ttf', 20)

        # Background
        self.background_color = (1, 85, 25)

        # Players
        self.players = []
        self.player_group = pygame.sprite.Group()
        self.edit_controls_buttons = []

        # Monsters
        self.monsters_group = pygame.sprite.Group()
        self.monsters = []

        # fog
        self.fog_group = pygame.sprite.Group()
        self.fogs = []

        # Controls
        self.controls_joysticks = []
        self.config_list = [
            "up",
            "down",
            "right",
            "left",
            "execute"
        ]

        # Joysticks
        self.joysticks = []
        self.init_joysticks()

        # Time
        self.time = 0

        # Score
        self.previous_score = 0
        self.best_score = 0
        with open("text_files/score.txt", encoding='utf-8') as file:
            lines = file.readlines()[0]
            scores = lines.split(",")
            self.previous_score = int(scores[0])
            self.best_score = int(scores[1])
            file.close()

        # Music
        # self.background_music = pygame.mixer.Sound(
        #     "ressources/music/the-game-is-on-outrun-retro-electro-synthwave-mix.mp3")

    def init_joysticks(self):
        # clear variables
        self.joysticks.clear()
        self.players.clear()
        self.player_group.empty()
        self.edit_controls_buttons.clear()
        # create joysticks and players for all joysticks connected
        for i in range(pygame.joystick.get_count()):

            # init joysticks
            self.joysticks.append(pygame.joystick.Joystick(i))
            self.joysticks[i].init()

            # create players and their buttons for controls configuration
            self.players.append(Player(i+1, self.player_group))
            self.edit_controls_buttons.append(EditButton(i+1, pygame.joystick.get_count(), self.screen))

        self.load_controls()

    def run(self):

        clock = pygame.time.Clock()

        # Game loop
        running = True

        while running:

            # Update joystick number
            if pygame.joystick.get_count() != len(self.joysticks):
                self.init_joysticks()

            # background
            self.screen.fill(self.background_color)

            self.screen.blit(self.knight_helmet_image, self.knight_helmet_rect)
            self.screen.blit(self.press_text_image, self.press_text_rect)

            # Configuration text
            text_render = self.font.render("Config buttons :", True, (165, 159, 223))
            x = 15
            y = self.screen.get_height() - 175  # Text height = 57
            self.screen.blit(text_render, (x, y))

            for b in self.edit_controls_buttons:
                if b.check_collide(pygame.mouse.get_pos()):
                    self.selector_rect = self.selector_image.get_rect(center=b.pos)
                    self.screen.blit(self.selector_image, self.selector_rect)
                self.screen.blit(b.image, b.rect)

            # Score
            text_render = self.font_2.render("Previous score : " + str(self.previous_score), True, (165, 159, 223))
            x = self.screen.get_width() / 2 - (text_render.get_width() / 2) - 200
            y = self.screen.get_height() - 80
            self.screen.blit(text_render, (x, y))

            x = self.screen.get_width() / 2 - (text_render.get_width() / 2) + 200
            text_render = self.font_2.render("Best score : " + str(self.best_score), True, (165, 159, 223))
            self.screen.blit(text_render, (x, y))

            # Update screen
            pygame.display.flip()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

                if event.type == pygame.JOYBUTTONUP and event.button == 1:
                    self.play()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for b in self.edit_controls_buttons:
                        if b.check_collide(pygame.mouse.get_pos()):
                            self.edit_menu(self.players[b.number - 1])

            # Clock
            clock.tick(60)

    def save_controls(self, data_controls):
        # Save in the text folder
        # print("Input data_controls", data_controls)

        file_name = "text_files/controls.txt"
        with open(file_name, "w+", encoding='utf-8') as file:
            text = ""
            for player in data_controls:
                # text = ""
                for control in player:
                    for info in control:
                        text += str(info)
                        text += "!"
                    text = text[:-1]
                    text += "?"
                text = text[:-1]
                text += "\n"
            text = text[:-1]
            file.write(text)

            file.close()

    def load_controls(self):
        # load all controls in the system from the text folder

        self.controls_joysticks.clear()
        for i in range(len(self.joysticks)):

            # Create controls check system
            self.controls_joysticks.append({})
            # JOYBUTTONUP
            self.controls_joysticks[i]["JOYBUTTONUP"] = {}
            for j in range(self.joysticks[i].get_numbuttons()):
                self.controls_joysticks[i]["JOYBUTTONUP"][j] = None
            # JOYHATMOTION
            self.controls_joysticks[i]["JOYHATMOTION"] = {}
            numbers = [-1, 0, 1]
            for n1 in numbers:
                for n2 in numbers:
                    self.controls_joysticks[i]["JOYHATMOTION"][(n1, n2)] = None

        # Open file
        data_controls = []
        with open("text_files/controls.txt", encoding='utf-8') as file:
            # For every lines which are for every player
            for line in file:
                a = line.split("?")
                list_ = []
                # for every duos of controls
                for i in a:
                    el = i.split("!")
                    # remove \n
                    z = el[2].replace("\n", "")
                    el[2] = z
                    list_.append(el)
                data_controls.append(list_)
            file.close()

        # load
        # for player in range(len(data_controls)):
        for player in range(len(self.joysticks)):
            for config in range(len(self.config_list)):
                action = self.config_list[config]
                typ = data_controls[player][config][0]
                value = "fail"
                if typ == "JOYBUTTONUP":
                    value = int(data_controls[player][config][1])
                elif typ == "JOYHATMOTION":
                    value = eval(data_controls[player][config][1])
                joy = data_controls[player][config][2]
                # print("typ: "+typ, ", value: "+str(value), ", joy: "+joy, ", action: "+action)
                self.controls_joysticks[int(joy)][typ][value] = [player, action]

        # print("controls_joysticks", self.controls_joysticks)

    def edit_menu(self, player):
        # print(f"Edit Menu for player {player.number}")

        config_list = [
            "Go up :",
            "Go down :",
            "Go right :",
            "Go left :",
            "Execute :"
        ]

        data_controls = []
        buttons = []

        # Open file
        with open("text_files/controls.txt", encoding='utf-8') as file:
            # For every lines which are for every player
            for line in file:
                a = line.split("?")
                list_ = []
                # for every duos of controls
                for i in a:
                    el = i.split("!")
                    # remove \n
                    z = el[2].replace("\n", "")
                    el[2] = z
                    list_.append(el)
                data_controls.append(list_)
            file.close()

        # Buttons to change 1 control
        for control in data_controls[player.number - 1]:
            y = 140 + 85 * data_controls[player.number - 1].index(control)
            buttons.append(
                ConfigButton(self.config_list[data_controls[player.number - 1].index(control)],
                             control[0], control[1], control[2], (400, y)))

        clock = pygame.time.Clock()

        # Game loop
        running = True

        while running:

            # background
            self.screen.fill(self.background_color)

            # Text : Player x configuration
            text_render = self.font.render(f"Player {player.number} configuration", True, (165, 159, 223))
            x = self.screen.get_width() / 2 - (text_render.get_width() / 2)
            y = 30
            self.screen.blit(text_render, (x, y))

            y = 140
            for c in config_list:
                text_render = self.font.render(c, True, (165, 159, 223))
                x = 200
                self.screen.blit(text_render, (x, y))
                y += 85
            for b in buttons:
                self.screen.blit(b.image, b.rect)

            # Update screen
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.save_controls(data_controls)
                    self.load_controls()
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for b in buttons:
                        if b.check_collide(pygame.mouse.get_pos()):
                            b.update_image(fill=True)
                            self.screen.blit(b.image, b.rect)
                            self.edit_a_buttton(player, b, data_controls)

            # Clock
            clock.tick(60)

    def edit_a_buttton(self, player, button, data_controls):

        running = True

        while running:
            for event in pygame.event.get():

                # Update screen
                pygame.display.flip()

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    button.update_image()
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    button.update_image()
                    running = False

                if event.type == pygame.JOYHATMOTION:
                    data_controls[player.number - 1][self.config_list.index(button.name)] = [
                        "JOYHATMOTION", event.value, event.joy]
                    button.typ = "JOYHATMOTION"
                    button.value = event.value
                    button.joy = event.joy
                    button.update_image()
                    running = False

                elif event.type == pygame.JOYBUTTONUP:
                    data_controls[player.number - 1][self.config_list.index(button.name)] = [
                        "JOYBUTTONUP", event.button, event.joy]
                    button.typ = "JOYBUTTONUP"
                    button.value = event.button
                    button.joy = event.joy
                    button.update_image()
                    running = False

    def spawn_monster(self):
        min_ = round(100/len(self.joysticks))
        minus = round(self.time/3*len(self.joysticks))
        if 100 - minus > min_:
            v = 100 - minus
        else:
            v = min_
        minus2 = 0
        if self.time > 240:
            minus2 = round((self.time - 240)/16*len(self.joysticks))
            if minus2 > 50 - (50/len(self.joysticks)):
                minus2 = round(50 - (50/len(self.joysticks)))
        if random.randint(0, v - minus2) == 0:
            self.monsters.append(Monster(self.screen, self.time, self.monsters_group))

    def spawn_fog(self):
        if self.time > 420:  # 360
            if self.time - 420 < 400:
                v = 800 - (self.time - 420)
            else:
                v = 400
            if random.randint(0, v) == 0:
                self.fogs.append(Fog(self.screen, self.time, self.fog_group))

    def play(self):

        clock = pygame.time.Clock()
        t = 0

        # Reset
        self.monsters_group.empty()
        self.monsters = []
        self.fog_group.empty()
        self.fogs = []
        self.time = 0

        # Music
        # self.background_music.play()

        # Game loop
        running = True

        while running:

            # Time
            t += 1
            if t == 60:
                t = 0
                self.time += 1
                # print(self.time)

            # background
            self.screen.fill(self.background_color)

            # Players
            self.player_group.update(self.screen)
            self.player_group.draw(self.screen)

            # Monsters
            self.spawn_monster()
            self.monsters_group.update(self.player_group)
            self.monsters_group.draw(self.screen)

            # Fog
            self.spawn_fog()
            self.fog_group.update()
            self.fog_group.draw(self.screen)

            # Score
            text_render = self.font_2.render("Score : " + str(self.time), True, (80, 0, 0))
            self.screen.blit(text_render, (self.screen.get_width() / 2 - (text_render.get_width() / 2), 5))

            # Check end
            for m in self.monsters:
                if m.check_end():

                    # End music
                    # self.background_music.fadeout(1000)

                    # Game over image
                    self.screen.blit(self.game_over_image, self.game_over_rect)

                    # Score text
                    text_render = self.font.render("Score : " + str(self.time), True, (80, 0, 0))
                    x = self.screen.get_width() / 2 - (text_render.get_width() / 2)
                    y = self.screen.get_height() - 200
                    self.screen.blit(text_render, (x, y))

                    # Score storage
                    self.previous_score = self.time
                    if self.previous_score > self.best_score:
                        self.best_score = self.previous_score

                    # Stop
                    pygame.display.flip()
                    pygame.time.wait(1000*8)
                    running = False

            # Update screen
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

                if event.type == pygame.JOYHATMOTION:
                    # if event.value == (0, 1):
                    #     self.players[event.joy].move_up()
                    # if event.value == (1, 0):
                    #     self.players[event.joy].move_right()
                    # if event.value == (0, -1):
                    #     self.players[event.joy].move_down()
                    # if event.value == (-1, 0):
                    #     self.players[event.joy].move_left()

                    control = self.controls_joysticks[event.joy]["JOYHATMOTION"][event.value]
                    if control is not None:
                        if control[1] == "up":
                            self.players[control[0]].move_up()
                        elif control[1] == "down":
                            self.players[control[0]].move_down()
                        elif control[1] == "right":
                            self.players[control[0]].move_right()
                        elif control[1] == "left":
                            self.players[control[0]].move_left()

                if event.type == pygame.JOYBUTTONUP:
                    control = self.controls_joysticks[event.joy]["JOYBUTTONUP"][event.button]
                    if control is not None:
                        if control[1] == "up":
                            self.players[control[0]].move_up()
                        elif control[1] == "down":
                            self.players[control[0]].move_down()
                        elif control[1] == "right":
                            self.players[control[0]].move_right()
                        elif control[1] == "left":
                            self.players[control[0]].move_left()

            # Clock
            clock.tick(60)
