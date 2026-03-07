RAD_TO_DEG = 57.29577951308232
DEG_TO_RAD = 0.017453292519943295

def clamp(p_value, p_min, p_max):
	if p_value < p_min:
		return p_min
	if p_value > p_max:
		return p_max
	return p_value

def toDegrees(p_radians):
	return p_radians * RAD_TO_DEG

def toRadians(p_degrees):
	return p_degrees * DEG_TO_RAD