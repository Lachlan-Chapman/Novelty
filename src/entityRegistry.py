from src.entity import Entity
class EntityRegistry:
	def __init__(self):
		self.m_entityCount = 0 #makes it easier so i can avoid calling len(self.m_entites) every time i wanna quickly query it, also i think better readability
		self.m_entities = []
		self.m_currentCollisions = set()
		self.m_previousCollisions = set()
		self.m_entityIdentityCounter = 0

	def add(self, p_other: "Entity"):
		if isinstance(p_other, Entity):
			#register with a unique once only ID
			p_other.m_identity = self.m_entityIdentityCounter
			self.m_entityIdentityCounter += 1 #always increment never reused ID
			
			self.m_entities.append(p_other)
			self.m_entityCount += 1
		else:
			print("entityRegistry.add() was given not Entity type")

	def update(self): #asks all entities to update themseleves for PURELY internal data if they have such logic
		for entity in self.m_entities:
			entity.updatePosition()

	def handleCollision(self):
		for entity in self.m_entities:
			entity.m_collisionCount = 0 #reset collision at the start of each frame

		self.m_currentCollisions.clear()

		for current_entity in range(len(self.m_entities)):
			for other_entity in range(current_entity + 1, len(self.m_entities)): #too avoid a collides with b then b collides with a
				a = self.m_entities[current_entity]
				b = self.m_entities[other_entity]

				if not a.m_alive or not b.m_alive: #possible for an entity to be dead mid frame but not yet cleared
					continue

				if a.m_owner is b or b.m_owner is a:
					continue #friendly collision means they are transparent to one another and allowed to collide

				if a.collideWith(b): #stage just to see if the objects touch
					pair = (a.m_identity, b.m_identity) #since our loop is already from start of list to latest the ID at the end of the registry is always greater than the previous | dont need sorting
					#pair = tuple(sorted(a.m_identity, b.m_identity)) #using sorting and the set non duplicate method
					self.m_currentCollisions.add(pair) #if it already exists it wont duplicate as we used set()
					a.m_collisionCount += 1
					b.m_collisionCount += 1
					
					if pair not in self.m_previousCollisions:
						a.onCollisionEnter(b)
						b.onCollisionEnter(a)
		self.m_previousCollisions = self.m_currentCollisions.copy()

		for entity in self.m_entities: #for debugging
			entity.drawCollision()


	
	def removeDead(self):
		#slower than looping but for now its the easiest option | for small entity count such is this game, its fine
		self.m_entities = [entity for entity in self.m_entities if entity.m_alive]
		self.m_entityCount = len(self.m_entities)
		#for entity in self.m_entities:
			#if entity.m_alive is False:
				#self.m_entities.remove(entity)

	def draw(self):
		for entity in self.m_entities:
			entity.draw()

ENTITY_REGISTRY = EntityRegistry()