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
        from simulation import STATUS_AVAILABLE
        self.id = id
        self.type = grainType
        self.pos = -1
        self.queueWaitTime = 0
        self.status = STATUS_AVAILABLE
    
    def getQueueSize(self, queueList):
        return len(queueList)

    def enterQueue(self, truckDictKey, queueList):
        from simulation import STATUS_AVAILABLE, STATUS_ONQUEUE

        if self.status == STATUS_AVAILABLE:
            queueList.append(truckDictKey)
            self.pos = self.getQueueSize(queueList)
            self.status = STATUS_ONQUEUE
        #else:
        #    raise ValueError("Truck not available for queueing")
 