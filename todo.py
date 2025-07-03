import pygame
import sys
import datetime

# Pygame-i işə sal
pygame.init()

# Ekran ölçüləri
WIDTH = 800
HEIGHT = 600

# Rənglər
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (70, 130, 180)
RED = (220, 20, 60)
GREEN = (60, 179, 113)
LIGHT_GREEN = (144, 238, 144)

# Fontlar
font_small = pygame.font.SysFont('Arial', 20)
font_medium = pygame.font.SysFont('Arial', 24)
font_large = pygame.font.SysFont('Arial', 32)

# TODO maddələri
todos = []
input_text = ""
input_active = False
edit_index = None

# Ekran yarat
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TODO Proqramı")

def draw_todo_list():
    # Arxa fon
    screen.fill(WHITE)
    
    # Başlıq
    title = font_large.render("TODO List", True, BLUE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
    
    # Tarix
    now = datetime.datetime.now()
    date_text = now.strftime("%d.%m.%Y %H:%M")
    date_surface = font_medium.render(date_text, True, BLACK)
    screen.blit(date_surface, (WIDTH - date_surface.get_width() - 20, 25))
    
    # Giriş sahəsi
    pygame.draw.rect(screen, GRAY if input_active else WHITE, (50, 80, WIDTH-100, 40))
    pygame.draw.rect(screen, BLUE, (50, 80, WIDTH-100, 40), 2)
    
    text_surface = font_medium.render(input_text, True, BLACK)
    screen.blit(text_surface, (60, 87))
    
    # Əlavə et/Təyin et düyməsi
    btn_text = "Təyin Et" if edit_index is not None else "Elave Et"
    pygame.draw.rect(screen, GREEN, (WIDTH-150, 130, 100, 35))
    text_btn = font_medium.render(btn_text, True, WHITE)
    screen.blit(text_btn, (WIDTH-150 + (100 - text_btn.get_width())//2, 135))
    
    # TODO maddələri
    for i, todo in enumerate(todos):
        y_pos = 180 + i * 50
        
        # Maddə mətni
        text = font_medium.render(todo, True, BLACK)
        screen.blit(text, (60, y_pos))
        
        # Sil düyməsi
        pygame.draw.rect(screen, RED, (WIDTH-150, y_pos, 100, 35))
        text_del = font_medium.render("Sil", True, WHITE)
        screen.blit(text_del, (WIDTH-150 + (100 - text_del.get_width())//2, y_pos+5))
        
        # Düzəlt düyməsi
        pygame.draw.rect(screen, BLUE, (WIDTH-260, y_pos, 100, 35))
        text_edit = font_medium.render("Düzelt", True, WHITE)
        screen.blit(text_edit, (WIDTH-260 + (100 - text_edit.get_width())//2, y_pos+5))

def add_or_update_todo():
    global input_text, edit_index
    if input_text.strip():
        if edit_index is not None:
            todos[edit_index] = input_text
            edit_index = None
        else:
            todos.append(input_text)
        input_text = ""

def delete_todo(index):
    global todos
    if 0 <= index < len(todos):
        todos.pop(index)

def edit_todo(index):
    global input_text, edit_index
    if 0 <= index < len(todos):
        input_text = todos[index]
        edit_index = index

# Əsas proqram döngüsü
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Giriş sahəsini aktivləşdir
            if 50 <= event.pos[0] <= WIDTH-50 and 80 <= event.pos[1] <= 120:
                input_active = True
            else:
                input_active = False
            
            # Əlavə et/Təyin et düyməsi
            if WIDTH-150 <= event.pos[0] <= WIDTH-50 and 130 <= event.pos[1] <= 165:
                add_or_update_todo()
            
            # TODO maddələri üzərində əməliyyatlar
            for i in range(len(todos)):
                y_pos = 180 + i * 50
                
                # Sil düyməsi
                if WIDTH-150 <= event.pos[0] <= WIDTH-50 and y_pos <= event.pos[1] <= y_pos+35:
                    delete_todo(i)
                    break
                
                # Düzəlt düyməsi
                if WIDTH-260 <= event.pos[0] <= WIDTH-160 and y_pos <= event.pos[1] <= y_pos+35:
                    edit_todo(i)
                    break
        
        elif event.type == pygame.KEYDOWN:
            if input_active:
                if event.key == pygame.K_RETURN:
                    add_or_update_todo()
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
    
    draw_todo_list()
    pygame.display.flip()
