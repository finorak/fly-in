import pygame

class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("App")
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