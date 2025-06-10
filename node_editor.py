# TODO: fix mouse wheel press and scroll at the same time, it gives bugs

import json
import pygame

pygame.init()

window_w = 1920
window_h = 1080

screen = pygame.display.set_mode([window_w, window_h])
font_size = 48
font = pygame.font.SysFont('Arial', font_size)

font_size = 16
font_16 = pygame.font.SysFont('Arial', font_size)
font_size = 32
font_32 = pygame.font.SysFont('Arial', font_size)
font_size = 48
font_48 = pygame.font.SysFont('Arial', font_size)
font_size = 64
font_64 = pygame.font.SysFont('Arial', font_size)
fonts = []
fonts.append(font_16)
fonts.append(font_32)
fonts.append(font_48)
fonts.append(font_64)

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
    'zoom': 1,
    'x': 0,
    'y': 0,
    'x_start': 0,
    'y_start': 0,
    'x_abs': 0,
    'y_abs': 0,
    'x_abs_start': 0,
    'y_abs_start': 0,
}

node_example = {
    'id': 1,
    'lines': ['this is a sample text',],
    'line_index': 0,
    'char_index': 0,
    'x': 500,
    'y': 500,
    'w': 500,
    'h': 500,
}

edge_example = {
    'id_1': -1,
    'id_2': -1,
    'x1': 100,
    'y1': 100,
    'x2': 400,
    'y2': 200,
}

edge_tmp = {
    'id_1': -1,
    'id_2': -1,
    'x1': 0,
    'y1': 0,
    'x2': 0,
    'y2': 0,
    'show': 0,
}

nodes = []
edges = []

node_active_id = -1
if node_active_id != -1: 
    node_active = [node for node in nodes if node['id'] == node_active_id][0]
else: node_active = None

cursor = {
    'x': 0,
    'y': 0,
    'w': 1,
    'h': 16,
}

input_flags = {
    'control': 0,
}

def update_cursor():
    if node_active == None: return
    node_x, node_y = node_pos_get(node_active)
    _line_index = node_active['line_index']
    _char_index = node_active['char_index']
    _lines = node_active['lines']
    text_prev = _lines[_line_index][:_char_index]
    _font = fonts[camera['zoom']-1]
    w, h = _font.size(text_prev)
    line = _lines[0]
    line_w, line_h = _font.size(line)
    cursor['x'] = node_x + w
    cursor['y'] = node_y + line_h*_line_index

def input_keybord_char(key_name):
    if len(key_name) == 1:
        _line_index = node_active['line_index']
        _char_index = node_active['char_index']
        _lines = node_active['lines']
        text_prev = _lines[_line_index][:_char_index]
        text_next = _lines[_line_index][_char_index:]
        _lines[_line_index] = text_prev + key_name + text_next
        _char_index += 1
        node_active['line_index'] = _line_index
        node_active['char_index'] = _char_index

def input_keybord_space():
    _line_index = node_active['line_index']
    _char_index = node_active['char_index']
    _lines = node_active['lines']
    text_prev = _lines[_line_index][:_char_index]
    text_next = _lines[_line_index][_char_index:]
    _lines[_line_index] = text_prev + ' ' + text_next
    _char_index += 1
    node_active['line_index'] = _line_index
    node_active['char_index'] = _char_index

def input_keybord_return():
    _line_index = node_active['line_index']
    _char_index = node_active['char_index']
    _lines = node_active['lines']
    text_prev = _lines[_line_index][:_char_index]
    text_next = _lines[_line_index][_char_index:]
    _lines.append('')
    for _line_i in range(len(_lines)-1, _line_index, -1):
        _lines[_line_i] = _lines[_line_i-1]
    _lines[_line_index] = _lines[_line_index][:_char_index]
    _line_index += 1
    _lines[_line_index] = _lines[_line_index][_char_index:]
    _char_index = 0
    node_active['line_index'] = _line_index
    node_active['char_index'] = _char_index
    node_active['lines'] = _lines

def input_keybord_delete():
    _line_index = node_active['line_index']
    _char_index = node_active['char_index']
    _lines = node_active['lines']
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
    node_active['line_index'] = _line_index
    node_active['char_index'] = _char_index
    node_active['lines'] = _lines

def input_keybord_backspace():
    _line_index = node_active['line_index']
    _char_index = node_active['char_index']
    _lines = node_active['lines']
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
    node_active['line_index'] = _line_index
    node_active['char_index'] = _char_index
    node_active['lines'] = _lines

def input_keybord_up():
    _line_index = node_active['line_index']
    _char_index = node_active['char_index']
    _lines = node_active['lines']
    if _line_index > 0: 
        _line_index -= 1
        if _char_index > len(_lines[_line_index]):
            _char_index = len(_lines[_line_index])
    node_active['line_index'] = _line_index
    node_active['char_index'] = _char_index
    node_active['lines'] = _lines

def input_keybord_down():
    _line_index = node_active['line_index']
    _char_index = node_active['char_index']
    _lines = node_active['lines']
    if _line_index < len(_lines)-1: 
        _line_index += 1
        if _char_index > len(_lines[_line_index]):
            _char_index = len(_lines[_line_index])
    node_active['line_index'] = _line_index
    node_active['char_index'] = _char_index
    node_active['lines'] = _lines

def input_keybord_left_ctrl():
    _line_index = node_active['line_index']
    _char_index = node_active['char_index']
    _lines = node_active['lines']
    if _char_index > 0: 
        for _char_i in range(_char_index-2, -1, -1):
            if _lines[_line_index][_char_i] == ' ':
                _char_index = _char_i+1
                break
        if _char_i == 0:
            _char_index = _char_i
    node_active['line_index'] = _line_index
    node_active['char_index'] = _char_index
    node_active['lines'] = _lines

def input_keybord_left():
    _line_index = node_active['line_index']
    _char_index = node_active['char_index']
    _lines = node_active['lines']
    if _char_index > 0: 
        _char_index -= 1
    node_active['line_index'] = _line_index
    node_active['char_index'] = _char_index
    node_active['lines'] = _lines

def input_keybord_right_ctrl():
    _line_index = node_active['line_index']
    _char_index = node_active['char_index']
    _lines = node_active['lines']
    if _char_index < len(_lines[_line_index]): 
        for _char_i in range(_char_index+1, len(_lines[_line_index]), 1):
            if _lines[_line_index][_char_i] == ' ':
                _char_index = _char_i
                break
        if _char_i == len(_lines[_line_index])-1:
            _char_index = _char_i+1
    node_active['line_index'] = _line_index
    node_active['char_index'] = _char_index
    node_active['lines'] = _lines

def input_keybord_right():
    _line_index = node_active['line_index']
    _char_index = node_active['char_index']
    _lines = node_active['lines']
    if _char_index < len(_lines[_line_index]): 
        _char_index += 1
    node_active['line_index'] = _line_index
    node_active['char_index'] = _char_index
    node_active['lines'] = _lines

def input_keybord_node_add():
    global nodes
    if nodes != []: id_next = nodes[-1]['id'] + 1
    else: id_next = 0
    # ;jump
    line = 'enter note here'
    _font = fonts[camera['zoom']-1]
    text_surface = _font.render(line, False, (255, 255, 255))
    text_w, text_h = _font.size(line)
    node = {
        'id': id_next,
        'lines': [line],
        'line_index': 0,
        'char_index': 0,
        'x_start': (mouse['x'] - camera['x'])//camera['zoom'],
        'y_start': (mouse['y'] - camera['y'])//camera['zoom'],
        'x': (mouse['x'] - camera['x'])//camera['zoom'],
        'y': (mouse['y'] - camera['y'])//camera['zoom'],
        'w': text_w//camera['zoom'],
        'h': text_h//camera['zoom'],
    }
    nodes.append(node)

def node_delete():
    global nodes
    global edges
    global node_active_id
    global node_active
    if node_active != None:
        edges_remove = []
        for edge_i, edge in enumerate(edges):
            if edge['id_1'] == node_active['id'] or edge['id_2'] == node_active['id']:
                edges_remove.append(edge)
        edges = [edge for edge in edges if edge not in edges_remove]
        for node_i, node in enumerate(nodes):
            if node['id'] == node_active['id']:
                del nodes[node_i]
                break
        node_active_id = -1
        node_active = None
            
def node_active_update():
    global node_active
    global node_active_id
    x = mouse['x']
    y = mouse['y']
    if pygame.mouse.get_pressed()[0]:
        found = False
        for node in nodes:
            x1, y1, x2, y2 = node_bounding_box_get(node)
            if x >= x1 and y >= y1 and x < x2 and y < y2:
                node_active_id = node['id']
                node_active = [node for node in nodes if node['id'] == node_active_id][0]
                found = True
                break
        if not found:
            node_active_id = -1
            node_active = None

def input_mouse_left_click():
    if node_active != None:
        ### create edge
        if input_flags['control'] == 1:
            node_start = node_active
            edge_tmp['id_1'] = node_start['id']
            edge_tmp['x1'] = node_start['x']
            edge_tmp['y1'] = node_start['y']
            mouse['x_start'] = mouse['x']
            mouse['y_start'] = mouse['y']
            edge_tmp['show'] = 1
        else:
            mouse['left_click_drag'] = 1
            mouse['x_start'] = mouse['x']
            mouse['y_start'] = mouse['y']
            node_active['x_start'] = node_active['x']
            node_active['y_start'] = node_active['y']

def input_mouse_left_release():
    mouse['left_click_drag'] = 0
    if edge_tmp['show'] == 1:
        node_end = None
        for node in nodes:
            x = mouse['x']
            y = mouse['y']
            x1 = node['x'] + camera['x']
            y1 = node['y'] + camera['y']
            x2 = x1 + (node['w'] * camera['zoom'])
            y2 = y1 + (node['h'] * camera['zoom'])
            if x >= x1 and y >= y1 and x < x2 and y < y2:
                node_active_id = node['id']
                node_active = [node for node in nodes if node['id'] == node_active_id][0]
                node_end = node_active
                break
        if node_end != None:
            edge_tmp['id_2'] = node_end['id']
            edge_tmp['x2'] = node_end['x']
            edge_tmp['y2'] = node_end['y']
            edge_new = {
                'id_1': edge_tmp['id_1'],
                'id_2': edge_tmp['id_2'],
                'x1': edge_tmp['x1'],
                'y1': edge_tmp['y1'],
                'x2': edge_tmp['x2'],
                'y2': edge_tmp['y2'],
            }
            edges.append(edge_new)
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
            camera['x_abs_start'] = camera['x_abs']
            camera['y_abs_start'] = camera['y_abs']
    else:
        mouse['middle_click_cur'] = 0
        if mouse['middle_click_old'] != mouse['middle_click_cur']:
            mouse['middle_click_old'] = mouse['middle_click_cur']
            mouse['middle_click_pan'] = 0
    if mouse['middle_click_pan'] == 1:
        camera['x'] = camera['x_start'] + (mouse['x'] - mouse['x_pan_start'])
        camera['y'] = camera['y_start'] + (mouse['y'] - mouse['y_pan_start'])
        camera['x_abs'] = camera['x_abs_start'] + (mouse['x'] - mouse['x_pan_start'])//camera['zoom']
        camera['y_abs'] = camera['y_abs_start'] + (mouse['y'] - mouse['y_pan_start'])//camera['zoom']

def input_mouse_right():
    mouse_press = pygame.mouse.get_pressed()[2]
    mouse['right_click_cur'] = mouse_press
    if mouse['right_click_cur'] == 1:
        if mouse['right_click_old'] != mouse['right_click_cur']:
            mouse['right_click_old'] = mouse['right_click_cur']
            input_keybord_node_add()
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
            node_active_update()
            input_mouse_left_click()
    else:
        if mouse['left_click_old'] != mouse['left_click_cur']:
            mouse['left_click_old'] = mouse['left_click_cur']
            input_mouse_left_release()
    if mouse['left_click_drag'] == 1:
        node_active['x'] = node_active['x_start'] + (mouse['x'] - mouse['x_start']) // camera['zoom']
        node_active['y'] = node_active['y_start'] + (mouse['y'] - mouse['y_start']) // camera['zoom']

def input_mouse():
    mouse['x'], mouse['y'] = pygame.mouse.get_pos()
    input_mouse_left()
    input_mouse_middle()
    input_mouse_right()

def project_save():
    filepath = f'data.json'
    data = {
        'nodes': nodes,
        'edges': edges,
    }
    j = json.dumps(data, indent=4)
    with open(filepath, 'w') as f:
        print(j, file=f)

def project_load():
    global nodes
    global edges
    filepath = f'data.json'
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    nodes = data['nodes']
    edges = data['edges']

def input_events():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                project_save()
            elif event.key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_CTRL:
                project_load()
            elif event.key == pygame.K_DELETE and pygame.key.get_mods() & pygame.KMOD_CTRL:
                node_delete()
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
            offset_x = window_w//2 - camera['x_abs']
            offset_y = window_h//2 - camera['y_abs']
            if event.y == -1:
                if camera['zoom'] > 1:
                    camera['zoom'] -= 1
                    camera['x'] += offset_x
                    camera['y'] += offset_y
            else:
                if camera['zoom'] < len(fonts):
                    camera['zoom'] += 1
                    camera['x'] -= offset_x
                    camera['y'] -= offset_y

def input_main():
    input_events()
    update_cursor()
    input_mouse()

def draw_edges():
    for edge in edges:
        id_1 = edge['id_1']
        id_2 = edge['id_2']
        id_1_found = False
        id_2_found = False
        for node in nodes:
            if not id_1_found:
                if node['id'] == id_1:
                    start_x, start_y, start_w, start_h = node_rect_get(node)
                    start_x += start_w//2
                    start_y += start_h//2
                    id_1_found = True
            if not id_2_found:
                if node['id'] == id_2:
                    end_x, end_y, end_w, end_h = node_rect_get(node)
                    end_x += end_w//2
                    end_y += end_h//2
                    id_2_found = True
            if id_1_found and id_2_found:
                break
        pygame.draw.line(screen, '#ffffff', (start_x, start_y), (end_x, end_y), 1)

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

def node_bounding_box_get(node):
    text_w, text_h = node_text_size_get(node)
    x1, y1 = node_pos_get(node)
    x2 = x1 + text_w
    y2 = y1 + text_h
    return [x1, y1, x2, y2]

def node_text_size_get(node):
    _font = fonts[camera['zoom']-1]
    w_max = 0
    h_tot = 0
    for line_i, line in enumerate(node['lines']):
        text_surface = _font.render(line, False, (255, 255, 255))
        text_w, text_h = _font.size(line)
        if w_max < text_w: w_max = text_w
        h_tot += text_h
    return w_max, h_tot

def node_pos_get(node):
    x = node['x'] * camera['zoom'] + camera['x']
    y = node['y'] * camera['zoom'] + camera['y']
    return [x, y]

def node_rect_get(node):
    node_x, node_y = node_pos_get(node)
    text_w, text_h = node_text_size_get(node)
    x = node_x
    y = node_y
    w = text_w
    h = text_h
    return [x, y, w, h]

def view_pos_get(val):
    view_pos = val * camera['zoom'] + camera['x']
    return view_pos

def draw_nodes():
    for node in nodes:
        ### node rect
        x, y, w, h = node_rect_get(node)
        pygame.draw.rect(screen, '#101010', pygame.Rect(x, y, w, h))
        pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, w, h), 1)
        ### node text
        _font = fonts[camera['zoom']-1]
        for line_i, line in enumerate(node['lines']):
            text_surface = _font.render(line, False, (255, 255, 255))
            text_w, text_h = _font.size(line)
            screen.blit(text_surface, (x, y+text_h*line_i))
        ### node pos debug
        if 0:
            y_cur = y
            y_cur -= 24*camera['zoom']
            line = f"{x}, {y}"
            text_surface = _font.render(line, False, (255, 255, 255))
            screen.blit(text_surface, (x, y_cur))
            y_cur -= 24*camera['zoom']
            line = f"{node['x']}, {node['y']}"
            text_surface = _font.render(line, False, (255, 255, 255))
            screen.blit(text_surface, (x, y_cur))
        ### node active
        if node['id'] == node_active_id:
            pygame.draw.rect(screen, '#00ff00', pygame.Rect(x, y, w, h), 1)
        ### cursor
        x = cursor['x']
        y = cursor['y']
        w = cursor['w'] * camera['zoom']
        h = cursor['h'] * camera['zoom']
        pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, w, h), 1)


def draw_debug():
    _font = fonts[camera['zoom']-1]
    ###
    x = 32
    y = 32
    line = f"{mouse['x']}, {mouse['y']}"
    text_surface = _font.render(line, False, (255, 255, 255))
    screen.blit(text_surface, (x, y))
    y += 24
    line = f"{camera['x']}, {camera['y']}"
    text_surface = _font.render(line, False, (255, 255, 255))
    screen.blit(text_surface, (x, y))
    y += 24
    line = f"{camera['x_abs']}, {camera['y_abs']}"
    text_surface = _font.render(line, False, (255, 255, 255))
    screen.blit(text_surface, (x, y))
    if 0:
        y += 24
        line = f"{node_active_id}, {node_active}"
        text_surface = _font.render(line, False, (255, 255, 255))
        screen.blit(text_surface, (x, y))

def draw_main():
    screen.fill('#101010')
    draw_edges()
    draw_nodes()
    draw_edge_tmp()
    draw_debug()
    pygame.display.flip()

running = True
while running:
    input_main()
    draw_main()

pygame.quit()

