import pygame
import math
import parser
import pandas as pd

SCREEN_HEIGHT, SCREEN_WIDTH = 1000, 1000
FPS = 50
SIM_TIME = 60  # Simulation time in seconds
dt = 1/FPS  # Number of seconds that pass between frames


class Car(pygame.sprite.Sprite):
    def __init__(self, x0: int, y0: int, img_path: str):
        super().__init__()
        self.x, self.y = (x0, y0)
        self.image = pygame.image.load(img_path)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.width, self.length = self.image.get_size()
        self.angle = 0.0


def draw(image, x, y, angle, window):
    """Perform any transforms to the image and draw it on the window."""
    # x += 15
    # y -= 15
    # rect = image.get_rect()  # Get outline rectangle
    # rect.center = (x, y)  # Center rectangle
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_rectangle = rotated_image.get_rect()
    rotated_rectangle.center = (x, y)
    window.blit(rotated_image, rotated_rectangle)


def main():
    pygame.init()
    win = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
    pygame.display.set_caption("Traffic Sim")

    clock = pygame.time.Clock()

    # Car image paths
    car_imgs = [f"images/car{i+1}.png" for i in range(4)]
    # Read in car path data
    car_paths = parser.get_car_paths_from_csv("data/car_data.csv")
    # Initialize Car objects
    cars = []
    for idx, path in enumerate(car_paths):
        car = Car(x0=path[0][0][0], y0=path[0][0][1], img_path=car_imgs[idx])
        cars.append(car)

    # Read in road data
    road_data_df = pd.read_csv("data/road_data.csv", sep=';')

    running = True
    i = 0
    t = 0
    while running:
        clock.tick(FPS)
        t += dt
        if t >= SIM_TIME:
            break
        # Check to see if we are trying to close the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # Fill the screen with white
        win.fill((255, 255, 255))
        # Draw the map map
        parser.draw_map_from_csv(win, road_data_df)
        # Update cars angle and positions
        for idx, car in enumerate(cars):
            car.x, car.y = car_paths[idx][i][0]
            car.angle = car_paths[idx][i][1]
            draw(car.image, car.x, car.y, car.angle, win)
        i += 1
        pygame.display.update()

    print("Simulation Complete!")
    pygame.quit()


if __name__ == "__main__":
    main()