from typing import Any

import pygame
from settings import WIN_SIZE


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
        self.zoom_scale: float = 1
        self.internal_surf_size = WIN_SIZE
        self.internal_surf = pygame.Surface(
            (self.internal_surf_size), pygame.SRCALPHA
        )
        self.internal_rect = self.internal_surf.get_rect(
            center=(WIN_SIZE[0] // 2, WIN_SIZE[1] // 2)
        )
        self.internal_surf_size_vector = pygame.math.Vector2(
            self.internal_surf_size
        )

    def update_offset(self, dt: float) -> None:
        """
        Updating the camera we see on the screen
        I didn't use delta time for this one because
        it was way to slow, probably because the value is
        already betweeen 0->1, and dt is bettween
        that value as well.
        TODO: use delta time
        Parameters:
            dt: delta time
        """
        keys = pygame.key.get_pressed()
        dx = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        dy = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.offset.x -= dx * self.speed * dt
        self.offset.y -= dy * self.speed * dt

    def zoom_camera(self, event: Any, dt: float) -> None:
        """Zooming method for the images
        Parameters:
            event: the mousewheell
            dt: delta time. """
        self.zoom_scale += event.y * dt

    def custom_draw(
            self, screen: pygame.Surface,
            background_image: pygame.Surface, dt: float
    ) -> None:
        """A custom draw function that let us
        move the camera to the way we want it
        Parameters:
            screen: wher do we want to draw the
                    sprites
            dt: delta time
        """
        self.update_offset(dt)
        self.internal_surf.blit(background_image)
        conn_sprites: list[Any] = [
            sprite for sprite in self.sprites()
            if hasattr(sprite, 'network')
        ]
        cell_sprites: list[Any] = [
            sprite for sprite in self.sprites()
            if hasattr(sprite, 'neighboors')
        ]
        drone_sprites: list[Any] = [
            sprite for sprite in self.sprites()
            if hasattr(sprite, 'move')
        ]
        for sprites in [conn_sprites, cell_sprites, drone_sprites]:
            for sprite in sorted(sprites,
                                 key=lambda sprite: sprite.rect.centery):
                offset = sprite.rect.center + self.offset
                if sprite not in cell_sprites and sprite not in drone_sprites:
                    offset = sprite.rect.topleft + self.offset
                self.internal_surf.blit(sprite.image, offset)
        scaled_surf = pygame.transform.scale(
            self.internal_surf,
            self.internal_surf_size_vector * self.zoom_scale
        )
        scaled_rect = scaled_surf.get_rect(
            center=(WIN_SIZE[0] // 2, WIN_SIZE[1] // 2))
        screen.blit(scaled_surf, scaled_rect)
