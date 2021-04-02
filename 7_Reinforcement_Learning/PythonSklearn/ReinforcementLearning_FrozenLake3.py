import numpy as np

import gym
import time

env = gym.make("FrozenLake-v0")

EPSILON = 0.9  # Exploration / Exploitation

NUM_EPOCHS = 10000  # Also called episodes
MAX_STEPS = 100

learning_rate = 0.8
gamma = 0.95

Q = np.zeros((env.observation_space.n, env.action_space.n))  # 16 x 4


def choose_action(state):
    action = 0
    if np.random.uniform(0, 1) < EPSILON:
        action = env.action_space.sample()
    else:
        action = np.argmax(Q[state, :])

    return action


def learn(state, state2, reward, action):
    # Attempt this with NN!!
    predict = Q[state, action]
    target = reward + gamma * np.max(Q[state2, :])
    Q[state, action] = Q[state, action] + learning_rate * (target - predict)


for epoch in range(NUM_EPOCHS):
    state = env.reset()
    step = 0
    while step < MAX_STEPS:
        env.render()
        action = choose_action(state)
        new_state, reward, done, info = env.step(action)
        learn(state, new_state, reward, action)
        state = new_state
        step += 1

        print(Q)
        print("Epoch ", epoch, "  Step ", step)

        if done:
            print("Completed!")
            break
