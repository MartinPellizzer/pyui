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

textarea_1 = {
    'id': 0,
    'type': 'textarea',
    'lines': [
        'this is a sample text',
        'this is a sample text',
        'this is a sample text',
    ],
    'line_index': 0,
    'char_index': 0,
    'x': 0,
    'y': 0,
    'w': 500,
    'h': 500,
}

textarea_2 = {
    'id': 1,
    'type': 'textarea',
    'lines': [
        'this is a sample text',
    ],
    'line_index': 0,
    'char_index': 0,
    'x': 500,
    'y': 500,
    'w': 500,
    'h': 500,
}

components = []
components.append(textarea_1)
components.append(textarea_2)

component_focus_id = 1
component_focus = components[component_focus_id]

'''
lines = [
    'line 1',
    'line 2',
    'line 3',
]
line_index = 0
char_index = 0
'''

def cursor_update():
    x = component_focus['x']
    y = component_focus['y']
    _line_index = component_focus['line_index']
    _char_index = component_focus['char_index']
    _lines = component_focus['lines']
    text_prev = _lines[_line_index][:_char_index]
    w, h = font.size(text_prev)
    pygame.draw.rect(screen, '#ffffff', pygame.Rect(x+w, y+_line_index*50, 1, 50), 1)

def input_keybord_char(key_name):
    if len(key_name) == 1:
        _line_index = component_focus['line_index']
        _char_index = component_focus['char_index']
        _lines = component_focus['lines']
        text_prev = _lines[_line_index][:_char_index]
        text_next = _lines[_line_index][_char_index:]
        _lines[_line_index] = text_prev + key_name + text_next
        _char_index += 1
        component_focus['line_index'] = _line_index
        component_focus['char_index'] = _char_index

def input_keybord_space():
    _line_index = component_focus['line_index']
    _char_index = component_focus['char_index']
    _lines = component_focus['lines']
    text_prev = _lines[_line_index][:_char_index]
    text_next = _lines[_line_index][_char_index:]
    _lines[_line_index] = text_prev + ' ' + text_next
    _char_index += 1
    component_focus['line_index'] = _line_index
    component_focus['char_index'] = _char_index

def input_keybord_return():
    _line_index = component_focus['line_index']
    _char_index = component_focus['char_index']
    _lines = component_focus['lines']
    text_prev = _lines[_line_index][:_char_index]
    text_next = _lines[_line_index][_char_index:]
    _lines.append('')
    for _line_i in range(len(_lines)-1, _line_index, -1):
        _lines[_line_i] = _lines[_line_i-1]
    _lines[_line_index] = _lines[_line_index][:_char_index]
    _line_index += 1
    _lines[_line_index] = _lines[_line_index][_char_index:]
    _char_index = 0
    component_focus['line_index'] = _line_index
    component_focus['char_index'] = _char_index
    component_focus['lines'] = _lines

def input_keybord_delete():
    _line_index = component_focus['line_index']
    _char_index = component_focus['char_index']
    _lines = component_focus['lines']
    if _char_index < len(_lines[_line_index]): 
        _lines[_line_index] = _lines[_line_index][:_char_index] + _lines[_line_index][_char_index+1:]
    else:
        if len(_lines) > 1:
            for _line_i in range(_line_index, len(_lines)-1):
                if _line_i == _line_index:
                    _lines[_line_i] += _lines[_line_i+1]
                else:
                    _lines[_line_i] = _lines[_line_i+1]
            _lines = _lines[:-1]
    component_focus['line_index'] = _line_index
    component_focus['char_index'] = _char_index
    component_focus['lines'] = _lines

def input_keybord_backspace():
    _line_index = component_focus['line_index']
    _char_index = component_focus['char_index']
    _lines = component_focus['lines']
    if _char_index > 0: 
        _char_index -= 1
        _lines[_line_index] = _lines[_line_index][:_char_index] + _lines[_line_index][_char_index+1:]
    else:
        if _line_index > 0:
            _line_index -= 1
            _char_index = len(_lines[_line_index])
            for _line_i in range(_line_index, len(_lines)-1):
                _lines[_line_i] += _lines[_line_i+1]
                _lines[_line_i+1] = ''
            _lines = _lines[:-1]
    component_focus['line_index'] = _line_index
    component_focus['char_index'] = _char_index
    component_focus['lines'] = _lines

def input_keybord_up():
    _line_index = component_focus['line_index']
    _char_index = component_focus['char_index']
    _lines = component_focus['lines']
    if _line_index > 0: 
        _line_index -= 1
        if _char_index > len(_lines[_line_index]):
            _char_index = len(_lines[_line_index])
    component_focus['line_index'] = _line_index
    component_focus['char_index'] = _char_index
    component_focus['lines'] = _lines

def input_keybord_down():
    _line_index = component_focus['line_index']
    _char_index = component_focus['char_index']
    _lines = component_focus['lines']
    if _line_index < len(_lines)-1: 
        _line_index += 1
        if _char_index > len(_lines[_line_index]):
            _char_index = len(_lines[_line_index])
    component_focus['line_index'] = _line_index
    component_focus['char_index'] = _char_index
    component_focus['lines'] = _lines

def input_keybord_left_ctrl():
    _line_index = component_focus['line_index']
    _char_index = component_focus['char_index']
    _lines = component_focus['lines']
    if _char_index > 0: 
        for _char_i in range(_char_index-2, -1, -1):
            if _lines[_line_index][_char_i] == ' ':
                _char_index = _char_i+1
                break
        if _char_i == 0:
            _char_index = _char_i
    component_focus['line_index'] = _line_index
    component_focus['char_index'] = _char_index
    component_focus['lines'] = _lines

def input_keybord_left():
    _line_index = component_focus['line_index']
    _char_index = component_focus['char_index']
    _lines = component_focus['lines']
    if _char_index > 0: 
        _char_index -= 1
    component_focus['line_index'] = _line_index
    component_focus['char_index'] = _char_index
    component_focus['lines'] = _lines

def input_keybord_right_ctrl():
    _line_index = component_focus['line_index']
    _char_index = component_focus['char_index']
    _lines = component_focus['lines']
    if _char_index < len(_lines[_line_index]): 
        for _char_i in range(_char_index+1, len(_lines[_line_index]), 1):
            if _lines[_line_index][_char_i] == ' ':
                _char_index = _char_i
                break
        if _char_i == len(_lines[_line_index])-1:
            _char_index = _char_i+1
    component_focus['line_index'] = _line_index
    component_focus['char_index'] = _char_index
    component_focus['lines'] = _lines

def input_keybord_right():
    _line_index = component_focus['line_index']
    _char_index = component_focus['char_index']
    _lines = component_focus['lines']
    if _char_index < len(_lines[_line_index]): 
        _char_index += 1
    component_focus['line_index'] = _line_index
    component_focus['char_index'] = _char_index
    component_focus['lines'] = _lines

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_UP:
                input_keybord_up()
            elif event.key == pygame.K_DOWN:
                input_keybord_down()
            elif event.key == pygame.K_LEFT and pygame.key.get_mods() & pygame.KMOD_CTRL:
                input_keybord_left_ctrl()
            elif event.key == pygame.K_LEFT:
                input_keybord_left()
            elif event.key == pygame.K_RIGHT and pygame.key.get_mods() & pygame.KMOD_CTRL:
                input_keybord_right_ctrl()
            elif event.key == pygame.K_RIGHT:
                input_keybord_right()
            elif event.key == pygame.K_BACKSPACE:
                input_keybord_backspace()
            elif event.key == pygame.K_DELETE:
                input_keybord_delete()
            elif event.key == pygame.K_RETURN:
                input_keybord_return()
            elif event.key == pygame.K_SPACE:
                input_keybord_space()
            else:
                key_name = pygame.key.name(event.key)
                input_keybord_char(key_name)

    screen.fill('#101010')

    x, y = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0]:
        for component in components:
            x1 = component['x']
            y1 = component['y']
            x2 = component['x'] + component['w']
            y2 = component['y'] + component['h']
            if x >= x1 and y >= y1 and x < x2 and y < y2:
                component_focus_id = component['id']
                component_focus = components[component_focus_id]
                break

    cursor_update()

    for component in components:
        x = component['x']
        y = component['y']
        w = component['w']
        h = component['h']
        pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, w, h), 1)

        for line_i, line in enumerate(component['lines']):
            text_surface = font.render(line, False, (255, 255, 255))
            screen.blit(text_surface, (x, y+font_size*line_i))

    pygame.display.flip()

pygame.quit()

