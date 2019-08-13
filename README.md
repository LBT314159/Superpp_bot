刷梗圖機器人
===

# 動機

隨著資訊科技日新月異，我們的溝通方式也漸漸從對話演變至通訊，更從句子的傳遞，變成了有圖片為輔助的更加深動活潑形態。為此我們想要收集大家廣爲使用的--梗圖--，製作成一個蒐集處理器，能夠更加方便地在茫茫圖海中找到想輸送的圖片，因此，這個bot誕生了。

# 介紹

梗圖機器人能讓使用者爲圖片標上標籤(tag),並能在日常聊天中叫出bot並送出圖片,讓使用者更加方便聊天(or嗆聲)
# 安裝依賴套件
請確保您的Python3環境具備以下套件:
* [Pytorch](https://pytorch.org/)
    > 請自行前往官網選擇適當版本安裝
* [Requests:](https://pypi.org/project/requests/)
    > pip install requests
* [Monpa:](https://github.com/monpa-team/monpa)
    > pip install monpa
* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
    > pip install python-telegram-bot
# 使用流程:
### 開始使用
輸入 /start Bot將會為您介紹使用方式
### 上傳圖片
先輸入 /add
1. 傳送一張圖片
2. 傳一個描述梗圖文字
    > ex: 黑人玩踩地雷
3. 生成一些按鈕讓使用者選擇
    > ex:【黑人】【玩】【踩地雷】
4. 使用者選擇完畢後按下確認送出

或者:
1. 傳送一張圖片
2. 傳送Tags
    > ex:#黑人#踩地雷

### 傳送梗圖:
1. 在對話方塊輸入Bot名稱
    > ex:@superpp_bot
2. 在Bot名稱後以空格分開tags，Bot將為您把匹配Tag的圖片列出來供您選擇
