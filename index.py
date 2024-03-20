import pygame;

SCREEN_WIDTH = 600;
SCREEN_HEIGHT = 400;

FPS = 60;
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Runner Man')


class Background:
  def __init__(self) -> None:
    self.background_shift_offset = 0;
    self.BACKGROUND_IMAGE = pygame.image.load("./assets/environment/desert_BG.png").convert_alpha()  
    self.REMAINING_IMAGE_OFFSET = self.BACKGROUND_IMAGE.get_width() - SCREEN_WIDTH;

  def draw(self) -> None:
    if self.background_shift_offset >= self.BACKGROUND_IMAGE.get_width():
      self.background_shift_offset = 0
    
    self.background_shift_offset += 1;
    
    screen.blit(self.BACKGROUND_IMAGE,(0 - self.REMAINING_IMAGE_OFFSET - self.background_shift_offset,0));
    screen.blit(self.BACKGROUND_IMAGE,(SCREEN_WIDTH - self.background_shift_offset,0));


background = Background();

gameIsRunning = True 
while gameIsRunning:
  clock.tick(FPS)

  background.draw();

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      gameIsRunning = False

  pygame.display.update();

pygame.quit()