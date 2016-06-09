# Infection-KA
Infection Algorithms for Khan Academy Interview

<h1>Modelling</h1>
User holds attributes like id and version as well as connections to other user instances defining teacher-student relations.
UserBase is a dictionary of User instances.

Together, Users and UserBase generalize to a collection of graphs (clusters).

<h1>Instructions</h1>
main.py runs the total_infection, limited_infection, and the 'exact' variation of limited_infection algorithms on pre-made test cases or custom test cases. main.py takes in a single argument (from system/command line):
'test1': Runs algorithms on a pre-made 8 cluster UserBase
'test2': Runs algorithms on a pre-made 5 cluster UserBase
'random': Runs algorithms on randomly generated Userbase
'custom_test': Prompts you to indicate cluster sizes to build the UserBase and parameters for the algorithms

<h1>Algorithms</h1>
<h4>total_infection</h4> Infects entire clusters given a single user in that cluster (Graph Traversal)
<h4>limited_infection</h4> The 'limit' interperated as a hard limit; algorithm 'greedily' infects users up to the 'limit' amount.
<h4>limited_infection_exact</h4> Uses dynamic programming to infect users if and only if 1. all teacher-student pairs will be infected and 2. the exact amount of users indicated ('limit') are to be infected. Otherwise, it will not infect any user and return False.

