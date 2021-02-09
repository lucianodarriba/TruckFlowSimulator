class HydraulicsClass():
    def __init__(self, id, type, inUse, serviceTime):
        self.id = id
        self.grainType = type #Tipo de grano
        self.inUse = inUse
        self.unloadStartTime = 0
        self.serviceTime = serviceTime #ServiceTime es el tiempo que tarda en descargar
        if self.inUse:
            self.remainingTime = self.serviceTime
        else:
            self.remainingTime = 0

    def startUnload(self, it):
        self.unloadStartTime = it
        self.inUse = True

    def free(self):
        self.inUse = False


class TruckClass():
    def __init__(self, id, grainType):
        self.id = id
        self.type = grainType
        self.pos = -1
        self.queueWaitTime = 0
    
    def getQueueSize(self, queueList):
        return len(queueList) + 1

    def enterQueue(self, truckDictKey, queueList):

        self.pos = self.getQueueSize(queueList)
        queueList.append(truckDictKey)
        #self.queueWaitTime = self.getQueueWaitTime(queueList, hydraulicsList)
    
    # def getQueueWaitTime(self, queueList, trucksDict, hydraulicsList):
    #     truckIndex = queueList.index(self.id)

    #     if truckIndex < 0:
    #         print("Error: Truck with ID " + self.id + " is not in queue.")
    #         return
    #     elif truckIndex == 0:
    #         self.queueWaitTime = min(list(hydraulic.remainingTime for hydraulic in hydraulicsList if hydraulic.grainType == self.type))
    #     else:
    #         self.queueWaitTime += trucksDict[queueList[truckIndex - 1]].queueWaitTime + min(list(hydraulic.serviceTime for hydraulic in hydraulicsList if hydraulic.grainType == self.type))

            
