from tgAPI import *
from sentencecut import check
# 從給定的Tags產生按鈕供使用這點選
def CreateButton(tags,uid,fid):
    keyboard = [[],[]]
    for i in tags:
        keyboard[0].append(InlineKeyboardButton(i, callback_data=i))# $id$fid
    keyboard[1].append(InlineKeyboardButton('確認送出', callback_data='${}${}'.format(str(uid),str(fid))))
    return InlineKeyboardMarkup(keyboard)
def GetUserObj(db,update):
    if update.message != None:
        return db.GetUser(update.message.from_user.id)
    elif update.inline_query != None:
        return db.GetUser(update.inline_query.from_user.id)
    elif update.callback_query != None:
        # callback_query
        return db.GetUser(update.callback_query.from_user.id)
# 用來Tag新增/修改
class Tag:
    def __init__(self,db,telegram):
        self.db                 =   db
        self.tg                 =   telegram
        self.creat_button_lock  =   {}
        self.reply_markup       =   {}
    def AddTag(self,bot,update):
        user_obj = GetUserObj(self.db,update)
        uid = update.message.from_user.id
        if user_obj['current_mode'] == 'add':
            if update.message.text.find('#') != -1:
                for i in range(len(user_obj['photos'])):
                    if len(user_obj['photos'][i]['tag']) == 0:
                        user_obj['photos'][i]['tag'] = update.message.text.split('#')[1:]
                        bot.sendMessage(uid,'好ㄉ，已為id為'+str(user_obj['photos'][i]['fid'])+'的圖片加上tag'+update.message.text)
                        return
                bot.sendMessage(uid,'很抱歉，目前沒有圖片是還未加上Tag的喔')
            else:
                userinPut = update.message.text.replace('\n', ' ')
                button_data = check(userinPut)
                for i in range(len(user_obj['photos'])):
                    if len(user_obj['photos'][i]['tag']) == 0:
                        if not str(uid) in self.creat_button_lock.keys():
                            self.creat_button_lock[str(uid)] = True
                            self.reply_markup[str(uid)] = CreateButton(button_data,
                                                        update.message.from_user.id,
                                                        user_obj['photos'][i]['fid'])
                            user_obj['current_tags'] = []
                            bot.sendMessage(uid,'點擊按鈕即可為圖片{}加入標籤'.format(user_obj['photos'][i]['fid']), reply_markup=self.reply_markup[str(uid)])
                        else:
                            bot.sendMessage(uid,'在之前的按鈕送出前無法再產生新的')
        elif user_obj['current_mode'] == 'tag':
            text = update.message.text.split(':')
            fid = int(text[0])
            for i in range(len(user_obj['photos'])):
                if user_obj['photos'][i]['fid'] == fid:
                    user_obj['photos'][i]['tag'] = text[1].split('#')[1:]
                    user_obj['current_mode'] = 'none'
                    bot.sendMessage(uid,'好ㄉ，已為id為'+str(user_obj['photos'][i]['fid'])+'的圖片加上tag:'+text[1]+'\n\n同時已離開Tag編輯模式，輸入 /tag 再次進入')
                    return
            bot.sendMessage(uid,'很抱歉，找不到符合ID的圖片，請檢察您的輸入')
    def ButtonCallback(self, bot, update):
        user_obj = GetUserObj(self.db,update)
        query = update.callback_query
        qdata = query.data
        #print(query)
        uid = update.callback_query.from_user.id
        if qdata.find('$') != -1:
            result = qdata.split('$')[1:]# [id,fid]
            fid = int(result[1])
            for photo in user_obj['photos']:
                if photo['fid'] == fid:
                    photo['tag'] = user_obj['current_tags'].copy()
                    del user_obj['current_tags']
                    del self.creat_button_lock[str(uid)]
                    del self.reply_markup[str(uid)]
                    query.edit_message_text(text='id:{}的圖片已加入Tag:{}'.format(fid,photo['tag']))
        else:
            if qdata in self.db.GetUser(update.callback_query.from_user.id)['current_tags']:
                user_obj['current_tags'].remove(qdata)
            else:
                user_obj['current_tags'].append(qdata)
            query.edit_message_text(text='已選擇標籤(再次點擊可取消): {}'.format(user_obj['current_tags']), reply_markup=self.reply_markup[str(uid)])

# 用來加入圖片
class Photos:
    def __init__(self,db,telegram):
        self.db                 =   db
        self.tg                 =   telegram
    def AddPhoto(self,bot,update):
        user_obj = GetUserObj(self.db,update)
        uid = update.message.from_user.id
        if user_obj['current_mode'] == 'add':
            #print(update.message.from_user.id)
            fid = len(user_obj['photos'])
            user_obj['photos'].append({'photo':update.message.photo[0].file_id,'fid':fid,'tag':[],'date':time.time()})
            bot.sendMessage(uid,'已加入一張圖片，id為:' + str(fid) + '\n接著請輸入該圖片的tag(ex:#Dog#玩球)或是一句符合該圖片的描述句子BOT將把該句子轉換成適合的tag供您選擇')
# 用來處理inline查詢請求(叫出圖片)
class InlineHandler:
    def __init__(self,db,telegram):
        self.db                 =   db
        self.tg                 =   telegram
    def InlineQuery(self, update, context):
        user_obj = GetUserObj(self.db,context)
        query = context.inline_query.query.split(' ')
        results = []
        photo_list = {}
        uid = context.inline_query.from_user.id
        photo_list[str(uid)] = [photo for photo in user_obj['photos'] if list_serach(query,photo['tag'])]
        photo_list[str(uid)].sort(key = get_photo_date,reverse = True)
        for i in range(len(photo_list[str(uid)])):
            results.append(
                InlineQueryResultCachedPhoto(
                    id = uuid4(),
                    photo_file_id = photo_list[str(uid)][i]['photo']
                )
            )
        context.inline_query.answer(results)

# 處理當前模式的切換
class Bot:
    def __init__(self,db,telegram):
        self.db                 =   db
        self.tg                 =   telegram
    def start_command(self,bot,update):
        uid = update.message.from_user.id
        if not self.db.CheckUserExist(uid):
            self.db.AddUser(uid)
        else:
            pass
        bot.sendMessage(uid,'新來的童鞋你好，歡迎使用本Bot，輸入 /add 進入新增模式，此模式下可以加入梗圖，在此模式下傳送給偶的所有圖片都會被加入資料庫，如果想離開這個模式輸入 /cancel 即可\n')
        bot.sendMessage(uid,'如果要修改標籤，輸入 /tag 即可進入標籤修改模式')
        bot.sendMessage(uid,'在聊天欄內輸入 @superpp_bot 後面加上之前加的tag即可選擇所匹配的梗圖喔!多個Tag用空格分開即可')
    def add_mode(self,bot,update):
        GetUserObj(self.db,update)['current_mode'] = 'add'
        update.message.reply_text('已進入新增模式，傳些好料的圖片吧')
    def cancel_mode(self,bot,update):
        GetUserObj(self.db,update)['current_mode'] = 'none'
        update.message.reply_text('離開當前模式')
    def tag_change_command(self,bot,update):
        GetUserObj(self.db,update)['current_mode'] = 'tag'
        update.message.reply_text('已進入Tag修改模式，請輸入 <圖片ID>:<新的Tags>')