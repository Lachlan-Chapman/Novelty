import math
import random
RAD_TO_DEG: float = 180 / math.pi #57.29577951308232 
DEG_TO_RAD: float = math.pi / 180 #0.017453292519943295 

def clamp(p_value, p_min: int | float, p_max: int | float) -> int | float:
	if p_value < p_min:
		return p_min
	if p_value > p_max:
		return p_max
	return p_value

def toDegrees(p_radians: float) -> float:
	return p_radians * RAD_TO_DEG

def toRadians(p_degrees: float) -> float:
	return p_degrees * DEG_TO_RAD

def randomRange(p_min: float, p_max: float) -> float: #returns number in range inclusive
	return p_min + random.random() * (p_max - p_min)