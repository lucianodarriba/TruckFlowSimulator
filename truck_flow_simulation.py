from simulation import Simulation, sim
import itertools
'''
Este programa calcula el flujo de descarga de camiones bajo las siguientes suposiciones:
    - Hay G tipos de diferentes de granos
    - Existe una cola cola de descarga
    - Hay NH hidráulicas de descarga
    - Puede haber entre 1 y NH hidráulicas destinadas a un mismo tipo de grano
    - Si hay camiones con granos de tipo j, entonces hay al menos una hidráulica de tipo j
'''

#-----------------------------------------------
#Parametros del sistema
N = 10 #Largo de la cola
Nfixed = 90
grainTypesList = [1, 2, 3] #Lista de los distintos tipos de grano
NH = 5 #Cantidad de hidráulicas en el sistema
endTime = 100
#-----------------------------------------------

#sim = Simulation()

sim.initializeParams(N, NH, Nfixed, grainTypesList, endTime)

sim.initialize()


print("Cola fija")
print(len(sim.fixedQueue))
print(sim.fixedQueue)

print("Cola a llamar")
print(len(sim.queue))
print(sim.queue)

sim.fixedQueue = sim.updateFixedQueue(sim.fixedQueue, sim.queue)
print("Nueva cola fija")
print(len(sim.fixedQueue))
print(sim.fixedQueue)

# sim.trucksDict = sim.generateTrucksDict(sim.N)
# sim.queue = sim.generate_queueList(sim.trucksDict, sim.N)

# print("Nueva cola a llamar")
# print(len(sim.queue))
# print(sim.queue)

# print(list(sim.trucksDict[j].type for j in sim.queue))
# # print(set(sim.trucksDict[j].type for j in sim.queue))
# print(list(h.grainType for h in sim.hydraulicsList))

# sim.runSimulation(sim.queue)
# print(f"Simulacion terminada a tiempo {sim.globalTime}")
# print(sim.queue)
# sim.log.outputLog()












# print(sim.queue)
# print(list(sim.trucksDict[j].type for j in sim.queue))

# lista = []
# for i in sim.queue:
#     lista.append(sim.trucksDict[i].type)

# # tuplaDeColas = list(itertools.permutations(sim.queue, len(sim.queue)))
# tuplaDeColas = list(itertools.permutations(lista, len(lista)))

# listaDeColas = []
# for t in tuplaDeColas:
#     listaDeColas.append(list(t))
# #listaDeColas = [[1, 2, 3], [1, 3, 2], [1, 2, 3]]

# print(type(listaDeColas))
# print(len(listaDeColas))
# #print(listaDeColas)
# # for i in listaDeColas:
# #     print(i)

# #setDeColas = set(listaDeColas)
# setDeColas = [list(item) for item in set(tuple(row) for row in listaDeColas)]
# print(type(setDeColas))
# print(len(setDeColas))
# #print(setDeColas)

# listaDeTiempos = []
# for i in range(len(setDeColas)):
#     queue = setDeColas[i]
#     sim.runSimulation(queue)

#     listaDeTiempos.append(sim.globalTime)
#     print(i, sim.globalTime)

#     sim.restartSimulation()

# print(max(listaDeTiempos), min(listaDeTiempos))