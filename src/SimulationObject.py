import pygame

class SimulationObject(pygame.sprite.Sprite):
    '''A simulation object in the drill.

    Args:
        pygame (Sprite): A sprite object from pygame.
    '''

    def __init__(self, img_path: str, x: int, y: int):
        '''Constructor for SimulationObject.

        Args:
            img_path (str): The path to the image to be displayed for this sprite. 
            x (int): Starting x position.
            y (int): Starting y position.
        '''
        super().__init__()
        
        img = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(img, (25, 25))
        self.rect = self.image.get_rect()
        self.rect.center = self.target = (x,y)
        self.path = []
        
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
        
    def move(self, speed: int) -> bool:
        '''Move according to the path defined in 'self.path'. 

        Args:
            speed (int): The speed at which to move.

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

        if distance <= speed:
            self.rect.center = self.target
            if self.path:
                self.target = self.path.pop(0)
            else:
                self.target = None
        else:
            step_x = speed * (dx / distance)
            step_y = speed * (dy / distance)
            self.rect.move_ip(step_x, step_y)

        return True  # Still moving
    
    def draw(self, surface: pygame.Surface):
        '''Draw the sprite on the surface.

        Args:
            surface (pygame.Surface): The surface to draw the sprite on.
        '''
        surface.blit(self.image, self.rect)