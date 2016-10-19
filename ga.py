import random as rn

# convertion integer to bit array
def int_to_bit(n):
    return [1 if digit == '1' else 0 for digit in bin(n)[2:]]

# convertion bit array to integer
def bit_to_int(bits):
    return int(''.join(str(x) for x in bits), 2)

class GA:
    def __init__(self, length, popSize, mutCount, winCount, kidCount, newCount, genCount):
        self.length = length        # chromosome length
        self.popSize = popSize      # population size
        self.mutCount = mutCount    # mutations count
        self.winCount = winCount    # winners
        self.kidCount = kidCount    # childs
        self.newCount = newCount    # new chromosomes
        self.genCount = genCount    # iteration count

    def new_chromosome(self):
        return [rn.randint(0, 1) for i in range(self.length)]

    def mutate(self, vec):
        i = rn.randint(0, self.length - 1)
        return vec[0:i] + [1 if vec[i] == 0 else 0] + vec[i + 1:]

    def new_child(self, r1, r2, i):
        return r1[0:i] + r2[i:]

    def optimise(self):
        # initialize current population to random values within range
        cur_population = []
        for i in range(self.popSize):
            cur_population.append(self.new_chromosome())

        # generation iterations
        for i in range(self.genCount):
            scores = [(-bit_to_int(v), v) for v in cur_population]
            scores.sort()
            ranked = [v for (s, v) in scores]
            cur_population = ranked[0:self.winCount]

            for i in range(int(self.kidCount / 2)):
                c1 = rn.randint(0, self.winCount)
                c2 = rn.randint(0, self.winCount)
                i = rn.randint(1, self.length - 2)
                cur_population.append(self.new_child(ranked[c1], ranked[c2], i))
                cur_population.append(self.new_child(ranked[c2], ranked[c1], i))

            for i in range(self.newCount):
                cur_population.append(self.new_chromosome())

            for i in range(self.mutCount):
                c = rn.randint(self.winCount, len(cur_population) - 1)
                cur_population[c] = self.mutate(cur_population[c])

        return scores[0]