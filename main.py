
# BEGIN
import pygame, sys, random, time

# Initialize pygame
pygame.init()

# Set the dimensions of the screen
screen_width = 1200
screen_height = 600

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Create the screen
 # Set the initial position of the character
character_x_deafult, character_y_deafult = 50, 280
enemy_x_deafult, enemy_y_deafult = 900, 280

 # Set the animation frame rate
animation_speed = 5  # Lower value means slower animation
attack_duration = 6  # Ilość klatek trwania animacji ataku
# Set the clock to control the frame rate
clock = pygame.time.Clock()
character_speed = 300  # Dodajmy prędkość postaci


# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0 , 255, 0)
BLUE = (0, 0, 255)

# Define fonts
pygame.font.init()
font = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", 20)

# Load the floor image
floor_image = pygame.image.load("floorGreen.png")
bc_image = pygame.image.load("bc.png")

character_run = [
    pygame.transform.scale(pygame.image.load("run (1).png"), (225, 225)),
    pygame.transform.scale(pygame.image.load("run (2).png"), (225, 225)),
    pygame.transform.scale(pygame.image.load("run (6).png"), (225, 225)),
    pygame.transform.scale(pygame.image.load("run (9).png"), (225, 225)),
    pygame.transform.scale(pygame.image.load("run (10).png"), (225, 225)),
    pygame.transform.scale(pygame.image.load("run (11).png"), (225, 225)),
]

character_images = [
    pygame.transform.scale(pygame.image.load("idle (1).png"), (225, 225)),
    pygame.transform.scale(pygame.image.load("idle (2).png"), (225, 225)),
    pygame.transform.scale(pygame.image.load("idle (3).png"), (225, 225)),
    pygame.transform.scale(pygame.image.load("idle (4).png"), (225, 225)),
    pygame.transform.scale(pygame.image.load("idle (5).png"), (225, 225)),
    pygame.transform.scale(pygame.image.load("idle (6).png"), (225, 225)),
]

character_attack = [
    # pygame.transform.scale(pygame.image.load("attack (1).png"), (225, 225)),
    # pygame.transform.scale(pygame.image.load("attack (2).png"), (225, 225)),
    # pygame.transform.scale(pygame.image.load("attack (3).png"), (225, 225)),
    # pygame.transform.scale(pygame.image.load("attack (4).png"), (225, 225)),
    # pygame.transform.scale(pygame.image.load("attack (5).png"), (225, 225)),
    # pygame.transform.scale(pygame.image.load("attack (6).png"), (225, 225)),
    pygame.transform.scale(pygame.image.load("attack (7).png"), (225, 225)),
    pygame.transform.scale(pygame.image.load("attack (8).png"), (225, 225)),
    pygame.transform.scale(pygame.image.load("attack (9).png"), (225, 225)),
    pygame.transform.scale(pygame.image.load("attack (10).png"), (225, 225)),
    pygame.transform.scale(pygame.image.load("attack (11).png"), (225, 225)),
    pygame.transform.scale(pygame.image.load("attack (12).png"), (225, 225)),
]
# Create mirrored character images
mirrored_character_images = [pygame.transform.flip(image, True, False) for image in character_images]
mirrored_character_attack = [pygame.transform.flip(image, True, False) for image in character_attack]
mirrored_character_run = [pygame.transform.flip(image, True, False) for image in character_run]
# Define buttons
text_offset = 40 # Przesunięcie tekstu względem przycisków
button_offset = 10  # Przesunięcie pionowe od podłogi
floor_height = screen_height - floor_image.get_height()
button_image = pygame.image.load("button1.png")
resize_button_image = pygame.transform.scale(button_image, (100, 50))
ROCK_BUTTON = pygame.Rect(30, floor_height + text_offset, 100, 50)
PAPER_BUTTON = pygame.Rect(140, floor_height + text_offset, 100, 50)
SCISSORS_BUTTON = pygame.Rect(250, floor_height + text_offset, 100, 50)

# Define button texts
rock_text = font.render("Rock", True, BLACK)
paper_text = font.render("Paper", True, BLACK)
scissors_text = font.render("Scissors", True, BLACK)

# Set the positions of the button texts
rock_text_rect = rock_text.get_rect(center=ROCK_BUTTON.center)
paper_text_rect = paper_text.get_rect(center=PAPER_BUTTON.center)
scissors_text_rect = scissors_text.get_rect(center=SCISSORS_BUTTON.center)

# Funkcja do rysowania paska życia
hbar_width = 400
hbar_height = 30

def healt_bar(healt, max_healt, position, is_enemy=False):  
    global hbar_width
    hbar_width = 400
    
    global hbar_height
    hbar_height = 30
    
    proporcja_zycia = max(healt / max_healt, 0)  # Zapewnienie, że proporcja zycia jest nieujemna
    szerokosc_zycia = int(hbar_width * proporcja_zycia)
    
    hp_back_image = pygame.image.load("hp_back.png")
    hp_back_image = pygame.transform.scale(hp_back_image, (hbar_width+40, hbar_height+10))
    
    if szerokosc_zycia > 0:  # Sprawdzenie, czy szerokosc zycia jest wieksza od zera
        greenbar_image = pygame.image.load("HP_bar.png")
        greenbar_image = pygame.transform.scale(greenbar_image, (szerokosc_zycia, hbar_height))  # Zmniejszenie grafiki
        
        if is_enemy:
            hp_back_image = pygame.transform.flip(hp_back_image, True, False)  # Odwrócenie obrazu
            greenbar_image = pygame.transform.flip(greenbar_image, True, False)  # Odwrócenie obrazu
            screen.blit(hp_back_image , (position[0],position[1]))
            screen.blit(greenbar_image, (position[0] + hbar_width - szerokosc_zycia+5, position[1]))
        else:
            screen.blit(hp_back_image, (position[0]-35, position[1]))
            screen.blit(greenbar_image, (position[0], position[1]))


def main_menu():
    while True:
        # Clear the screen
        screen.fill(BLACK)
        
        # Display the main menu options
        start_text = font.render("Start Game", True, WHITE)
        quit_text = font.render("Quit", True, WHITE)
        start_text_rect = start_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        quit_text_rect = quit_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
        screen.blit(start_text, start_text_rect)
        screen.blit(quit_text, quit_text_rect)
        
        # Update the display
        pygame.display.flip()
        
        # Handle user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_text_rect.collidepoint(mouse_pos):
                    game_mode_menu()
                    break
                elif quit_text_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

def game_mode_menu():
    while True:
        # Clear the screen
        screen.fill(BLACK)
        
        # Display the game mode menu options
        singleplayer_text = font.render("Singleplayer", True, WHITE)
        multiplayer_text = font.render("Multiplayer", True, WHITE)
        back_text = font.render("Back", True, WHITE)
        singleplayer_text_rect = singleplayer_text.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
        multiplayer_text_rect = multiplayer_text.get_rect(center=(screen_width // 2, screen_height // 2))
        back_text_rect = back_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
        screen.blit(singleplayer_text, singleplayer_text_rect)
        screen.blit(multiplayer_text, multiplayer_text_rect)
        screen.blit(back_text, back_text_rect)
        
        # Update the display
        pygame.display.flip()
        
        # Handle user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if singleplayer_text_rect.collidepoint(mouse_pos):
                    start_singleplayer_game()
                    break
                elif multiplayer_text_rect.collidepoint(mouse_pos):
                    start_multiplayer_game()
                elif back_text_rect.collidepoint(mouse_pos):
                    main_menu()

def start_singleplayer_game():
    running = True
    zycie_gracza = 200
    max_zycie_gracza = 200
    zycie_przeciwnika = 200
    max_zycie_przeciwnika = 200
    current_frame = 0
    is_player_animating = True
    is_player_attacking = False
    is_enemy_animating = True
    is_enemy_attacking = False
    is_enemy_running = False
    is_player_running = False
    attack_counter = 0
    character_x, character_y = 50, 280
    enemy_x, enemy_y = 900, 280
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if is_player_animating == True and is_enemy_animating == True:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if ROCK_BUTTON.collidepoint(mouse_pos):
                        player_pick = "rock"
                    elif PAPER_BUTTON.collidepoint(mouse_pos):
                        player_pick = "paper"
                    elif SCISSORS_BUTTON.collidepoint(mouse_pos):
                        player_pick = "scissors"
                    else:
                        player_pick = "None"
                
                    computer_pick = random.choice(["rock", "paper", "scissors"])
                    print("Computer picked " + computer_pick + ".")
                    print("Player picked " + player_pick + ".")
                    print("Player health: " + str(zycie_gracza))
                    print("Computer health: " + str(zycie_przeciwnika))
                    
                    if player_pick == "rock" and computer_pick == "scissors":
                        is_player_animating = False
                        is_player_running = True
                    elif player_pick == "paper" and computer_pick == "rock":
                        is_player_animating = False
                        is_player_running = True
                    elif player_pick == "scissors" and computer_pick == "paper":
                        is_player_animating = False
                        is_player_running = True
                    elif computer_pick == "rock" and player_pick == "scissors":
                        is_enemy_animating = False
                        is_enemy_running = True
                    elif computer_pick == "paper" and player_pick == "rock":
                        is_enemy_animating = False
                        is_enemy_running = True
                    elif computer_pick == "scissors" and player_pick == "paper":
                        is_enemy_animating = False
                        is_enemy_running = True

        screen_buffer = pygame.Surface((screen_width, screen_height))
        screen_buffer.blit(bc_image, (0, 0))

        if is_player_animating:
            screen.blit(character_images[current_frame], (character_x, character_y))
            # Update the animation frame
            current_frame = (current_frame + 1) % len(character_images)
        
        if is_player_attacking:
            # Animacja ataku
            screen.blit(character_attack[current_frame], (character_x, character_y))

            attack_counter += 1
            if attack_counter == 3:
                zycie_przeciwnika -= 20
            if attack_counter >= attack_duration:
                is_player_attacking = False
                attack_counter = 0


                is_enemy_running = True

        if is_player_running:
            if is_player_animating == False:
                # Animacja podbiegania do przeciwnika podczas ataku
                screen.blit(character_run[current_frame], (character_x, character_y))

                direction_vector = pygame.math.Vector2(enemy_x - 250 - character_x, enemy_y - character_y)
                if direction_vector.length() > 1:
                    direction_vector.normalize_ip()

                # Przesunięcie postaci zgodnie z wektorem kierunku i prędkością
                character_x += direction_vector.x * character_speed
                character_y += direction_vector.y * character_speed
                if character_x >= enemy_x - 250:
                    is_player_running = False
                    is_player_attacking = True
            elif is_enemy_animating == False:
                # Animacja podbiegania do przeciwnika podczas ataku
                screen.blit(character_run[current_frame], (enemy_x, enemy_y))

                direction_vector = pygame.math.Vector2(enemy_x_deafult - enemy_x, enemy_y_deafult-enemy_y)
                if direction_vector.length() > 1:
                    direction_vector.normalize_ip()

                # Przesunięcie postaci zgodnie z wektorem kierunku i prędkością
                enemy_x += direction_vector.x * character_speed
                enemy_y += direction_vector.y * character_speed
                if enemy_x == enemy_x_deafult:
                    is_player_running = False
                    is_enemy_animating = True

        if is_enemy_running:
            if is_player_animating == False:
                # Animacja podbiegania do przeciwnika podczas ataku
                screen.blit(mirrored_character_run[current_frame], (character_x, character_y))

                direction_vector = pygame.math.Vector2(character_x - character_x_deafult, character_y-character_y_deafult)
                if direction_vector.length() > 1:
                    direction_vector.normalize_ip()

                # Przesunięcie postaci zgodnie z wektorem kierunku i prędkością
                character_x -= direction_vector.x * character_speed
                character_y -= direction_vector.y * character_speed
                if character_x == character_x_deafult:
                    is_enemy_running = False
                    is_player_animating  = True
            elif is_enemy_animating == False:
                # Animacja podbiegania do przeciwnika podczas ataku
                screen.blit(mirrored_character_run[current_frame], (enemy_x, enemy_y))

                direction_vector = pygame.math.Vector2(character_x + 250 - enemy_x, character_y - enemy_y)
                if direction_vector.length() > 1:
                    direction_vector.normalize_ip()

                # Przesunięcie postaci zgodnie z wektorem kierunku i prędkością
                enemy_x += direction_vector.x * character_speed
                enemy_y += direction_vector.y * character_speed
                if enemy_x <= character_x + 250:
                    is_enemy_running = False
                    is_enemy_attacking = True

        if is_enemy_animating:
            screen.blit(mirrored_character_images[current_frame], (enemy_x, enemy_y))
            # Update the animation frame
            current_frame = (current_frame + 1) % len(character_images)
        
        
        if is_enemy_attacking:
            # Animacja ataku
            is_enemy_animating = False
            screen.blit(mirrored_character_attack[current_frame], (enemy_x, enemy_y))
            attack_counter += 1
            if attack_counter == 3:
                zycie_gracza -= 20
            if attack_counter >= attack_duration:
                is_enemy_attacking = False
                attack_counter = 0
                is_player_running = True
        
        offset = 15
        for i in range(screen_width + offset // floor_image.get_width()):
            screen_buffer.blit(floor_image, (i * floor_image.get_width() - i * offset, floor_height))
        
        screen_buffer.blit(resize_button_image, (30, floor_height + button_offset + 30))
        screen_buffer.blit(resize_button_image, (140, floor_height + button_offset + 30))
        screen_buffer.blit(resize_button_image, (250, floor_height + button_offset + 30))

        rock_text_rect = rock_text.get_rect(topleft=(55, floor_height + button_offset + text_offset))
        paper_text_rect = paper_text.get_rect(topleft=(160, floor_height  + button_offset + text_offset))
        scissors_text_rect = scissors_text.get_rect(topleft=(260, floor_height + button_offset + text_offset))

        screen_buffer.blit(rock_text, rock_text_rect)
        screen_buffer.blit(paper_text, paper_text_rect)
        screen_buffer.blit(scissors_text, scissors_text_rect)
        
        healt_bar(zycie_gracza, max_zycie_gracza, (45, 50))
        healt_bar(zycie_przeciwnika, max_zycie_przeciwnika, (750, 50), is_enemy=True)
        
        pygame.display.update()
        pygame.display.flip()
        clock.tick(animation_speed)
        screen.blit(screen_buffer, (0, 0))

        if zycie_gracza <= 0 or zycie_przeciwnika <= 0:
            screen.fill(BLACK)
            zycie_gracza = 0
            is_player_animating = False
            is_enemy_animating = False
            is_player_attacking = False
            is_enemy_animating = False
            zycie_przeciwnika = 0
            death_text = font.render("Game Over", True, WHITE)
            restart_text = font.render("Press R to restart", True, WHITE)
            main_menu_text = font.render("Main Menu", True, WHITE)
            death_text_rect = death_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
            restart_text_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
            main_menu_rect = main_menu_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
            screen.blit(death_text, death_text_rect)
            screen.blit(restart_text, restart_text_rect)
            screen.blit(main_menu_text, main_menu_rect)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if restart_text_rect.collidepoint(mouse_pos):
                        zycie_gracza = max_zycie_gracza
                        zycie_przeciwnika = max_zycie_przeciwnika
                        is_player_animating = True
                        is_enemy_animating = True
                    elif main_menu_rect.collidepoint(mouse_pos):
                        main_menu()            
        

    # END


def start_multiplayer_game():
    # Code for starting a multiplayer game goes here
    pass

# Call the main menu function to start the game
# Run the main menu
main_menu()
