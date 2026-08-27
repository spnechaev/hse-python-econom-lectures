"""Open a window and move a ball from side to side."""

import pygame


WIDTH = 640
HEIGHT = 360
RADIUS = 24


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("A very small Pygame program")
    clock = pygame.time.Clock()

    x = float(RADIUS)
    speed = 220.0
    running = True

    while running:
        seconds = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        x += speed * seconds
        if x >= WIDTH - RADIUS:
            x = WIDTH - RADIUS
            speed = -abs(speed)
        elif x <= RADIUS:
            x = RADIUS
            speed = abs(speed)

        screen.fill("midnightblue")
        pygame.draw.circle(screen, "gold", (x, HEIGHT / 2), RADIUS)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
