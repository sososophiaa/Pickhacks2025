import random

def stage1_play(screen, font, pygame, stars):
    screen.fill(("black"))  # Example for stage1, fill with black
    text = font.render("Stage 1", True, ("white"))
    screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2))


     # Generate stars (x, y, initial brightness)
    for i in range(len(stars)):
        x, y, brightness = stars[i]
        brightness += random.randint(-5, 5)  # Slight flickering effect
        brightness = max(100, min(255, brightness))  # Keep brightness in range
        stars[i] = (x, y, brightness)  # Update star with new brightness
        pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), 2)  # Draw star

    # Mars properties
    mars_radius = 1200  # Increased Mars size
    mars_center = mars_radius  # Center offset for drawing

    # Create Mars texture
    mars_surface = pygame.Surface((mars_radius * 2, mars_radius * 2), pygame.SRCALPHA)
    mars_surface.fill((0, 0, 0, 0))  # Transparent background

    # Draw the base red-orange planet
    pygame.draw.circle(mars_surface, (210, 90, 40), (mars_center, mars_center+1200), mars_radius)  # Mars base color

    # Add shading (radial gradient effect)
    for i in range(mars_radius, 0, -1):  # From outer edge to center
        color = (max(100, 210 - i * 2), max(40, 90 - i), max(20, 40 - i // 2))  # Darker towards edges
        pygame.draw.circle(mars_surface, color, (mars_center, mars_center+1200), i)

    screen.blit(mars_surface, (screen.get_width() // 2 - mars_radius, screen.get_height() // 2 - mars_radius))

   # lander_image = pygame.image.load("lander.png").convert_alpha()  # Load PNG with transparency
   # lander_image = pygame.transform.scale(lander_image, (70, 70))  # Resize if needed
   # lander_rect = lander_image.get_rect(center=lander_pos)