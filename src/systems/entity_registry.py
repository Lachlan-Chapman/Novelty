from core.console import CONSOLE
from entities.entity import Entity
class EntityRegistry:
	def __init__(self):
		self._entities: list[Entity] = []
		self._entityCount: int = 0 #makes it easier so i can avoid calling len(self._entites) every time i wanna quickly query it, also i think better readability
		self._entityIdentityCounter: int = 0

		self._currentCollisions: set[tuple[int, int]] = set()
		self._previousCollisions: set[tuple[int, int]] = set()

	def add(self, p_other: Entity):
		if isinstance(p_other, Entity):
			#register with a unique once only ID
			p_other.setId(self._entityIdentityCounter)
			self._entityIdentityCounter += 1 #always increment never reused ID
			
			self._entities.append(p_other)
			self._entityCount += 1
		else:
			CONSOLE.warn("entityRegistry.add() was given not Entity type")

	def update(self): #asks all entities to update themseleves for PURELY internal data if they have such logic
		for entity in self._entities:
			entity.update()

	def handleCollision(self):
		for entity in self._entities:
			entity._collider._collisionCount = 0 #reset collision at the start of each frame

		self._currentCollisions.clear()

		for current_entity in range(0, self._entityCount):
			for other_entity in range(current_entity + 1, self._entityCount): #too avoid a collides with b then b collides with a
				a = self._entities[current_entity]
				b = self._entities[other_entity]

				if not a.alive or not b.alive: #possible for an entity to be dead mid frame but not yet cleared
					continue

				a.updateGeometry()
				b.updateGeometry()
				if a.overlaps(b): #stage just to see if the objects touch
					pair = (a.id, b.id) #since our loop is already from start of list to latest the ID at the end of the registry is always greater than the previous | dont need sorting
					#pair = tuple(sorted(a._identity, b._identity)) #using sorting and the set non duplicate method
					self._currentCollisions.add(pair) #if it already exists it wont duplicate as we used set()
					a._collider._collisionCount += 1
					b._collider._collisionCount += 1
					
					if pair not in self._previousCollisions:
						a.onCollisionEnter(b)
						b.onCollisionEnter(a)
		self._previousCollisions = self._currentCollisions.copy()

		for entity in self._entities: #for debugging
			entity.drawCollision()
	
	def removeDead(self):
		#slower than looping but for now its the easiest option | for small entity count such is this game, its fine
		self._entities = [entity for entity in self._entities if entity.alive]
		self._entityCount = len(self._entities)
		#for entity in self._entities:
			#if entity._alive is False:
				#self._entities.remove(entity)

	def draw(self):
		for entity in self._entities:
  			entity.draw()

ENTITY_REGISTRY = EntityRegistry()