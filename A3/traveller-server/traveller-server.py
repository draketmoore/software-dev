#
# traveller-server.py
# authors: Michael Curley & Drake Moore
#
# The provided module called for a lot of tuples, but many of these were changed to lists,
# so that they could be updated if new towns add new paths, or players change locations
#

import sys

# ----- main class -------------------------------------------------------------------

# Overall class for the entire town network, containing all information and methods
class TownNetwork:


	# initializes towns and characters as empty lists
	def __init__(self):
		self.towns = []
		self.characters = []


	# ----- helper methods -----------------------------------------------------------

	# checks a list to see if it contains a duplicate name already
	def check_dup(self, name, given_list):
		for obj in given_list:
			if (name == obj[0]):
				return True
		return False

	# given a name, returns the matching "object" from a list
	def list_get(self, name, given_list):
		for obj in given_list:
			if (name == obj[0]):
				return obj
		return False


	# ----- main implemention methods ------------------------------------------------

	# creates a new town in the network, with a given name and list of neighbors
	def create_town(self, town_name, neighbors):

		# Make sure duplicate town does not already exist
		if (self.check_dup(town_name, self.towns)):
			return "Town already exists"

		# if town is neighbors with an existing town, add new town to the neighbors of the existing town
		for existing_town in self.towns:
			existing_town_name = existing_town[0]
			existing_town_neighbors = existing_town[1]
			if (existing_town_name in neighbors):
				existing_town_neighbors.append(town_name)

		# add new town to list of towns
		self.towns.append((town_name, neighbors))


	# places a character in a given town name
	def place_character(self, char_name, town_name):

		# Make sure duplicate character does not already exist
		if (self.check_dup(char_name, self.characters)):
			return "Character already exists"

		# Checks that the town the character is placed in exists
		if (not self.check_dup(town_name, self.towns)):
			return "Town does not exist"

		self.characters.append([char_name, town_name])


	# Checks to see if there is a path to the town that is unblocked
	# Returns True is there is an open path, False otherwise
	def path_is_unblocked(self, char_name, dest):

		char = self.list_get(char_name, self.characters)
		start_name = char[1]
		start = self.list_get(start_name, self.towns)

		return self.path_bfs(self.towns, start, dest)


	# Given a town name, checks to see if any character has that town as their given location
	def player_in_town(self, town_name):
		for char in self.characters:
			if (char[1] == town_name):
				return True
		return False


	# Conducts BFS along the Town Network, checking for any unblocked path
	def path_bfs(self, towns, start, end):

		# Queue and visited lists are initialized emtpy
		visited = []
		queue = []
		start_name = start[0]
		start_neighbors = start[1]

		# Do not want to start at starting town, since the current player resides there
		visited.append(start_name)

		# Adds all the town's neighbors to the queue
		for neighbor in start_neighbors:

			# town_tuple is the actual town object
			town_tuple = self.list_get(neighbor, self.towns)
			visited.append(town_tuple)
			queue.append(town_tuple)
		
		# BFS search algorithm
		while(queue):
			current = queue.pop(0)
			current_town_name = current[0]
			current_town_neighbors = current[1]

			# if there is a player in the town, skip this town and continue
			if (self.player_in_town(current_town_name)):
				continue

			# checks if we have reached the destination yet
			if current_town_name == end:
				return True

			# Adds all unvisited neighbors to the queue to continue searching down
			for neighbor in current_town_neighbors:
				if neighbor not in visited:
					town_tuple = self.list_get(neighbor, self.towns)
					visited.append(town_tuple)
					queue.append(town_tuple)

		return False


# ----- end of file ------------------------------------------------------------------





