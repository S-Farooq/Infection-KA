__author__ = 'Shaham'
from UserBase import *
import random

random.seed(5)
def create_graph(ub, clusters):
    '''Takes in an array 'clusters' and a userbase, updates userbase with a graph contained specified cluster ammounts
    :input:
    ub: UserBase instance
    clusters: array of cluster amounts to create in the graph

    :return: None
    '''
    v = 0
    #print 'Clusters:'
    for cluster in clusters:
        nodes = range(v,v+cluster)
        shuf_nodes = nodes
        ub.add_users(nodes)
        for n in nodes:
            random.shuffle(shuf_nodes)
            ub.add_teachers(n,shuf_nodes[:len(shuf_nodes)])
            ub.add_students(n,shuf_nodes[len(shuf_nodes)+1:])
        v += cluster
        #print nodes
    #print ' ---------------------------------- '

def random_graph(ub):
    r = random.randint(1,12)
    clusters =random.sample(range(20),r)
    create_graph(ub, clusters)


if __name__ == '__main__':
    ub = UserBase()
    clusters = [25,2,4]
    create_graph(ub,clusters)
    new_version = 'Z'

    ub.display_userbase()

    ub.limited_infection_exact(new_version,limit=9)
    ub.reset()
    ub.limited_infection(new_version,limit=2)
    ub.reset()
    ub.total_infection(id=7,new_version=new_version)



    ub.display_userbase()
