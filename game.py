__author__ = 'Florian Tautz'

import pygame
import pygame.midi


class Game:
    def __init__(self):
        pygame.init()
        pygame.midi.init()
        midi_port = pygame.midi.get_default_output_id()
        self._midi = pygame.midi.Output(midi_port)
        self._midi.set_instrument(56)

        size = self._width, self._height = 1920, 1200
        self._speed = [2, 2]

        self._screen = pygame.display.set_mode(size, pygame.FULLSCREEN|
                                                     pygame.DOUBLEBUF|
                                                     pygame.HWSURFACE)
        self._ball = pygame.image.load("ball.png")
        self._ball_rect = self._ball.get_rect()

        self._last_update = 0

    def run(self):
        while True:
            for event in pygame.event.get():
                self.handle_event(event)

            self.update(pygame.time.get_ticks())
            self.draw()

    def update(self, game_time):
        time_passed = game_time - self._last_update
        if time_passed < 10:
            return
        self._last_update = game_time

        v = 0.2
        dx = self._speed[0] * (time_passed / (1/v))
        dy = self._speed[1] * (time_passed / (1/v))

        self._ball_rect = self._ball_rect.move(dx, dy)

        # keep ball in bounds
        if self._ball_rect.left < 0 or self._ball_rect.right > self._width:
            self._speed[0] *= -1
        if self._ball_rect.top < 0 or self._ball_rect.bottom > self._height:
            self._speed[1] *= -1

    def draw(self):
        self._screen.fill((255, 255, 255))
        self._screen.blit(self._ball, self._ball_rect)
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.stop()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.stop()
            if event.key == pygame.K_f:
                self._midi.note_on(72, 127) # c
            if event.key == pygame.K_g:
                self._midi.note_on(74, 127) # d
            if event.key == pygame.K_h:
                self._midi.note_on(76, 127) # e
            if event.key == pygame.K_j:
                self._midi.note_on(77, 127) # f
            if event.key == pygame.K_k:
                self._midi.note_on(79, 127) # g
            if event.key == pygame.K_l:
                self._midi.note_on(81, 127) # a
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_f:
                self._midi.note_off(72, 127) # c
            if event.key == pygame.K_g:
                self._midi.note_off(74, 127) # d
            if event.key == pygame.K_h:
                self._midi.note_off(76, 127) # e
            if event.key == pygame.K_j:
                self._midi.note_off(77, 127) # f
            if event.key == pygame.K_k:
                self._midi.note_off(79, 127) # g
            if event.key == pygame.K_l:
                self._midi.note_off(81, 127) # a

    def stop(self):
        del self._midi
        pygame.midi.quit()
        exit()