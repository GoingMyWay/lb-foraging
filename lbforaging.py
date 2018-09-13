import argparse
import random
import time
from collections import defaultdict

import numpy as np
from tqdm import tqdm

from agents import H1, H2, H3, H4, QAgent
import lb_foraging
import gym
import logging

_MAX_STEPS = 1000

logger = logging.getLogger(__name__)


# class TypeSpacePlayer(Player):
#     """
#     Changes the controller (Agent) every change_every() times to a random type_space
#     """
#
#     def __init__(self, type_space, change_every):
#         self.type_space = type_space
#         self.change_every = change_every
#         self.next_change = 0
#         super().__init__()
#
#     def step(self, obs):
#         if self.next_change <= 0:
#             self.set_controller(random.choice(self.type_space)(self))
#             self.next_change = self.change_every()
#
#         self.next_change -= 1
#         return super().step(obs)


def _game_loop(env, render):
    """
    """
    obs = env.reset()

    if render:
        env.render()
        time.sleep(1)

    for _ in range(_MAX_STEPS):
        actions = []
        for i, player in enumerate(env.players):
            actions.append(player.step(obs[i]))
        obs, rewards, done, info = env.step(actions)

        if render:
            env.render()
            time.sleep(1)

        if env.game_over:
            break

    # loop once more so that agents record the game over event
    for i, player in enumerate(env.players):
        player.step(obs[i])


def evaluate(game_count, render):

    env = gym.make("lb-foraging-simple-v0")

    efficiency = 0
    flexibility = 0

    pbar = tqdm if game_count > 1 else (lambda x: x)  # use tqdm for game_count >1

    for _ in pbar(range(game_count)):
        _game_loop(env, render)

        efficiency += env.players[0].score / env.current_step
        if env.current_step < _MAX_STEPS:
            flexibility += 1

    for player in env.players:
        player.controller.cleanup()

    efficiency /= game_count
    flexibility /= game_count

    logger.warning("{} - Efficiency: {} - Flexibility: {}".format(players[0].name, efficiency, flexibility))


def main(game_count=1, render=False):

    evaluate(game_count, render)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Play the level foraging game.')

    parser.add_argument('--render', action='store_true')
    parser.add_argument('--times', type=int, default=1, help='How many times to run the game')

    args = parser.parse_args()
    main(args.times, args.render)
