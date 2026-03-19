import math
from types import NotImplementedType
class Vec2:
	def __init__(
		self,
		p_x: float = 0.0,
		p_y: float = 0.0
	):
		self.x: float = p_x
		self.y: float = p_y
	
	#OPERATOR OVERLOADS
	def __add__(self, p_other: "Vec2") -> "Vec2 | NotImplementedType":
		if not isinstance(p_other, Vec2):
			return NotImplemented
		return Vec2(self.x + p_other.x, self.y + p_other.y)

	def __sub__(self, p_other: "Vec2") -> "Vec2 | NotImplementedType":
		if not isinstance(p_other, Vec2):
			return NotImplemented
		return Vec2(self.x - p_other.x, self.y - p_other.y)
	
	def __mul__(self, p_other: "int | float | Vec2") -> "Vec2 | NotImplementedType":
		if isinstance(p_other, (int, float)):
			return Vec2(self.x * p_other, self.y * p_other)
		if isinstance(p_other, Vec2):
			return Vec2(self.x * p_other.x, self.y * p_other.y)
		return NotImplemented

	def __rmul__(self, p_scalar: int | float) -> "Vec2 | NotImplementedType":
		if not isinstance(p_scalar, (int, float)):
			return NotImplemented
		return self.__mul__(p_scalar)
	
	def __imul__(self, p_scalar: int | float) -> "Vec2 | NotImplementedType":
		if not isinstance(p_scalar, (int, float)):
			return NotImplemented
		self.x *= p_scalar
		self.y *= p_scalar
		return self
	
	def __truediv__(self, p_other: "int | float | Vec2"):
		if isinstance(p_other, (int, float)):
			return Vec2(self.x / p_other, self.y / p_other)
		if isinstance(p_other, Vec2):
			return Vec2(self.x / p_other.x, self.y / p_other.y)
		return NotImplemented


	def __eq__(self, p_other: object) -> bool | NotImplementedType:
		if not isinstance(p_other, Vec2):
			return NotImplemented
		return self.x == p_other.x and self.y == p_other.y
	
	def __repr__(self) -> str:
		return f"({self.x}, {self.y})"
	
	#VECTOR SPECIFICS
	def dot(self, p_other: "Vec2") -> float:
		if not isinstance(p_other, Vec2):
			raise TypeError("Vec2.dot() expected Vec2")
		return (self.x * p_other.x) + (self.y * p_other.y)

	@property
	def magnitude(self) -> float:
		return math.sqrt(self.x * self.x + self.y * self.y)
	
	@property
	def lengthSquared(self) -> float:
		return self.x * self.x + self.y * self.y
	
	@property
	def unit(self) -> "Vec2":
		_magnitude = self.magnitude
		if _magnitude == 0:
			return Vec2(0.0, 0.0)
		return Vec2(self.x / _magnitude, self.y / _magnitude)
	
	@property
	def copy(self) -> "Vec2":
		return Vec2(self.x, self.y)


class Vec2i:
	def __init__(
		self,
		p_x: int = 0,
		p_y: int = 0
	):
		self.x: int = int(p_x)
		self.y: int = int(p_y)
	
	#OPERATOR OVERLOADS
	def __add__(self, p_other: "Vec2i") -> "Vec2i | NotImplementedType":
		if not isinstance(p_other, Vec2i):
			return NotImplemented
		return Vec2i(self.x + p_other.x, self.y + p_other.y)

	def __sub__(self, p_other: "Vec2i") -> "Vec2i | NotImplementedType":
		if not isinstance(p_other, Vec2i):
			return NotImplemented
		return Vec2i(self.x - p_other.x, self.y - p_other.y)
	
	def __mul__(self, p_other: int | float | "Vec2i") -> "Vec2i | NotImplementedType":
		if isinstance(p_other, int):
			return Vec2i(self.x * p_other, self.y * p_other)
		if isinstance(p_other, float):
			return Vec2i(round(self.x * p_other), round(self.y * p_other))
		if isinstance(p_other, Vec2i):
			return Vec2i(self.x * p_other.x, self.y * p_other.y)
		return NotImplemented

	def __rmul__(self, p_scalar: int | float) -> "Vec2i | NotImplementedType":
		return self.__mul__(p_scalar)

	def __imul__(self, p_scalar: int | float) -> "Vec2i | NotImplementedType":
		if isinstance(p_scalar, int):
			self.x *= p_scalar
			self.y *= p_scalar
			return self
		if isinstance(p_scalar, float):
			self.x = round(self.x * p_scalar)
			self.y = round(self.y * p_scalar)
			return self
		return NotImplemented
	
	def __floordiv__(self, p_other: int) -> "Vec2i | NotImplementedType":
		if not isinstance(p_other, int):
			return NotImplemented
		return Vec2i(self.x // p_other, self.y // p_other)

	def __eq__(self, p_other: object) -> bool | NotImplementedType:
		if not isinstance(p_other, Vec2i):
			return NotImplemented
		return self.x == p_other.x and self.y == p_other.y
	
	def __repr__(self) -> str:
		return f"({self.x}, {self.y})"
	
	#VECTOR SPECIFICS (safe ones)
	def dot(self, p_other: "Vec2i") -> int:
		if not isinstance(p_other, Vec2i):
			raise TypeError("Vec2i.dot() expected Vec2i")
		return (self.x * p_other.x) + (self.y * p_other.y)

	@property
	def lengthSquared(self) -> int:
		return self.x * self.x + self.y * self.y
	
	@property
	def copy(self) -> "Vec2i":
		return Vec2i(self.x, self.y)

	def tuple(self) -> tuple[int, int]:
		return (self.x, self.y)