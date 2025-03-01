import pygame
import random
import math

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# Generate stars
stars = [(random.randint(0, screen.get_width()), random.randint(0, screen.get_height())) for _ in range(100)]

# Create Mars texture
mars_surface = pygame.Surface((80, 80), pygame.SRCALPHA)  # Transparent surface
mars_surface.fill((0, 0, 0, 0))  # Fully transparent background

# Draw the base red-orange planet
pygame.draw.circle(mars_surface, (210, 90, 40), (40, 40), 40)  # Mars base color

# Add shading (radial gradient effect)
for i in range(40, 0, -1):  # From outer edge to center
    color = (max(100, 210 - i*3), max(40, 90 - i*2), max(20, 40 - i))  # Darker towards edges
    pygame.draw.circle(mars_surface, color, (40, 40), i)

# Place non-overlapping craters
craters = []
max_attempts = 50  # Prevent infinite loops

for _ in range(5):  # Place 5 craters
    for _ in range(max_attempts):  # Try multiple times if needed
        angle = random.uniform(0, 2 * math.pi)  # Random angle
        distance = random.uniform(5, 30)  # Stay inside Mars

        # Convert to Cartesian (Mars center is at (40,40))
        cx = int(40 + distance * math.cos(angle))
        cy = int(40 + distance * math.sin(angle))
        radius = random.randint(5, 10)

        # Check for overlap
        overlap = any(math.dist((cx, cy), (ox, oy)) < (radius + oradius) for ox, oy, oradius in craters)
        
        if not overlap:  # If no overlap, accept this crater
            craters.append((cx, cy, radius))
            break  # Exit the loop once a valid spot is found

# Draw craters
for cx, cy, radius in craters:
    pygame.draw.circle(mars_surface, (150, 50, 30), (cx, cy), radius)  # Dark brown craters
    pygame.draw.circle(mars_surface, (180, 70, 50), (cx + 2, cy + 2), max(radius - 2, 2))  # Lighter highlight

while running:
    # Poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill screen with black
    screen.fill("black")

    # Draw stars
    for star in stars:
        pygame.draw.circle(screen, "white", star, 2)

    # Draw Mars (blitted so transparency works)
    screen.blit(mars_surface, (player_pos.x - 40, player_pos.y - 40))  # Center Mars on player_pos

    # Handle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    # Flip display
    pygame.display.flip()

    # Limit FPS to 60, update delta time
    dt = clock.tick(60) / 1000

pygame.quit()
