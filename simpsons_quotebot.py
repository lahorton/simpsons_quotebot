import schedule
import requests
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import os

account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)


def get_quote():
    r = requests.get("https://frinkiac.com/api/random")
    if r.status_code == 200:
        json = r.json()
        
        timestamp, episode, _ = map(str, json["Frame"].values())
        
        caption = "\n".join([subtitle["Content"] for subtitle in json["Subtitles"]])
        return caption


def send_MMS():
    body = get_quote()
    print(body)
    try:
        message = client.messages \
            .create(
                to="+13132589798",
                from_="+12486218673",
                body=body
                #media_url=media
            )
        print("Message sent!")
    except TwilioRestException as e:
        print(e)

schedule.every(60).seconds.do(send_MMS)

while True:
    schedule.run_pending()

