import random

from scene import *

		
class Planet:
	def __init__(self):
		self.id = 0
		self.mass = 0.0
		self.scale = 1.0
		
		self.pos = Vector2(0, 0)
		self.v = Vector2(0, 0)
		self.a = Vector2(0, 0)
		

class Galaxy:
	planets = []
	
	def __init__(self, size, w, h):
		for i in range(size):
			self.planets.append(Planet())
			self.planets[i].id = i
			self.planets[i].mass = random.randint(1, 1)
			self.planets[i].pos = Vector2(random.randint(0, w), random.randint(0,h))
			self.planets[i].v = Vector2(random.randint(-700, 700),
																		random.randint(-700, 700))


def findPlanetInRadius(thisPlanet: Planet, otherPlanets: Galaxy.planets, R):
	newPlanets = []
	newPlanets.append(thisPlanet)
	for thatPlanet in otherPlanets:
		r = ((thisPlanet.pos[0]-thatPlanet.pos[0])**2 +
					(thisPlanet.pos[1] - thatPlanet.pos[1])**2)**0.5
		if r <= R:
			newPlanets.append(thatPlanet)
	return newPlanets


def findF(thisPlanet: Planet, otherPlanets: Galaxy.planets):
	G = 1
	xi = 0.0
	yi = 0.0
	for thatPlanet in otherPlanets:
		if thisPlanet.id != thatPlanet.id:
			xi += G*thatPlanet.mass * (thisPlanet.pos[0]-thatPlanet.pos[0]) / \
																((thisPlanet.pos[0]-thatPlanet.pos[0])**2 +
																	(thisPlanet.pos[1]-thatPlanet.pos[1])**2)**(3/2)
																
			yi += G*thatPlanet.mass * (thisPlanet.pos[1]-thatPlanet.pos[1]) / \
																((thisPlanet.pos[0]-thatPlanet.pos[0])**2 +
																	(thisPlanet.pos[1]-thatPlanet.pos[1])**2)**(3/2)
	return xi, yi


def displace(thisPlanet: Planet, otherPlanets: Galaxy.planets):
	T = 1e-3

	thisPlanet.a = -1*Vector2(findF(thisPlanet, otherPlanets)[0],
														findF(thisPlanet, otherPlanets)[1])
	
	thisPlanet.v = Vector2(thisPlanet.v[0] + thisPlanet.a[0] * T,
													thisPlanet.v[1] + thisPlanet.a[1] * T)
	
	thisPlanet.pos = Vector2(thisPlanet.pos[0] + thisPlanet.v[0] * T,
														thisPlanet.pos[1] + thisPlanet.v[1] * T)
	
	
def bornKarman(planet: Planet, minX, minY, maxX, maxY):
		if planet.pos[0] <= minX:
			planet.pos = Vector2(planet.pos[0]+maxX-1, planet.pos[1])
		if planet.pos[1] <= minY:
			planet.pos = Vector2(planet.pos[0], planet.pos[1]+maxY-1)
		if planet.pos[0] >= maxX:
			planet.pos = Vector2(planet.pos[0]-maxX+1, planet.pos[1])
		if planet.pos[1] >= maxY:
			planet.pos = Vector2(planet.pos[0], planet.pos[1]-maxY+1)
			
			
def bordersReflection(planet: Planet, minX, minY, maxX, maxY):
		if planet.pos[0] <= minX or planet.pos[0] >= maxX:
			planet.v = Vector2(planet.v[0]*-0.05, planet.v[1])
		if planet.pos[1] <= minY or planet.pos[1] >= maxY:
			planet.v = Vector2(planet.v[0], planet.v[1]*-0.05)
			
			
def collision(thisPlanet: Planet, otherPlanets: Galaxy.planets):
	for thatPlanet in otherPlanets:
		if thisPlanet.id != thatPlanet.id:
			if thisPlanet.pos[0] == thatPlanet.pos[0] and \
					thisPlanet.pos[1] == thatPlanet.pos[1]:
				thisPlanet.v = thisPlanet.v*-1
				
				
def braking(planet: Planet):
	if planet.v[0] >= 1000 or planet.v[1] >= 1000:
		planet.v -= planet.v*0.1
	elif planet.v.x >= 5000:
		planet.v -= planet.v*0.5
	
	
class Simulation (Scene):
	def setup(self):
		self.background_color = 'black'
		self.gal = Galaxy(1, self.size.w, self.size.h)
		
		masses = []
		for planet in self.gal.planets:
			masses.append(planet.mass)
		maxMass = max(masses)
		for planet in self.gal.planets:
			planet.scale = planet.mass/maxMass
			
		self.sprites = []
		for planet in self.gal.planets:
			self.sprites.append(SpriteNode('plf:Item_CoinSilver', scale=planet.scale,
																			position=(planet.pos[0], planet.pos[1])))
		for sprite in self.sprites:
			self.add_child(sprite)
			
		self.gal.planets[0].mass = 1e8
		self.gal.planets[0].v = Vector2(0,0)
		self.gal.planets[0].pos = Vector2(self.size.w/2, self.size.h/2)
		
			
	def update(self):
		for planet, sprite in zip(self.gal.planets, self.sprites):
			oldPos = planet.pos
			displace(planet, self.gal.planets)
			#bordersReflection(planet, 0, 0, self.size.w, self.size.h)
			bornKarman(planet, 0, 0, self.size.w, self.size.h)
			braking(planet)
			sprite.position = planet.pos[0], planet.pos[1]
			newPos = planet.pos
			
	def touch_began(self, touch):
		x, y = touch.location
		self.gal.planets.append(Planet())
		self.gal.planets[-1].mass = 1e8
		self.gal.planets[-1].pos = Vector2(x, y)
		self.gal.planets[-1].v = Vector2(random.randint(-700, 700),
																			random.randint(-700, 700))
		self.gal.planets[-1].id = len(self.gal.planets)-1
		self.gal.planets[-1].scale = 1.0
		
		self.sprites.append(SpriteNode('plf:Item_CoinSilver',
																		scale=self.gal.planets[-1].scale,
																		position=(self.gal.planets[-1].pos[0],
																		self.gal.planets[-1].pos[1])))
		self.add_child(self.sprites[-1])


run(Simulation(), frame_interval=1, show_fps=True)

		
