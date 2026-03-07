from core.vector import Vec2
from core.utils import clamp

class Collider:
	def __init__(self):
		self.m_canCollide = True
		self.m_collisionCount = 0

	def canCollide(self, p_canCollide):
		self.m_canCollide = p_canCollide #allows enabling/disabling collisions without causing null references

	def collideCircleCirlce(self, p_a, p_b) -> bool: #for circle to circle comparison
		delta = Vec2(
			(p_a.m_position.x - p_b.m_position.x),
			(p_a.m_position.y - p_b.m_position.y)
		)
		radius = p_a.m_radius + p_b.m_radius
		return (delta.x * delta.x + delta.y * delta.y) <= radius * radius
	
	def collideOOB(self, p_circle, p_rectangle) -> bool: #for circle to rect collision
		p_rectangle.updateGeometry() #ensure local normals are accurate
		to_circle = p_circle.m_position - p_rectangle.m_position; #to circle from rect
		projected_axes = Vec2(
			to_circle.dot(p_rectangle.m_axes[0]), #project upon the rects local x axis
			to_circle.dot(p_rectangle.m_axes[1]) #these are now the circle in the rect space being rect is origin and axis aligned
		)
		closest_point = Vec2(
			clamp(projected_axes.x, -p_rectangle.m_halfDimensions.x, p_rectangle.m_halfDimensions.x),
			clamp(projected_axes.y, -p_rectangle.m_halfDimensions.y, p_rectangle.m_halfDimensions.y)
		) #this gets the closest point to/in the rect at whatever is the closest by clamping it now to the dimensions of the box on both m_axes
		closest_world_point = p_rectangle.m_position + (p_rectangle.m_axes[0] * closest_point.x) + (p_rectangle.m_axes[1] * closest_point.y) #convert back into the true world space out of this rect origin axis aligned world
		delta = p_circle.m_position - closest_world_point #now go to the circle from the closest point on the rect
		delta_len = delta.length() #sqaure distance, use magnitude() for typical ||v|| sizing
		# print(f"{delta_len} | {p_circle.m_radius * p_circle.m_radius}")
		return (delta_len) < (p_circle.m_radius * p_circle.m_radius) #if the dist to circle is < than the circle radius we must be colliding

	def collideSAT(self, p_a, p_b) -> bool: #for rect to rect collision
		p_a.updateGeometry() #only SAT needs vertices and normals to be accurate, so this allows for only doing all that math each collision over each frame
		p_b.updateGeometry() #make sure shapes vertices and surface are all set before we start doing collision logic
		edge_normals = p_a.getEdgeNormals() + p_b.getEdgeNormals() #combined lists of both shapes local m_axes
		for axis in edge_normals:
			a_min_max = p_a.project(axis)
			b_min_max = p_b.project(axis)

			if a_min_max.y < b_min_max.x or b_min_max.y < a_min_max.x:
				return False #found at least 1 axis they dont touch on
		return True
	
	def overlaps(self, p_a, p_b):
		if not self.m_canCollide:
			return False
		if p_a.m_shape == "circle" and p_b.m_shape == "circle":
			#print("circle circle collide")
			return self.collideCircleCirlce(p_a, p_b)
		
		if p_a.m_shape == "circle" and p_b.m_shape == "rectangle":
			#print("circle circle rectangle")
			return self.collideOOB(p_a, p_b)
		
		if p_a.m_shape == "rectangle" and p_b.m_shape == "circle":
			#print("rectangle circle collide")
			return self.collideOOB(p_b, p_a) #swap to make sure its rect upon circle
		
		if p_a.m_shape == "rectangle" and p_b.m_shape == "rectangle":
			#print("rectangle rectangle collide")
			return self.collideSAT(p_a, p_b)
		return False #default if its not one of those types
	
