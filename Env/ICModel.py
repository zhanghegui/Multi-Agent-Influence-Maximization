import os
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import time
import Agents as ag


class ICModel(object):
    def __init__(self):
        self.G = self.init_graph()
        # pos = nx.random_layout(self.G)
        #
        # nx.draw_networkx(self.G, pos)
        # plt.show()
        # print(len(self.G.nodes()), len(self.G.edges()))

    def init_graph(self):
        dirs = os.listdir('../Dataset')
        print(dirs)
        index = int(input("Plz input the index of a dataset:"))
        graph = nx.read_edgelist('../Dataset/' + dirs[index], nodetype=int, data=(('weight', float),),
                                 create_using=nx.DiGraph)
        for node in graph.nodes():
           graph.node[node]['SA'] = node
        print(graph.nodes(data=True))
        return graph

    def diffusion(self, original_users, times, p=0.01):
        spread = []
        for i in range(times):
            print('\rTime step: %d' % (i), end='')
            new_active, already_active = original_users[:], original_users[:]
            new_ones = []
            while new_active:
                for user in new_active:
                    np.random.seed(i)
                    for neighbor in self.G.neighbors(user):
                        if np.random.uniform(0, 1) < p:
                            new_ones.append(neighbor)
                new_active = list(set(new_ones) - set(already_active))
                already_active += new_active
            spread.append(len(already_active))
        return np.mean(spread)


if __name__ == '__main__':
    IC = ICModel()
