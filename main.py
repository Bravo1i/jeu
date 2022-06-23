#!/usr/bin/env python
import pygame
import sys
import random
from math import sin, cos, pi

# parametre
speed_player = 10
speed_falling = 8
ball_number = 5
fps = 60
duree = 30
diffculty = ['easy','normal','hard']
bar_mode = 1
nb_expr = 1

# config
screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
screen_width = screen.get_width()
screen_height = screen.get_height()
time = 0
ball_type = 1

class Ball(pygame.sprite.Sprite):
    # 定义构造函数
    def __init__(self, type, location):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.random_pos = random.randint(0, screen_height)
        self.status = 0
        if type == 0:
            self.image = pygame.image.load("Image/circle_gray.png")
            self.image = pygame.transform.scale(self.image, (86, 86))
        elif type == 1:
            self.image = pygame.image.load("Image/circle_green.png")
            self.speed_x = 0
            self.speed_y = speed_falling
            self.image = pygame.transform.scale(self.image, (74, 74))
        elif type == 2:
            self.image = pygame.image.load("Image/circle_pink.png")
            self.speed_x = 0
            self.speed_y = speed_falling
            self.image = pygame.transform.scale(self.image, (74, 74))
        elif type == 3:  
            self.image = pygame.image.load("Image/circle_orange.png")  
            self.speed_x = 0
            self.speed_y = speed_falling
            self.image = pygame.transform.scale(self.image, (74, 74))
        elif type == 4:
            self.image = pygame.image.load("Image/square.png")
            self.image = pygame.transform.scale(self.image, (86, 86))
        # 加载图片并且缩小
        self.rect = self.image.get_rect()
        # 获取图片rect区域
        self.rect.topleft = location
        # 设置位置

def ready(word):
    my_font = pygame.font.SysFont('arial', 80)
    text = my_font.render(word, True, (0, 0, 0))
    # 获得显示对象的 rect区域大小
    textRect = text.get_rect()
    # 设置显示对象居中
    textRect.center = (screen_width/2, 200)
    screen.blit(text, textRect)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_ESCAPE:
                    show_record()
                    file_record.close()
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.QUIT:
                show_record()
                file_record.close()
                pygame.quit()
                sys.exit()

def control_ball_bar():
    global speed_player
    global step
    key_pressed_is = pygame.key.get_pressed()
    if key_pressed_is[pygame.K_LEFT] & (player_ball.rect.left > 0):
        player_ball.rect.left -= speed_player
    if key_pressed_is[pygame.K_RIGHT] & (player_ball.rect.right < screen_width):
        player_ball.rect.left += speed_player
    if key_pressed_is[pygame.K_UP]:
        speed_player += 1
    if key_pressed_is[pygame.K_DOWN] & (abs(speed_player) > 1):
        speed_player -= 1
    if key_pressed_is[pygame.K_SPACE]:
        step -= 5

def draw_balls():
    global score
    global step
    for ball in group_ball:
        if (ball.status == 0) and (ball.rect.top > ball.random_pos):   
            if ball.type == 1:
                ball.speed_x = 0
                ball.speed_y = speed_falling
            elif (ball.type == 2) and (random.randint(0, 9) < 4):
                ball.speed_x = speed_falling * random.randrange(-1,2,2) * sin(pi/6)
                ball.speed_y = speed_falling * cos(pi/6)
            elif (ball.type == 3) and (random.randint(0, 9) < 9):  
                ball.speed_x = speed_falling * random.randrange(-1,2,2) * sin(pi/6)
                ball.speed_y = speed_falling * cos(pi/6)
            ball.status = 1
        ball.rect.left += ball.speed_x
        ball.rect.top += ball.speed_y
        if bar_mode == 1:
            if ball.rect.left < 0 or ball.rect.right > screen_width:
                ball.speed_x = - ball.speed_x
            if ball.rect.top < 0 or (ball.rect.bottom > screen_height-30):
                score += 1
                group_ball.remove(ball)
                group_ball.add(Ball(random.randint(1,ball_type), (random.randint(0, screen_width - 100), 0)))
        elif bar_mode == 2:
            if ball.rect.left < 30 or ball.rect.right > screen_width:
                ball.speed_x = - ball.speed_x
            if ball.rect.top < 0 or ball.rect.bottom > screen_height:
                score += 1
                group_ball.remove(ball)
                group_ball.add(Ball(random.randint(1,ball_type), (random.randint(30, screen_width - 100), 0)))
        # 下落小球 碰撞边界变向
        crash_result = pygame.sprite.collide_mask(player_ball, ball)
        if crash_result:
            score -= 10
            group_ball.remove(ball)
            if bar_mode == 2:
                group_ball.add(Ball(random.randint(1,ball_type), (random.randint(30, screen_width - 100), 0)))
            else:
                group_ball.add(Ball(random.randint(1,ball_type), (random.randint(0, screen_width - 100), 0)))
            # print("score:%d" % score)
            # show_score()
            # group_ball.empty()
            # score = 0
            # step = 0
            # ball_number = 5
            # ready("Crash!!Press enter to restart or esc to quit")
            # for i in range(ball_number):
            #     group_ball.add(Ball(random.randint(1,3), (random.randint(0, screen_width - 100), 0)))
        # 碰撞检测

def init():
    global clock
    global add_ball
    global get_score
    global tick1s
    global score
    global step
    global file_record
    pygame.init()
    # 初始化pygame
    pygame.mouse.set_visible(False)
    # shu biao bu ke jian
    score = 0
    step = 0
    fileName = 'data.txt'
    file_record = open(fileName,'a+')
    screen.fill((156, 156, 156))
    # 填充屏幕颜色
    pygame.display.set_caption('Jeu de boule')
    # 设置窗口标题
    clock = pygame.time.Clock()
    # create clock
    get_score = pygame.USEREVENT + 2
    pygame.time.set_timer(get_score,300)
    # get score while maintain bar in 0.7-0.9
    tick1s = pygame.USEREVENT + 3
    pygame.time.set_timer(tick1s, 1000)
    # set timer

def show_score():
    my_font = pygame.font.SysFont('arial', 50)
    dy = f"score:{score} expr:{nb_expr}"
    text = my_font.render(dy, True, (0, 0, 0))
    # 获得显示对象的 rect区域大小
    textRect = text.get_rect()
    # 设置显示对象居中
    textRect.center = (300, 800)
    screen.blit(text, textRect)
    # 得分显示

def show_time():
    my_font = pygame.font.SysFont('arial', 50)
    dy = f"time:{duree - time}"
    text = my_font.render(dy, True, (0, 0, 0))
    # 获得显示对象的 rect区域大小
    textRect = text.get_rect()
    # 设置显示对象居中
    textRect.center = (300, 300)
    screen.blit(text, textRect)
    # 得分显示

def flash():
    screen.fill((156, 156, 156))
    draw_balls()
    draw_bar(bar_mode)
    screen.blit(player_ball.image, player_ball.rect)
    for ball in group_ball:
        screen.blit(ball.image, ball.rect)
    show_score()
    show_time()
    pygame.display.flip()
    # 刷新界面显示

def draw_bar(bar_mode):
    global step
    global score
    if bar_mode == 1:
        pygame.draw.rect(screen,(192,192,192),(0,screen_height-30,screen_width,30))
        pygame.draw.rect(screen,(0,0,255),(screen_width*0.5, screen_height-30, step, 30))
        pygame.draw.rect(screen,(0,0,255),(screen_width*0.5-step, screen_height-30, step, 30))
        pygame.draw.rect(screen,(0,0,0),(screen_width*0.7,screen_height-30,5,30))
        pygame.draw.rect(screen,(0,0,0),(screen_width*0.9,screen_height-30,5,30))
        pygame.draw.rect(screen,(0,0,0),(screen_width*0.1,screen_height-30,5,30))
        pygame.draw.rect(screen,(0,0,0),(screen_width*0.3,screen_height-30,5,30))
        if step < screen_width*0.5:
            step += 1
    if bar_mode == 2:
        pygame.draw.rect(screen,(192,192,192),(0,0,30,screen_height))
        pygame.draw.rect(screen,(0,0,255),(0, screen_height/2, 30, step))
        pygame.draw.rect(screen,(0,0,255),(0, screen_height/2-step, 30, step))
        pygame.draw.rect(screen,(0,0,0),(0,screen_height*0.7,30,5))
        pygame.draw.rect(screen,(0,0,0),(0,screen_height*0.9,30,5))
        pygame.draw.rect(screen,(0,0,0),(0,screen_height*0.1,30,5))
        pygame.draw.rect(screen,(0,0,0),(0,screen_height*0.3,30,5))
        if step < screen_width*0.5:
            step += 1
    # bar
    # full_result = (step == screen_width*0.5)
    # if full_result:
    #     screen.fill((156, 156, 156))
    #     print("score:%d" % score)
    #     show_score()
    #     group_ball.empty()
    #     score = 0
    #     step = 0
    #     ball_number = 5
    #     ready("Full!!Press enter to restart or esc to quit")
    #     for i in range(ball_number):
    #         group_ball.add(Ball(random.randint(1,3), (random.randint(0, screen_width - 100), 0)))
    # test bar 

def menu():
    global ball_type
    pygame.mouse.set_visible(True)
    my_font = pygame.font.SysFont('arial', 80)
    textRect = []
    for i in range(0,3):
        word = diffculty[i]
        text = my_font.render(word, True, (0, 0, 0))
        textRect.append(text.get_rect())
        textRect[i].center = ((i+1)*screen_width/4, 500)
        screen.blit(text, textRect[i])
        # show "easy"
    
    word = "diffculty"
    text = my_font.render(word, True, (0, 0, 0))
    # 获得显示对象的 rect区域大小
    textRect_diff = text.get_rect()
    # 设置显示对象居中
    textRect_diff.center = (screen_width/2, 200)
    screen.blit(text, textRect_diff)
    # show diffculty
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect in textRect:
                    if rect.collidepoint(event.pos):
                        ball_type = 1 + textRect.index(rect)
                        screen.fill((156, 156, 156))
                        return
            if event.type == pygame.QUIT:
                f.close()
                pygame.quit()
                sys.exit()

def choose_nb_ball():
    global ball_number
    my_font = pygame.font.SysFont('arial', 80)
    textRect = []
    for i in range(5,10):
        word = str(i)
        text = my_font.render(word, True, (0, 0, 0))
        # 获得显示对象的 rect区域大小
        textRect.append(text.get_rect())
        # 设置显示对象居中
        textRect[i-5].center = ((i-4)*screen_width/6, 500)
        screen.blit(text, textRect[i-5])
    word = "ball number"
    text = my_font.render(word, True, (0, 0, 0))
    # 获得显示对象的 rect区域大小
    textRect_nb = text.get_rect()
    # 设置显示对象居中
    textRect_nb.center = (screen_width/2, 200)
    screen.blit(text, textRect_nb)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect in textRect:
                    if rect.collidepoint(event.pos):
                        ball_number = 5 + textRect.index(rect)
                        screen.fill((156, 156, 156))
                        return
            if event.type == pygame.QUIT:
                file_record.close()
                pygame.quit()
                sys.exit()

def choose_bar():
    global  bar_mode
    my_font = pygame.font.SysFont('arial', 80)
    word = ["Choose bar mode","Horizontal","Vertical"]
    textRect = []
    for i in range(0,3):
        text = my_font.render(word[i], True, (0, 0, 0))
        textRect.append(text.get_rect())
        textRect[i].center = (screen_width / 2, (i+1) * screen_height / 4)
        screen.blit(text, textRect[i])
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect in textRect:
                    if rect.collidepoint(event.pos):
                        if textRect.index(rect) == 0:
                            continue
                        bar_mode = textRect.index(rect)
                        screen.fill((156, 156, 156))
                        return
            if event.type == pygame.QUIT:
                file_record.close()
                pygame.quit()
                sys.exit()

def choose_sqr():
    global player_ball
    location = (screen_width / 2, screen_height * 0.8)
    my_font = pygame.font.SysFont('arial', 80)
    word = ["square","circle"]
    textRect = []
    for i in range(0,2):
        text = my_font.render(word[i], True, (0, 0, 0))
        textRect.append(text.get_rect())
        textRect[i].center = (screen_width / 2, (i+1) * screen_height / 3)
        screen.blit(text, textRect[i])
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect in textRect:
                    if rect.collidepoint(event.pos):
                        if textRect.index(rect):
                            player_ball = Ball(0, location)
                            # 创建玩家的球
                        else:
                            player_ball = Ball(4, location)
                            # 创建玩家的球
                        screen.fill((156, 156, 156))
                        return
            if event.type == pygame.QUIT:
                f.close()
                pygame.quit()
                sys.exit()

def show_record():
    fileName = "data.txt"
    file_record = open(fileName, 'r')
    record = [0, 0, 0]
    for line in file_record:
        for i in range(0, 3):
            if int(line.strip('\n')) > record[i]:
                record[i] = int(line.strip('\n'))
                break
    print(record)
    file_record.close()


if __name__ == '__main__':   
    init()
    menu()
    choose_nb_ball()
    choose_bar()
    choose_sqr()
    pygame.mouse.set_visible(False)
    ready("Are You Ready? Press enter to begin")
    # ready function
    group_ball = pygame.sprite.Group()
    # 向组内添加一个精灵
    if bar_mode == 2:
        for i in range(ball_number):
            group_ball.add(Ball(random.randint(1,ball_type), (random.randint(30, screen_width - 100), 0)))
    else:
        for i in range(ball_number):
            group_ball.add(Ball(random.randint(1,ball_type), (random.randint(0, screen_width - 100), 0)))
        # 创建下落的球组
    while True:
        clock.tick(fps)
        # 游戏主循环
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                file_record.close()
                show_record()
                pygame.quit()
                sys.exit()
            if event.type == get_score:
                if (step > screen_width*0.2)and (step < screen_width*0.4):
                    score += 1
                # add score while time pass and bar is in 0.7-0.9
            if event.type == tick1s:
                time += 1
                if time >= duree:
                    file_record.write(str(score)+'\n')
                    time = 0
                    screen.fill((156, 156, 156))
                    show_score()
                    group_ball.empty()
                    score = 0
                    step = 0
                    ball_number = 5
                    ready("Time's up!!Press enter to restart or esc to quit")
                    screen.fill((156, 156, 156))
                    menu()
                    choose_nb_ball()
                    choose_bar()
                    choose_sqr()
                    pygame.mouse.set_visible(False)
                    ready("Are You Ready? Press enter to begin")
                    nb_expr += 1
                    if bar_mode == 2:
                        for i in range(ball_number):
                            group_ball.add(Ball(random.randint(1,ball_type), (random.randint(30, screen_width - 100), 0)))
                    else:
                        for i in range(ball_number):
                            group_ball.add(Ball(random.randint(1,ball_type), (random.randint(0, screen_width - 100), 0)))
        control_ball_bar()
        # 移动玩家小球
        flash()
        # flash
