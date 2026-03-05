import math
class Vec2:
	def __init__(self, p_x: float = 0.0, p_y: float = 0.0):
		self.x = p_x
		self.y = p_y
	
	def __add__(self, p_other):
		return Vec2(self.x + p_other.x, self.y + p_other.y)

	def __sub__(self, p_other):
		return Vec2(self.x - p_other.x, self.y - p_other.y)
	
	def __mul__(self, p_other):
		return Vec2(self.x * p_other.x, self.y * p_other.y)

	def __rmul__(self, p_scalar):
		return Vec2(self.x * p_scalar, self.y * p_scalar)
	
	def __imul__(self, p_scalar):
		return Vec2(self.x * p_scalar, self.y * p_scalar)

	def __eq__(self, p_other):
		return self.x == p_other.x and self.y == p_other.y
	def magnitude(self):
		return math.sqrt(self.x * self.x + self.y * self.y)
	
	def length(self):
		return self.x * self.x + self.y * self.y
	
	def normalise(self):
		mag = self.magnitude()
		if mag == 0:
			return Vec2()
		return Vec2(self.x / mag, self.y / mag)
	
	def __repr__(self):
		return f"({self.x}, {self.y})"
	
	def dot(self, p_other):
		return (self.x * p_other.x) + (self.y * p_other.y)
