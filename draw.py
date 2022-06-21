import pygame
def draw_sence():
    fileName = "data.txt"
    f = open(fileName,'r')
    print(f.read())
    f.close()

if __name__ == '__main__':
    #screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
    draw_sence()