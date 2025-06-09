import pygame

pygame.init()

window_w = 1920
window_h = 1080

screen = pygame.display.set_mode([window_w, window_h])
font_size = 48
font = pygame.font.SysFont('Arial', font_size)

font_size = 16
font_16 = pygame.font.SysFont('Arial', font_size)

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

node_1 = {
    'id': 2,
    'type': 'node',
    'x': 300,
    'y': 300,
    'w': 300,
    'h': 300,
}

mouse = {
    'x': 0,
    'y': 0,
    'left_click_cur': 0,
    'left_click_old': 0,
    'left_click_drag': 0,
    'middle_click_cur': 0,
    'middle_click_old': 0,
    'middle_click_pan': 0,
    'right_click_cur': 0,
    'right_click_old': 0,
}

camera = {
    'x': 0,
    'y': 0,
    'zoom': 1,
    'x_start': 0,
    'y_start': 0,
}

components = []
# components.append(textarea_1)
# components.append(textarea_2)
# components.append(node_1)

component_active_id = -1
if component_active_id != -1: 
    component_active = components[component_active_id]
else: component_active = None

cursor = {
    'x': 0,
    'y': 0,
    'w': 1,
    'h': 50,
}

input_flags = {
    'control': 0,
}

edge_tmp = {
    'x1': 0,
    'y1': 0,
    'x2': 0,
    'y2': 0,
    'show': 0,
}

def draw_component_textarea(component):
    # ;jump
    x = component['x'] + camera['x']
    y = component['y'] + camera['y']
    w = component['w'] * camera['zoom']
    h = component['h'] * camera['zoom']
    pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, w, h), 1)
    font_size = 16 * camera['zoom']
    _font = pygame.font.SysFont('Arial', font_size)
    for line_i, line in enumerate(component['lines']):
        text_surface = _font.render(line, False, (255, 255, 255))
        text_w, text_h = _font.size(line)
        screen.blit(text_surface, (x, y+text_h*line_i))
    if component['id'] == component_active_id:
        pygame.draw.rect(screen, '#00ff00', pygame.Rect(x, y, w, h), 1)
    ### cursor
    x = cursor['x'] + camera['x']
    y = cursor['y'] + camera['y']
    w = cursor['w'] 
    h = cursor['h']
    pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, w, h), 1)

def draw_component_node(component):
    x = component['x']
    y = component['y']
    w = component['w']
    h = component['h']
    pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, w, h), 1)

def draw_components():
    for component in components:
        if component['type'] == '':
            pass
        elif component['type'] == 'textarea':
            draw_component_textarea(component)
        elif component['type'] == 'node':
            draw_component_node(component)
        elif component['type'] == 'label':
            component_label_draw(component)
        elif component['type'] == 'button':
            component_button_draw(component)
        elif component['type'] == 'image':
            component_image_draw(component)

def update_cursor():
    if component_active == None: return
    x = component_active['x']
    y = component_active['y']
    _line_index = component_active['line_index']
    _char_index = component_active['char_index']
    _lines = component_active['lines']
    text_prev = _lines[_line_index][:_char_index]
    w, h = font.size(text_prev)
    # w =
    # h =
    cursor['x'] = x+w
    cursor['y'] = y+_line_index*cursor['h']

def input_keybord_char(key_name):
    if len(key_name) == 1:
        _line_index = component_active['line_index']
        _char_index = component_active['char_index']
        _lines = component_active['lines']
        text_prev = _lines[_line_index][:_char_index]
        text_next = _lines[_line_index][_char_index:]
        _lines[_line_index] = text_prev + key_name + text_next
        _char_index += 1
        component_active['line_index'] = _line_index
        component_active['char_index'] = _char_index

def input_keybord_space():
    _line_index = component_active['line_index']
    _char_index = component_active['char_index']
    _lines = component_active['lines']
    text_prev = _lines[_line_index][:_char_index]
    text_next = _lines[_line_index][_char_index:]
    _lines[_line_index] = text_prev + ' ' + text_next
    _char_index += 1
    component_active['line_index'] = _line_index
    component_active['char_index'] = _char_index

def input_keybord_return():
    _line_index = component_active['line_index']
    _char_index = component_active['char_index']
    _lines = component_active['lines']
    text_prev = _lines[_line_index][:_char_index]
    text_next = _lines[_line_index][_char_index:]
    _lines.append('')
    for _line_i in range(len(_lines)-1, _line_index, -1):
        _lines[_line_i] = _lines[_line_i-1]
    _lines[_line_index] = _lines[_line_index][:_char_index]
    _line_index += 1
    _lines[_line_index] = _lines[_line_index][_char_index:]
    _char_index = 0
    component_active['line_index'] = _line_index
    component_active['char_index'] = _char_index
    component_active['lines'] = _lines

def input_keybord_delete():
    _line_index = component_active['line_index']
    _char_index = component_active['char_index']
    _lines = component_active['lines']
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
    component_active['line_index'] = _line_index
    component_active['char_index'] = _char_index
    component_active['lines'] = _lines

def input_keybord_backspace():
    _line_index = component_active['line_index']
    _char_index = component_active['char_index']
    _lines = component_active['lines']
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
    component_active['line_index'] = _line_index
    component_active['char_index'] = _char_index
    component_active['lines'] = _lines

def input_keybord_up():
    _line_index = component_active['line_index']
    _char_index = component_active['char_index']
    _lines = component_active['lines']
    if _line_index > 0: 
        _line_index -= 1
        if _char_index > len(_lines[_line_index]):
            _char_index = len(_lines[_line_index])
    component_active['line_index'] = _line_index
    component_active['char_index'] = _char_index
    component_active['lines'] = _lines

def input_keybord_down():
    _line_index = component_active['line_index']
    _char_index = component_active['char_index']
    _lines = component_active['lines']
    if _line_index < len(_lines)-1: 
        _line_index += 1
        if _char_index > len(_lines[_line_index]):
            _char_index = len(_lines[_line_index])
    component_active['line_index'] = _line_index
    component_active['char_index'] = _char_index
    component_active['lines'] = _lines

def input_keybord_left_ctrl():
    _line_index = component_active['line_index']
    _char_index = component_active['char_index']
    _lines = component_active['lines']
    if _char_index > 0: 
        for _char_i in range(_char_index-2, -1, -1):
            if _lines[_line_index][_char_i] == ' ':
                _char_index = _char_i+1
                break
        if _char_i == 0:
            _char_index = _char_i
    component_active['line_index'] = _line_index
    component_active['char_index'] = _char_index
    component_active['lines'] = _lines

def input_keybord_left():
    _line_index = component_active['line_index']
    _char_index = component_active['char_index']
    _lines = component_active['lines']
    if _char_index > 0: 
        _char_index -= 1
    component_active['line_index'] = _line_index
    component_active['char_index'] = _char_index
    component_active['lines'] = _lines

def input_keybord_right_ctrl():
    _line_index = component_active['line_index']
    _char_index = component_active['char_index']
    _lines = component_active['lines']
    if _char_index < len(_lines[_line_index]): 
        for _char_i in range(_char_index+1, len(_lines[_line_index]), 1):
            if _lines[_line_index][_char_i] == ' ':
                _char_index = _char_i
                break
        if _char_i == len(_lines[_line_index])-1:
            _char_index = _char_i+1
    component_active['line_index'] = _line_index
    component_active['char_index'] = _char_index
    component_active['lines'] = _lines

def input_keybord_right():
    _line_index = component_active['line_index']
    _char_index = component_active['char_index']
    _lines = component_active['lines']
    if _char_index < len(_lines[_line_index]): 
        _char_index += 1
    component_active['line_index'] = _line_index
    component_active['char_index'] = _char_index
    component_active['lines'] = _lines

def input_keybord_textarea_add():
    global components
    if components != []: id_next = components[-1]['id'] + 1
    else: id_next = 0
    # ;jump
    line = 'enter note here'
    font_size = 16 * camera['zoom']
    _font = pygame.font.SysFont('Arial', font_size)
    text_surface = _font.render(line, False, (255, 255, 255))
    text_w, text_h = _font.size(line)
    textarea = {
        'id': id_next,
        'type': 'textarea',
        'lines': [line],
        'line_index': 0,
        'char_index': 0,
        'x': mouse['x'],
        'y': mouse['y'],
        'w': text_w,
        'h': text_h,
    }
    components.append(textarea)

def component_active_update():
    global component_active
    global component_active_id
    x, y = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0]:
        found = False
        for component in components:
            x1 = component['x'] + camera['x']
            y1 = component['y'] + camera['y']
            x2 = x1 + (component['w'] * camera['zoom'])
            y2 = y1 + (component['h'] * camera['zoom'])
            if x >= x1 and y >= y1 and x < x2 and y < y2:
                component_active_id = component['id']
                component_active = components[component_active_id]
                found = True
                break
        if not found:
            component_active_id = -1
            component_active = None

def input_mouse_left_click():
    if component_active != None:
        if component_active['type'] == 'textarea':
            if input_flags['control'] == 1:
                mouse['x_start'] = mouse['x']
                mouse['y_start'] = mouse['y']
                edge_tmp['show'] = 1
            else:
                mouse['left_click_drag'] = 1
                mouse['x_start'] = mouse['x']
                mouse['y_start'] = mouse['y']
                component_active['x_start'] = component_active['x']
                component_active['y_start'] = component_active['y']

def input_mouse_left_release():
    mouse['left_click_drag'] = 0
    edge_tmp['show'] = 0

def input_mouse_middle():
    mouse_middle_press = pygame.mouse.get_pressed()[1]
    if mouse_middle_press == True:
        mouse['middle_click_cur'] = 1
        if mouse['middle_click_old'] != mouse['middle_click_cur']:
            mouse['middle_click_old'] = mouse['middle_click_cur']
            mouse['middle_click_pan'] = 1
            mouse['x_pan_start'] = mouse['x']
            mouse['y_pan_start'] = mouse['y']
            camera['x_start'] = camera['x']
            camera['y_start'] = camera['y']
    else:
        mouse['middle_click_cur'] = 0
        if mouse['middle_click_old'] != mouse['middle_click_cur']:
            mouse['middle_click_old'] = mouse['middle_click_cur']
            mouse['middle_click_pan'] = 0
    if mouse['middle_click_pan'] == 1:
        camera['x'] = camera['x_start'] + (mouse['x'] - mouse['x_pan_start'])
        camera['y'] = camera['y_start'] + (mouse['y'] - mouse['y_pan_start'])

def input_mouse_right():
    mouse_press = pygame.mouse.get_pressed()[2]
    mouse['right_click_cur'] = mouse_press
    if mouse['right_click_cur'] == 1:
        if mouse['right_click_old'] != mouse['right_click_cur']:
            mouse['right_click_old'] = mouse['right_click_cur']
            input_keybord_textarea_add()
    else:
        if mouse['right_click_old'] != mouse['right_click_cur']:
            mouse['right_click_old'] = mouse['right_click_cur']

def input_mouse_left():
    mouse_left_press = pygame.mouse.get_pressed()[0]
    # mouse['left_press_cur'] = mouse_left_press
    mouse['left_click_cur'] = mouse_left_press
    if mouse['left_click_cur'] == 1:
        if mouse['left_click_old'] != mouse['left_click_cur']:
            mouse['left_click_old'] = mouse['left_click_cur']
            component_active_update()
            input_mouse_left_click()
    else:
        if mouse['left_click_old'] != mouse['left_click_cur']:
            mouse['left_click_old'] = mouse['left_click_cur']
            input_mouse_left_release()
    if mouse['left_click_drag'] == 1:
        component_active['x'] = component_active['x_start'] + (mouse['x'] - mouse['x_start'])
        component_active['y'] = component_active['y_start'] + (mouse['y'] - mouse['y_start'])

def input_mouse():
    mouse['x'], mouse['y'] = pygame.mouse.get_pos()
    input_mouse_left()
    input_mouse_middle()
    input_mouse_right()

def input_events():
    global running
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
            elif event.key == pygame.K_KP_PLUS:
                pass
            else:
                key_name = pygame.key.name(event.key)
                input_keybord_char(key_name)
            if event.key == pygame.K_LCTRL:
                input_flags['control'] = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL:
                input_flags['control'] = 0
        if event.type == pygame.MOUSEWHEEL:
            if event.y == -1:
                if camera['zoom'] > 1:
                    camera['zoom'] -= 1
            else:
                if camera['zoom'] < 32:
                    camera['zoom'] += 1

def input_main():
    input_events()
    update_cursor()
    input_mouse()

def draw_edge_tmp():
    if edge_tmp['show'] == 1:
        edge_tmp['x1'] = mouse['x_start']
        edge_tmp['y1'] = mouse['y_start']
        edge_tmp['x2'] = mouse['x']
        edge_tmp['y2'] = mouse['y']
        x1 = edge_tmp['x1']
        y1 = edge_tmp['y1']
        x2 = edge_tmp['x2']
        y2 = edge_tmp['y2']
        pygame.draw.line(screen, '#ffffff', (x1, y1), (x2, y2), 1)

def draw_main():
    screen.fill('#101010')
    draw_components()
    draw_edge_tmp()
    pygame.display.flip()

running = True
while running:
    input_main()
    draw_main()

pygame.quit()

