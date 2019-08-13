import json
import os, sys
DEFULT_USER = {
    'id' : 0000
}
class database:
    def __init__(self):
        if not os.path.exists('data'):
            os.makedirs('data')
        self.users_info_path = 'data/users.json'
        if os.path.exists(self.users_info_path):
            self.users = self.loadJson(self.users_info_path)
        else:
            self.users = {}
        #self.saveObj(data,self.users_db_path)
    def saveObj(self, obj, path):
        with open(path, 'w') as file:
            json_str = json.dumps(obj)
            file.write(json_str)
    def loadJson(self, path):
        with open(path, 'r') as file:
            json_str = file.read()
            python_obj = json.loads(json_str)
            return python_obj
    def check_user_exist(self, user_id):
        return not self.users.get(str(user_id)) == None
    def delete_user(self, user_id):
        if self.check_user_exist(user_id):
            del self.users[str(user_id)]
    def add_user(self, user_id):
        if not self.check_user_exist(user_id):
            self.users[str(user_id)] = {
                'total_files':0,
                'current_mode':'none',
                'photos':[]
                }
            self.saveObj(self.users,self.users_info_path)
            return True
        else:
            return False
    def get_user(self, user_id):
        if self.check_user_exist(user_id):
            return self.users[str(user_id)]
        else:
            self.add_user(user_id)
            return self.users[str(user_id)]
    def save_all(self):
        self.saveObj(self.users,self.users_info_path)
