import os
import sys
import pygame
from pygame import mixer

pygame.init()
pygame.key.set_repeat(200, 70)

# константы
FPS = 500
WIDTH = 600
HEIGHT = 600
STEP = 10
lvls = ["1lvl.txt", "2lvl.txt", "3lvl.txt", "4lvl.txt"]
lvl_sch = 0
fl_pos = False
part_of_lvl = 0
part_of_story = 0

# сюжет и остальные текстовые константы
texts = [["Цели:", "", "Найдите поставщика.", "", "Заберите посылку.", "", "Найдите портал."], ['Цели:', "", "Донесите посылку до базы (blue base).",
                      "", "Найдите следуеющий портал."], ["Цель:", "Найдите следующего поставщика."],
         ["Цель:", "", "Донести важную посылку."]]
story = [["Адамант:", "", "О, а вот и ты. А я тут как раз думал о тебе.", "",
          "Сэм Бриджес:", "", "Мне некогда болтать. Где товар? Скоро начнется", "ливень смерти.", "",
          "Адамант:", "", "Ладно. Держи посылку. Отнеси её на blue base на северную сторону.", "",
          "Сэм Бриджес:", "", "Хорошо. Отметьте меня в списке. Я пошел.", "",
          "Адамант:", "", "Стой! Будь аккуратен. Говорят 'BT' вышли из спячки на востоке и ", "перебрались на север.", "",
          "Сэм Бриджес:", "", "Вот д****о. Спасибо за ифнормацию. Буду аккуратнее."],
         ["Сэм Бриджес:", "", "Почему место выдачи не определено в списках?", "",
          "Грундаль:", "", "Тише! Это очень важная посылка.", "Судя по твоему рейтингу в блоке ты самый лучший доставщик.",
          "По этому я доверяю это тебе.", "Тебе нужно отнести её на blue base в запретную зону.", "",
          "Сэм Бриджес:", "", "Что такого в этой посылке?", "",
          "Грундаль:", "", "Я не могу говорить об этом. дело государственной важности важности."]]
if __name__ == '__main__':

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # группы спрайтов всех обьектов в игре
    player = None
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    portals_group = pygame.sprite.Group()
    actors_group = pygame.sprite.Group()
    base_group = pygame.sprite.Group()
    zombie_group = pygame.sprite.Group()


    # функции загрузки
    def load_image(name, color_key=None):
        fullname = os.path.join('data', name)
        try:
            image = pygame.image.load(fullname).convert()
        except pygame.error as message:
            print('Cannot load image:', name)
            raise SystemExit(message)

        if color_key is not None:
            if color_key == -1:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key)
        else:
            image = image.convert_alpha()
        return image


    def load_level(filename):
        filename = "lvls/" + filename
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]    
        max_width = max(map(len, level_map)) 
        return list(map(lambda x: x.ljust(max_width, '*'), level_map))


    def generate_level(level):
        new_player, x, y = None, None, None
        fl = False
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile('empty', x, y)
                    fl = 'empty'
                elif level[y][x] == '#':
                    Tile('wall', x, y)
                elif level[y][x] == '+':
                    Tile('black', x, y)
                    fl = 'black'
                elif level[y][x] == '@':
                    Tile('spawn', x, y)
                    new_player = Player(x, y)
                elif level[y][x] == '*':
                    Tile('snow', x, y)
                    fl = 'snow'
                elif level[y][x] == '-':
                    Tile('portal', x, y)
                elif level[y][x] == '%':
                    Tile(fl, x, y)
                    Actor('actor', x, y)
                elif level[y][x] == "!":
                    Tile('base', x, y)
                elif level[y][x] == "=":
                    Tile('empty2', x, y)
                    fl = 'empty2'
                elif level[y][x] == "9":
                    Tile(fl, x, y)
                    Zombie('zombie', x, y)                       
        return new_player, x, y


    def terminate():
        pygame.quit()
        sys.exit()

    # основной цикл игры
    def game(lvl):
        player, level_x, level_y = generate_level(load_level(lvl))
        camera = Camera((level_x, level_y))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    player_group.update(event, player)
            camera.update(player)
            for sprite in all_sprites:
                camera.apply(sprite)
            screen.fill(pygame.Color(0, 0, 0))
            tiles_group.draw(screen)
            wall_group.draw(screen)
            portals_group.draw(screen)
            player_group.draw(screen)
            actors_group.draw(screen)
            base_group.draw(screen)
            zombie_group.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)
        terminate()
        
    # главная заставка

    def start_screen():
        intro_text = ["Death stranding", "", "", "            18+"]

        fon = pygame.transform.scale(load_image('fon2.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 70)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 50, (47, 69, 56))
            intro_rect = string_rendered.get_rect()
            text_coord += 50
            intro_rect.top = text_coord
            intro_rect.x = 115
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN:
                    return
            pygame.display.flip()
            clock.tick(FPS)

    # инструкция
    def instruction_screen():
        intro_text = ["УПРАВЛЕНИЕ", "Стрелочки : движение героя.", "", "F : взаимодействие.", "", "Зажмите левый SHIFT, чтобы ускориться.", "", "SPACE : начать игру заново на финальных экранах.", "", "", "", "", "", "", "", "", "", "",
                    "", "", "", "", "", "", "Кнопка 'F' предназначена для взаимодействия с персонажами", "и порталами."]

        fon = pygame.transform.scale(load_image('fon4.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 25)
        text_coord = 20
        for line in intro_text:
            string_rendered = font.render(line, 50, (255, 240, 255))
            intro_rect = string_rendered.get_rect()
            text_coord += 1
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN:
                    return
            pygame.display.flip()
            clock.tick(FPS)

    # интро уровней
    def first_screen():
        intro_text = ["Однажды произошел взрыв, он породил пространство и время.",
                    "", "Однажды произошел взрыв и планета начала вращаться в пространстве.",
                    "", "Однажды произошел взрыв, он породил жизнь, какой мы её знаем.",
                    "", " Затем ещё один взрыв…", "", "… и для нас он станет последним"]

        fon = pygame.transform.scale(load_image('fon3.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 20)
        text_coord = 50
        mixer.music.load("music\{}.mp3".format('death_stranding_08. John'))
        mixer.music.play()
        for line in intro_text:
            string_rendered = font.render(line, 50, (189, 182, 191))
            intro_rect = string_rendered.get_rect()
            text_coord += 1
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN:
                    return
            pygame.display.flip()
            clock.tick(FPS)
            
    # экран при game over
    def final_screen():
        global lvl_sch, fl_pos, part_of_lvl, part_of_story
        fon = pygame.transform.scale(load_image('game_over.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 40)
        mixer.music.load("music\{}.mp3".format('game_over'))
        mixer.music.play()    
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        all_sprites.empty()
                        tiles_group.empty()
                        wall_group.empty()
                        player_group.empty()
                        portals_group.empty()
                        actors_group.empty()
                        base_group.empty()
                        zombie_group.empty()
                        lvl_sch = 0
                        fl_pos = False
                        part_of_lvl = 0
                        part_of_story = 0
                        start_screen()
                        instruction_screen()
                        first_screen()
                        second_screen()
                        
                        game(lvls[lvl_sch])

            pygame.display.flip()
            clock.tick(FPS)
    # конечный экран
    def over_screen():
        global lvl_sch, fl_pos, part_of_lvl, part_of_story
        fon = pygame.transform.scale(load_image('over.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 60)
        mixer.music.load("music\{}.mp3".format('death_stranding_10. Heartman'))
        mixer.music.play()
        intro_text = ["Thanks for playing.", "", "Game by lotofmyself"]
        text_coord = 100
        for line in intro_text:
            string_rendered = font.render(line, 50, (255, 240, 255))
            intro_rect = string_rendered.get_rect()
            text_coord += 1
            intro_rect.top = text_coord
            intro_rect.x = 70
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        all_sprites.empty()
                        tiles_group.empty()
                        wall_group.empty()
                        player_group.empty()
                        portals_group.empty()
                        actors_group.empty()
                        base_group.empty()
                        zombie_group.empty()
                        lvl_sch = 0
                        fl_pos = False
                        part_of_lvl = 0
                        part_of_story = 0
                        start_screen()
                        instruction_screen()
                        first_screen()
                        second_screen()
                        game(lvls[lvl_sch])
            pygame.display.flip()
            clock.tick(FPS)
            
    def second_screen():
        global part_of_lvl
        intro_text = texts[part_of_lvl]
        part_of_lvl += 1

        fon = pygame.transform.scale(load_image('fon3.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 40)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 50, (189, 182, 191))
            intro_rect = string_rendered.get_rect()
            text_coord += 1
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN:
                    return
            pygame.display.flip()
            clock.tick(FPS)
    # экран диалогов
    def story_screen():
        global part_of_story
        intro_text = story[part_of_story]
        part_of_story += 1

        fon = pygame.transform.scale(load_image('paper.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 20)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 50, (138, 69, 19))
            intro_rect = string_rendered.get_rect()
            text_coord += 1
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return
            pygame.display.flip()
            clock.tick(FPS)
    # константы изображений всех объектов
    tile_images = {'wall': load_image('empty4.png'), 'empty': load_image('empty.png'),
                'snow': load_image('snow.png'), 'spawn': load_image('spawn.png'),
                'actor': load_image('actor2.png', color_key=-1),
                'portal': load_image('spawn.png'), 'base': load_image('base.jpg'),
                'empty2': load_image('empty2.png'), 'black': load_image('black.jfif'),
                'zombie': load_image('zombie.png', color_key=-1)}
    player_image = load_image('gamer.png', color_key=-1)
    player_image = pygame.transform.scale(player_image, (40, 40))

    tile_width = tile_height = 50

    # классы карты

    class Tile(pygame.sprite.Sprite):
        def __init__(self, tile_type, pos_x, pos_y):
            if tile_type == 'wall':
                super().__init__(tiles_group, all_sprites)
                self.image = tile_images[tile_type]
                self.image = pygame.transform.scale(self.image, (50, 50))
                self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
            elif tile_type == 'base':
                super().__init__(base_group, all_sprites)
                self.image = tile_images[tile_type]
                self.image = pygame.transform.scale(self.image, (50, 50))
                self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
            elif tile_type == 'portal':
                super().__init__(portals_group, all_sprites)
                self.image = tile_images['portal']
                self.image = pygame.transform.scale(self.image, (50, 50))
                self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
            else:
                super().__init__(wall_group, all_sprites)
                self.image = tile_images[tile_type]
                self.image = pygame.transform.scale(self.image, (50, 50))
                self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
                
    # класс персонажей
    class Actor(pygame.sprite.Sprite):
        def __init__(self, actor_type, pos_x, pos_y):
            super().__init__(actors_group, all_sprites)
            self.image = tile_images[actor_type]
            self.image = pygame.transform.scale(self.image, (50, 50))
            self.image.set_colorkey((255, 255, 255))
            screen.blit(self.image, (0, 0))
            self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
            self.x = pos_x
            self.y = pos_y
            
    # класс врагов
    class Zombie(pygame.sprite.Sprite):
        def __init__(self, zombie_type, pos_x, pos_y):
            super().__init__(zombie_group, all_sprites)
            self.image = tile_images[zombie_type]
            self.image = pygame.transform.scale(self.image, (50, 50))
            self.image.set_colorkey((255, 255, 255))
            screen.blit(self.image, (0, 0))
            self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
            self.x = pos_x
            self.y = pos_y
            
    # класс игрока
    class Player(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y):
            super().__init__(player_group, all_sprites)
            if fl_pos:
                self.image = load_image('gamer_with.png', color_key=-1)
                self.image = pygame.transform.scale(self.image, (40, 40))
            else:
                self.image = player_image
            self.image.set_colorkey((255, 255, 255))
            screen.blit(self.image, (0, 0))
            self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
            self.x = pos_x
            self.y = pos_y
            
        # апдейт для всех взаимодействий с окружающим миром игрока
        def update(self, event, player):
            global lvl_sch, STEP, fl_pos
            x = player.rect.x
            y = player.rect.y
            keys = pygame.key.get_pressed()
            if event.key == pygame.K_LEFT:
                S = -STEP
                player.rect.x += S
            if event.key == pygame.K_RIGHT:
                S = STEP
                player.rect.x += S
            if event.key == pygame.K_UP:
                S = -STEP
                player.rect.y += S
            if event.key == pygame.K_DOWN:
                S = STEP
                player.rect.y += S
            if keys[pygame.K_LSHIFT]:
                STEP = 18
            else:
                STEP = 10
            if pygame.sprite.spritecollideany(self, tiles_group):
                player.rect.x = x
                player.rect.y = y
            if pygame.sprite.spritecollideany(self, portals_group):
                if event.key == pygame.K_f:
                    print(lvl_sch)
                    if lvl_sch == 3:
                        over_screen()
                    else:
                        second_screen()
                        all_sprites.empty()
                        tiles_group.empty()
                        wall_group.empty()
                        player_group.empty()
                        portals_group.empty()
                        actors_group.empty()
                        base_group.empty()
                        zombie_group.empty()
                        lvl_sch += 1
                        game(lvls[lvl_sch])
            if pygame.sprite.spritecollideany(self, actors_group):
                if event.key == pygame.K_f and fl_pos == False:
                    story_screen()
                    self.image = load_image('gamer_with.png', color_key=-1)
                    self.image = pygame.transform.scale(self.image, (40, 40))
                    self.image.set_colorkey((255, 255, 255))
                    screen.blit(self.image, (0, 0))
                    fl_pos = True
            if pygame.sprite.spritecollideany(self, base_group):
                player.rect.x = x
                player.rect.y = y
                self.image = load_image('gamer.png', color_key=-1)
                self.image = pygame.transform.scale(self.image, (40, 40))
                self.image.set_colorkey((255, 255, 255))
                screen.blit(self.image, (0, 0))
                fl_pos = False
            if pygame.sprite.spritecollideany(self, zombie_group):
                final_screen()
                all_sprites.empty()
                tiles_group.empty()
                wall_group.empty()
                player_group.empty()
                portals_group.empty()
                actors_group.empty()
                base_group.empty()
                zombie_group.empty()

    # класс камеры
    class Camera:
        def __init__(self, field_size):
            self.dx = 0
            self.dy = 0
            self.field_size = field_size

        def apply(self, obj):
            obj.rect.x += self.dx
            if obj.rect.x < -obj.rect.width:
                obj.rect.x += (self.field_size[0] + 1) * obj.rect.width       
            if obj.rect.x >= (self.field_size[0]) * obj.rect.width:
                obj.rect.x += -obj.rect.width * (1 + self.field_size[0])
            obj.rect.y += self.dy
            if obj.rect.y < -obj.rect.height:
                obj.rect.y += (self.field_size[1] + 1) * obj.rect.height
            if obj.rect.y >= (self.field_size[1]) * obj.rect.height:
                obj.rect.y += -obj.rect.height * (1 + self.field_size[1])

        def update(self, target):
            self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
            self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


    # Начальная ИГРОВАЯ ПОСЛЕДОВАТЕЛЬНОСТЬ
    start_screen()
    instruction_screen()
    first_screen()
    second_screen()
    game(lvls[lvl_sch])

