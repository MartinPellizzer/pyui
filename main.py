###########################################
# TODO: manage ctrl in text area
###########################################

import pygame

pygame.init()

window_w = 1920
window_h = 1080

screen = pygame.display.set_mode([window_w, window_h])
font_size = 48
font = pygame.font.SysFont('Arial', font_size)

lines = [
    'line 1',
    'line 2',
    'line 3',
]
line_index = 0
char_index = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_UP:
                if line_index > 0: 
                    line_index -= 1
                    if char_index > len(lines[line_index]):
                        char_index = len(lines[line_index])
            elif event.key == pygame.K_DOWN:
                if line_index < len(lines)-1: 
                    line_index += 1
                    if char_index > len(lines[line_index]):
                        char_index = len(lines[line_index])
            elif event.key == pygame.K_LEFT and pygame.key.get_mods() & pygame.KMOD_CTRL:
                if char_index > 0: 
                    for char_i in range(char_index-2, -1, -1):
                        if lines[line_index][char_i] == ' ':
                            char_index = char_i+1
                            break
                    if char_i == 0:
                        char_index = char_i
            elif event.key == pygame.K_LEFT:
                if char_index > 0: 
                    char_index -= 1
            elif event.key == pygame.K_RIGHT and pygame.key.get_mods() & pygame.KMOD_CTRL:
                if char_index < len(lines[line_index]): 
                    for char_i in range(char_index+1, len(lines[line_index]), 1):
                        if lines[line_index][char_i] == ' ':
                            char_index = char_i
                            break
                    if char_i == len(lines[line_index])-1:
                        char_index = char_i+1
            elif event.key == pygame.K_RIGHT:
                if char_index < len(lines[line_index]): 
                    char_index += 1
            elif event.key == pygame.K_BACKSPACE:
                if char_index > 0: 
                    char_index -= 1
                    lines[line_index] = lines[line_index][:char_index] + lines[line_index][char_index+1:]
                else:
                    if line_index > 0:
                        line_index -= 1
                        char_index = len(lines[line_index])
                        for line_i in range(line_index, len(lines)-1):
                            lines[line_i] += lines[line_i+1]
                            lines[line_i+1] = ''
                        lines = lines[:-1]
            elif event.key == pygame.K_DELETE:
                if char_index < len(lines[line_index]): 
                    lines[line_index] = lines[line_index][:char_index] + lines[line_index][char_index+1:]
                else:
                    if len(lines) > 1:
                        for line_i in range(line_index, len(lines)-1):
                            if line_i == line_index:
                                lines[line_i] += lines[line_i+1]
                            else:
                                lines[line_i] = lines[line_i+1]
                        lines = lines[:-1]
            elif event.key == pygame.K_SPACE:
                lines[line_index] = lines[line_index][:char_index] + ' ' + lines[line_index][char_index:]
                char_index += 1
            elif event.key == pygame.K_RETURN:
                lines.append('')
                for line_i in range(len(lines)-1, line_index, -1):
                    lines[line_i] = lines[line_i-1]
                lines[line_index] = lines[line_index][:char_index]
                line_index += 1
                lines[line_index] = lines[line_index][char_index:]
                char_index = 0
            else:
                key_name = pygame.key.name(event.key)
                if len(key_name) == 1:
                    lines[line_index] = lines[line_index][:char_index] + key_name + lines[line_index][char_index:]
                    char_index += 1

    screen.fill('#101010')

    for line_i, line in enumerate(lines):
        text_surface = font.render(line, False, (255, 255, 255))
        screen.blit(text_surface, (0, font_size*line_i))

    substring = lines[line_index][:char_index]
    w, h = font.size(substring)
    pygame.draw.rect(screen, '#ffffff', pygame.Rect(w, line_index*50, 1, 50), 1)

    pygame.display.flip()

pygame.quit()
