import pygame
from gameGrid import Grid
from gameCell import Cell

pygame.init()

win_width = 600
win_height = 600
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Game of Life')

black = (0, 0, 0)
white = (255, 255, 255)
highlight_color = (255, 0, 0)
button_color = (0, 255, 0)
button_hover_color = (0, 200, 0)
stop_button_color = (255, 0, 0)
stop_button_hover_color = (200, 0, 0)
reset_button_color = (0, 0, 255)
reset_button_hover_color = (0, 0, 200)

cell_size = 10
cols, rows = win_width // cell_size, win_height // cell_size

grid = Grid(cols, rows, cell_size)

clock = pygame.time.Clock()
fps = 10

running = False

start_button_rect = pygame.Rect(win_width // 2 - 160, win_height - 50, 100, 40)
stop_button_rect = pygame.Rect(win_width // 2 - 50, win_height - 50, 100, 40)
reset_button_rect = pygame.Rect(win_width // 2 + 60, win_height - 50, 100, 40)

zoom_slider_rect = pygame.Rect(450, 10, 140, 20)
speed_slider_rect = pygame.Rect(450, 40, 140, 20)
zoom_slider_value = 10  # Initial value
speed_slider_value = 10
zoom_dragging = False
speed_dragging = False

def draw_slider(win, rect, value, max_value):
    pygame.draw.rect(win, white, rect, 2)
    fill_rect = rect.copy()
    fill_rect.width = rect.width * (value / max_value)
    pygame.draw.rect(win, white, fill_rect)

def draw_sliders(win):
    draw_slider(win, zoom_slider_rect, zoom_slider_value, 40)
    draw_slider(win, speed_slider_rect, speed_slider_value, 30)

def update_slider_value(x_pos, rect, max_value):
    relative_x = x_pos - rect.x
    value = max(1, min(max_value, (relative_x / rect.width) * max_value))
    return value

def handle_slider_event(event, dragging, rect, value, max_value):
    if event.type == pygame.MOUSEBUTTONDOWN and rect.collidepoint(event.pos):
        dragging = True
    elif event.type == pygame.MOUSEMOTION and dragging:
        value = update_slider_value(event.pos[0], rect, max_value)
    elif event.type == pygame.MOUSEBUTTONUP:
        dragging = False
    return dragging, value

def draw_buttons(win):
    mouse_pos = pygame.mouse.get_pos()

    start_color = button_hover_color if start_button_rect.collidepoint(mouse_pos) else button_color
    pygame.draw.rect(win, start_color, start_button_rect)
    font = pygame.font.SysFont(None, 24)
    start_text = font.render('Start', True, black)
    start_text_rect = start_text.get_rect(center=start_button_rect.center)
    win.blit(start_text, start_text_rect)

    stop_color = stop_button_hover_color if stop_button_rect.collidepoint(mouse_pos) else stop_button_color
    pygame.draw.rect(win, stop_color, stop_button_rect)
    stop_text = font.render('Stop', True, black)
    stop_text_rect = stop_text.get_rect(center=stop_button_rect.center)
    win.blit(stop_text, stop_text_rect)

    reset_color = reset_button_hover_color if reset_button_rect.collidepoint(mouse_pos) else reset_button_color
    pygame.draw.rect(win, reset_color, reset_button_rect)
    reset_text = font.render('Reset', True, black)
    reset_text_rect = reset_text.get_rect(center=reset_button_rect.center)
    win.blit(reset_text, reset_text_rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button_rect.collidepoint(event.pos):
                running = True
            elif stop_button_rect.collidepoint(event.pos):
                running = False
            elif reset_button_rect.collidepoint(event.pos):
                # Reset grid when the reset button is clicked and recreate it
                cell_size = int(zoom_slider_value)
                cols, rows = win_width // cell_size, win_height // cell_size
                grid = Grid(cols, rows, cell_size)  # Recreate the grid
            else:
                grid.handle_click(event.pos)

        zoom_dragging, zoom_slider_value = handle_slider_event(event, zoom_dragging, zoom_slider_rect, zoom_slider_value, 40)
        speed_dragging, speed_slider_value = handle_slider_event(event, speed_dragging, speed_slider_rect, speed_slider_value, 30)

    if running:
        grid.update()

    # Update cell_size based on slider value
    cell_size = max(5, int(zoom_slider_value))  # Minimum cell_size is 5
    cols, rows = win_width // cell_size, win_height // cell_size
    if cell_size != grid.cell_size:
        grid.resize(cols, rows, cell_size)

    fps = int(speed_slider_value)

    win.fill(black)
    grid.draw(win)
    draw_buttons(win)
    draw_sliders(win)
    pygame.display.update()
    clock.tick(fps)
