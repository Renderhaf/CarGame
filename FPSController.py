import time, sys, math

class FPSController():
	def __init__(self, fps:int):
		self.fps = fps
		self.tick_length = 1.0/fps
		self.power = 1
		self.kP = 0.00025
		self.kD = -0.00003
		self.max_power = 0.05
		self.lastE = None

	def sleep(self, work_time:float, real_fps:float, debug = False):
		'''
		This function:
			- Sleeps the amount of time required to keep the desired FPS
			- Calulates the amount of time to sleep using PD closed-loop control
		'''
		# Sleep for the required time
		milliseconds = max(self.tick_length-work_time, 0) * 1000
		tts = ((milliseconds)/1000) * self.power
		tts = 0 if tts <= 0 else tts
		time.sleep(tts)

		# Make sure that pygame.time.Clock.get_fps did not return inf
		if self._isBadNumber(real_fps):
			real_fps = self.fps
		
		# Calculate the pd
		error = (self.fps - real_fps)
		p = self.kP * error
		if self.lastE != None:
			d = self.kD * (error - self.lastE)
		else:
			d = 0
		pd = self._clamp(p + d, self.max_power)

		# Adjust the power based on the PD value
		self.power -= pd
		
		self.lastE = error

		if debug:
			sys.stdout.write("FPS: {}  Power: {}  PD: {}\r".format(real_fps, self.power, pd))

	@staticmethod
	def _clamp(value:float, min_max:float):
		if value > min_max:
			return min_max
		elif value < -min_max:
			return -min_max
		else:
			return value
		
	@staticmethod
	def _isBadNumber(number)->bool:
		return number != number or number == float("inf") or number == -float("inf")