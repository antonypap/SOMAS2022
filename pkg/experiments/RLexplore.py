####################################
# script to run the training model
# for the RL agent
####################################

# imports 
# standards
from collections import deque
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
# packages
from player import (
    agent,
    game_env
)


eps = 500
battles = 10
done = False

env = game_env.escapeThePitEnv()  # initiate the environemnt class
state_size = env.state_size
numNewAgents = env.numNewAgents
step_size = 3   # the step size for action space generation
agent = agent.agent(state_size, numNewAgents, step_size)  # initiate the learning agent

batch_size = 32
ep_reward_list = deque(maxlen=50)
av_rewards = []

print("================== STARTING TRAINING ==================")

for e in tqdm(range(eps)):
    state = env.reset()
    total_reward = 0
    for battle in range(battles):
        action = agent.act(state)
        next_state, reward, done = env.step(action)
        total_reward += reward

        agent.remember(state, action, reward, next_state, done)
        state = next_state
        if done:
            break
        if len(agent.memory) >= batch_size:
            agent.replay(batch_size)

    # append total reward to the deque
    ep_reward_list.append(total_reward)
    # calclate the average over the deque (50 episode average)
    ep_reward_avg = np.array(ep_reward_list).mean()
    # append to average rewards
    av_rewards.append(ep_reward_avg)
    if (e+1) % 5 == 0:
        print("End of Episode {}/{}, Score: {}, Epsilon: {:.2}, Avg Score Over Last 50 Eps: {:.2f}"
            .format(e+1, eps, total_reward, agent.epsilon, ep_reward_avg))
    
print("================== END OF TRAINING ==================")
agent.save("RL_agent_mode2_wegihts")

# plot average rewards
plt.figure()
plt.plot(range(0,len(av_rewards)), av_rewards, color='blue', label='Average Reward')
plt.legend()
plt.xlabel('Episodes', fontsize=16)
plt.ylabel('Average Reward', fontsize=16)
plt.title('Average Reward vs Episodes', fontsize=25)
plt.show()
plt.savefig("Average Reward vs Episodes.png")

    
