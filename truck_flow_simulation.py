from simulation import Simulation
'''
Este programa calcula el flujo de descarga de camiones bajo las siguientes suposiciones:
    - Hay G tipos de diferentes de granos
    - Existe una cola cola de descarga
    - Hay NH hidráulicas de descarga
    - Puede haber entre 1 y NH hidráulicas destinadas a un mismo tipo de grano
    - Si hay camiones con granos de tipo j, entonces hay al menos una hidráulica de tipo j
'''

#Parametros del sistema
N = 20 #Largo de la cola
grainTypesList = [1, 2, 3, 4, 5] #Lista de los distintos tipos de grano
NH = 5 #Cantidad de hidráulicas en el sistema
endTime = 100


sim = Simulation()

sim.initializeParams(N, NH, grainTypesList, endTime)

sim.initialize()

sim.runSimulation()

#sim.log.outputLog()