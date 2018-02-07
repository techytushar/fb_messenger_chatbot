from fbchat import Client,log
from fbchat.models import *
import json,requests
import credentials as cred

#extending the class Client imported from fbchat
class techytushar(Client):
    
    def onMessage(self, author_id=None, message=None,thread_id=None, thread_type=ThreadType.USER, **kwargs):
        #marking the message as read
        self.markAsRead(author_id)
        #printing to terminal as a message is received.
        log.info("Message {} from {} in {}".format(message,thread_id,thread_type.name))
        #printing message text
        print("The received message - ",message)
        #if we are not the sender of the message
        if author_id!=self.uid:
            #sending the message.
            reply = cleverbot_reply(message)
            print("Chatbot reply - ",reply)
            self.sendMessage(reply, thread_id = thread_id, thread_type = thread_type)

        self.markAsDelivered(author_id,thread_id)

def cleverbot_make():
        body = {"user":cred.cleverbot_user,"key":cred.cleverbot_key}
        r = requests.post('https://cleverbot.io/1.0/create', json=body)
        r = json.loads(r.text)
        if(r["status"]!="success"):
            print("Error creating the bot. Please check the internet connection.")
        else:
            print("Chatbot created successfully!!")

def cleverbot_reply(text):
        body = {"user":cred.cleverbot_user,"key":cred.cleverbot_key}
        try:
            body["text"] = text
            reply = requests.post('https://cleverbot.io/1.0/ask', json=body)
            reply = json.loads(reply.text)
            reply = reply['response']
            return reply
        except Exception as e:
            print("Error occured while getting reply from chatbot.",e)
            return("Sorry, techytushar is not available.")
        
if __name__ == "__main__":
    cleverbot_make()
    #logging into facebook.(importing email and password from credentials file.)
    client = techytushar(cred.email,cred.password)
    #listen for incoming message
    client.listen()