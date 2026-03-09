import math
from core.vector import Vec2
from core.transform import Transform
from core.utils import clamp

class Collider:
	def __init__(
		self,
		p_ignoreColliders: set["Collider"] | None = None
	):
		self._ignoreColliders: set["Collider"] = p_ignoreColliders if p_ignoreColliders is not None else set()
		self._position: Vec2 = Vec2(0.0, 0.0)
		self._canCollide: bool = True
		self._collisionCount: int = 0


	def canCollide(self, p_canCollide: bool) -> None:
		self._canCollide = p_canCollide

	def updateTransform(self, p_transform: Transform) -> None:
		self._position = p_transform.position

	@staticmethod #Cirlce vs Circle | Squared Distance Test
	def collideCircleCircle(p_circleA: "CircleCollider", p_circleB: "CircleCollider") -> bool: #for circle to circle comparison
		delta = Vec2(
			(p_circleA._position.x - p_circleB._position.x),
			(p_circleA._position.y - p_circleB._position.y)
		)
		combined_radius = p_circleA._radius + p_circleB._radius
		return (delta.x * delta.x + delta.y * delta.y) <= combined_radius * combined_radius
	
	@staticmethod #Cricle vs Rectangle | Oriented Bounding Box (OBB)
	def collideCircleRectangle( p_circle: "CircleCollider", p_rectangle: "RectangleCollider") -> bool: #for circle to rect collision
		to_circle = p_circle._position - p_rectangle._position; #to circle from rect
		
		projected_axes = Vec2(
			to_circle.dot(p_rectangle._axisI), #project upon the rects local x axis
			to_circle.dot(p_rectangle._axisJ) #these are now the circle in the rect space being rect is origin and axis aligned
		)

		closest_point = Vec2(
			clamp(projected_axes.x, -p_rectangle._halfSize.x, p_rectangle._halfSize.x),
			clamp(projected_axes.y, -p_rectangle._halfSize.y, p_rectangle._halfSize.y)
		) #this gets the closest point to/in the rect at whatever is the closest by clamping it now to the dimensions of the box on both _axes
		
		closest_world_point = p_rectangle._position + (p_rectangle._axisI * closest_point.x) + (p_rectangle._axisJ * closest_point.y) #convert back into the true world space out of this rect origin axis aligned world
		delta = p_circle._position - closest_world_point #now go to the circle from the closest point on the rect
		delta_length = delta.lengthSquared() #sqaure distance, use magnitude() for typical ||v|| sizing
		return (delta_length) < (p_circle._radius * p_circle._radius) #if the dist to circle is < than the circle radius we must be colliding

	@staticmethod # Polygon vs Polygon | Seperating Axis Theorem (SAT)
	def collidePolygonPolygon(p_polygonA: "PolygonCollider", p_polygonB: "PolygonCollider") -> bool: #for rect to rect collision
		edge_normals = p_polygonA.edgeNormals + p_polygonB.edgeNormals #combined lists of both shapes local _axes
		for axis in edge_normals:
			a_min_max = p_polygonA.project(axis)
			b_min_max = p_polygonB.project(axis)

			if a_min_max.y < b_min_max.x or b_min_max.y < a_min_max.x:
				return False #found at least 1 axis they dont touch on
		return True
	
	def overlaps(self, p_other: "Collider") -> bool:
		if not self._canCollide:
			return False
		
		if p_other in self._ignoreColliders:
			return False
		
		if isinstance(self, CircleCollider) and isinstance(p_other, CircleCollider):
			return Collider.collideCircleCircle(self, p_other)
		
		if isinstance(self, CircleCollider) and isinstance(p_other, RectangleCollider):
			return Collider.collideCircleRectangle(self, p_other)
		
		if isinstance(self, RectangleCollider) and isinstance(p_other, CircleCollider):
			return Collider.collideCircleCircle(p_other, self) #swap to make sure its rect upon circle
		
		if isinstance(self, PolygonCollider) and isinstance(p_other, PolygonCollider):
			return Collider.collidePolygonPolygon(self, p_other)
		
		return False #default if its not one of those types

	@property
	def collisionCount(self) -> int:
		return self._collisionCount
	
class CircleCollider(Collider):
	def __init__(
		self,
		p_radius: float
	):
		Collider.__init__(self)
		self._radius: float = p_radius
	
	def updateTransform(self, p_transform):
		super().updateTransform(p_transform)
		self._radius = p_transform.size.x
	

class PolygonCollider(Collider):
	def __init__(self):
		Collider.__init__(self)
		self._rotation = 0.0
		self._vertices: list[Vec2] = []

	def updateTransform(self, p_transform):
		super().updateTransform(p_transform)
		self._rotation = p_transform.rotation

	def project(self, p_axis: Vec2) -> Vec2:
		min_projection = float("inf")
		max_projection = -float("inf")

		for vertex in self._vertices: #project and track min and max
			projection = vertex.dot(p_axis)
			if projection < min_projection:
				min_projection = projection
			if projection > max_projection:
				max_projection = projection
		return Vec2(min_projection, max_projection)

class RectangleCollider(PolygonCollider):
	def __init__(
		self,
		p_size: Vec2
	):
		PolygonCollider.__init__(self)
		self._size: Vec2 = p_size
		self._halfSize: Vec2 = p_size * 0.5
		self._axisI: Vec2 = Vec2(1.0, 0.0)
		self._axisJ: Vec2 = Vec2(0.0, 1.0)

	def updateTransform(self, p_transform):
		super().updateTransform(p_transform)
		self._size = p_transform.size
		self._halfSize = p_transform.size * 0.5
		
		#generate vertices | local axis aligned vertices
		self._vertices = [
			Vec2(-self._halfSize.x, self._halfSize.y), #top left
			Vec2(self._halfSize.x, self._halfSize.y), #top right
			Vec2(self._halfSize.x, -self._halfSize.y), #bottom right
			Vec2(-self._halfSize.x, -self._halfSize.y) #bottom left
		]

		#get reusable sin cos for current theta
		cos_theta = math.cos(self._rotation)
		sin_theta = math.sin(self._rotation)

		#reuse sin and cos to create local x and y axis of unit length
		self._axisI = Vec2(cos_theta, sin_theta)
		self._axisJ = Vec2(-sin_theta, cos_theta)

		for index, vertex in enumerate(self._vertices): #rotate all points then put back into world space using I and J
			x = vertex.x
			y = vertex.y
			self._vertices[index] = Vec2(
				(x * self._axisI.x) + (y * self._axisJ.x) + self._position.x,
				(x * self._axisI.y) + (y * self._axisJ.y) + self._position.y
			)

	@property
	def edgeNormals(self) -> tuple[Vec2, Vec2]:
		return self._axisI, self._axisJ
