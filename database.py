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
    def getUserMode(self, user_id):
        user_current_mode = self.GetUser(user_id)['current_mode']
        return user_current_mode
    def setUserMode(self, user_id, mode):
        self.GetUser(user_id)['current_mode'] = mode
    def getUserPhotos(self, user_id):
        pass
    def getPhotoFromID(self, user_id, fid):
        for photo in self.GetUser(user_id)['photos']:
            if photo['fid'] == fid:
                return photo
        return []
    def getPhotosByTags(self, user_id, Tags):
        all_user_photos = self.GetUser(user_id)['photos']
        result_photos   = []
        for photo in all_user_photos:
            for tag in Tags:
                if tag in photo['tag']:
                    result_photos.append(photo)
        return result_photos[:]
    def getNoTagPhotos(self, user_id):
        all_user_photos = self.GetUser(user_id)['photos']
        no_tag_photos = [photo for photo in all_user_photos if not len(photo['tag'])]
        return no_tag_photos[:]
    def hasNoTagPhotos(self, user_id):
        all_user_photos = self.GetUser(user_id)['photos']
        for photo in all_user_photos:
            if not len(photo['tag']):
                return True
        return False
    def appendUserPhotos(self, user_id):
        pass
    def getPhotoTags(self, user_id, photo_id):
        photo_id    = int(photo_id)
        photo_tags  = self.GetUser(user_id)['photos'][photo_id]['tag']
        return photo_tags[:]
    def setPhotoTags(self, user_id, photo_id, tags):
        photo_id    = int(photo_id)
        self.GetUser(user_id)['photos'][photo_id]['tag'] = tags[:]
    def SaveAll(self):
        self.SaveObj(self.users,self.users_info_path)
