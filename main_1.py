import  pygame,os,random

from base_game import Alive, Player, Level, BasicPlatform

pygame.init()

SIZESCREEN = WIDTH, HEIGHT = 1366, 740
screen = pygame.display.set_mode(SIZESCREEN)
clock = pygame.time.Clock()

path = os.path.join(os.getcwd(), 'img')
file_names = os.listdir(path)
LIGHTGREEN = pygame.color.THECOLORS['lightgreen']


BACKGROUND = pygame.image.load(os.path.join(path, 'background.jpg')).convert()
file_names.remove('background.jpg')

IMAGES = {}
for file_name in file_names:
    image_name = file_name[:-4]
    IMAGES[image_name] = pygame.image.load(os.path.join(path, file_name)).convert_alpha(BACKGROUND)



other_platform_list = [IMAGES['kw4'], IMAGES['kw4'], IMAGES['kw4'],
                       IMAGES['kw5'], IMAGES['kw5'], IMAGES['kw5'],
                       IMAGES['kw3'], IMAGES['kw3'], IMAGES['kw3']]
powerups_list = [IMAGES['kw1'], IMAGES['kw5']]
Test_Level = Level(BACKGROUND, 100, 200, screen, IMAGES['testGrafika1'],IMAGES['testGrafika1'],IMAGES['testGrafika1'], other_platform_list, powerups_list)

other_images_player = [IMAGES['kw5']]
Test = Player(IMAGES['kw1'], 100, 100, 2, Test_Level, other_images_player)









#pętla gry

window_open = True
while window_open:
    Test.move(pygame.key.get_pressed())


    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                window_open = False
        if event.type == pygame.QUIT:

            window_open = False

    Test.draw(screen)



    pygame.display.flip()
    Test_Level.add_basic_platform()
    Test_Level.add_powerup()
    Test_Level.update_level()
    clock.tick(60)


pygame.quit()
