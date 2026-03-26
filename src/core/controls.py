import pygame
class Actions:
	ROTATE_LEFT: str = "rotate_left"
	ROTATE_RIGHT: str = "rotate_right"
	SHOOT: str = "shoot"
	NEXT_WEAPON: str = "next_weapon"
	PREVIOUS_WEAPON: str = "previous_weapon"
	EXIT: str = "exit"
	RESET: str = "reset"

BINDINGS: dict[str, tuple[int, ...]] = {
	Actions.ROTATE_LEFT: (pygame.K_a, pygame.K_LEFT),
	Actions.ROTATE_RIGHT: (pygame.K_d, pygame.K_RIGHT),
	Actions.SHOOT: (pygame.K_SPACE,),
	Actions.NEXT_WEAPON: (pygame.K_w, pygame.K_UP),
	Actions.PREVIOUS_WEAPON: (pygame.K_s, pygame.K_DOWN),
	Actions.EXIT: (pygame.K_ESCAPE,),
	Actions.RESET: (pygame.K_r,)
}

class InputState:
	def __init__(self):
		self._current = None
		self._previous = None
		self._held: dict[str, bool] = {}
		self._pressed: dict[str, bool] = {}
		self._released: dict[str, bool] = {}

	def update(self) -> None:
		#these are lists of key inputs
		self._previous = self._current
		self._current = pygame.key.get_pressed()

		for action, keys in BINDINGS.items(): #for all key/value pairs
			#these are booleans of if a key is pressed (more is a key of the possible bindings pressed)
			current = any(self._current[key] for key in keys) #for all keys in the possible key for a given action, are any of them true
			previous = False if self._previous is None else any(self._previous[key] for key in keys) #for this action, are any of the keys true in the previous frame

			self._held[action] = current #this frames key pressed, if it was pressed then its helf
			self._pressed[action] = current and not previous #its pressed if this is the first frame its active
			self._released[action] = not current and previous #released of now in the previous but no longer in the current frame input

	def isHeld(self, action: str) -> bool:
		return self._held.get(action, False)
	
	def isPressed(self, action: str) -> bool:
		return self._pressed.get(action, False)
	
	def isReleased(self, action: str) -> bool:
		return self._released.get(action, False)
	
INPUT_STATE: InputState = InputState()