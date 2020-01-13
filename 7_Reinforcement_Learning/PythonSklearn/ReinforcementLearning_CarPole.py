import gym
import time

class RandomAgent:
    def __init__(self, action_space):
        self.action_space = action_space
        
    def act(self, observation, reward, done):
        # Here the parameters should be accounted for better learning
        return self.action_space.sample()


if __name__ == '__main__':   
    env = gym.make("CartPole-v1")

    agent = RandomAgent(env.action_space)

    episode_count = 100
    reward = 0
    done = False

    for i in range(episode_count):
        # Observation
        ob = env.reset()
        while(True):
            # Action
            action = agent.act(ob, reward, done)
            ob, reward, done, info = env.step(action)
            if done:
                print("Game Over :D")
                break
            # Loop until smth happens
            env.render()
            time.sleep(1/30)
    print("Game Completed :D")
    env.close()