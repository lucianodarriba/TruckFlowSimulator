class Simulation():
    def __init__(self):
        import log
        self.globalTime = 0
        self.log = log.Log() 

    def initializeParams(self, N, NH, grainTypesList, endTime):
        self.N = N
        self.NH = NH
        self.grainTypesList = grainTypesList
        self.endTime = endTime

    def initialize(self):
        #Genero la lista de camiones
        self.generateTrucksDict()

        #Genero una cola ubicando los camiones, a priori, en el orden que fueron creados.
        #Es decir, en la posición i está el camión con Id i.
        self.generate_queue()

        #Creo las hidráulicas. Supongo una de cada tipo de grano
        self.generate_hydraulics()

    def generateTrucksDict(self):
        from classes import TruckClass
        import random

        self.trucksDict = {}

        for i in range(self.N):
            truckId = i + 1
            self.trucksDict[truckId] = TruckClass(truckId, random.choice(self.grainTypesList))

    def generate_queue(self):
        from classes import TruckClass
        
        self.queue = []

        for key in self.trucksDict:
            self.trucksDict[key].enterQueue(key, self.queue)

    def generate_hydraulics(self):
        from classes import HydraulicsClass
        
        self.hydraulicsList = []
        for i in range(self.NH):
            self.hydraulicsList.append(HydraulicsClass(i + 1, i + 1, False, 5))

    def runSimulation(self):
        while (self.globalTime <= self.endTime) and (self.checkEmptyqueue):# and any(hydraulic.inUse for hydraulic in self.hydraulicsList):
            #Evaluate one time step
            self.evaluateOneTimeStep()
            #Advance one time unit
            self.advanceTime()

    def evaluateOneTimeStep(self):
        #Check if there´s a hydraulic that ended downloading and free it
        self.checkFreeHydraulic()
      
        #Check if there´s a hydraulic of the first truck´s current type that is free
        if (len(self.queue) > 0):
             self.truckEnterDownload()


    def checkFreeHydraulic(self):
        for hydraulic in self.hydraulicsList:
            if (hydraulic.remainingTime == 0) and (hydraulic.inUse == True):
                hydraulic.inUse = False
                self.log.enterLogRegister(f"La hidráulica {hydraulic.id} fue liberada al tiempo {self.globalTime}.")

    def truckEnterDownload(self):
        import log

        for hydraulic in self.hydraulicsList:
            if (hydraulic.inUse == False) and (hydraulic.grainType == self.trucksDict[self.queue[0]].type):
                hydraulic.inUse = True
                hydraulic.remainingTime = hydraulic.serviceTime
                temp = hydraulic.id

        #Enters a registry in the process log
        #self.log.enterLogRegister("El Camión " + str(self.trucksDict[self.queue[0]].id) + " ha entrado a hidráulica de descarga al timepo " + str(self.globalTime) + ".")
                self.log.enterLogRegister(f"El Camión {str(self.trucksDict[self.queue[0]].id)} ha entrado a la hidráulica de descarga {temp} al tiempo {str(self.globalTime)}.")

        #In the complete version, it should be moved to the exit weight queue
                self.trucksDict.pop(self.queue[0]) #Remove it from the trucks dictionary
                self.queue.pop(0) #Remove it from queue
                if self.checkEmptyqueue:
                    break

    def checkEmptyqueue(self):
        return False if len(self.queue) > 0 else True        

    def advanceTime(self):
        self.globalTime += 1
        for hydraulic in self.hydraulicsList:
            hydraulic.remainingTime -= 1