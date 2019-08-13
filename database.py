import json
import os, sys
class Database:
    def __init__(self):
        if not os.path.exists('data'):
            os.makedirs('data')
        self.users_info_path = 'data/users.json'
        if os.path.exists(self.users_info_path):
            self.users = self.LoadJson(self.users_info_path)
        else:
            self.users = {}
    def SaveObj(self, obj, path):
        with open(path, 'w') as file:
            json_str = json.dumps(obj)
            file.write(json_str)
    def LoadJson(self, path):
        with open(path, 'r') as file:
            json_str = file.read()
            python_obj = json.loads(json_str)
            return python_obj
    def CheckUserExist(self, user_id):
        return not self.users.get(str(user_id)) == None
    def DeleteUser(self, user_id):
        if self.CheckUserExist(user_id):
            del self.users[str(user_id)]
    def AddUser(self, user_id):
        if not self.CheckUserExist(user_id):
            self.users[str(user_id)] = {
                'total_files':0,
                'current_mode':'none',
                'photos':[]
                }
            self.SaveObj(self.users,self.users_info_path)
            return True
        else:
            return False
    def GetUser(self, user_id):
        if self.CheckUserExist(user_id):
            return self.users[str(user_id)]
        else:
            self.AddUser(user_id)
            return self.users[str(user_id)]
    def SaveAll(self):
        self.SaveObj(self.users,self.users_info_path)
