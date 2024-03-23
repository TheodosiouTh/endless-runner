import pygame;
import random;

SCREEN_WIDTH = 600;
SCREEN_HEIGHT = 400;

FPS = 60;
clock = pygame.time.Clock()

GRAVITY = 1

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Runner Man')


class Background:
  def __init__(self) -> None:
    self.update_time = 0;
    
    self.background_shift_offset = 0;
    self.BACKGROUND_IMAGE = pygame.image.load("./assets/environment/desert_BG.png").convert_alpha()  
    self.REMAINING_IMAGE_OFFSET = self.BACKGROUND_IMAGE.get_width() - SCREEN_WIDTH;

  def draw(self) -> None:
    if not game_over:
      if self.background_shift_offset >= self.BACKGROUND_IMAGE.get_width():
        self.background_shift_offset = 0
      
      self.background_shift_offset += 1;
      
    screen.blit(self.BACKGROUND_IMAGE,(0 - self.REMAINING_IMAGE_OFFSET - self.background_shift_offset,0));
    screen.blit(self.BACKGROUND_IMAGE,(SCREEN_WIDTH - self.background_shift_offset,0));

class Character:
  def __init__(self, position, scale, jump_height) -> None:
    self.idleAnimation();

    self.position = position
    self.scale = scale

    self.is_jumping = False;
    self.jump_height = jump_height;
    self.velocity = self.jump_height;

    self.animation_list = []
    self.load_animations();

  def load_animations(self):
    temp_image_list = []
    for i in range(8):
      temp_image = pygame.image.load(f"./assets/character/run/{i}.png");
      temp_image = pygame.transform.scale(temp_image, (temp_image.get_width() * self.scale, temp_image.get_height() * self.scale));
      temp_image_list.append(temp_image);
    self.animation_list.append(temp_image_list);
    self.image = self.animation_list[self.action][self.frame];

    jump_image = pygame.image.load(f"./assets/character/jump/0.png");
    jump_image = pygame.transform.scale(jump_image, (jump_image.get_width() * self.scale, jump_image.get_height() * self.scale));
    self.animation_list.append([jump_image]);

    landing_image = pygame.image.load(f"./assets/character/landing/0.png");
    landing_image = pygame.transform.scale(landing_image, (landing_image.get_width() * self.scale, landing_image.get_height() * self.scale));
    self.animation_list.append([landing_image])

  def idleAnimation(self):
    self.action = 0;
    self.update_time = 0;
    self.frame = 0;

  def jumpAnimation(self):
    self.action = 1;
    self.update_time = 0;
    self.frame = 0;
  
  def fallAnimation(self):
    self.action = 2;
    self.update_time = 0;
    self.frame = 0;
    
  def update_rect(self):
    self.rect = self.image.get_rect();
    self.rect.center = self.position

  def jump(self):
    self.position = (self.position[0], self.position[1] - self.velocity);
    self.velocity -= GRAVITY;

    should_switch_to_falling = self.velocity < 0;
    if should_switch_to_falling:
      self.fallAnimation();
    
    if self.velocity < -self.jump_height:
      self.is_jumping = False;
      self.velocity = self.jump_height;
      self.idleAnimation()


  def draw(self):
    if not game_over:
      self.update();
      self.image = self.animation_list[self.action][self.frame]
      self.update_rect();

    screen.blit(self.image, self.position)

  def update(self):
    animation_cooldown = 100;
    if pygame.time.get_ticks() - self.update_time > animation_cooldown:
      self.update_time = pygame.time.get_ticks()
      self.frame = 0 if self.frame == len(self.animation_list[self.action]) - 1 else self.frame + 1 


class Bolder:
  def __init__(self) -> None:
    self.image = pygame.image.load("./assets/environment/bolder.png").convert_alpha();
    
    self.original_position = (650, 300);
    self.position = self.original_position

    self.update_rect();
    
    self.angle = 0;
    self.update_time = 0;
    self.speed = random.randint(5,11);


  def update_rect(self):
    self.rect = self.image.get_rect();
    self.rect.center = self.position

  def draw(self):
    if not game_over:
      self.position = (self.position[0] - self.speed, self.position[1]);
    
      if self.position[0] < -100:
        self.speed = random.randint(5,11);
        self.position = self.original_position;
      
      self.update_rect();
    screen.blit(self.image, self.position);



background = Background();

runner = Character((200, 280), 2, 15)


bolder = Bolder();

game_over = False
gameIsRunning = True 
while gameIsRunning:
  clock.tick(FPS)

  background.draw();

  runner.draw();

  bolder.draw();

  if runner.is_jumping: 
    runner.jump()

  if runner.rect.colliderect(bolder.rect):
    runner.idleAnimation();
    game_over = True;
  
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN and not game_over:
      if event.key == pygame.K_SPACE:
        runner.jumpAnimation();
        runner.is_jumping = True
    if event.type == pygame.QUIT:
      gameIsRunning = False

  pygame.display.update();

pygame.quit()