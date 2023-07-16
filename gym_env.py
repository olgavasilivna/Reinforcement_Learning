import gym
from gym import spaces
import numpy as np
from gym import spaces
from gym.spaces import Box, Dict, Discrete, MultiBinary, MultiDiscrete
from game import Game
from stable_baselines3 import A2C
from torch.utils.tensorboard import SummaryWriter
from stable_baselines3 import PPO

class GridworldEnv(gym.Env):
    def __init__(self, game):
        self.action_space = Discrete(5)
        self.observation_space = Dict({
            'position': Box(low=0, high=24, shape=(2,), dtype=np.int),
            'goal1': Box(low=0, high=1, shape=(2,), dtype=np.int),
            'distance': Box(low=0, high=np.inf, shape=(1,), dtype=np.float32),
            'pit_start': Box(low=0, high=24, shape=(2,), dtype=np.int),
            'pit_end': Box(low=0, high=24, shape=(2,), dtype=np.int),
            'world': Box(low=0, high=3, shape=game.world.shape, dtype=np.int)
        })
        self.game = game

    def calculate_distance(self):
        agent_pos = np.array(self.game.pos)
        goal_pos = np.array(self.game.goal1)
        distance = np.linalg.norm(agent_pos - goal_pos)
        return distance
    
    def step(self, action):
        info = {}
        reward = 0
        done = False
        if action == 4:
            game_over = self.game.move(self.do_action(action))
        else:
            game_over = self.game.move(self.do_action(action))
        if game_over == 'Game over':
            reward = 1000
            done = True
            self.reset()
        else: 
            reward = -1
        obs = {
            'position': np.array(self.game.pos),
            'goal1': np.array(self.game.goal1),
            'distance': self.calculate_distance(),
            'pit_start': np.array(self.game.pit_start),  # Assign actual pit_start value
            'pit_end': np.array(self.game.pit_end),  # Assign actual pit_end value
            'world': self.convert_world_to_numeric()  # Convert the game world to numeric representation
        }
        # Return step information
        return obs, reward, done, info

    def reset(self):
        # Reset sim
        self.game.game_reset()
        obs = {
            'position': np.array(self.game.pos),
            'goal1': np.array(self.game.goal1),
            'distance': self.calculate_distance(),
            'pit_start': np.array(self.game.pit_start),  # Assign actual pit_start value
            'pit_end': np.array(self.game.pit_end),  # Assign actual pit_end value
            'world': self.convert_world_to_numeric()  # Convert the game world to numeric representation
        }
        return obs

    def do_action(self, action):
        if action == 0:
            return 'w'
        if action == 1:
            return 'a'
        if action == 2:
            return 's'            
        if action == 3:
            return 'd'
        if action == 4:
            return 't'

    def convert_world_to_numeric(self):
        # Convert the game world to a numeric representation
        numeric_world = np.zeros(self.game.world.shape, dtype=np.int)
        numeric_world[self.game.world == '#'] = 1  # Wall
        numeric_world[self.game.world == 'X'] = 2  # Goal
        numeric_world[self.game.world == '@'] = 3  # Agent
        return numeric_world


if __name__ == "__main__":
    env = GridworldEnv(Game((25, 25)))

    writer = SummaryWriter("logs/")

    model = A2C("MultiInputPolicy", env, verbose=1, n_steps=20, gamma=0.85, tensorboard_log="logs")
    
    model.learn(total_timesteps=100000)

    writer.close()


    #model.save("~/Reinforcement_Learning/model.zip")
