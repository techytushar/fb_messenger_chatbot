from fbchat import Client,log
from fbchat.models import *
import json,apiai
import credentials as cred

#extending the class Client imported from fbchat
class techytushar(Client):
    #apiai method for setting up connection and getting the reply.
    def apiai(self):
        self.ClientAccessToken = 'dialogflow api'
        self.ai = apiai.ApiAI(self.ClientAccessToken)
        self.request = self.ai.text_request()
        self.request.lang = 'de'
        self.request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"

    #modifying pre defined method onMessage, where author_id is the sender id, thread_id is the id of the chatbox or the
    #  thread and thread_type is weather its personal chat or group chat.
    def onMessage(self, author_id=None, message=None,thread_id=None, thread_type=ThreadType.USER, **kwargs):
        #marking the message as read
        self.markAsRead(author_id)
        #printing to terminal as a message is received.
        log.info("Message {} from {} in {}".format(message,thread_id,thread_type.name))
        #printing message text
        print("The received message - ",message)
        try:
            #setting up connection with apiai
            self.apiai()
            #sending the query (message received)
            self.request.query = message
            #getting the json response
            api_response = self.request.getresponse()
            json_reply = api_response.read()
            #decoding to utf-8 (converting byte object to json format)
            decoded_data = json_reply.decode("utf-8")
            #loading it into json
            response = json.loads(decoded_data)
            #taking out the reply from json
            reply = response['result']['fulfillment']['speech']
        except Exception as e:
            print(e)
            reply = "sorry, techytushar is not available."

        #if we are not the sender of the message
        if author_id!=self.uid:
            #sending the message.
            self.sendMessage(reply, thread_id = thread_id, thread_type = thread_type)

        self.markAsDelivered(author_id,thread_id)

print(cred.email,cred.password)
#logging into facebook.(importing email and password from credentials file.)
client = techytushar(cred.email,cred.password)
#listen for incoming message
client.listen()