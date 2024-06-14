import  pygame,os,random

from base_game import Alive, Player, Level, BasicPlatform, Button

pygame.init()

SIZESCREEN = WIDTH, HEIGHT = 1366, 740
screen = pygame.display.set_mode(SIZESCREEN)
clock = pygame.time.Clock()

path = os.path.join(os.getcwd(), 'img')
file_names = os.listdir(path)

YELLOW = pygame.color.THECOLORS['yellow']
LIGHTGREEN = pygame.color.THECOLORS['lightgreen']


BACKGROUND = pygame.image.load(os.path.join(path, 'background.jpg')).convert()
file_names.remove('background.jpg')

IMAGES = {}
for file_name in file_names:
    image_name = file_name[:-4]
    IMAGES[image_name] = pygame.image.load(os.path.join(path, file_name)).convert_alpha(BACKGROUND)



other_platform_list = [IMAGES['vanishStart'], IMAGES['vanishMiddle'], IMAGES['vanishEnd'],
                       IMAGES['mrozStart'], IMAGES['mrozMiddle'], IMAGES['mrozEnd'],
                       IMAGES['slimeStart'], IMAGES['slimeMiddle'], IMAGES['slimeEnd']]
powerups_list = [IMAGES['powerUp'], IMAGES['kw5']]
Test_Level = Level(BACKGROUND, 100, 200, screen, IMAGES['platformStart'],IMAGES['platformMiddle'],IMAGES['platformEnd'], other_platform_list, powerups_list)


other_images_player = [IMAGES['kwmroz']]
Test = Player(IMAGES['kw1'], 100, 100, 2, Test_Level, other_images_player)

start_button = Button(IMAGES['powerUp'], 533, 45, "START", LIGHTGREEN, 90, "Arial", YELLOW, 300, 150)
quit_button = Button(IMAGES['powerUp'], 533, 245, "QUIT", LIGHTGREEN, 90, "Arial", YELLOW, 300, 150)
restart_button = Button(IMAGES['powerUp'], 533, 445, "RESTART", LIGHTGREEN, 60, "Arial", YELLOW, 300, 150)








#pętla gry

window_open = True
active_game = False
paused_game = False


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
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.rect.collidepoint(pygame.mouse.get_pos()):
                active_game = True
                paused_game = False
                pygame.time.delay(200)
            if quit_button.rect.collidepoint(pygame.mouse.get_pos()):
                window_open = False
                pygame.time.delay(200)
            if restart_button.rect.collidepoint(pygame.mouse.get_pos()):
                Test_Level.restart_level()
                Test.restart_player()
                active_game = True
                paused_game = False


    if active_game:
        Test_Level.add_basic_platform()
        Test_Level.add_powerup()
        Test_Level.update_level()
        Test.move(pygame.key.get_pressed())
        Test.draw(screen)
        Test.show_points()
        Test.points_text.draw_text(screen)

    else:
        start_button.draw_button(screen)
        quit_button.draw_button(screen)
        if paused_game:
            restart_button.draw_button(screen)




    ##pygame.display.flip()
    ##Test_Level.add_basic_platform()
    ##Test_Level.add_powerup()
    ##Test_Level.update_level()

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
