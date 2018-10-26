import random
import datetime
import re
# ---------------------------------------------------------------------------------
# ---------------------------- Main Handler ----------------------------------------
def lambda_handler(event, context):
    
    if event['request']['type'] == "LaunchRequest" :
        return onLaunch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest" :
        return onIntent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest" :
        return onSessionEnd(event['request'], event['session'])
        
# --------------------------------------------------------------------------------------

def onLaunch(launchRequest, session):
    return welcome()
    

def onIntent(intentRequest, session):
             
    intent = intentRequest['intent']
    intentName = intentRequest['intent']['name']

    if intentName == "spread_smiles":
        return spread_smiles(intent, session)
    elif intentName == "complete_task":
        return complete_task(intent, session)
    elif intentName == "AMAZON.HelpIntent":
        return welcome()
    elif intentName == "AMAZON.CancelIntent" or intentName == "AMAZON.StopIntent":
        return handleSessionEndRequest()
    elif intentName == "AMAZON.FallbackIntent":
        return fallBackIntent()
    else:
        raise ValueError("Invalid intent")
        
        

def onSessionEnd(sessionEndedRequest, session):
    print("on_session_ended requestId=" + sessionEndedRequest['requestId'] + ", sessionId=" + session['sessionId'])
        
    
# ------------------------------------------------------------------------------------------------------------------------
def fallBackIntent():
    sessionAttributes = {}
    cardTitle = "Sorry!"
    speechOutput = "<speak>"\
                    "You have spoken something different from utterances, Please try again!"\
                    "</speak>"
    repromptText = None
    cardOutput = "You have spoken something different from utterances, Please try again!"
    shouldEndSession = False
    return buildResponse(sessionAttributes, buildSpeechletResponse(cardTitle, speechOutput, cardOutput, repromptText, shouldEndSession))
    
def welcome():
    sessionAttributes = {}
    cardTitle = " Hey!! folks "
    speechOutput =  "<speak>"\
                    "Welcome to spread smiles. " \
                    "<audio src='https://s3.amazonaws.com/ask-soundlibrary/human/amzn_sfx_crowd_applause_03.mp3'/>I will give you a simple task every day. It will make the other person smile " \
                    "and so as you.<break/>  I hope you will do it. "\
                    " You can ask me a new task to do by saying.<break/> " \
                    " Tell me a task "\
                    "</speak>"
    repromptText =  "You can ask me a new task to do by saying.  " \
                    "Tell me the task of the day."
    cardOutput = "Welcome to spread smiles. " \
                "I will give you a simple task every day. It will make the other person smile " \
                "and so as you. I hope you will do it. "\
                " You can ask me a new task to do by saying." \
                " Tell me a task. "                
    shouldEndSession = False
    
    return buildResponse(sessionAttributes, buildSpeechletResponse(cardTitle, speechOutput, cardOutput, repromptText, shouldEndSession))
    

def spread_smiles(intent, session):

    today = datetime.datetime.now()
    task = [i for i in tasklist if i[1] == int(today.strftime("%d"))]

    cardTitle = "Spread smiles"
    sessionAttributes = {}
    shouldEndSession = True
    speechOutput = "<speak>"\
                   "Today's task.<audio src='https://s3.amazonaws.com/ask-soundlibrary/musical/amzn_sfx_drum_comedy_01.mp3'/> " + task[0][0] 
    repromptText = "You can ask me a new task to do by saying, " \
                    "Tell me a new Task"
    cardOutput = re.sub('<[^>]*>', '', speechOutput)                   
    return buildResponse(sessionAttributes, buildSpeechletResponse(cardTitle, speechOutput, cardOutput, repromptText, shouldEndSession))

def complete_task(intent, session):
    complete_message = ["<speak>"\
                        "Congratulations,<audio src='https://s3.amazonaws.com/ask-soundlibrary/human/amzn_sfx_crowd_applause_03.mp3'/> you make someone smile. Thank you for trying spread smiles Alexa Skill."\
                        "</speak>",
                        "<speak>"\
                        "woa!<audio src='https://s3.amazonaws.com/ask-soundlibrary/human/amzn_sfx_crowd_applause_03.mp3'/> thats really great. Thank you for trying spread smiles Alexa Skill."\
                        "</speak>",
                        "<speak>"\
                        "Oh thats really nice.<audio src='https://s3.amazonaws.com/ask-soundlibrary/human/amzn_sfx_crowd_applause_03.mp3'/> Thank you for trying spread smiles Alexa Skill."\
                        "</speak>",
                        "<speak>"\
                        "Now,you even make me smile.<audio src='https://s3.amazonaws.com/ask-soundlibrary/human/amzn_sfx_crowd_applause_03.mp3'/> Thank you for trying spread smiles Alexa Skill. keep spreading smiles"\
                        "</speak>",
                        "<speak>"\
                        "I hope it makes you feel better.<audio src='https://s3.amazonaws.com/ask-soundlibrary/human/amzn_sfx_crowd_applause_03.mp3'/> Thank you for trying spread smiles Alexa Skill."\
                        "</speak>"]
    cardTitle = "Keep spreading smiles"
    sessionAttributes = {}
    shouldEndSession = True
    speechOutput = random.choice(complete_message)
                   
    cardOutput = re.sub('<[^>]*>', '', speechOutput) + "Thank you for trying spread smiles Alexa Skill. Keep spreading smiles. " \
                    "Have a nice day!"                  
    return buildResponse(sessionAttributes, buildSpeechletResponse(cardTitle, speechOutput, cardOutput, None, shouldEndSession))



def handleSessionEndRequest():
    cardTitle = "Good bye!"
    speechOutput = "<speak>"\
                    "Thank you for trying spread smiles Alexa Skill.<audio src='https://s3.amazonaws.com/ask-soundlibrary/human/amzn_sfx_crowd_applause_03.mp3'/> Keep spreading smiles. " \
                    "Have a nice day!"\
                    "</speak>"
    shouldEndSession = True
    cardOutput = "Thank you for trying spread smiles Alexa Skill. Keep spreading smiles. " \
                    "Have a nice day!"
    return buildResponse({}, buildSpeechletResponse(cardTitle, speechOutput, cardOutput, None, shouldEndSession))    

# ------------------------------------------------------------------------------

def buildSpeechletResponse(title, output,cardOutput, repromptTxt, endSession):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': output
            },
            
        'card': {
            'type': 'Simple',
            'title': title,
            'content': cardOutput
            },
            
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': repromptTxt
                }
            },
        'shouldEndSession': endSession
    }


def buildResponse(sessionAttr , speechlet):
    return {
        'version': '1.0',
        'sessionAttributes': sessionAttr,
        'response': speechlet
    }


    
#----------------------------------------------------------------------------------------------------------------------------------------
tasklist=[["Can you think of two persons who helped you some how. Say thanks to them. and yes you may have already thanked them. But it may make them smile that you still remember. good luck!"\
          "</speak>",1],
          ["Look for variety of locations where you can donate your goods like books, toys, clothes etc. <break/>Go<emphasis level='moderate'> and donate.</emphasis> "\
          "</speak>",2],
          ["If you don’t live with your folks anymore, snap a picture of yourself with your phone and send it to them just to show them that you’re doing well and that you love them."\
          "</speak>",3],
          ["If you have a maid at your home, ask your mother to give her sanitary napkins along with her salary."\
          "</speak>",4],
          ["Compliment your friends and thank them for being by your side. it may seem funny to you but this can make someone smile. Go for it."\
          "</speak>",5],
          ["Take an oath to contribute towards our environment by saying, I will not throw waste on the roads or in the river and ask your friends also. I hope you will do it."\
          "</speak>",6],
          ['please give chocolates to the person you love. <amazon:effect name="whispered">Hey! this person can be anyone.</amazon:effect>'\
          "</speak>",7],
          ["Think of a friend or a family member you haven't caught up with in awhile. call him or go and hang out with him."\
          "</speak>",8],
          ["feed a stray animal. it's good to do once in awhile."\
          "</speak>",9],
          ["Thank cashiers and service people by using the name on their name-tag. they will feel recognized and understood"\
          "</speak>",10],
          ["leave Surprise Notes for your friends or family member. Surprise notes can really be anything, like a simple <break/> <emphasis level='strong'> have a great day!</emphasis>"\
          "</speak>",12],
          ["Find a new recipe and cook it for your family or friends. it will definitly make them smile. i hope you can atleast prepare instant noodles. it doesnt matter what you cook. it's all about your feelings."\
          "</speak>",11],
          ["Make a list of ten things you absolutely love about yourself.<emphasis level='reduced'> Brag away! </emphasis>  It’s not like you have to show it to anyone."\
          "</speak>",13],
          ["Pick up litter and toss it in the trash. if someone throw their empty bag of chips on the ground? Just pick it up. Throw it away. You’re a superhero, remember?"\
          "</speak>",14],
          ["Could you please give some time from your busy social media life to your grand parents or your elder. Go,sit and talk with them about their life and about their health. They may not be here with you but you can call them. good luck."\
          "</speak>",15],
          ["give your old clothes to the person, who really need them. "\
          "</speak>",16],
          ["Pick a section of your house and clean it. Pick something smaller, like your desk or kitchen, and get to work! i think it will definitely make your mother smile."\
          "</speak>",17],
          ["Hug someone in your family for no reason."\
          "</speak>",18],
          ["Let someone know you miss them. it might make you and him smile."\
          "</speak>",19],
          ["if you find an elderly person holding heavy bags, then ask him to help. It makes you feel better "\
          "</speak>",20],
          ["Please donate blood, if you are fit and healthy."\
          "</speak>",21],
          ["If the ambulance approaches you, slowly start moving your car on your left lane or either stop. And ask others to do the same"\
          "</speak>",22],
          ["Offer your seat to more needy person, while travelling by public transport."\
          "</speak>",23],
          ["Tell someone which quality you like most about them."\
          "</speak>",24],
          ["donate sanitary napkins to some girl-care home."\
          "</speak>",25],
          ["While you are in a car, ask everyone to buckle up, because they are important to you."\
          "</speak>",26],
          ["Bring the person a cup of tea or coffee. If you're in the same house, brew a fresh cup, and if you're out, bring in a nice, cafe-made beverage"\
          "</speak>",27],
          ["Share an old photo with a person. Dig up the funniest, silliest, or just the most ridiculous photo and share it with that person when he or she least expects it. "\
          "</speak>",28],
          ["Be a mentor or coach to someone. May be someone waiting for your help."\
          "</speak>",29],
          ["Thank your parents for being the parents they tried hard to be, and spend time with them. Go for it."\
          "</speak>",30],
          ["Ask someone if they need you to pick up anything while you’re out shopping."\
          "</speak>",31]]
