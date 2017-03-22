# Message bot using AWS Lambda and Alexa Skills Kit

It is a simple Alexa Skill built with AWS Lambda function and the Alexa SDK. It uses Twilio and SparkPost API to send text and email messages.

## Setup

Alexa Skill Setup:

The following intent schema allows to handle the mobile number or email address of the recipient.

	'''{
      "intent": "textBot",
      "slots": [
        {
          "name": "numberSlot",
          "type": "AMAZON.NUMBER"
        },
        {
          "name": "msgSlot",
          "type": "AMAZON.LITERAL"
        }
      ]
    },
    {
      "intent": "emailBot",
      "slots": [
        {
          "name": "addressSlot",
          "type": "AMAZON.LITERAL"
        },
        {
          "name": "messageSlot",
          "type": "AMAZON.LITERAL"
        }
      ]
    }'''

Here, NUMBER slot type handles any number in words, whereas, LITERAL slot type handles free form text.
In configuration, use the AWS lambda arn:aws:lambda:us-east-1:607231461091:function:askMessageBot

Twilio Account Setup:

- Register in Twilio and buy a number.
- Setup a Messaging Service under Programable SMS service using the number.
- Keep a note of the ACCOUNT-SID and AUTH-TOKEN which will be used for authentication.

SparkPost Account Setup:

- Register in SparkPost and create a sending domain.
- Use the REST api key for authentication to send emails.


AWS Lambda Setup:

- Go to the AWS Console and click on the Lambda link from us-east.
- Click on the Create a Lambda Function or Get Started Now button.
- Skip the blueprint
- Create a Lambda Function such as "askMessageBot"
- Select the runtime as Python 2.7
- Go to the the src directory, select all files in lib/python2.7/site-packages and then create a zip file.
- Upload the zip file to the lambda function where the main function is named as lambda_function and save it.


## Working

Go to the Skills section in Alexa app and search for messageBot to install the skill.
It uses the lambda created at arn:aws:lambda:us-east-1:607231461091:function:askMessageBot

Try some of the interactions recorded:

- help please
- textBot send text to six zero seven three seven two three seven seven zero that alexa is cool
- emailBot send email to vidyasagar dot zero three nine at gmail dot com that it's an email from alexa
- brickhackBot what is brick hack
- vidya who is Sagar
- strangerthings what is Amazon Alexa
- stop thank you