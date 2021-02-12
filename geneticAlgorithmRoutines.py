import numpy as np, random, operator, pandas as pd, matplotlib.pyplot as plt
from simulation import sim

class fixedQueuesClass():
    from simulation import Simulation, sim
    def __init__(self, size):
        self.fixedMaxSize = size
        self.fixedQueueList = []
        self.fixedTrucksDict = {}

    def createFixedTrucksDict(self, N):
        return sim.generateTrucksDict(N)

    def createFixedQueue(self, trucksDict, N):
        if len(trucksDict) <= N:
            return sim.generate_queueList(trucksDict, N)
        else:
            raise ValueError("Queue size cannot be larger that trucks waiting.")



#Create a fitness function
class Fitness:
    def __init__(self):
        self.fitness= 0.0
        self.queuesTimesList = []
    
    def simulateAllPopulation(self, pop):
        import copy

        self.queuesTimesList = []
        sim.restartSimulation()

        for p in pop:
            #The individual is comprised of a fixed queue and the last tail which
            #are the trucks to be called.
            individual = copy.deepcopy(sim.fixedQueue + p)
            # print(f"--------- {len(individual)} {pop.index(p)}")
            # print(individual)
            
            # for key, value in sim.trucksDict.items():
            #     print(key)
            # exit()
            sim.runSimulation(individual)
            # print("------------ Termino")
            self.queuesTimesList.append(1.0 / sim.globalTime)
            
            sim.restartSimulation()
        
        # print("************")
        # print(list(sim.fixedQueue))
        # print(list(sim.trucksDict[j].id for j in sim.fixedQueue))

        # exit()

#Create our initial population
#This method generates a random sample from the trucks list
def createTruckQueue(queueList):
    from classes import TruckClass
    import random

    queue = random.sample(queueList, len(queueList))
    return queue

#Create first "population" (list of truck queues)
#This method created a random population of the specified size.

def initialPopulation(popSize, popList):
    population = []

    for i in range(0, popSize):
        population.append(createTruckQueue(popList))
    return population

#Create the genetic algorithm
#Rank individuals
#This function takes a population and orders it in descending order using the fitness of each individual
def rankIndividuals(population):
    fitnessResults = {}
    for i in range(0, len(population)):
        #fitnessResults[i] = Fitness(population[i]).timeFitness(population[i])
        fitnessResults[i] = fit.queuesTimesList[i]
        
    sorted_results=sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)
    return sorted_results

#Create a selection function that will be used to make the list of parent queues

def selection(popRanked, eliteSize):
    selectionResults = []
    df = pd.DataFrame(np.array(popRanked), columns=["Index","Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()
    
    for i in range(0, eliteSize):
        selectionResults.append(popRanked[i][0])
    for i in range(0, len(popRanked) - eliteSize):
        pick = 100*random.random()
        for j in range(0, len(popRanked)):
            if pick <= df.iat[j,3]:
                selectionResults.append(popRanked[i][0])
                break
    return selectionResults

#Create mating pool

def matingPool(population, selectionResults):
    matingpool = []
    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        matingpool.append(population[index])
    return matingpool

#Create a crossover function for two parents to create one child
def breed(parent1, parent2):
    child = []
    childP1 = []
    childP2 = []
    
    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))
    
    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(startGene, endGene):
        childP1.append(parent1[i])
        
    childP2 = [item for item in parent2 if item not in childP1]
    #print(startGene, endGene)

    #print(parent1)
    #print(parent2)

    #print(childP1)
    #print(childP2)
    child = childP1 + childP2

    #print(child)
    return child

#Create function to run crossover over full mating pool

def breedPopulation(matingpool, eliteSize):
    children = []
    length = len(matingpool) - eliteSize
    pool = random.sample(matingpool, len(matingpool))

    for i in range(0,eliteSize):
        children.append(matingpool[i])
    
    for i in range(0, length):
        child = breed(pool[i], pool[len(matingpool)-i-1])
        children.append(child)
    return children

#Create function to mutate a single individual
def mutate(individual, mutationRate):
    for swapped in range(len(individual)):
        if(random.random() < mutationRate):
            swapWith = int(random.random() * len(individual))
            
            truck1 = individual[swapped]
            truck2 = individual[swapWith]
            
            individual[swapped] = truck2
            individual[swapWith] = truck1
    return individual

#Create function to run mutation over entire population

def mutatePopulation(population, mutationRate):
    mutatedPop = []
    
    for ind in range(0, len(population)):
        mutatedInd = mutate(population[ind], mutationRate)
        mutatedPop.append(mutatedInd)
    return mutatedPop

#Put all steps together to create the next generation

def nextGeneration(currentGen, eliteSize, mutationRate):
    popRanked = rankIndividuals(currentGen)
    selectionResults = selection(popRanked, eliteSize)
    matingpool = matingPool(currentGen, selectionResults)
    children = breedPopulation(matingpool, eliteSize)
    nextGeneration = mutatePopulation(children, mutationRate)
    return nextGeneration


#----------------------------------------------------------
#Final step: create the genetic algorithm

def geneticAlgorithm(population, popSize, eliteSize, mutationRate, generations):

    pop = initialPopulation(popSize, population)
    fit.simulateAllPopulation(pop)
    progress = [1 / rankIndividuals(pop)[0][1]]
        
    for i in range(1, generations+1):        #Reinitialize the truck flow simulation
        fit.simulateAllPopulation(pop)
        pop = nextGeneration(pop, eliteSize, mutationRate)
        progress.append(1 / rankIndividuals(pop)[0][1])
        if i%1==0:
            print('Generation '+str(i),"Time: ",progress[i])
        
        
    bestTimeIndex = rankIndividuals(pop)[0][0]
    bestTimeValue = rankIndividuals(pop)[0][1]
    bestTimeQueue = pop[bestTimeIndex]
    
    plt.plot(progress)
    plt.ylabel('Time')
    plt.xlabel('Generation')
    plt.title('Best Fitness vs Generation')
    plt.tight_layout()
    plt.show()
       
    return bestTimeQueue, bestTimeValue

fit = Fitness()
