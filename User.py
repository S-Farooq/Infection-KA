__author__ = 'Shaham'

class User():
    #modeling a student of KA

    def __init__(self, version, id, name='Random'):
        self.id = id
        self.version = version
        self.name = name
        self.teachers=[]
        self.students=[]

    def update_version(self,new_version):
        self.version = new_version