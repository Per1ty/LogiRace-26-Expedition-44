import pygame
pygame.init()
pygame.font.init()
class PyBtn:
    def __init__(self,x,y,width = 200,height = 100,color = (255,255,255),bound = 0, text = 'Hello world!',text_color = (0,0,0),text_size = 30,screen = None):
        self.rect = pygame.Rect(x,y,width,height)
        self.color = color
        if self.color[0] > 50:
            self.dark1 = self.color[0] - 50
        else:
            self.dark1 = 0
        if self.color[1] > 50:
            self.dark2 = self.color[1] - 50
        else:
            self.dark2 = 0
        if self.color[2] > 50:
            self.dark3 = self.color[2] - 50
        else:
            self.dark3 = 0
        self.darkcolor = (self.dark1, self.dark2, self.dark3)
        self.bound = bound
        self.font = pygame.font.SysFont('comicsans', text_size)
        self.surf_text = self.font.render(text,True,text_color)
        self.text_color = text_color
        self.screen = screen
    def draw(self):
        pygame.draw.rect(self.screen,self.color,self.rect)
        pygame.draw.rect(self.screen,self.darkcolor,self.rect,self.bound)
        self.text_rect = self.surf_text.get_rect(center = self.rect.center)
        self.screen.blit(self.surf_text,self.text_rect)
    def action(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
