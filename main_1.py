import  pygame,os,random

from base_game import Alive, Player, Level, BasicPlatform, Button, Text

pygame.init()
pygame.mixer.init()

SIZESCREEN = WIDTH, HEIGHT = 1366, 740
screen = pygame.display.set_mode(SIZESCREEN)
clock = pygame.time.Clock()

path = os.path.join(os.getcwd(), 'img')
file_names = os.listdir(path)

YELLOW = pygame.color.THECOLORS['yellow']
WHITE = pygame.color.THECOLORS['white']
LIGHTGREEN = pygame.color.THECOLORS['lightgreen']
DARKRED = pygame.color.THECOLORS['darkred']
DARKBLUE = pygame.color.THECOLORS['darkblue']





BACKGROUND = pygame.image.load(os.path.join(path, 'tlo2.png')).convert()

file_names.remove('tlo2.png')

IMAGES = {}
for file_name in file_names:
    image_name = file_name[:-4]
    IMAGES[image_name] = pygame.image.load(os.path.join(path, file_name)).convert_alpha(BACKGROUND)

difficulty = 1



other_platform_list = [IMAGES['vanishStart'], IMAGES['vanishMiddle'], IMAGES['vanishEnd'],
                       IMAGES['mrozStart'], IMAGES['mrozMiddle'], IMAGES['mrozEnd'],
                       IMAGES['slimeStart'], IMAGES['slimeMiddle'], IMAGES['slimeEnd']]
powerups_list = [IMAGES['powerUp1'], IMAGES['powerUp2']]
enemy_list = [IMAGES['kw1'], IMAGES['kwmroz']]
enemy_animation = [[IMAGES['cir1'], IMAGES['cir2'], IMAGES['cir3']],[IMAGES['tri1'], IMAGES['tri2'], IMAGES['tri3']]]
Test_Level = Level(BACKGROUND, 0, 0, screen, IMAGES['platformStart'],IMAGES['platformMiddle'],IMAGES['platformEnd'], other_platform_list, powerups_list, difficulty, enemy_list, enemy_animation )
animation_list = [IMAGES['kw1'], IMAGES['kwm1'], IMAGES['kw11'], IMAGES['kw2'], IMAGES['kwm2'], IMAGES['kw22'], IMAGES['kw3'], IMAGES['kwm3'], IMAGES['kw33']]

other_images_player = [IMAGES['kwmroz']]
Test = Player(IMAGES['kw1'], 100, 100, 2, Test_Level, other_images_player,animation_list)

start_button = Button(IMAGES['powerUp1'], 533, 45, "START", LIGHTGREEN, 90, "Arial", YELLOW, 300, 150)
quit_button = Button(IMAGES['powerUp1'], 533, 245, "QUIT", LIGHTGREEN, 90, "Arial", YELLOW, 300, 150)
restart_button = Button(IMAGES['powerUp1'], 533, 445, "RESTART", LIGHTGREEN, 60, "Arial", YELLOW, 300, 150)
difficulty_button = Button(IMAGES['powerUp1'], 533, 445, "DIFFICULTY", LIGHTGREEN, 50, "Arial", YELLOW, 300, 150)

easy_button = Button(IMAGES['powerUp1'], 533, 80, "EASY", LIGHTGREEN, 70, "Arial", YELLOW, 300, 100)
med_button = Button(IMAGES['powerUp1'], 533, 270, "MEDIUM", LIGHTGREEN, 70, "Arial", YELLOW, 300, 100)
diff_button = Button(IMAGES['powerUp1'], 533, 450, "HARD", LIGHTGREEN, 70, "Arial", YELLOW, 300, 100)
quit_dif_button = Button(IMAGES['powerUp1'], 533, 630, "DONE", LIGHTGREEN, 70, "Arial", WHITE , 300, 100,34)

won_text = Text(IMAGES['powerUp1'], 120, 200, "WINNNER!!!",DARKRED , 250, "dubai")
lost_text = Text(IMAGES['powerUp1'], 80, 200, "GAME OVER", DARKRED, 250, "dubai")





#pętla gry

window_open = True
active_game = False
paused_game = False
difficulty_choice = False

game_lost = False
game_won = False





pygame.mixer.music.load('sounds/back2.wav')




pygame.mixer.music.play()
pygame.mixer.music.set_volume(1)

while window_open:
    ##Test.move(pygame.key.get_pressed())

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if not paused_game:
                    active_game = False
                    paused_game = True
                elif paused_game:
                    active_game = True
                    paused_game = False
        if event.type == pygame.QUIT:

            window_open = False
        if event.type == pygame.MOUSEBUTTONDOWN and not active_game:
            if start_button.rect.collidepoint(pygame.mouse.get_pos()) and not difficulty_choice:
                active_game = True
                paused_game = False
                pygame.time.delay(200)
            elif start_button.rect.collidepoint(pygame.mouse.get_pos()) and difficulty_choice:
                Test_Level.difficulty = 1
            if quit_button.rect.collidepoint(pygame.mouse.get_pos()) and not difficulty_choice:
                window_open = False
                pygame.time.delay(200)
            elif quit_button.rect.collidepoint(pygame.mouse.get_pos()) and difficulty_choice:
                Test_Level.difficulty = 2
            if restart_button.rect.collidepoint(pygame.mouse.get_pos()) and paused_game:
                Test_Level.restart_level()
                Test.restart_player()
                active_game = True
                paused_game = False
            elif restart_button.rect.collidepoint(pygame.mouse.get_pos()) and not paused_game and not difficulty_choice:
                difficulty_choice = True
            elif restart_button.rect.collidepoint(pygame.mouse.get_pos()) and not paused_game and difficulty_choice:
                Test_Level.difficulty = 3
            if quit_dif_button.rect.collidepoint(pygame.mouse.get_pos()):
                difficulty_choice = False


    if active_game:
        Test_Level.add_basic_platform()
        Test_Level.add_powerup()
        Test_Level.update_level()
        Test.move(pygame.key.get_pressed())
        Test.draw(screen)
        Test.show_points()
        Test.points_text.draw_text(screen)
        if Test.jump_boost:
            Test.boost_one_text.draw_text(screen)
        if Test.immunity:
            Test.boost_two_text.draw_text(screen)

        if Test.points >= 100:
            game_won = True
            window_open = False
        if Test.points < -20:
            game_lost = True
            window_open = False

    else:
        if not paused_game and not difficulty_choice:
            screen.fill(DARKRED)
            start_button.draw_text(screen)
            quit_button.draw_text(screen)
            difficulty_button.draw_text(screen)
        elif difficulty_choice:
            if Test_Level.difficulty == 1:
                screen.fill(DARKBLUE)
            elif Test_Level.difficulty == 2:
                screen.fill(LIGHTGREEN)
            elif Test_Level.difficulty == 3:
                screen.fill(DARKRED)
            easy_button.draw_text(screen)
            med_button.draw_text(screen)
            diff_button.draw_text(screen)
            quit_dif_button.draw_text(screen)
        else:
            start_button.draw_text(screen)
            quit_button.draw_text(screen)
            restart_button.update_text()
            restart_button.draw_text(screen)




    ##pygame.display.flip()
    ##Test_Level.add_basic_platform()
    ##Test_Level.add_powerup()
    ##Test_Level.update_level()

    pygame.display.flip()
    clock.tick(60)

if game_lost:
    pygame.time.delay(500)
    screen.fill(YELLOW)
    lost_text.update_text()
    lost_text.draw_text(screen)
    pygame.display.update()
    pygame.time.delay(2000)

if game_won:
    pygame.time.delay(500)
    screen.fill(LIGHTGREEN)
    won_text.update_text()
    won_text.draw_text(screen)
    pygame.display.update()
    pygame.time.delay(2000)
pygame.quit()

