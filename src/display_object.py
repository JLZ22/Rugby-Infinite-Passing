import pygame
import utils

class DisplayObject(pygame.sprite.Sprite):
    '''A simulation object in the drill.

    Args:
        pygame (Sprite): A sprite object from pygame.
    '''

    def __init__(
        self, 
        img_path: str, 
        x: int, 
        y: int, 
        id: int,
    ):
        '''Constructor for DisplayObject.

        Args:
            img_path (str): The path to the image to be displayed for this sprite. 
            x (int): Starting x position.
            y (int): Starting y position.
            id (int): The unique id of the sprite.
        '''
        super().__init__()
        
        img = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.smoothscale(img, utils.get_new_dims(20, img))
        self.rect = self.image.get_rect()
        self.rect.center = self.target = (x,y)
        self.path = []
        self.id = id
        
    def set_path(self, target_x: int, target_y: int, split_ratio: float=0.5):
        '''Define a path for this sprite that ends at the target 
        x,y location. This path will always comprise of two x 
        segments separated by one y segment. The distance of 
        each x segment is determined by the split_ratio.

        Args:
            target_x (int): The target x location.
            target_y (_type_): The target y location.
            split_ratio (float, optional): The length of the first x segment. Defaults to 0.5.
        '''
        start_x = self.rect.center[0]
        start_y = self.rect.center[1]
        
        delta_x = target_x - start_x
        delta_y = target_y - start_y

        # Split horizontal movement
        right1_distance = delta_x * split_ratio

        self.path = [
            (start_x + right1_distance, start_y),  # First right
            (start_x + right1_distance, start_y + delta_y),  # Down
            (target_x, target_y),  # Second right
        ]
        self.target = self.path.pop(0)
        
    def set_tint(self, color: utils.RGB | utils.RGBA | None):
        '''Set the tint of the sprite.

        Args:
            color (RGB | RGBA): The color to tint the sprite.
        '''
        if color:
            utils.tint_image(self.image, color)
        
    def update(self, adjusted_speed: float) -> bool:
        '''Move according to the path defined in 'self.path'. 

        Args:
            adjusted_speed (float): The speed at which to move, already adjusted by delta time.

        Returns:
            bool: True if there are still instructions in the path array, otherwise False.
        '''
        if not self.target:
            return False  # No target, movement complete

        target_x, target_y = self.target
        current_x, current_y = self.rect.center

        # Calculate movement step
        dx = target_x - current_x
        dy = target_y - current_y
        distance = (dx**2 + dy**2) ** 0.5

        if distance <= adjusted_speed:
            self.rect.center = self.target
            if self.path:
                self.target = self.path.pop(0)
            else:
                self.target = None
        else:
            step_x = adjusted_speed * (dx / distance)
            step_y = adjusted_speed * (dy / distance)
            self.rect.move_ip(step_x, step_y)

        return True  # Still moving
    
    def draw(self, surface: pygame.Surface, debug: bool = False):
        '''Draw the sprite on the surface.

        Args:
            surface (pygame.Surface): The surface to draw the sprite on.
            debug (bool, optional): Whether to display the id of the sprite. Defaults to False.
        '''
        if debug:
            font = pygame.font.Font(None, 40)
            text = font.render(str(self.id), True, (0,0,0))
            surface.blit(text, self.rect.center)
        else:
            surface.blit(self.image, self.rect)