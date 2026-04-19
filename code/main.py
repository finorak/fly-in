import sys
import json
import pygame
from utils.map_parsing import parsing, get_path


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("App")
        # try:
        self.config = parsing(get_path("maps", "easy", "01_linear_path.txt"))
        # except Exception as e:
        #     print(e)
        #     print("Aborting...")
        #     sys.exit(1)
        with open("map.json", "w") as file:
            json.dump(self.config, file, indent=4)
        self.running = True

    def run(self):
        while self.running:
            self.draw(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
            pygame.display.update()
        pygame.quit()

    def draw(self, screen: pygame.Surface):
        screen.fill("white")


if __name__ == "__main__":
    app = App()
    app.run()
