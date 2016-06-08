__author__ = 'Shaham'
from User import User
import random

class UserBase(dict):

    def __init__(self):
        self.total_users = 0
        self.default_version = 'A'

    def add_users(self, ids, version=None):
        #Adding Users (for modelling purposes) with default software version = 2.0
        if version==None:
            version = self.default_version

        for id in ids:
            if not self.has_key(id):
                self[id]= User(version,id)
                self.total_users += 1
            else:
                raise KeyError('Error: Sorry, this user already exists in the database.')

    def add_teachers(self, id, teachers):
        #Creating teacher/student links (for modelling purposes)
        try:
            for t in teachers:
                if t!=id:
                    self[id].teachers.append(self[t])
                    self[t].students.append(self[id])
        except KeyError:
            print 'Error: This user does not exist.'

    def add_students(self, id, students):
        #Creating teacher/students links (for modelling purposes)
        try:
            for s in students:
                if s!=id:
                    self[id].students.append(self[s])
                    self[s].teachers.append(self[id])
        except KeyError:
            print 'Error: This user does not exist.'

    def get_user_version(self,id):
        try:
            return self[id].version
        except KeyError:
            print 'Error: Sorry, this user does not exist. Please double check you have the correct User ID.'

    def display_clusters(self, user,cluster_list,checked):

        try:
            checked.append(user.id)
            cluster_list.append(str(user.id)+'('+str(user.version)+')')
            if len(user.teachers)>0:
                for t in user.teachers:
                    if t.id not in checked:
                        self.display_clusters(t,cluster_list,checked)
            if len(user.students)>0:
                for s in user.students:
                    if s.id not in checked:
                        self.display_clusters(s,cluster_list,checked)
        except KeyError:
            print 'Error: Sorry, this user (id=' + str(id) + ') does not exist. Please double check you have the correct User ID.'

    def reset(self):
        print 'Resetting Userbase...'
        for i in self.keys():
            self[i].version = self.default_version
        print ' ---------------------------------- '

    def display_userbase(self, inf_list=None):
        #Helper Function to help with debugging
        checked = []
        if not inf_list:
            print 'Clusters in graph:'
            for i in self.keys():
                if i in checked:
                    continue
                cluster_list =[]
                self.display_clusters(self[i],cluster_list, checked)

                print str(len(cluster_list)) +' nodes: [ ' + ' '.join(cluster_list) + ' ]'
            print ' ---------------------------------- '

        else:
            for i in inf_list:
                line =[str(i) + ': { ']

                for t in self[i].teachers:
                    line.append(str(t.id)+' ')
                for s in self[i].students:
                    line.append(str(s.id) + ' ')
                line.append('}')

                print ''.join(line)
                print ' ---------------------------------- '


    def total_infection(self, id, new_version):
        #Total Infection coded below, uses infect_all function
        print 'Infecting TOTALLY....'
        infected_list = []
        try:
            self.infect_all(self[id],new_version, infected_list)
            print 'Infected: [' + ' '.join([str(x) for x in infected_list]) + ' ]'
            print 'I Infected ' + str(len(infected_list)) + ' users.'

        except KeyError:
            print 'Error: Sorry, this user (id=' + str(id) + ') does not exist. Please double check you have the correct User ID.'
        print ' ---------------------------------- '

    def infect_all(self, user, new_version, infected):
        #1. Start with a user, infect it and add it into an 'infected' list
        #2. Look at any of its teachers or students, if NOT in 'infected' list, make them the user
        #3. recursive formula with teacher/student as user until all nodes connected to the original user are in 'infected' list
        #4. Final 'infected' list will have all unique nodes that were infected

        try:
            user.update_version(new_version)
            infected.append(user.id)
            if len(user.teachers)>0:
                for t in user.teachers:
                    if t.id not in infected:
                        self.infect_all(t,new_version,infected)
            if len(user.students)>0:
                for s in user.students:
                    if s.id not in infected:
                        self.infect_all(s,new_version,infected)
        except KeyError:
            print 'Error: Sorry, this user (id=' + str(id) + ') does not exist. Please double check you have the correct User ID.'




#Limited Infection Solution:

#Note: Limit is taken to be hard limit, if a bit less than limit infected, it's okay because prioritizes user experience over infecting exactly a limited amount
#Solution uses greedy approach (not optimal solution but close enough and specification taken to mean it's not so important to get EXACTLY the limited amount but AROUND that)

    def limited_infection(self, new_version, limit):
        #Limited Infection Coded below, uses infect_count function
        print 'Infecting LIMITEDLY.... (' + str(limit) + ' users MAX)\n'
        if self.total_users == 0:
            print 'There are no users in the database...'
            return

        #Randomize/Shuffle users in Userbase

        ids = self.keys()
        random.shuffle(ids)

        #Start with a random user
        id = ids.pop()


        checked = []
        infected = 0

        #While we have not infected more than the limit:
        while infected <limit:
            #empty to_infect_list
            to_infect_list = []

            #Infect_count will get us the amount of NOT infected users in the specific cluster which randomly chosen user is a part of
            self.infect_count(self[id],new_version, to_infect_list, checked)

            #If the NOT infected in the cluster is less than the the limit minus what we've already infected, then:
            if len(to_infect_list)<= (limit-infected):
                #Infect all the users in the to_infect_list
                infected += len(to_infect_list)
                for i in to_infect_list:
                    self[i].update_version(new_version)
                print str(len(to_infect_list)) +' infected ---->' +str(infected) +'/'+str(limit) + '(Infected so far / infection Limit)'
                print 'Infected: [' + ' '.join([str(x) for x in to_infect_list]) + ' ]'

            #Extra while loop to make sure the random user we select has not already been 'checked'
            while id in checked:
                if len(ids)==0:
                    #Means we've checked all users, can't go any further, quit infection loop
                    print 'I infected ' + str(infected) + ' users.'
                    print ' ---------------------------------- '
                    return
                id = ids.pop()




        print 'I infected ' + str(infected) + ' users.'
        print ' ---------------------------------- '


    def infect_count(self, user, new_version, to_infect,checked):
        #basically the infect_all function but instead of blindly infecting users, it only counts how many can potentially be infected
        #1. Start with a user, add to counter if NOT infected yet and add it into an 'to_infect' list
        #2. Look at any of its teachers or students, if NOT in 'checked' list, make them the user
        #3. recursive formula with teacher/student as user until all nodes connected to the original user are in 'checked' list
        #4. Final 'to_infect_list' list will have all unique nodes that can be infected, final 'checked' list will have all unique nodes in cluster

        try:
            if user.version != new_version:
                to_infect.append(user.id)
            checked.append(user.id)
            if len(user.teachers)>0:
                for t in user.teachers:
                    if t.id not in checked:
                        self.infect_count(t,new_version,to_infect,checked)
            if len(user.students)>0:
                for s in user.students:
                    if s.id not in checked:
                        self.infect_count(s,new_version,to_infect,checked)
        except KeyError:
            print 'Error: Sorry, this user (id=' + str(id) + ') does not exist. Please double check you have the correct User ID.'




#Limited Infection that only infects if EXACT amount can be infected Solution:

    def limited_infection_exact(self, new_version, limit):
        #Infects a limited amount of users if and only if:
        # 1. all teacher-student pairs will be infected
        # 2. Exactly the limited amount of users will be infected
        # Return Value: True (if fulfilled the above conditions), False (if could not fulfill above conditions)
        print 'Infecting EXACTLY.... (' + str(limit) + ' users)\n'

        #If limit is greater, obviously cannot fulfill conditions, return False
        if limit>self.total_users:
            print 'Limit greater than total users...'
            print ' ---------------------------------- '
            return False


        #Solution is basically to first gather knowledge of ALL the clusters in our userbase and how many users can be
        #potentially infected in each of those clusters
        #Once we have that information, the problem boils down to a Coin Change variation with limited supply of coins
        #Then, we can use the below 'find' function to dynamically program a solution and find those clusters (if they exist)
        #that will lead to satisfying the above conditions
        ids = self.keys()

        random.shuffle(ids)
        id = ids.pop()

        #To fill with nodes we've already checked
        checked = []

        #TO store cluster information
        clusters = {}
        cluster_amounts = [] #A list to be used to determine best solution afterwards
        cluster_indx = 0

        while True:
            to_infect_list = []

            while id in checked:
                if len(ids)==0:
                    break
                id = ids.pop()

            self.infect_count(self[id],new_version, to_infect_list, checked)

            #If potentially infectable nodes less than limit, add to cluster list
            if len(to_infect_list)<limit:
                cluster_amounts.append(len(to_infect_list))
                clusters[cluster_indx] = to_infect_list
                cluster_indx +=1

            #If cluster has potentially infectable nodes as the limit, infect those limit, return True
            elif len(to_infect_list)==limit:
                for i in to_infect_list:
                    self[i].update_version(new_version)
                print str(len(to_infect_list)) +' infected ---->' +str(len(to_infect_list)) +'/'+str(limit) + '(Infected so far / infection Limit)'
                return True

            if len(ids)==0:
                break

            id = ids.pop()



        #indexes will be filled with the cluster indices that should be infected
        indexes = []

        #Find if solution exists and if so, fill up the indexes
        res = self.find(cluster_amounts,limit,indexes)

        if res:
            print 'Solution found! Infecting...'
            infected = 0
            for x in indexes:
                to_infect_list = clusters[x]

                for i in to_infect_list:
                    self[i].update_version(new_version)
                infected += len(to_infect_list)
                print str(len(to_infect_list)) +' infected ---->' +str(infected) +'/'+str(limit) + '(Infected so far / infection Limit)'
                print 'Infected: [' + ' '.join([str(x) for x in to_infect_list]) + ' ]'
            print ' ---------------------------------- '
            return True
        else:
            print 'No solution found. Nothing infected.'
            print ' ---------------------------------- '
            return False


    def find(self,elements, n,indexes):
        #Dynamic programming for coin change problem with limited supply of coins (elements in this case)
        m = len(elements)
        C = [False for x in range(n+1)]
        C[0] = True

        table = [[0 for x in range(m)] for x in range(n+1)] #To keep track of if we have already used the element or not

        for i in range(m):
            table[0][i] = 1

        B = [0 for x in range(n+1)] #Backtrace vector so we can find solution afterwards
        for i in range(1, n+1):

            for j in range(m):
                #if we already know we can sum the amount i, then C[i] will be true, and we don't do anything
                if C[i]:
                    table[i][j] = table[i-elements[j]][j]
                    continue

                #If including the jth element can get a sum of i, then C[i] is True and we can add the jth element to the backtrace
                if (i-elements[j]>=0) and table[i-elements[j]][j]>0 and C[i-elements[j]]:
                    B[i]=j

                    C[i] = True
                    table[i][j] = table[i-elements[j]][j]-1

                elif (i-elements[j]<0):
                    table[i][j] = 1

                #If including the jth element does not sum to i, C[i] remains false
                else:
                    table[i][j] = table[i-elements[j]][j]

        #The final if amount 'n' can be summed from our elements will be in C[n]
        if C[n]:
            #Since we can sum to n, use backtrace to get the indexes of the elements that sum to n
            t=n
            while t!=0:
                indexes.append(B[t])
                t -= elements[B[t]]
            return C[n]
        else:
            #If we cannot sum to n, return C[n] (which will be False)
            return C[n]



