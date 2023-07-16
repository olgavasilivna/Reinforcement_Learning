import numpy as np
import time
import os
import sys
import random
np.set_printoptions(suppress=True, linewidth=sys.maxsize, threshold=sys.maxsize)

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

class Game():
    def __init__(self, size):
        self.world = np.full(size, " ")
        self.size = size
        self.world[[0, self.size[0]-1], :] = "#"
        self.world[:, [0, self.size[1]-1]] = "#"
        self.goal1 = [12, 8]
        self.world[self.goal1[0], self.goal1[1]] = "X"
        self.world[3, 2] = "@"
        self.pos = [3, 2]
        self.prev_pos = [3, 2]
        self.teleport_spots = [[6, 6], [6, 18], [18, 6], [18, 18]]
        self.pit_size = [5, 5]
        self.pit_start = [0, 0]  # Initialize pit_start
        self.pit_end = [0, 0]  # Initialize pit_end
        self.randomize_pit()
        print(self.world)


    def randomize_pit(self):
        self.world[self.pit_start[0]:self.pit_end[0]+1, self.pit_start[1]:self.pit_end[1]+1] = " "
        valid_pit_start = [1, 1]
        valid_pit_end = [self.size[0]-self.pit_size[0]-1, self.size[1]-self.pit_size[1]-1]
        self.pit_start = [random.randint(valid_pit_start[0], valid_pit_end[0]), random.randint(valid_pit_start[1], valid_pit_end[1])]
        self.pit_end = [self.pit_start[0] + self.pit_size[0] - 1, self.pit_start[1] + self.pit_size[1] - 1]
        self.world[self.pit_start[0]:self.pit_end[0]+1, self.pit_start[1]:self.pit_end[1]+1] = "P"

    def move(self, direction):
        if direction == "w":
            self.pos[0] -= 1
        if direction == "s":
            self.pos[0] += 1
        if direction == "a":
            self.pos[1] -= 1
        if direction == "d":
            self.pos[1] += 1
        if direction == "t":
            self.teleport_agent()

        if (self.pos[0] == 0) or (self.pos[1] == 0):
            self.pos = self.prev_pos.copy()
        if (self.pos[0] == self.size[0]-1) or (self.pos[1] == self.size[1]-1):
            self.pos = self.prev_pos.copy()

        if (self.pit_start[0] <= self.pos[0] <= self.pit_end[0]) and (self.pit_start[1] <= self.pos[1] <= self.pit_end[1]):
            self.game_reset()
            return 'Game over'

        goal1_indices = np.where(self.world == 'X')
        if goal1_indices[0].size > 0 and goal1_indices[1].size > 0:
            goal1 = (goal1_indices[0][0], goal1_indices[1][0])
            if goal1 == tuple(self.pos):
                self.game_reset()
                return 'Game over'

        self.prev_pos = self.pos.copy()
        self.world[self.world == '@'] = " "
        self.world[self.pos[0], self.pos[1]] = "@"
        return 'Game not over'

    def teleport_agent(self):
        teleport_spot = random.choice(self.teleport_spots)
        self.pos = teleport_spot.copy()
        self.prev_pos = self.pos.copy()
        self.world[self.world == '@'] = " "
        self.world[self.pos[0], self.pos[1]] = "@"

    def game_reset(self):
        self.pos = [3, 2]
        self.world[self.world == '@'] = " "
        self.world[3, 2] = "@"

        goal_locations = [[8, 12], [10, 7], [17, 17]]
        self.goal1 = random.choice(goal_locations)
        self.world[self.goal1[0], self.goal1[1]] = "X"

        self.randomize_pit()

if __name__ == "__main__":
    grid = Game((25, 25))

    while True:
        i = input("dir: ")
        grid.move(i)
        clearConsole()
        print(grid.world)
