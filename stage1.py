def stage1_play(screen, font):
    screen.fill((255, 255, 255))  # Example for stage1, fill with white
    text = font.render("Stage 1", True, (0, 0, 0))
    screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2))
    