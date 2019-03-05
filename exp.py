import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from timeit import default_timer as timer

from grafocasuale import RandomGraph


# crea più volte un grafo casuale con numero di nodi e probabilità specificati
# aggiunge la tripla (probabilità, numero nodi, numero di scc) alla lista points
# restituisce il numero medio di componenti fortemente connesse
def test(n, p, points):

    numProve = 10
    avgEdgesNumber = 0
    avgSccsNumber = 0
    avgTime = 0
    for i in range(numProve):
        g = RandomGraph(n, p)
        start = timer()
        numSCC = g.getNumStronglyConnectedComponents()
        end = timer()
        avgEdgesNumber += g.numEdges
        avgSccsNumber += numSCC
        avgTime += (end-start)

    e = avgEdgesNumber/numProve
    zscc = avgSccsNumber/numProve
    zt = avgTime/numProve

    points.append([p, n, e, zscc, zt])

    return e, zscc, zt


if __name__ == "__main__":

    '''
    Verranno creati tre grafici 3D aventi:
     - probabilità sull'asse x
     - numero nodi sull'asse y
     - sull'asse z: numero archi, numero SCC, tempo esecuzione  
    '''

    probs = np.arange(0, 1.01, 0.02)   # ndarray contenente le probabilità da testare
    numNodes = np.arange(1, 100, 2)     # ndarray contenente i numeri di nodi da testare

    # creo una lista che conterrà i punti (x,y,z) che verranno salvati su file
    points = []
    values = []
    npProb = []
    npNumNodes = []

    # eseguo il test per ogni probabilità e numero di nodi
    for nn in numNodes:
        for pr in probs:
            npProb.append(pr)
            npNumNodes.append(nn)
            values.append(test(nn, pr, points))

    npNumEdges = np.array([tupla[0] for tupla in values])
    zsccs = np.array([tupla[1] for tupla in values])
    ztime = np.array([tupla[2] for tupla in values])

    # salvo su file i risultati
    dataFile = open("data.csv", "wt")
    dataFile.write("probability;nodes_number;edges_number;sccs_number;exec_time\n")
    for point in points:
        dataFile.write(str(point[0]) + ";" + str(point[1]) + ";" + str(point[2]) + str(point[3]) + str(point[4]) + "\n")
    dataFile.flush()

    # creo il primo grafico
    fig = plt.figure(1)
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_trisurf(npProb, npNumNodes, npNumEdges, antialiased=True)

    ax.set_xlabel('Probabilità di generazione archi')
    ax.set_ylabel('Numero di nodi')
    ax.set_zlabel('Numero di archi')

    # mostro il primo grafico
    plt.show()

    # creo il secondo grafico
    fig = plt.figure(2)
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_trisurf(npProb, npNumNodes, zsccs, antialiased=True)

    ax.set_xlabel('Probabilità di generazione archi')
    ax.set_ylabel('Numero di nodi')
    ax.set_zlabel('Numero componenti fortemente connesse')

    # mostro il secondo grafico
    plt.show()

    # creo il terzo grafico
    fig = plt.figure(3)
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_trisurf(npProb, npNumNodes, ztime, antialiased=True)

    ax.set_xlabel('Probabilità di generazione archi')
    ax.set_ylabel('Numero di nodi')
    ax.set_zlabel('Tempo')

    # mostro il terzo grafico
    plt.show()
