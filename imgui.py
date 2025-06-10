import pygame

pygame.init()

window_w = 1920
window_h = 1080
screen = pygame.display.set_mode([window_w, window_h])

font_size = 16
font_16 = pygame.font.SysFont('Arial', font_size)

flags = {
    'input_keyboard': None,
    'input_mouse': None,
}

mouse = {
    'x': 0,
    'y': 0,
    'left_click_cur': 0,
    'left_click_old': 0,
}

def ui_frame(text, x, y, w, h, color_background, color_text, color_border):
    # update
    action = False
    '''
    if flags['input_mouse'] == 'clicked':
        x1 = x
        y1 = y
        x2 = x + w
        y2 = y + h
        if mouse['x'] >= x1 and mouse['y'] >= y1 and mouse['x'] < x2 and mouse['y'] < y2:
            flags['input_mouse'] = 'None'
            action = True
    '''
    # render
    pygame.draw.rect(screen, color_background, pygame.Rect(x, y, w, h))
    pygame.draw.rect(screen, color_border, pygame.Rect(x, y, w, h), 1)
    text_surface = font_16.render(text, False, color_text)
    screen.blit(text_surface, (x, y))
    return action

def ui_button(text, x, y, w, h, color_background, color_text):
    # update
    action = False
    if flags['input_mouse'] == 'clicked':
        x1 = x
        y1 = y
        x2 = x + w
        y2 = y + h
        if mouse['x'] >= x1 and mouse['y'] >= y1 and mouse['x'] < x2 and mouse['y'] < y2:
            flags['input_mouse'] = 'None'
            action = True
    # render
    pygame.draw.rect(screen, color_background, pygame.Rect(x, y, w, h))
    text_surface = font_16.render(text, False, color_text)
    screen.blit(text_surface, (x, y))
    # return action
    return action

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                flags['input_keyboard'] = 'space'

    mouse['x'], mouse['y'] = pygame.mouse.get_pos()
    mouse_left_press = pygame.mouse.get_pressed()[0]
    mouse['left_click_cur'] = mouse_left_press
    if mouse['left_click_cur'] == 1:
        if mouse['left_click_old'] != mouse['left_click_cur']:
            mouse['left_click_old'] = mouse['left_click_cur']
            flags['input_mouse'] = 'clicked'
    else:
        if mouse['left_click_old'] != mouse['left_click_cur']:
            mouse['left_click_old'] = mouse['left_click_cur']
            flags['input_mouse'] = 'released'

    screen.fill('#101010')

    x = 32
    y = 32
    # line = f"{mouse['x']}, {mouse['y']}"
    line = f"test"
    text_surface = font_16.render(line, False, (255, 255, 255))
    screen.blit(text_surface, (x, y))

    if ui_frame('', 0, 0, window_w, window_h, '#101010', '#ffffff', '#ffffff'):
        pass

    if ui_button('button 1', 100, 100, 100, 30, '#888888', '#ffffff'):
        print('button 1')

    if ui_button('button 2', 200, 200, 100, 30, '#ffffff', '#000000'):
        print('button 2')

    pygame.display.flip()

pygame.quit()
