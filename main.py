import random
import statistics
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import xlabel

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
        siden -1 er bevegelse mot venstre må vi gange reward med -1 om den er på venstre side.
        -1 forsterker oppførsel på venstre side, mens 1 gjør den sterkere
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

    def reward(self, m, correct_m=3):
        # 0 or 1 or 2 or 3
        if m <= correct_m:
             reward = 1 if random.random() < m * 0.2 else -1
             #p=0 for m=0, p=0.2 for m=1,p=0.4 for m=2, p=0.6 for m=3
        # 4 and 5
        else :
            reward = 1 if random.random() < ((correct_m*0.2)-((m-correct_m)*0.2)) else -1
            #p = 0.4 for m=4, p=0.2 for m=5
        self.update(reward)
        #print(f'a{self.name} reward is {reward} for m = {m}')
        return reward

    def confidence(self):
        #gives a confidence rating between 0% and 100% idk
        return abs(self.pos-(self.states+0.5))/(self.states+0.5)

class Env:
    def __init__(self, states, it=10000, bots=5):
        #make 5 robots
        self.automata = []
        self.iterations = it
        self.ms = []
        for i in range(bots):
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
            print(f'after {self.iterations} iterations the states are:\n')
            i = 0
            for a in self.automata:
                print( f' a{i}: {a.pos},\n')
                i += 1
            print(f'With mean M of {sum(self.ms)/len(self.ms)}, stddev of {statistics.stdev(self.ms)} in total \n '
                  f'and mean M of {sum(self.ms[-1000:])/len(self.ms[-1000:])}, stddev {statistics.stdev(self.ms[-1000:])} in the last 1000 iterations')

    def mean_m(self):
        return sum(self.ms)/len(self.ms)

#env = Env(10, it=100000)
#env = Env(3)
#env.train()
'''
mean_of_means = []
stds = []
#max_levels = 21 den slutter basically å bli noe særlig bedre etter rundt n=5
max_levels = 15
x = np.arange( max_levels)
for i in range(max_levels):
    means = []
    for j in range(10):
        env = Env(states=i, it=20000)
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
plt.xlabel('Number of states')
plt.ylabel('Mean number of yes votes')
plt.title('Number of yes votes by number of states')
plt.show()
'''

"""
Jo flere flere n(umber of states) desto nærmere kommer vi et snitt på 3 ja-stemmer/riktig oppførsel
"""

## HER SJEKKER VI HVA SOM SKJER OM DU ØKER ANTALLET BOTS UTEN Å ØKE ANTALLET STATES. NÅ MÅ VI BARE VISE AT MAN KAN STØTTE ET STØRRE ANTALL BOTS VED Å GI DEM FLERE STATES
"""
max_bots = 10
mean_of_means = []
stds = []
x = np.arange(5, max_bots+5)

for i in range(5, max_bots+5):
    means = []
    for j in range(10):
        env = Env(states=7, it=20000, bots=i)
        env.train()
        means.append(env.mean_m())
    mean_of_means.append(sum(means) / len(means))
    stds.append(statistics.stdev(means))
mmmm = np.array(mean_of_means)
mstds = np.array(stds)
upper_bound = mmmm + mstds
lower_bound = mmmm - mstds

fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(x, mean_of_means, label='Mean')
ax.fill_between(x, lower_bound, upper_bound, color='green', alpha=0.5, label='1 std dev')
plt.xlabel('Number of bots')
plt.xticks(np.arange(min(x), max(x)+1, 1))
plt.ylabel('Mean number of yes votes')
plt.title('Number of yes votes by number of bots')
plt.show()
"""

'''
Om du øker antall bots (n) må du også øke antall states for at det skal funke. For 9 automata må du ha n=11 for at de skal lære systemet.
Antall iterations virker ikke som det har noe særlig effekt.
'''
"""
max_bots = 9
x = np.arange(5, max_bots)
max_levels = 11
stds = np.zeros((max_bots-5,max_levels-5))
mean_of_means = np.zeros((max_bots-5,max_levels-5))

for horse in range(5, max_levels):
    for i in range(5, max_bots):
        means = []
        for j in range(2):
            env = Env(states=horse, it=10000, bots=i)
            env.train()
            means.append(env.mean_m())
        mean_of_means[i-5,  horse-5] = sum(means) / len(means)
        stds[i-5,  horse-5] = statistics.stdev(means)
#rows = np.arange(5, max_bots)
#cols = np.arange(5, max_levels)
fig, ax = plt.subplots(figsize=(10, 5))
im = ax.imshow(mean_of_means, interpolation='nearest', cmap=plt.cm.Blues)
#ax.set_xticks(cols)
#ax.set_yticks(rows)
plt.show()
"""
import seaborn as sns

states = [19,21,23,25,27,29,31,33,35,37,39]
number_of_bots = [11,12,13,14,15,16,17,18,19,20]


means = np.zeros((len(number_of_bots), len(states)))
state_idx = 0
bot_idx = 0
for state in states:
    bot_idx = 0

    for bot_n in number_of_bots:
        sum_of_means = 0
        for i in range(10):
            env = Env(states=state, it=10000, bots=bot_n)
            env.train()
            sum_of_means += env.mean_m()
        means[bot_idx, state_idx] = sum_of_means/10
        bot_idx += 1
    state_idx += 1

sns.heatmap(means, annot=True, fmt=".2f", cmap="viridis", xticklabels=states, yticklabels=number_of_bots)
plt.title("Heatmap of yes votes by bots and levels target=3")
plt.xlabel("levels")
plt.ylabel("number of bots")

#plt.xticks(len(number_of_bots), labels=number_of_bots)
#plt.yticks(len(states), labels=states)
plt.show()