core -> physics/render -> entites -> gameplay/systems -> main
core are independent or at worst use pygame (the game engine my game sits above). These items serve as a bedrock which are used by other objects. often technical tools and data structures like Vec2 or the TIME instance for tracking delta_time globally

physics and render are technical components that are purely for the computational side of the game. They can be considered agnostic to this specific game. Things like squares colliding with circles is because its a requirement of this game but many other games would need the same thing.

Entities are the actors in our game. They act without the environment built by our physics and rendering system. They are very blurred line between purely computations and game specific logic. It acts as the bridge between the computational systems and the game specific logic. They contain parts agnostic of this game but also game specific parts

gameplay is very game specific and are made to handle things only this game would have. They have parts that the user would interact with which are apart of what they would describe the game to a friend. 

the systems while on the same layer as gameplay, serve as logical helpers to help coordinate runtime. These are tools needed to allow, technically the gameplay to exist. Entities interact within the world which the user sees, the entity registry exists to allow such thing to work as expected