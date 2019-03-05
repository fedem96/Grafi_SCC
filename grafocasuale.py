import numpy as np
from random import random
from timeit import default_timer as timer


class Node:

    def __init__(self, id):
        self.id = id    # numero intero che identifica il nodo

        # inizializzo attributi che verranno usati nella dfs
        self.color = "white"
        self.p = None   # riferimento a nodo precedente
        self.d = None   # tempo di scoperta del nodo
        self.f = None   # tempo di completamento visita sul nodo

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return "Node " + str(self.id) + ": p = " + str(self.p) + ", d = " + str(self.d) + ", f = " + str(self.f)


class Graph:

    def __init__(self, adjMatrix=None, numNodes=0, numEdges=0):

        self.time = 0
        self.numEdges = numEdges

        if adjMatrix is not None:
            # se specificata, inizializzo il grafo tramite la matrice di adiacenza
            self.adjMatrix = adjMatrix
            numNodes = adjMatrix.shape[0]
            self.nodes = [Node(i) for i in range(numNodes)]
        else:
            # inizializzo la matrice di adiacenza con tutti zeri
            self.adjMatrix = np.full((numNodes, numNodes), False, dtype=bool)

        # creo lista di nodi
        self.nodes = [Node(i) for i in range(numNodes)]

    def dfs(self, firstGraph=None):
        # firstGraph serve per eseguire il secondo ciclo in un preciso ordine (serve per trovare le componenti fortemente connesse)
        # quando firstGraph non viene passato, viene eseguita la dfs semplice

        for node in self.nodes:
            node.color = "white"
            node.p = None
        self.time = 0

        if firstGraph is None:
            # se non è specificato un altro grafo, nel prossimo ciclo scorro gli indici in ordine
            indexes = range(len(self.nodes))
        else:
            # creo una lista di tuple:
            # il primo elemento della tupla è l'id del nodo, il secondo elemento della tupla è il campo f del nodo
            tuples = [(i, firstGraph.nodes[i].f) for i in range(len(self.nodes))]
            # riordino la lista di tuple in modo decrescente rispetto al campo f
            tuples.sort(key=lambda tup: tup [1], reverse=True)
            # creo la lista di indici
            indexes = [tup[0] for tup in tuples]

        numTreesInForest = 0
        for i in indexes:
            if self.nodes[i].color == "white":
                self.dfsVisit(i)
                numTreesInForest += 1
        return numTreesInForest

    def dfsVisit(self, nodeId):
        u = self.nodes[nodeId]
        self.time += 1
        u.d = self.time
        u.color = "gray"

        adiacenti = self.adjMatrix[nodeId]
        nodes = self.nodes

        for i in range(self.adjMatrix.shape[0]):
            if adiacenti[i]:
                # se l'arco dal nodo nodeIndex al nodo i esiste
                v = nodes[i]
                if v.color == "white":
                    v.p = u
                    self.dfsVisit(i)
        u.color = "black"
        self.time += 1
        u.f = self.time

    def transpose(self):
        gt = Graph(self.adjMatrix.transpose(), numEdges=self.numEdges)
        return gt

    # algoritmo usato nei test
    def getNumStronglyConnectedComponents(self):
        self.dfs()
        gt = self.transpose()
        return gt.dfs(self)

    # in realtà questo algoritmo non viene usato nei test
    def getStronglyConnectedComponents(self):
        self.dfs()
        gt = self.transpose()
        gt.dfs(self)
        sccs = []
        for node in gt.nodes:
            found = False
            for scc in sccs:
                if node.f < scc[0].d or scc[0].f < node.d:
                    continue
                scc.append(node)
                found = True
                break

            if not found:
                sccs.append([node])

        return sccs


class RandomGraph(Graph):

    # genera un grafo casuale con numero di nodi e probabilità di generazione archi indicati
    def __init__(self, numNodes, prob):

        Graph.__init__(self, numNodes=numNodes)

        if prob == 0:
            return

        # ogni elemento della matrice di adiacenza diventa un 1 con probabilità prob
        for i in range(numNodes):
            for j in range(numNodes):
                r = random()
                if prob > r:
                    self.adjMatrix[i][j] = True
                    self.numEdges += 1


if __name__ == "__main__":
    g = RandomGraph(30, 0.1)
    g.dfs()
    sccs = g.getStronglyConnectedComponents()
    print("Il numero di componenti fortemente connesse è: " + str(len(sccs)))
    for scc in sccs:
        print("Componente fortemente connessa formata da nodi: " + str([node.id for node in scc]))
