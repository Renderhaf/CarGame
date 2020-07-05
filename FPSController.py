import time 

class FPSController():
	def __init__(self, fps:int):
		self.fps = fps
		self.tick_length = 1.0/fps
		self.cutoff = 3
		self.kP = 0.01
		self.kD = -0.0001
		self.max_power = 0.05
		self.lastE = None

	def sleep(self, work_time:float, real_fps:float, debug = False):
		milliseconds = max(self.tick_length-work_time, 0) * 1000

		if milliseconds < self.cutoff:
			return
		else:
			tts = (milliseconds)/1000
			time.sleep(tts)

		error = (self.fps - real_fps)
		p = self.kP * error
		d = self.kD * (error - self.lastE)
		self.cutoff += self._clamp(p + d, self.max_power)
		
		self.lastE = error

		if debug:
			print(self.cutoff, p)

	@staticmethod
	def _clamp(value:float, min_max:float):
		if value > min_max:
			return min_max
		elif value < -min_max:
			return -min_max
		else:
			return value
		