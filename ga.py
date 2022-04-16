import random
import copy


def cross_simple(c1, c2):
    if len(c1.value) != len(c2.value):
        raise ValueError('Impossible Cross diferent sizes')
    v1 = []
    v2 = []
    for i in range(0,len(c1.value)):
        if random.uniform(0,1) < 0.5:
            v1.append(c2.value[i])
            v2.append(c1.value[i])
        else:
            v1.append(c1.value[i])
            v2.append(c2.value[i])

    return Chromosome(v1), Chromosome(v2)


def cross_arithmetic(c1, c2):
    if len(c1.value) != len(c2.value):
        raise ValueError('Impossible Cross diferent sizes')
    
    v1 = []
    v2 = []
    for i in range(0,len(c1.value)):
        if random.uniform(0,1) < 0.5:
            v1.append(c1.value[i])
            v2.append(c2.value[i])
        else:
            v = (c1.value[i] + c2.value[i]) / 2
            v1.append(v)
            v2.append(v)
    
    return Chromosome(v1), Chromosome(v2)

def cross_one_point(c1, c2):
    if len(c1.value) != len(c2.value):
        raise ValueError('Impossible Cross diferent sizes')
    
    v1 = []
    v2 = []

    point = random.randint(0, len(c1.value)-1)

    for i in range(0,len(c1.value)):
        if i < point:
            v1.append(c1.value[i])
            v2.append(c2.value[i])
        else:
            v1.append(c2.value[i])
            v2.append(c1.value[i])

    return Chromosome(v1), Chromosome(v2)


def cross_one_point_arithmetic(c1, c2):
    if len(c2.value) != len(c1.value):
        raise ValueError('Impossible Cross diferent sizes')
    
    v1 = []
    v2 = []

    point = random.randint(0, len(self.c1)-1)

    for i in range(0,len(self.c1)):
        if i < point:
            v1.append(c1.value[i])
            v2.append(c2.value[i])
        else:
            v = (c1.value[i] + c2.value[i]) / 2
            v1.append(v)
            v2.append(v)

    return Chromosome(v1), Chromosome(v2)

def cross_two_points(c1, c2):
    if len(other.value) != len(self.value):
        raise ValueError('Impossible Cross diferent sizes')
    
    v1 = []
    v2 = []

    p_1 = random.randint(0, len(c1.value)-1)
    p_2 = random.randint(0, len(c1.value)-1)

    p_1, p_2 = (p_1, p_2) if p_1 < p_2 else (p_2, p_1)

    for i in range(0,len(c1.value)):
        if i < p_1 or i > p_2:
            v1.append(c1.value[i])
            v2.append(c2.value[i])
        else:
            v = (c1.value[i] + c2.value[i]) / 2
            v1.append(v)
            v2.append(v) 

    return Chromosome(v1), Chromosome(v2)


def cross_two_points_arithmetic(c1, c2):
    if len(c1.value) != len(c2.value):
        raise ValueError('Impossible Cross diferent sizes')
    
    v1 = []
    v2 = []

    p_1 = random.randint(0, len(c1.value)-1)
    p_2 = random.randint(0, len(c2.value)-1)

    p_1, p_2 = (p_1, p_2) if p_1 < p_2 else (p_2, p_1)

    for i in range(0,len(c1.value)):
        if i < p_1 or i > p_2:
            v1.append(c1.value[i])
            v2.append(c2.value[i])
        else:
            v = (c1.value[i] + c2.value[i]) / 2
            v1.append(v)
            v2.append(v)   

    return Chromosome(v1), Chromosome(v2)


class Chromosome(object):
    @classmethod
    def Random(cls, size, i_min=-1, i_max=1):
        return cls([random.uniform(i_min, i_max) for i in range(0,size)])
    
    def __init__(self, value: list, fitness=None):
        self.value = value
        self.fitness = fitness

    def __repr__(self):
        return str(self.value)

    def __eq__(self, other):
        if len(self.value) != len(other.value):
            return False

        for i in range(0,len(self.value)):
            if self.value[i] != other.value[i]:
                return False
        
        return True


    def mutate(self, mu_min=-2, mu_max=2):
        # Select who gen mutate 
        i = random.randint(0, len(self.value)-1)
        # Select operations 0 add, 1 sub
        self.value[i] = self.value[i] + random.uniform(mu_min,mu_max)


class AG(object):
    
    @classmethod
    def Random(cls, population_len, gen_len):
        return cls([Chromosome.Random(gen_len) for i in range(0,population_len)],None)

    def __init__(self, chromosome_list=None, fitness_list=None, elitist=True, cross_function=cross_simple):
        if chromosome_list is None:
            raise ValueError('Invalid argument')

        self.p_cx = 0.9
        self.p_mu = 0.3
        self.mu_min = -2
        self.mu_max = 2
        self.elitist = elitist
        self.cross_function = cross_function

        self.population = []
        if fitness_list is not None and len(chromosome_list) != len(fitness_list):
            raise ValueError('Impossible to init the AG')
    
        for i in range(0,len(chromosome_list)):
            c = chromosome_list[i]
            if fitness_list is not None:
                c.fitness = fitness_list[i]

            self.population.append(c)


    def get_winner(self, fitness_max=True):
        if len(self.population) == 0:
            return None
        
        value = self.population[0].fitness
        win   = self.population[0]

        for pop in self.population:
            if fitness_max:
                if pop.fitness > value:
                    value = pop.fitness
                    win   = pop
            else:
                if pop.fitness < value:
                    value = pop.fitness
                    win   = pop

        return Chromosome(win.value)

    def tournament(self, k=3, fitness_max=True):
        def key(v):
            return v.fitness

        n = random.sample(self.population, k)
        n.sort(reverse=fitness_max, key=key)

        return n

    @staticmethod
    def chromosome_in_list(chromosome:Chromosome, chromosome_list: list) -> bool:
        for obj in chromosome_list:
            if chromosome == obj:
                return True
        return False 


    def _after_cross(self, c1:Chromosome, c2:Chromosome, next_generation:list) -> list:
        if random.uniform(0,1) < self.p_mu:
            c1.mutate(self.mu_min,self.mu_max)
        if random.uniform(0,1) < self.p_mu:
            c2.mutate(self.mu_min,self.mu_max)

        if not self.chromosome_in_list(c1,next_generation):
            next_generation.append(c1)

        if not self.chromosome_in_list(c2,next_generation) and len(next_generation) < population_len:
            next_generation.append(c2)

        return next_generation


    def cross(self, k=3, fitness_max=True):
        next_generation = []
        population_len = len(self.population)

        if self.elitist:
            next_generation.append(self.get_winner(fitness_max))

        while len(next_generation) < population_len:
            wins = self.tournament(k, fitness_max)
            c1, c2 = wins[0], wins[1]
            # Return two new Chromosomes
            if random.uniform(0,1) < self.p_cx:
                c1, c2 = self.cross_function(c1,c2)

            next_generation = self._after_cross(c1,c2, next_generation)

        self.population = next_generation

    