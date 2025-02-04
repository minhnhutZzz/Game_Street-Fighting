import pygame
from pygame import mixer

from fighter import Fighter  # Ensure this class is defined in fighter.py

# Initialize mixer and pygame
mixer.init()
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Fighter data
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]

WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

Pack3_SIZE = 162
Pack3_SCALE = 4
Pack3_OFFSET = [105, 75]
Pack3_DATA = [Pack3_SIZE, Pack3_SCALE,Pack3_OFFSET]

PhapSu_SIZE = 200
PhapSu_SCALE = 3
PhapSu_OFFSET = [100,75]
PhapSu_DATA = [PhapSu_SIZE,PhapSu_SCALE,PhapSu_OFFSET]

Martial_SIZE = 162
Martial_SCALE = 3
Martial_OFFSET = [100,65]
Martial_DATA = [Martial_SIZE,Martial_SCALE,Martial_OFFSET]


# Animation steps
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]
Pack3_ANIMATION_STEPS = [10,6,1,4,5,3,9]
PhapSu_ANIMATION_STEPS = [8,8,4,8,8,4,5]
Martial_ANIMATION_STEPS = [10,8,3,6,8,3,10]
# Initialize display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fighter Game")
clock = pygame.time.Clock()

# Load assets\
main_menu_bg = pygame.image.load("asset/images/backgroundmenu/backgroundmenu.jpg").convert_alpha()  # Background for main menu
main_menu_bg = pygame.transform.scale(main_menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
victory_img = pygame.image.load("asset/images/icons/victory.png").convert_alpha()
bg_image = pygame.image.load("asset/images/background/background1.jpg").convert_alpha()
warrior_sheet = pygame.image.load("asset/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("asset/images/wizard/Sprites/wizard.png").convert_alpha()
pack3_sheet = pygame.image.load("asset/images/Medieval Warrior Pack 3/Sprites/pack_3.png").convert_alpha()
evil_sheet = pygame.image.load("asset/images/Evil Wizard/Sprites/Phap_Su_Lua.png").convert_alpha()
martial_sheet = pygame.image.load("asset/images/Martial Hero 3/Sprite/martial.png").convert_alpha()
anh_warrior = pygame.image.load("asset/images/warrior/warrior.png").convert_alpha()
anh_wizard = pygame.image.load("asset/images/wizard/wizard.png").convert_alpha()
anh_pack3 = pygame.image.load("asset/images/Medieval Warrior Pack 3/pack3.png").convert_alpha()
anh_magic = pygame.image.load("asset/images/Evil Wizard/evil.png").convert_alpha()
anh_martial = pygame.image.load("asset/images/Martial Hero 3/Preview.png").convert_alpha()


# Load sounds
sword_fx = pygame.mixer.Sound("asset/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("asset/audio/magic.wav")
magic_fx.set_volume(0.75)

# Fonts
count_font = pygame.font.Font("asset/front/turok.ttf", 80)
score_font = pygame.font.Font("asset/front/turok.ttf", 30)
image_font = pygame.font.Font("asset/front/turok.ttf", 50)

# Function to change music
def change_music(scene):
    pygame.mixer.music.stop()
    if scene == "menu":
        pygame.mixer.music.load("asset/audio/nhac_menu.mp3")
    elif scene == "character_selection":
        pygame.mixer.music.load("asset/audio/nhac_nen.mp3")
    elif scene == "battle":
        pygame.mixer.music.load("asset/audio/nhac_background.mp3")
    pygame.mixer.music.set_volume(0.75)
    pygame.mixer.music.play(-1)


# Draw text function
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Draw background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

# Draw health bar
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, GREEN, (x, y, 400 * ratio, 30))
# Function to handle pause menu
def pause_menu():
    global current_scene
    paused = True

    # Nút Pause Menu
    continue_button = pygame.Rect(SCREEN_WIDTH / 2 - 100, 200, 200, 50)
    menu_button = pygame.Rect(SCREEN_WIDTH / 2 - 100, 300, 200, 50)

    while paused:
        screen.fill((0, 0, 0))
        draw_text("Game Paused", count_font, WHITE, SCREEN_WIDTH / 2 - 200, 100)

        pygame.draw.rect(screen, GREEN, continue_button)
        draw_text("Continue", score_font, WHITE, SCREEN_WIDTH / 2 - 60, 210)

        pygame.draw.rect(screen, GREEN, menu_button)
        draw_text("Main Menu", score_font, WHITE, SCREEN_WIDTH / 2 - 85, 310)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if continue_button.collidepoint(mouse_x, mouse_y):
                    paused = False  # Tiếp tục trận đấu
                elif menu_button.collidepoint(mouse_x, mouse_y):
                    paused = False
                    main_game()  # Trở về menu chính

        pygame.display.update()
        clock.tick(FPS)
#Chon che do choi
def choose_mode():

    global current_scene
    current_scene = "menu"
    change_music(current_scene)

    selected_mode = None  # Lưu chế độ chơi
    choosing = True

    # Nút chế độ
    vs_player_button = pygame.Rect(SCREEN_WIDTH / 2 + 30, 150, 300, 60)
    vs_ai_button = pygame.Rect(SCREEN_WIDTH / 2 +30, 350, 300, 60)

    while choosing:
        screen.blit(main_menu_bg, (0, 0))
        draw_text("Chon che do choi", image_font, WHITE, SCREEN_WIDTH / 2 + 30 , 80)

        # Vẽ các nút
        pygame.draw.rect(screen, GREEN, vs_player_button)
        pygame.draw.rect(screen, GREEN, vs_ai_button)
        draw_text("1. Player vs Player", score_font, WHITE, vs_player_button.x + 30, vs_player_button.y + 10)
        draw_text("2. Player vs AI", score_font, WHITE, vs_ai_button.x + 30, vs_ai_button.y + 10)

        # Lắng nghe sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                # Kiểm tra nút
                if vs_player_button.collidepoint(mouse_x, mouse_y):
                    selected_mode = "vs_player"
                    choosing = False
                elif vs_ai_button.collidepoint(mouse_x, mouse_y):
                    selected_mode = "PVE"
                    choosing = False

        pygame.display.update()
        clock.tick(FPS)

    return selected_mode

# Character selection menu
def choose_character():
    global current_scene
    current_scene = "character_selection"
    change_music(current_scene)

    selected_character = [0, 0]  # [P1 chọn nhân vật, P2 chọn nhân vật]
    current_player = 0  # Bắt đầu với Player 1
    choosing = True
    start_game = False  # Cờ kiểm tra trạng thái nhấn nút Start

    # Nút Start
    start_button_rect = pygame.Rect(SCREEN_WIDTH / 2 - 100, 500, 200, 50)


    while choosing:
        screen.fill((0, 0, 0))  # Black background
        draw_text("Chon Nhan Vat", count_font, WHITE, SCREEN_WIDTH / 2 - 200, 60)

        # Hiển thị các nhân vật
        warrior_preview = pygame.transform.scale(anh_warrior, (150, 200))
        wizard_preview = pygame.transform.scale(anh_wizard, (150, 200))
        pack3_preview = pygame.transform.scale(anh_pack3, (150, 200))
        magic_preview = pygame.transform.scale(anh_magic, (150, 200))
        martial_preview = pygame.transform.scale(anh_martial, (150, 200))

        screen.blit(warrior_preview, (50, 200))
        screen.blit(wizard_preview, (240, 200))
        screen.blit(pack3_preview, (430, 200))
        screen.blit(magic_preview, (620, 200))
        screen.blit(martial_preview, (810, 200))

        # Hướng dẫn
        if current_player == 0:
            draw_text("Player 1: Click to choose!", score_font, WHITE, 50, 450)
        elif current_player == 1:
            draw_text("Player 2: Click to choose!", score_font, WHITE, 50, 450)

        # Kiểm tra nếu đã chọn xong
        if selected_character[0] != 0 and selected_character[1] != 0:
            pygame.draw.rect(screen, GREEN, start_button_rect)
            draw_text("START", score_font, WHITE, SCREEN_WIDTH / 2 - 50, 510)

        # Lắng nghe sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                # Kiểm tra chọn nhân vật
                if current_player == 0 or current_player == 1:
                    if 50 <= mouse_x <= 150 and 200 <= mouse_y <= 400:  # Warrior
                        selected_character[current_player] = 1
                    elif 250 <= mouse_x <= 350 and 200 <= mouse_y <= 400:  # Wizard
                        selected_character[current_player] = 2
                    elif 450 <= mouse_x <= 550 and 200 <= mouse_y <= 400:  # Pack3
                        selected_character[current_player] = 3
                    elif 650 <= mouse_x <= 750 and 200 <= mouse_y <= 400:  # Pháp Sư
                        selected_character[current_player] = 4
                    elif 850 <= mouse_x <= 950 and 200 <= mouse_y <= 400:  # Martial
                        selected_character[current_player] = 5

                    # Chuyển sang Player 2 nếu Player 1 đã chọn xong
                    if selected_character[current_player] != 0:
                        current_player += 1

                # Kiểm tra nhấn nút Start
                if selected_character[0] != 0 and selected_character[1] != 0:
                    if start_button_rect.collidepoint(mouse_x, mouse_y):
                        start_game = True

        # Thoát vòng lặp nếu nhấn nút Start
        if start_game:
            choosing = False

        pygame.display.update()
        clock.tick(FPS)

    return selected_character


# Main game loop
def main_game():
    global current_scene
    current_scene = "battle"
    change_music(current_scene)

    # Chọn chế độ chơi
    game_mode = choose_mode()

    # Chọn nhân vật nếu chơi Vs người
    if game_mode == "vs_player":
        selected_characters = choose_character()
    else:
        # Tự động chọn nhân vật nếu chơi Vs máy
        selected_characters=[1,2]
    # Create fighters based on selection
    if selected_characters[0] == 1:
        fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
    elif selected_characters[0]==2:
        fighter_1 = Fighter(1, 200, 310, False, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)
    elif selected_characters[0]==3:
        fighter_1 = Fighter(1, 200, 310, False, Pack3_DATA, pack3_sheet, Pack3_ANIMATION_STEPS, sword_fx)
    elif selected_characters[0]==4:
        fighter_1 = Fighter(1, 200, 310, False, PhapSu_DATA,evil_sheet, PhapSu_ANIMATION_STEPS, sword_fx)
    elif selected_characters[0] == 5:
        fighter_1 = Fighter(1, 200, 310, False, Martial_DATA,martial_sheet, Martial_ANIMATION_STEPS, sword_fx)

    if selected_characters[1] == 1:
        fighter_2 = Fighter(2, 700, 310, True, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
    elif selected_characters[1]==2:
        fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)
    elif selected_characters[1]==3:
        fighter_2 = Fighter(2, 700, 310, True, Pack3_DATA, pack3_sheet, Pack3_ANIMATION_STEPS, sword_fx)
    elif selected_characters[1]==4:
        fighter_2 = Fighter(2, 700, 310, True, PhapSu_DATA,evil_sheet, PhapSu_ANIMATION_STEPS, sword_fx)
    elif selected_characters[1] == 5:
        fighter_2 = Fighter(2, 700, 310, True, Martial_DATA,martial_sheet, Martial_ANIMATION_STEPS, sword_fx)

    fighter_2.ai_controlled = game_mode == "PVE"
    score = [0, 0]
    intro_count = 3
    last_count_update = pygame.time.get_ticks()
    round_over = False
    ROUND_OVER_COOLDOWN = 2000
    winner_text=""
    run = True
    while run:
        clock.tick(FPS)
        # Kiểm tra và đổi nhạc nếu cảnh thay đổi
        if current_scene != "battle":
            current_scene = "battle"
            change_music(current_scene)
        draw_bg()
        draw_health_bar(fighter_1.health, 20, 20)
        draw_health_bar(fighter_2.health, 580, 20)
        draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
        draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)

        if intro_count <= 0:
            fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
            if fighter_2.ai_controlled:
                fighter_2.ai_move(fighter_1, round_over)
            else:
                fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
        else:
            draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2 - 20, SCREEN_HEIGHT / 3)
            if pygame.time.get_ticks() - last_count_update >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()

        fighter_1.update()
        fighter_2.update()
        fighter_1.draw(screen)
        fighter_2.draw(screen)

        if not round_over:
            if not fighter_1.alive:
                score[1] += 1
                if game_mode=="vs_player":
                    winner_text = "Player 2 VICTORY!"
                else:
                    winner_text="       YOU LOSS"
                round_over = True
                round_over_time = pygame.time.get_ticks()
            elif not fighter_2.alive:
                score[0] += 1
                winner_text="Player 1 VICTORY!"
                round_over = True
                round_over_time = pygame.time.get_ticks()
        else:
            # Hiển thị tên người chiến thắng
            draw_text(winner_text, count_font, RED, SCREEN_WIDTH / 2 - 280, 100)
            #screen.blit(victory_img, (360, 150))
            if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                round_over = False
                intro_count = 3
                main_game()  # Reset game state
                # Kiểm tra sự kiện tạm dừng
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:  # Phím esc de dung
                pause_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

# Run the game
change_music("menu")  # Start with menu music
main_game()
pygame.quit()