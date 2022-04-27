from pygame.locals import *
# Importing the library
import pygame
  
# Initializing Pygame
pygame.init()


class Ship(object):
    def __init__(self):
        self.speed = 0
        self.fuel = 200
        self.size = 10
        self.color = pygame.Color('#222222')
        self.y = 10
        self.x = (480 / 2) - (self.size / 2) 

    def update(self, gravity):
        self.speed = self.speed + gravity
        self.y = self.y + self.speed

    def land(self, ground_level):
        if self.y + (self.size / 2) >= ground_level:
            return True
        return False

    def draw(self, window_object):
        pygame.draw.rect(window_object, self.color, pygame.Rect(self.x, self.y, self.size, self.size))


class Game(object):
    def __init__(self):
        self.window_object = pygame.display.set_mode( ( 480, 640) )
        self.gravity = 0.2
        self.ground_level = 500
        self.fps_timer = pygame.time.Clock()
        self.max_fps = 30
        self.ship = Ship()
        self.font_object = pygame.font.Font('/System/Library/Fonts/Supplemental/Arial.ttf', 16)

    def start(self, brain=None):
        end = False
        while not end:
            self.window_object.fill(pygame.Color('#abcdef'))

            pygame.draw.rect(self.window_object, pygame.Color('#993333'), (0, self.ground_level, self.window_object.get_width(), self.window_object.get_height()) )
            
            # Check for events
            presed = False
            for event in pygame.event.get():
                if event.type == KEYDOWN and brain is None:
                    if self.ship.fuel >= 20:
                        presed = True
                       

            if brain:
                if self.ship.fuel >= 20:
                    presed = True if brain([self.ship.speed, self.ground_level - self.ship.y+5])[0] == 1 else False

            if presed:
                self.ship.fuel -= 20

            self.ship.update(self.gravity if presed == False else self.gravity - 2)
            
            self.ship.draw(self.window_object)
            if self.ship.land(self.ground_level):
                end = True

            score_surface = self.font_object.render( 'Speed: %d - Distance: %d - Fuel: %d' % (self.ship.speed, self.ground_level - self.ship.y+5, self.ship.fuel), False, pygame.Color('#FFFFFF'))

            score_rect    = score_surface.get_rect()
            score_rect.topleft = (self.window_object.get_height() / 4 , 10)
            self.window_object.blit(score_surface, score_rect)

            pygame.display.flip()
            self.fps_timer.tick(self.max_fps)

        return self.ship.speed

if __name__ == '__main__':
    from ga import AG
    from ga import cross_arithmetic
    from ann import GetWeightLen
    from ann import CreateNetwork
    from ann import sigmoid

    generation = 0

    brains = AG.Random(10, GetWeightLen(2, [6,1]))
    brains.cross_function = cross_arithmetic
    while generation < 20:

        for pop in brains.population:
            game = Game()
            pop.fitness = game.start(CreateNetwork(2,[6,1],pop.value,sigmoid,False,['discrete']))
            print(pop.fitness)

        brains.next_generation(3,False)
        print(generation)
        generation += 1 
