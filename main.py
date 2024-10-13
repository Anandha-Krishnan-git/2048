import pygame
import sys
import time
from logic import Game2048
from ai import AI2048
pygame.init()

WIDTH, HEIGHT = 400, 500
GRID_SIZE = 4
CELL_SIZE = WIDTH // GRID_SIZE
FONT = pygame.font.Font(None, 36)
SMALL_FONT = pygame.font.Font(None, 24)

# Colors
BACKGROUND_COLOR = (187, 173, 160)
EMPTY_CELL_COLOR = (205, 193, 180)
TILE_COLORS = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

# Add this new constant for the button
STOP_BUTTON_COLOR = (200, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 Game")

def draw_tile(value, x, y, size):
    pygame.draw.rect(screen, TILE_COLORS.get(value, (237, 194, 46)), (x, y, size, size))
    if value:
        font_size = 36 if value < 100 else 24 if value < 1000 else 18
        font = pygame.font.Font(None, font_size)
        text = font.render(str(value), True, (0, 0, 0))
        text_rect = text.get_rect(center=(x + size // 2, y + size // 2))
        screen.blit(text, text_rect)

def draw_stop_button():
    button_width = 80
    button_height = 30
    button_x = WIDTH - button_width - 10
    button_y = HEIGHT - button_height - 10
    pygame.draw.rect(screen, STOP_BUTTON_COLOR, (button_x, button_y, button_width, button_height))
    stop_text = SMALL_FONT.render("STOP", True, (255, 255, 255))
    text_rect = stop_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(stop_text, text_rect)
    return pygame.Rect(button_x, button_y, button_width, button_height)

def draw_game(game, animations):
    screen.fill(BACKGROUND_COLOR)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x = j * CELL_SIZE
            y = i * CELL_SIZE
            pygame.draw.rect(screen, EMPTY_CELL_COLOR, (x, y, CELL_SIZE, CELL_SIZE))
    
    for (i, j), (value, progress) in animations.items():
        x = j * CELL_SIZE
        y = i * CELL_SIZE
        size = int(CELL_SIZE * progress)
        draw_tile(value, x + (CELL_SIZE - size) // 2, y + (CELL_SIZE - size) // 2, size)
    
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = game.grid[i][j]
            if value and (i, j) not in animations:
                x = j * CELL_SIZE
                y = i * CELL_SIZE
                draw_tile(value, x, y, CELL_SIZE)
    
    score_text = FONT.render(f"Score: {game.score}", True, (0, 0, 0))
    screen.blit(score_text, (10, HEIGHT - 40))
    
    stop_button_rect = draw_stop_button()
    
    pygame.display.flip()
    return stop_button_rect

def animate(animations):
    start_time = time.time()
    while animations:
        current_time = time.time()
        for key, (value, progress) in list(animations.items()):
            if value==0:
                del animations[key]
                continue
            progress = min((current_time - start_time) * 5, 1.0)
            animations[key] = (value, progress)
            if progress == 1.0:
                del animations[key]
        draw_game(game, animations)
        pygame.time.wait(20)

def main_menu():
    clock = pygame.time.Clock()
    while True:
        screen.fill(BACKGROUND_COLOR)
        title = FONT.render("2048", True, (0, 0, 0))
        play_button = FONT.render("Play", True, (0, 0, 0))
        ai_play_button = FONT.render("AI Play", True, (0, 0, 0))
        exit_button = FONT.render("Exit", True, (0, 0, 0))
        
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        screen.blit(play_button, (WIDTH // 2 - play_button.get_width() // 2, 200))
        screen.blit(ai_play_button, (WIDTH // 2 - ai_play_button.get_width() // 2, 250))
        screen.blit(exit_button, (WIDTH // 2 - exit_button.get_width() // 2, 300))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if WIDTH // 2 - play_button.get_width() // 2 <= mouse_pos[0] <= WIDTH // 2 + play_button.get_width() // 2:
                    if 200 <= mouse_pos[1] <= 200 + play_button.get_height():
                        return "play"
                    elif 250 <= mouse_pos[1] <= 250 + ai_play_button.get_height():
                        return "ai_play"
                    elif 300 <= mouse_pos[1] <= 300 + exit_button.get_height():
                        return "exit"
        
        clock.tick(60)  # Limit the frame rate to 60 FPS

def game_over_menu(score):
    clock = pygame.time.Clock()
    while True:
        screen.fill(BACKGROUND_COLOR)
        game_over_text = FONT.render("Game Over!", True, (0, 0, 0))
        score_text = FONT.render(f"Score: {score}", True, (0, 0, 0))
        play_again_button = FONT.render("Play Again", True, (0, 0, 0))
        ai_play_button = FONT.render("AI Play", True, (0, 0, 0))
        exit_button = FONT.render("Exit", True, (0, 0, 0))
        
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 100))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 150))
        screen.blit(play_again_button, (WIDTH // 2 - play_again_button.get_width() // 2, 200))
        screen.blit(ai_play_button, (WIDTH // 2 - ai_play_button.get_width() // 2, 250))
        screen.blit(exit_button, (WIDTH // 2 - exit_button.get_width() // 2, 300))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if WIDTH // 2 - play_again_button.get_width() // 2 <= mouse_pos[0] <= WIDTH // 2 + play_again_button.get_width() // 2:
                    if 200 <= mouse_pos[1] <= 200 + play_again_button.get_height():
                        return "play"
                    elif 250 <= mouse_pos[1] <= 250 + ai_play_button.get_height():
                        return "ai_play"
                    elif 300 <= mouse_pos[1] <= 300 + exit_button.get_height():
                        return "exit"
        
        clock.tick(60)  

def main():
    global game  # Make game a global variable so it can be accessed in draw_game
    
    while True:  # Outer loop for the entire game
        choice = main_menu()
        if choice == "exit":
            pygame.quit()
            sys.exit()
        
        game = Game2048()
        ai = AI2048()
        clock = pygame.time.Clock()
        ai_mode = choice == "ai_play"
        
        animations = {}
        
        game_running = True
        while game_running:  # Inner loop for each game session
            stop_button_rect = draw_game(game, animations)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if stop_button_rect.collidepoint(event.pos):
                        game_running = False  # Break the inner loop to return to main menu
                        break
                elif event.type == pygame.KEYDOWN and not ai_mode:
                    if event.key == pygame.K_UP:
                        moved, merged = game.move(0)
                    elif event.key == pygame.K_RIGHT:
                        moved, merged = game.move(1)
                    elif event.key == pygame.K_DOWN:
                        moved, merged = game.move(2)
                    elif event.key == pygame.K_LEFT:
                        moved, merged = game.move(3)
                    else:
                        moved, merged = False, []
                    
                    if moved:
                        animations.update({pos: (game.grid[pos[0]][pos[1]], 0) for pos in merged})
                        animations[game.last_new_tile] = (game.grid[game.last_new_tile[0]][game.last_new_tile[1]], 0)
            
            if ai_mode and game_running:
                move = ai.get_best_move(game)
                moved, merged = game.move(move)
                if moved:
                    animations.update({pos: (game.grid[pos[0]][pos[1]], 0) for pos in merged})
                    animations[game.last_new_tile] = (game.grid[game.last_new_tile[0]][game.last_new_tile[1]], 0)
            
            if animations:
                animate(animations)
            
            if game.is_game_over() and game_running:
                choice = game_over_menu(game.score)
                if choice == "exit":
                    pygame.quit()
                    sys.exit()
                elif choice == "play":
                    break  # Break the inner loop to start a new game
                elif choice == "ai_play":
                    ai_mode = True
                    game = Game2048()
            
            clock.tick(60)  # Limit to 60 FPS

if __name__ == "__main__":
    main()
