import random
import statistics
import matplotlib.pyplot as plt
import numpy as np

#fra 1 til 2N
#1,2,3,4,5,6

#lambda

#5 stasjoner
#reward for M = 0, 1, 2, 3. M * O.2
#punishment for 4, 5. 0,6 - (M-3) * 0.2
'''
1. 5 tsetlin automata
2. count yes responses (when state is < states)
3. reinforce good behaviour and weaken bad behaviour
4. ???
5. pro(o)fit (works)
'''

class tsetlinAutomata:
    def __init__(self, states, name):
        self.states = states
        self.name = name
        #init state tilfeldig til midten
        self.pos = states
        if random.random() < 0.5:
            self.pos += 1

    def update(self, reward):
        #reward er enten 1 eller -1
        if self.pos <= self.states:
            reward *= -1
        '''
        siden -1 er bevegelse mot venstre må vi gange reward med 
        '''
        self.pos += reward

        if self.pos > self.states*2:
            self.pos = self.states * 2
        elif self.pos < 1:
            self.pos = 1

    def step(self):
        #venstre side er nei, høyre side er ja
        # 1, 2, ... N, N+1, N+2, ... 2N
        if self.pos <= self.states:
            #no
            return 0
        else:
            #yes
            return 1

    def reward(self, m):
        # 0 or 1 or 2 or 3
        if m <= 3:
             reward = 1 if random.random() < m * 0.2 else -1
             #p=0 for m=0, p=0.2 for m=1,p=0.4 for m=2, p=0.6 for m=3
        # 4 and 5
        else :
            reward = 1 if random.random() < (0.6-((m-3)*0.2)) else -1
            #p = 0.4 for m=4, p=0.2 for m=5
        self.update(reward)
        #print(f'a{self.name} reward is {reward} for m = {m}')
        return reward
    def confidence(self):
        #gives a confidence rating between 0% and 100% idk
        return abs(self.pos-(self.states+0.5))/(self.states+0.5)

class Env:
    def __init__(self, states, it=10000):
        #make 5 robots
        self.automata = []
        self.iterations = it
        self.ms = []
        for i in range(5):
            self.automata.append(tsetlinAutomata(states, i))
    def loop(self):
        #station calls
        m = 0
        for a in self.automata:
            m += a.step()
        #now we have m, loop reward, put m in thing
        self.ms.append(m)
        #print(m)
        for a in self.automata:
            a.reward(m)
        #print(f'the states are a0 {self.automata[0].state}, a1 {self.automata[1].state}, a2 {self.automata[2].state}, a3 {self.automata[3].state}, a4 {self.automata[4].state}')

    def train(self, verbose=False):
        for i in range(self.iterations):
            self.loop()

        if verbose:
            print("Training finished!")
            print(f'after {self.iterations} iterations the states are:\n'
              f' a0: {self.automata[0].pos},\n'
              f' a1: {self.automata[1].pos},\n'
              f' a2: {self.automata[2].pos},\n'
              f' a3: {self.automata[3].pos},\n'
              f' a4: {self.automata[4].pos}\n'
              f'With mean M of {sum(self.ms)/len(self.ms)}, stddev of {statistics.stdev(self.ms)} in total \n'
              f'and mean M of {sum(self.ms[-1000:])/len(self.ms[-1000:])}, stddev {statistics.stdev(self.ms[-1000:])} in the last 1000 iterations')

    def mean_m(self):
        return sum(self.ms)/len(self.ms)

#env = Env(10, it=100000)
#env = Env(3)
#env.train()
mean_of_means = []
stds = []
max_levels = 21
x = np.arange(max_levels)
for i in range(max_levels):
    means = []
    for j in range(10):
        env = Env(states=i, it=100000)
        env.train()
        means.append(env.mean_m())
    mean_of_means.append(sum(means)/len(means))
    stds.append(statistics.stdev(means))
mmmm = np.array(mean_of_means)
mstds = np.array(stds)
upper_bound = mmmm + mstds
lower_bound = mmmm - mstds

fig, ax = plt.subplots(figsize=(10,5))

ax.plot(x, mean_of_means, label='Mean')
ax.fill_between(x, lower_bound, upper_bound, color='green', alpha=0.5, label='1 std dev')
plt.show()