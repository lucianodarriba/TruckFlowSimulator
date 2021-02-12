from geneticAlgorithmRoutines import geneticAlgorithm
from simulation import Simulation, sim
#-----------------------------------------------
#Parametros del sistema
N = 100 #Largo de la cola
Nfixed = 0 #Largo de la cola fija (es decir, los camiones que ya fueron llamados)
grainTypesList = [1, 2, 3] #Lista de los distintos tipos de grano
NH = 5 #Cantidad de hidráulicas en el sistema
endTime = 10000
#-----------------------------------------------
'''
The object 'sim' represents the simulation environment
'''

sim.initializeParams(N, NH, Nfixed, grainTypesList, endTime)

sim.initialize()

#El algoritmo devuelve la cola que mejor optimizó el tiempo de espera.
best_time_queue, best_time = geneticAlgorithm(population=sim.queue, popSize=100, eliteSize=20, mutationRate=0.01, generations=100)

print("Simulación terminada.")
print(best_time_queue)
print(f"Best time: {1 / best_time}")