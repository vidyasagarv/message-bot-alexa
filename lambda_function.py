from __future__ import print_function
from twilio.rest import TwilioRestClient
import wikipedia
# Import SparkPost for sending emails
from sparkpost import SparkPost

TWILIO_APPLICATION_ID="amzn1.ask.skill.def0feb0-5895-4396-ac80-d87ff1281cef"
# Account details for Twilio API to send text or message
ACCOUNT_SID = "AC3c2433c398c991ba434be345fc20a119"
AUTH_TOKEN = "138ad8a26744f7c96f1cef48759a539d"
TWILIO_NUMBER = "+16072501055"

contacts = {"vidya's contact": "vidyasagar.039@gmail.com",
                    "sagar's contact": "vvallur1@binghamton.edu",
                    "pradeep's contact": "puppula1@binghamton.edu",
                    "vaibhav's contact": "vkollip1@binghamton.edu",
                    "jack's contact": "jack.sparo435@gmail.com"}

def lambda_handler(event, context):

    session_attributes = {}

    applicationId = event['session']['application']['applicationId']
    if applicationId != TWILIO_APPLICATION_ID:
        should_end_session = True
        bad_request_output = "Bad Request"
        print("Bad ApplicationId Received: "+applicationId)
        return build_response(session_attributes, build_speech_resp("Twilio", bad_request_output, None, should_end_session))

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'])

def on_launch(launch_request):
    """ Called when the user launches the skill without specifying what they
    want
    """
    print("on_launch requestId=" + launch_request['requestId'])

    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request):
    """ Called when the user specifies an intent for this skill """
    print("on_intent requestId=" + intent_request['requestId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers

    if intent_name == "textBot":
        return textIntentHandler(intent)

    elif intent_name == "emailBot":
        return emailIntentHandler(intent)

    elif intent_name == "brickhackBot":
        return brickhackIntentHandler(intent)

    elif intent_name == "vidya":
        return vidyaIntentHandler(intent)

    elif intent_name == "pradeep":
        return pradeepIntentHandler(intent)

    elif intent_name == "vaibhav":
        return vaibhavIntentHandler(intent)

    elif intent_name == "strangerthings":
        return strangerIntentHandler(intent)

    elif intent_name == "help":
        return helpIntentHandler(intent)

    elif intent_name == "stop":
        return stopIntentHandler(intent)

    else:
        return misunderstoodHandler(intent)

# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    session_attributes = {}
    card_title = "Welcome"

    speech_output = "Hey welcome to Brick Hack.  " \
                    "I am Ritchie the tiger... Tell me what can I do for you? Ask help for more instructions."

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "sorry... could you repeat that for me?"

    should_end_session = False
    return build_response(session_attributes, build_speech_resp(
        card_title, speech_output, reprompt_text, should_end_session))

def brickhackIntentHandler(intent):
    card_title = "BrickHack"

    speech_output = "BrickHack is RIT's collegiate hackathon the place for hackers and it is at RIT, Rochester"

    return build_response(None, build_speech_resp(
        card_title, speech_output, None, False))

def vidyaIntentHandler(intent):
    card_title = "Vidya"

    speech_output = "He is an awesome hacker"

    return build_response(None, build_speech_resp(
        card_title, speech_output, None, False))

def pradeepIntentHandler(intent):
    card_title = "Pradeep"

    speech_output = "He is a true hacker"

    return build_response(None, build_speech_resp(
        card_title, speech_output, None, False))

def vaibhavIntentHandler(intent):
    card_title = "Vaibhav"

    speech_output = "He hacked a hacker"

    return build_response(None, build_speech_resp(
        card_title, speech_output, None, False))

def emailIntentHandler(intent):
    card_title = "Email"
    speech_output = ""

    try:
        emailId = ""
        messageContent = ""
        contactList = []

        slots = intent['slots']

        contactName = slots['contactSlot']['value']

        if contactName == "every contact":
            for contact in contacts:
                contactList.append(contacts[contact])
        else:
            emailId = contacts[contactName]
            contactList.append(emailId)

        messageContent = slots['messageSlot']['value']

        # call the method to send email
        if(sendEmail(to_addr= contactList, msg_text=messageContent)):
            #success
            speech_output = "Email sent"
        else:
            #failure
            speech_output = "Sorry could not sent the email... I will ask the support guys to fix the issue"
    except Exception:
        speech_output = "too much noise.... Sorry didn't get the details... please try again"

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(None, build_speech_resp(
        card_title, speech_output, None, False))

def sendEmail(to_addr, msg_text):
    sp = SparkPost('d87d06871e91927042aaa2a68bfd8cedc54275fa')

    response = sp.transmissions.send(
        recipients= list(to_addr),
        html='<p>'+msg_text+'</p>',
        from_email='vidyasagar@vidyasagarvalluri.com',
        subject='Hello from alexa - sparkpost'
    )
    if response["total_accepted_recipients"] > 0:
        return True
    else:
        return False

def textIntentHandler(intent):
    card_title = "Text"
    speech_output = ""

    try:
        mobileNumber = ""
        messageText = ""

        slots = intent['slots']

        mobileNumber = slots['numberSlot']['value']

        messageText = slots['msgSlot']['value']

        # call the method to send text
        if(sendText(to_num=mobileNumber,msg_text=messageText)):
            #success
            speech_output = "Message sent"
        else:
            #failure
            speech_output = "Sorry could not sent the message... Check the email address and try again"
    except Exception:
        speech_output = "too much noise.... Sorry didn't get the details... please try again"

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(None, build_speech_resp(
        card_title, speech_output, None, False))

def sendText(to_num, msg_text="Hey folks have a great Brick Hack", from_num=TWILIO_NUMBER):
    try:
        client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
        client.messages.create(
            to=to_num,
            from_=from_num,
            body=msg_text
            )
        return True
    except Exception as e:
        print("Failed to send message: ")
        print(e.code)
        print("Message: ")
        print(e.msg)
        return False

def strangerIntentHandler(intent):
    card_title = "Strangerthings"

    print(intent['slots'])

    slots = intent['slots']

    try:
        result = wikipedia.summary(slots['unknownSlot']['value'],sentences=1)

        speech_output = "All I know from Wikipedia is " + result
    except Exception as e:
        print(e)
        speech_output = "Oops something went wrong."

    return build_response(None, build_speech_resp(
        card_title, speech_output, None, False))

def misunderstoodHandler(intent):
    card_title = "Misunderstood"

    speech_output = "Sorry didn't get that... please try again"

    return build_response(None, build_speech_resp(
        card_title, speech_output, None, True))

def helpIntentHandler(intent):
    card_title = "Help"

    speech_output = "You can ask me about brickhack or an unknown thing or I can send a text or an email for you, thanks to SparkPost."

    return build_response(None, build_speech_resp(
        card_title, speech_output, None, False))

def stopIntentHandler(intent):
    card_title = "Stop"

    speech_output = "Goodbye feel free to call me again"

    return build_response(None, build_speech_resp(
        card_title, speech_output, None, True))

# --------------- Helpers that build all of the responses ----------------------


def build_speech_resp(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speech_resp):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speech_resp
    }
