__author__ = 'Shaham'

class User():
    #modeling a student of KA

    def __init__(self, version, id):
        '''Initialize with id, version, and array to be filled with other User instance sdefining its coaching relations'''
        self.id = id
        self.version = version
        self.teachers=[]
        self.students=[]

    def update_version(self,new_version):
        '''Updates its version to the one specified
        :return: None'''
        self.version = new_version