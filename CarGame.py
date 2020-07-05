import pygame
from BlockCar import *
from FPSController import *
import time, threading

pygame.init()

w, h = (800, 600)

screen = pygame.display.set_mode((w, h))

b = BlockCar(bounds=[w,h], size=[50,25])

update_fps = 500
draw_fps = 60

done = False

def update_thread(fps:float, clock:pygame.time.Clock):
	'''
	This loop runs on a seperate thread, and controls the internal game logic
	Currently, this should run at around 500 fps
	'''
	fps_controller = FPSController(fps)	
	
	global done
	while not done:
		s_time = time.time()
		
		b.drive(pygame.key.get_pressed())
		b.update_loc()
		
		e_time = time.time()
		work_time = e_time-s_time

		fps_controller.sleep(work_time, clock.get_fps())
		clock.tick(1000)


def draw_thread(fps:float, clock:pygame.time.Clock):
	'''
	This loop controls the graphics in the game, and runs on the main thread
	Should run at 60 FPS
	'''
	fps_controller = FPSController(fps)

	global done
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
		s_time = time.time()
		
		pygame.draw.rect(screen, (255,255,255), (0,0,w,h))
		b.draw(screen)
		pygame.display.flip()
		
		e_time = time.time()
		work_time = e_time-s_time

		fps_controller.sleep(work_time, clock.get_fps())

		clock.tick(1000)

drawClock = pygame.time.Clock()
updateClock = pygame.time.Clock()

threading.Thread(target=update_thread, args=[update_fps, updateClock]).start()
draw_thread(draw_fps, drawClock)

print("\nExited with 0")