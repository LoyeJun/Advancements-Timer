import pygame
import time
import datetime
import json
import os
import sys

class display:
    def text(screen, text:str, size:int, colour:tuple, pos:tuple, centered:bool):
        size = int(size)
        text = str(text)
        font = pygame.font.Font(get_path('assets/unifont-16.0.01.otf'), size)
        text_surface = font.render(text, False, colour)
        text_rect = text_surface.get_rect()
        if centered:
            text_rect.center = pos
            if pos[1]+text_rect.height/2 > 0 and pos[1]-text_rect.height/2 < screen.get_height():
                screen.blit(text_surface, text_rect)
        else:
            if pos[1]+text_rect.height > 0 and pos[1] < screen.get_height():
                screen.blit(text_surface, pos)

    def image(screen, image, pos:tuple, angle=0):
        image = pygame.image.load(image)

        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rect = rotated_image.get_rect()

        rotated_rect.center = pos
        screen.blit(rotated_image, rotated_rect)

    def rounded_rectangle(screen, in_color, out_color, postion, w, h, r, thickness:int, centered:bool):
        if centered:
            x,y = postion[0]-w/2,postion[1]-h/2
        else:
            x,y = postion[0],postion[1]
        pygame.draw.circle(screen, out_color, (x+r, y+r), r)
        pygame.draw.circle(screen, out_color, (x+w-r, y+h-r), r)
        pygame.draw.circle(screen, out_color, (x+r, y+h-r), r)
        pygame.draw.circle(screen, out_color, (x+w-r, y+r), r)
        
        pygame.draw.rect(screen, out_color, (x+r, y, w-r*2, h))
        pygame.draw.rect(screen, out_color, (x, y+r, w, h-r*2))

        r = r - thickness
        x = x + thickness
        y = y + thickness
        w = w - thickness * 2
        h = h - thickness * 2
        pygame.draw.circle(screen, in_color, (x+r, y+r), r)
        pygame.draw.circle(screen, in_color, (x+w-r, y+h-r), r)
        pygame.draw.circle(screen, in_color, (x+r, y+h-r), r)
        pygame.draw.circle(screen, in_color, (x+w-r, y+r), r)
        
        pygame.draw.rect(screen, in_color, (x+r, y, w-r*2, h))
        pygame.draw.rect(screen, in_color, (x, y+r, w, h-r*2))
        
def get_path(relative_path):
    try:
        base_path = sys._MEIPASS # pyinstaller打包后的路径
    except AttributeError:
        base_path = os.path.abspath(".") # 当前工作目录的路径
 
    return os.path.normpath(os.path.join(base_path, relative_path)) # 返回实际路径

        
pygame.init()
info = pygame.display.Info()
screen_size = (info.current_w, info.current_h)
icon = pygame.image.load(get_path('assets/icon.png'))  # 确保路径正确
icon = pygame.transform.scale(icon, (32, 32))  # 缩放图标到合适的大小
pygame.display.set_icon(icon)

window_width = 180
window_height = 50

x0, y0 = screen_size[0]-window_width, 10

with open(f'{os.getcwd()}/setting.json', 'r', encoding='utf-8') as file:
    setting = json.load(file)
    x1 = int(setting['pos']['x'])
    y1 = int(setting['pos']['y'])
    alarm = setting['alarm']
            
os.environ['SDL_VIDEO_WINDOW_POS'] = "{},{}".format(x0-x1, y0+y1)
window = pygame.display.set_mode((window_width, window_height), pygame.NOFRAME)
rect = window.get_rect()
    
pygame.display.set_caption('Advancements-Timer')


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            pass
    
    display.rounded_rectangle(window, (35,35,35), (80,80,80), (window_width/2,window_height/2), window_width, window_height, 3, 5, True)
    
    
    hour = int(datetime.datetime.fromtimestamp(time.time()).strftime('%H'))
    minute = int(datetime.datetime.fromtimestamp(time.time()).strftime('%M'))
    second = int(datetime.datetime.fromtimestamp(time.time()).strftime('%S'))
    now_hour = hour+12+minute/60+second/3600
    display.image(window, get_path('assets/dial.png'), 255, (window_height/1.8, window_height/1.8), (10+window_height/3, window_height/2), True, angle=360*-now_hour/24)
    display.image(window, get_path('assets/clock.png'), 255, (10, window_height/2), (10+window_height/3, window_height/2), True)
    
    display.text(window, f'{datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")}', 16, (252,252,  0), (35+window_height/3, window_height*0.1), False)
    
    if alarm == '':
        display.text(window, f'没有设置闹钟和倒计时', 12, (235,235,235), (35+window_height/3, window_height*0.5), False)
    else:
        display.text(window, f'闹钟 Beta - {alarm}', 12, (235,235,235), (35+window_height/3, window_height*0.5), False)
    
    
    pygame.display.update()

pygame.quit()