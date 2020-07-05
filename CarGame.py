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
	fps_controller = FPSController(fps)
	
	global done
	while not done:
		s_time = time.time()
		
		b.drive(pygame.key.get_pressed())
		b.update_loc()

		# print("Update FPS: ", clock.get_fps())
		
		e_time = time.time()
		work_time = e_time-s_time

		fps_controller.sleep(work_time, clock.get_fps(), True)
		clock.tick()

def draw_thread(fps:float, clock:pygame.time.Clock):
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

		print("Draw FPS: ", clock.get_fps())
		
		e_time = time.time()
		work_time = e_time-s_time

		fps_controller.sleep(work_time, clock.get_fps())

		clock.tick()

drawClock = pygame.time.Clock()
updateClock = pygame.time.Clock()

threading.Thread(target=update_thread, args=[update_fps, updateClock]).start()
draw_thread(draw_fps, drawClock)




