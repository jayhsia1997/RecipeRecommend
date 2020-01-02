from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser,WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, ImageMessage ,TextMessage, PostbackEvent,TextSendMessage ,ImageSendMessage


from module import run_1 ,run_2 ,run_3 ,send_3 ,send_Images_pro ,send_Text_pro #Func檔案名稱改這邊也要改

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)



def error_cb(err):
    print('Error: %s' % err)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    mtext = event.message.text
                    ########################################   這邊判斷到是 文字 ######################################
                    if mtext == '@傳送文字':
                        #下面這行 測試用到時候，到時候要換成 function
                        send_Text_pro.sendText(event)
                        #下面這行留著
                        return HttpResponse()

                    elif mtext == '@傳送圖片':
                        send_Images_pro.sendImage(event)
                        return HttpResponse()

                    elif mtext == '@按鈕樣板':
                        send_3.sendButton(event)
                        return HttpResponse()


                    elif mtext == '@確認樣板':
                        run_3.sendQuickreply(event)
                        return HttpResponse()


                    elif mtext == '@轉盤位置':
                        run_2.sendConfirm(event)
                        return HttpResponse()


                    elif mtext == '@快速選單':
                        run_1.sendCarousel(event)
                        return HttpResponse()


                elif isinstance(event.message,ImageMessage):
                    #########################################  這邊判斷到是照片 ###########################################

                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text='你傳送到照片了'))
                    return HttpResponse()

                    #message_content = line_bot_api.get_message_content(event.message.id)

                    # user_id = event.message.id
                    # user_id = str(user_id) + str(random.randrange(10 ,99))
                    # with open('E:/db104_2_project/static/{}.jpg' .format(user_id),'wb')as fd:
                    #     for chunk in message_content.iter_content():
                    #         fd.write(chunk)
                    #temp_pic = 'E:/db104_2_project/static/{}.jpg'.format(user_id)




                else:
                    ######################################### 不三不四 表情區 #######################################
                    ################################   這邊判斷到 文字 或 圖片外的東西 #########################################
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text='你傳了到圖片了'))
                    return HttpResponse()

            print("到文字、圖片或不三不四的表情區塊後，會跑到這，如果拿掉下面那行，會跑到 下面的 第三禁區 ")
            return HttpResponse()

        print("第三禁區")
        return HttpResponse()

    else:
        print("第四禁區")
        return HttpResponseBadRequest()























# def callback(request):
#     if request.method == 'POST':
#         signature = request.META['HTTP_X_LINE_SIGNATURE']
#         body = request.body.decode('utf-8')
#         try:
#             events = parser.parse(body, signature)
#         except InvalidSignatureError:
#             return HttpResponseForbidden()
#         except LineBotApiError:
#             return HttpResponseBadRequest()
#
#         for event in events:
#             if isinstance(event, MessageEvent):
#                 if isinstance(event.message, TextMessage):
#                     mtext = event.message.text
#
#                     if mtext == '@傳送文字':
#                         line_bot_api.reply_message(event.reply_token, TextSendMessage(text='傳送文字'))
#                         return HttpResponse()
#
#                     elif mtext == '@按鈕樣板':
#                         line_bot_api.reply_message(event.reply_token, sendButton(text='按鈕樣板'))
#                         return HttpResponse()
#
#
#                     elif mtext == '@確認樣板':
#                         line_bot_api.reply_message(event.reply_token, sendConfirm(text='確認樣板'))
#                         return HttpResponse()
#
#
#                     elif mtext == '@轉盤樣板':
#                         line_bot_api.reply_message(event.reply_token, sendCarousel(text='轉盤樣板'))
#                         return HttpResponse()
#
#                     elif mtext == '@傳送圖片':
#                         line_bot_api.reply_message(event.reply_token, sendImage(text='傳送圖片'))
#                         return HttpResponse()
#
#                     elif mtext == '@快速選單':
#                         line_bot_api.reply_message(event.reply_token, sendQuickreply(text='快速選單'))
#                         return HttpResponse()
#
#                 if isinstance(event, PostbackEvent):  # PostbackTemplateAction觸發此事件
#
#                     backdata = dict(parse_qsl(event.postback.data))  # 取得Postback資料
#
#                     if backdata.get('action') == 'buy':
#
#                         func.sendBack_buy(event, backdata)
#
#                     elif backdata.get('action') == 'sell':
#
#                         func.sendBack_sell(event, backdata)
#
#                 return HttpResponse()
#
#             else:
#
#                 return HttpResponseBadRequest()
