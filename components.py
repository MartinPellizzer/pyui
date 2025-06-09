def label_create(_id, text, x, y):
    obj = {
        'id': _id,
        'type': 'label',
        'text': text,
        'x': x,
        'y': y,
        'w': 0,
        'h': 0,
    }
    return obj

def button_create(_id, text, x, y):
    obj = {
        'id': _id,
        'type': 'button',
        'text': text,
        'x': x,
        'y': y,
        'w': 0,
        'h': 0,
        'px': 16,
        'py': 8,
    }
    return obj

def image_create(_id, filepath, x, y, w, h):
    pyimage = pygame.image.load(filepath)
    pyimage = pygame.transform.scale(pyimage, (w, h))
    obj = {
        'id': _id,
        'type': 'image',
        'filepath': filepath,
        'pyimage': pyimage,
        'x': x,
        'y': y,
        'w': w,
        'h': h,
    }
    return obj

components.append(label_create(2, 'Label 1', x=700, y=10))
components.append(label_create(99, 'Label 2', x=800, y=10))
components.append(button_create(3, 'Button 666', x=700, y=40))
components.append(button_create(4, 'Button 999', x=700, y=80))
components.append(image_create(5, 'abies-alba.jpg', x=700, y=120, w=128, h=128))

def component_label_draw(component):
    x = component['x']
    y = component['y']
    text = component['text']
    text_surface = font_16.render(text, False, (255, 255, 255))
    screen.blit(text_surface, (x, y))

def component_button_draw(component):
    x = component['x']
    y = component['y']
    px = component['px']
    py = component['py']
    text = component['text']
    ###
    text_surface = font_16.render(text, False, '#000000')
    w, h = font_16.size(text)
    pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, w+px*2, h+py*2))

    screen.blit(text_surface, (x+px, y+py))

def component_image_draw(component):
    x = component['x']
    y = component['y']
    pyimage = component['pyimage']
    screen.blit(pyimage, (x, y))

