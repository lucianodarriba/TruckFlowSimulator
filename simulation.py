STATUS_AVAILABLE = "AVAILABLE"
STATUS_ONQUEUE = "ONQUEUE"
STATUS_BUSY = "BUSY"
STATUS_FINISHED = "FINISHED"

class Simulation():
    def __init__(self):
        import log
        self.globalTime = 0
        self.log = log.Log()
        self.firstAvailableTruck = 0
        self.lastAvailableTruck = -1

    def initializeParams(self, N, NH, Nfixed, grainTypesList, endTime):
        self.N = N
        self.NH = NH
        self.Nfixed = Nfixed
        self.grainTypesList = grainTypesList
        self.endTime = endTime

    def initialize(self):
        #Genero una lista fija de camiones y su respectiva cola
        #Representan los camiones que ya están en cola al momento de llamar más.
        self.trucksDict, self.fixedQueue = self.generate_fixedLists(self.Nfixed)

        #Genero la lista de camiones
        self.trucksDict = {**self.trucksDict, **self.generateTrucksDict(self.N)}

        #Genero una cola ubicando los camiones, a priori, en el orden que fueron creados.
        #Es decir, en la posición i está el camión con Id i.
        self.queue = self.generate_queueList(self.trucksDict, self.N)

        #Creo las hidráulicas. Supongo una de cada tipo de grano
        self.hydraulicsList = self.generate_hydraulicsList()

        #Creo una copia del diccionario de camiones, la lista de cola y la lista de hidráulicas
        self.copyLists()

    def generate_fixedLists(self, Nfixed):
        fixedTrucksDict = sim.generateTrucksDict(Nfixed)
        fixedQueue = sim.generate_queueList(fixedTrucksDict, Nfixed)

        return fixedTrucksDict, fixedQueue

    def generateTrucksDict(self, N):
        from classes import TruckClass
        import random

        trucksDictionary = {}
        self.firstAvailableTruck = self.lastAvailableTruck + 1

        for i in range(N):
            truckId = self.firstAvailableTruck + i
            trucksDictionary[truckId] = TruckClass(truckId, random.choice(self.grainTypesList))

        self.lastAvailableTruck = self.firstAvailableTruck + N - 1
        return trucksDictionary

    def generateTrucksDictFixed(self):
        from classes import TruckClass
        import random

        self.trucksDict = {}

        #grains = [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3]
        grains = [1, 1, 1, 1, 2, 2, 2, 3, 3]
        for i in range(self.N):
            truckId = i + 1
            self.trucksDict[truckId] = TruckClass(truckId, grains[i])

    def generate_queueList(self, trucksDict, queueLength):
        from classes import TruckClass
        import random

        #Put the trucks in the order they were created
        queue = []
        for key in trucksDict:
            trucksDict[key].enterQueue(key, queue)
        
        return queue

        #Select randomly from the trucks list
        #self.queue = random.sample(list(self.trucksDict), queueLength)  
        

    def generate_hydraulicsList(self):
        from classes import HydraulicsClass
        #import random
        
        hydraulicsList = []
        # for i in range(self.NH):
        #     #The grain types of the hydraulics are chosen from the actual grain types
        #     #present in the trucks (i.e: if a grain type is missing, no hydraulic will be of that type).
        #     self.hydraulicsList.append(HydraulicsClass(i + 1, i + 1, False, 5))
        j = 0
        for i in range(self.NH):
            hydraulicsList.append(HydraulicsClass(i + 1, self.grainTypesList[j], False, 10))
            if j < len(self.grainTypesList) - 1:
                j += 1
            else:
                j = 0
        
        return hydraulicsList


    def runSimulation(self, queue):
        while (self.globalTime <= self.endTime) and (len(queue) > 0):#(self.checkEmptyqueue):# and any(hydraulic.inUse for hydraulic in self.hydraulicsList):
            #Evaluate one time step
            self.evaluateOneTimeStep(queue)
            #Advance one time unit
            self.advanceTime()

    def evaluateOneTimeStep(self, queue):
        #Check if there´s a hydraulic that ended downloading and free it
        self.checkFreeHydraulic()
      
        #Check if there´s a hydraulic of the first truck´s current type that is free
        if (len(self.queue) > 0):
            self.truckEnterDownload(queue)

    def checkFreeHydraulic(self):
        for hydraulic in self.hydraulicsList:
            if (hydraulic.remainingTime == 0) and (hydraulic.inUse == True):
                hydraulic.inUse = False
                self.log.enterLogRegister(f"La hidráulica {hydraulic.id} fue liberada al tiempo {self.globalTime}.")

    def truckEnterDownload(self, queue):
        import log
        for hydraulic in self.hydraulicsList:
            if (hydraulic.inUse == False) and (hydraulic.grainType == self.trucksDict[queue[0]].type):
                hydraulic.inUse = True
                hydraulic.remainingTime = hydraulic.serviceTime
                temp = hydraulic.id

        #Enters a registry in the process log
                self.log.enterLogRegister(f"El Camión {str(self.trucksDict[queue[0]].id)} ha entrado a la hidráulica de descarga {temp} al tiempo {str(self.globalTime)}.")

        #In the complete version, it should be moved to the exit weight queue
                queue.pop(0) #Remove it from queue
                #if self.checkEmptyqueue:
                if len(queue) == 0:
                    break

    def checkEmptyqueue(self):
        return False if len(self.queue) > 0 else True        

    def advanceTime(self):
        self.globalTime += 1
        for hydraulic in self.hydraulicsList:
            hydraulic.remainingTime -= 1

    def copyLists(self):
        import copy
        self.trucksDictCopy = copy.deepcopy(self.trucksDict)
        self.queueCopy = copy.deepcopy(self.queue)
        self.fixedQueueCopy = copy.deepcopy(self.fixedQueue)
        self.hydraulicsListCopy = copy.deepcopy(self.hydraulicsList)

    def restartSimulation(self):
        import log
        import copy

        self.globalTime = 0
        self.log.emptyLog()   
        self.trucksDict = copy.deepcopy(self.trucksDictCopy)
        self.queue = copy.deepcopy(self.queueCopy)
        self.hydraulicsList = copy.deepcopy(self.hydraulicsListCopy)

    def updateFixedQueue(self, fixedQueue, newQueue):
        #Remover los primeros len(newQueue) camiones y agregar los
        #nuevos al final de la cola. Esta pasa a ser la nueva cola fija

        return fixedQueue[len(newQueue):] + newQueue

sim = Simulation()