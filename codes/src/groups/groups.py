import pygame


class SpriteGroup(pygame.sprite.Group):
    """This custom group let us controll
    all the sprites on the screen, that include
    the platforms (cell) and the drones,
    this is mainly used for the cameras
    """
    def __init__(self) -> None:
        """Constructor for a SpriteGroup
        instance
        """
        super().__init__()
        self.speed = 500
        self.offset = pygame.math.Vector2()

    def update_offset(self, dt: float) -> None:
        """Updating the camera we see on the screen
        I didn't use delta time for this one because
        it was way to slow, probably because the value is
        already betweeen 0->1, and dt is bettween
        that value as well.
        TODO: use delta time
        Parameters:
            dt: delta time
        """
        keys = pygame.key.get_pressed()
        self.offset.x -= int(
                keys[pygame.K_RIGHT]) - int(
                        keys[pygame.K_LEFT]) * self.speed * dt
        self.offset.y -= int(
                keys[pygame.K_DOWN]) - int(
                        keys[pygame.K_UP]) * self.speed * dt

    def custom_draw(self, screen: pygame.Surface, dt: float) -> None:
        """A custom draw function that let us
        move the camera to the way we want it
        Parameters:
            screen: wher do we want to draw the
                    sprites
            dt: delta time
        """
        self.update_offset(dt)
        conn_sprites = [
                sprite for sprite in self.sprites()
                if hasattr(sprite, 'network')]
        all_sprites = [
                sprite for sprite in self.sprites()
                if not hasattr(sprite, 'network')]
        for sprites in [conn_sprites, all_sprites]:
            for sprite in sorted(sprites, key=lambda sprite: sprite.rect.centery):
                offset = sprite.rect.center + self.offset
                if sprite not in all_sprites:
                    offset = sprite.rect.topleft + self.offset
                screen.blit(sprite.image, offset)


class SimulationGroup(pygame.sprite.Group):
    """This class we'll be mainly used to
    controll the sprites for our simulation
    """
    def __init__(self) -> None:
        """Constructor for a simulationGroup
        instance.
        """
        super().__init__()

    def custom_draw(self, dt: float = 0) -> None:
        """Cusom draw for the simulation class
        that let us controll the simuluation
        sprites
        Parameters:
            dt: delta time
        """


class CameraGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
