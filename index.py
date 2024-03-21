import pygame;

SCREEN_WIDTH = 600;
SCREEN_HEIGHT = 400;

FPS = 60;
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Runner Man')


class Background:
  def __init__(self) -> None:
    self.update_time = 0;
    
    self.background_shift_offset = 0;
    self.BACKGROUND_IMAGE = pygame.image.load("./assets/environment/desert_BG.png").convert_alpha()  
    self.REMAINING_IMAGE_OFFSET = self.BACKGROUND_IMAGE.get_width() - SCREEN_WIDTH;

  def draw(self) -> None:
    if self.background_shift_offset >= self.BACKGROUND_IMAGE.get_width():
      self.background_shift_offset = 0
    
    self.background_shift_offset += 1;
    
    screen.blit(self.BACKGROUND_IMAGE,(0 - self.REMAINING_IMAGE_OFFSET - self.background_shift_offset,0));
    screen.blit(self.BACKGROUND_IMAGE,(SCREEN_WIDTH - self.background_shift_offset,0));

class Character:
  def __init__(self, position, scale) -> None:
    self.action = 0;
    self.frame = 0;
    self.update_time = 0;

    self.position = position
    self.scale = scale

    self.animation_list = []
    self.load_animations();

  def load_animations(self):
    temp_image_list = []
    for i in range(8):
      temp_image = pygame.image.load(f"./assets/character/run/{i}.png");
      temp_image = pygame.transform.scale(temp_image, (temp_image.get_width() * self.scale, temp_image.get_height() * self.scale));
      temp_image_list.append(temp_image);
    self.animation_list.append(temp_image_list);

    jump_image = pygame.image.load(f"./assets/character/jump/0.png");
    jump_image = pygame.transform.scale(jump_image, (jump_image.get_width() * self.scale, jump_image.get_height() * self.scale));
    self.animation_list.append([jump_image]);

    landing_image = pygame.image.load(f"./assets/character/landing/0.png");
    landing_image = pygame.transform.scale(landing_image, (landing_image.get_width() * self.scale, landing_image.get_height() * self.scale));
    self.animation_list.append([landing_image])

  def draw(self):
    self.update();
    screen.blit(self.animation_list[self.action][self.frame], self.position)

  def update(self):
    animation_cooldown = 100;
    if pygame.time.get_ticks() - self.update_time > animation_cooldown:
      self.update_time = pygame.time.get_ticks()
      self.frame = 0 if self.frame == len(self.animation_list[self.action]) - 1 else self.frame + 1 

background = Background();
runner = Character((200, 280), 2)

gameIsRunning = True 
while gameIsRunning:
  clock.tick(FPS)

  background.draw();

  runner.draw();

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      gameIsRunning = False

  pygame.display.update();

pygame.quit()