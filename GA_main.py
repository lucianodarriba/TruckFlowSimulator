#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
from geneticAlgorithmRoutines import geneticAlgorithm
from simulation import Simulation, sim
#-----------------------------------------------
#Parametros del sistema
N = 100 #Largo de la cola
grainTypesList = [1, 2, 3] #Lista de los distintos tipos de grano
NH = 5 #Cantidad de hidráulicas en el sistema
endTime = 1000
#-----------------------------------------------

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#Running the genetic algorithm
#Create list of cities

#sim = Simulation()

sim.initializeParams(N, NH, grainTypesList, endTime)

sim.initialize()

# print("isjfoisjfe")
# print(sim.grainTypesList)
# print(list(j.grainType for j in sim.hydraulicsList))
# exit()

best_time=geneticAlgorithm(population=sim.queue, popSize=100, eliteSize=20, mutationRate=0.005, generations=100)



# x=[]
# y=[]
# for i in best_route:
#   x.append(i.x)
#   y.append(i.y)
# x.append(best_route[0].x)
# y.append(best_route[0].y)
# plt.plot(x, y, '--o')
# plt.xlabel('X')
# plt.ylabel('Y')
# ax=plt.gca()
# plt.title('Final Route Layout')
# bbox_props = dict(boxstyle="circle,pad=0.3", fc='C0', ec="black", lw=0.5)
# for i in range(1,len(cityList)+1):
#   ax.text(cityList[i-1].x, cityList[i-1].y, str(i), ha="center", va="center",
#             size=8,
#             bbox=bbox_props)
# plt.tight_layout()
# plt.show()
