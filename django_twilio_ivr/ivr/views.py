from twilio.twiml.voice_response import VoiceResponse
from django.http import HttpResponse


def init_automated_call(request):
    """ initial end point called by twilio on making a phone call to your twilio number"""
    response = VoiceResponse()
    voice_message = 'Welcome to tiptapcode Press one to hear a monkey, two to receive an SMS'

    with response.gather(action='/respond/', num_digits=1) as g:
        g.say(voice_message)
        g.pause(length=1)

    # if user does not response with an option
    # call your http://{domain}/gather end point again to repeat options
    response.redirect('/gather/')

    # HttResponse will return xml response object for twilio api to process
    return HttpResponse(str(response), content_type='application/xml')


def handle_user_response(request):
    """ response handler function"""

    # twilio passes key pressed digits via form-data form key value Digits
    digits = request.POST.get('Digits', '')
    response = VoiceResponse()

    # evaluate user input from phones keypad and take an appropriate action
    if digits == '1':
        response.play('http://demo.twilio.com/hellomonkey/monkey.mp3')
    if digits == '2':
        number = request.POST.get('From', '')
        response.say('Thank you for calling, for more content see site blog')
        response.sms('Thanks for trying out this tutorial, share with your friends!', to=number)

    # HttResponse will return xml response object for twilio api to process
    return HttpResponse(str(response), content_type='application/xml')
