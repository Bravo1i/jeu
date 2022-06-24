import pygame
def draw_sence():
    fileName = "data.txt"
    file_record = open(fileName,'r')
    record = [0, 0, 0]
    for line in file_record:
        for i in range(0,3):
            if int(line.strip('\n')) > record[i]:
                record.insert(i,int(line.strip('\n')))
                record.pop()
                print(record[i])
                break
    print(record)
    file_record.close()

if __name__ == '__main__':
    #screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
    draw_sence()
"""
000
111
331
531

"""