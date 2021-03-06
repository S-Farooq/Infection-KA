__author__ = 'Shaham'
from UserBase import *
import random
import sys

def create_graph(ub, clusters):
    '''Takes in an array 'clusters' and a userbase, updates userbase with a graph contained specified cluster ammounts
    :Inputs:
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

def random_graph():
    '''Generates random graphs in userBase
        :return: UserBase Instance'''

    ub = UserBase()
    r = random.randint(1,12)
    clusters =random.sample(range(1,20),r)
    create_graph(ub, clusters)
    return ub

def test1():
    ub = UserBase()
    clusters = [1,3,17,19,5,13,11,7]
    create_graph(ub, clusters)
    new_version = 'Z'
    print 'Before infections:'
    ub.display_userbase()

    raw_input('press any key')
    print '\n----Total Infection starting from id=11'
    ub.total_infection(11,new_version) #should infect 4th cluster, 19 nodes
    ub.display_userbase()
    ub.reset()

    raw_input('press any key')
    print '\n----Limited Inflected with limit=35'
    ub.limited_infection(new_version,35) #Does not exceed more than 35 infections
    ub.display_userbase()
    ub.reset()

    raw_input('press any key')
    print '\n----Exact limited Inflection with limit =2'
    ub.limited_infection_exact(new_version,2) #cannot find exact solution
    ub.display_userbase()
    ub.reset()

    raw_input('press any key')
    print '\n----Exact limited Inflection with limit =35'
    ub.limited_infection_exact(new_version,35) #Solution found (13+17+5=35)
    ub.display_userbase()

def test2():
    ub = UserBase()
    clusters = [2,4,6,8,10]
    create_graph(ub, clusters)
    new_version = 'Z'
    print 'Before infections:'
    ub.display_userbase()

    raw_input('press any key')
    print '\n----Total Infection starting from id=11'
    ub.total_infection(6,new_version) #should infect 3rd cluster, 6 nodes
    ub.display_userbase()
    ub.reset()

    raw_input('press any key')
    print '\n----Limited Inflected with limit=23'
    ub.limited_infection(new_version,23) #Does not exceed more than 23 infections
    ub.display_userbase()
    ub.reset()


    # for l in [7,13,17]:
    #     raw_input('press any key')
    #     print '\n----Exact limited Inflection with limit = ' + str(l)
    #     ub.limited_infection_exact(new_version,l) #cannot find exact solution (odd #)
    #     #ub.display_userbase()
    #     ub.reset()

    raw_input('press any key')
    print '\n----Exact limited Inflection with limit =14'
    ub.limited_infection_exact(new_version,14) #Solution found (13+17+5=35)
    ub.display_userbase()

def random_test():
    ub = random_graph()
    new_version = 'Z'

    print 'Before infections:'
    ub.display_userbase()

    raw_input('press any key')
    id = random.choice(ub.keys())
    print '\n----Total Infection starting from id='+str(id)
    ub.total_infection(id,new_version)
    ub.display_userbase()
    ub.reset()

    raw_input('press any key')
    l = random.choice(range(1,ub.total_users+1))
    print '\n----Limited Inflected with limit = '  + str(l)
    ub.limited_infection(new_version,l)
    ub.display_userbase()
    ub.reset()

    raw_input('press any key')
    print '\n----Exact limited Inflection with limit = ' +str(l)
    ub.limited_infection_exact(new_version,l)
    ub.display_userbase()

def test(clusters,id,l):
    ub = UserBase()
    create_graph(ub, clusters)
    new_version = 'Z'

    print 'Before infections:'
    ub.display_userbase()

    raw_input('press any key')
    print '\n----Total Infection starting from id='+str(id)
    ub.total_infection(id,new_version)
    ub.display_userbase()
    ub.reset()

    raw_input('press any key')
    print '\n----Limited Inflected with limit = '  + str(l)
    ub.limited_infection(new_version,l) #Does not exceed more than 23 infections
    ub.display_userbase()
    ub.reset()

    raw_input('press any key')
    print '\n----Exact limited Inflection with limit = ' +str(l)
    ub.limited_infection_exact(new_version,l) #Solution found (13+17+5=35)
    ub.display_userbase()

if __name__ == '__main__':
    if len(sys.argv)!=2:
        print 'Please input ONLY one arguments out of: \'custom_test\', \'test1\', \'test2\', \'random\''
    else:
        if sys.argv[1]=='custom_test':
            print 'Please input comma-delimited numbers definined the sizes of user clusters in UserBase:\n(ex. 2,3 = a cluster of size 2 and a cluster of size 3)'
            clusters = [int(n, 10) for n in raw_input().split(",")]

            id = int(raw_input('Please input an id (a number) for total_infection that is less than the total number of users in your UserBase:'),10)
            l = int(raw_input('Please input a limit (a number) for limited_infection:'),10)
            test(clusters,id,l)

        elif sys.argv[1] == 'test1':
            test1()
        elif sys.argv[1] == 'test2':
            test2()
        elif sys.argv[1] == 'random':
            random_test()
        else:
            print 'Please pass in a single arguments out of: \'custom_test\', \'test1\', \'test2\', \'random\''
