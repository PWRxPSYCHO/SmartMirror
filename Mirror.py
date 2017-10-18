from __future__ import print_function
import time
from tkinter import *
import tkinter.font
from forecastiopy import *
import json
import datetime
import requests
import feedparser
import traceback
from PIL import ImageTk, Image
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# Text size
x_large_text_size = 94
large_text_size = 48
medium_text_size = 28
small_text_size = 18
x_small_text_size = 14


# tk objects
root = Tk()
root.title('Smart Mirror')
root.configure(background='black')
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Frames
frame_top = Frame(root, background='black')
frame_bottom = Frame(root, background='black')

frame_t_left = Frame(frame_top, background='black')
frame_calendar_image = Frame(frame_t_left, background='black')
frame_calendar = Frame(frame_t_left, background='black')

frame_t_right = Frame(frame_top, background='black')

frame_b_left = Frame(frame_bottom, background='black')
frame_news = Frame(frame_b_left, background='black')
frame_newspaper = Frame(frame_b_left, background='black')

frame_b_right = Frame(frame_bottom, background='black')

root.geometry('{}x{}'.format(screen_width, screen_height))


# Fonts
font_time = tkinter.font.Font(family='Helvetica', size=x_large_text_size)
font_date = tkinter.font.Font(family='Helvetica', size=medium_text_size)
font_location = tkinter.font.Font(family='Helvetica', size=medium_text_size)
font_temperature = tkinter.font.Font(family='Helvetica', size=x_large_text_size)
font_quote = tkinter.font.Font(family='Helvetica', size=medium_text_size)
font_holiday = tkinter.font.Font(family='Helvetica', size=small_text_size)
font_weather = tkinter.font.Font(family='Helvetica', size=small_text_size)
font_news = tkinter.font.Font(family='Helvetica', size=x_small_text_size)
font_news_headlines = tkinter.font.Font(family='Helvetica', size=medium_text_size)

# Weather
weather_api_key = ''
# latitude = 40.9393  # North +, South -, East +, West -
# longitude = -75.4349  # North +, South -, East +, West -
units = ForecastIO.ForecastIO.UNITS_US
lang = ForecastIO.ForecastIO.LANG_ENGLISH
time_format = '%I:%M'
date_format = '%A, %B %d, %Y'

# News
county_code = 'us'
google_news_url = "https://news.google.com/news?ned=us&output=rss"

# Calendar
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


# Asset images with launch word
weatherIcons = {"cloudy": 'assets/Cloud.png',
                "hail": 'assets/Hail.png',
                "fog": 'assets/Haze.png',
                "clear-night": 'assets/Moon.png',
                "partly-cloudy-night": 'assets/PartlyMoon.png',
                "partly-cloudy-day": 'assets/PartlySunny.png',
                "rain": 'assets/Rain.png',
                "snow-thin": 'assets/Snow.png',
                "storm": 'assets/Storm.png',
                "clear-day": 'assets/Sun.png',
                "sunrise": 'assets/Sunrise.png',
                "tornado": 'assets/Tornado.png',
                "wind": 'assets/Wind.png'
                }
weekly_data = []

# Images
image = Image.open("assets/Newspaper.png")
image = image.resize((25, 25), Image.ANTIALIAS)
image = image.convert('RGB')
photo = ImageTk.PhotoImage(image)

image_calendar = Image.open("assets/Calendar.png")
image_calendar = image_calendar.resize((25, 25), Image.ANTIALIAS)
image_calendar = image_calendar.convert('RGB')
photo_calendar = ImageTk.PhotoImage(image_calendar)


# Labels
weather_image_lg = Label(frame_t_right, bg='black', fg='white')


label_news_title = Label(frame_b_left, font=font_news_headlines,
                         text="Headlines",
                         bg='black',
                         fg='white')

label_date = Label(frame_t_left, font=font_date,
                   bg='black',
                   fg='white')
label_clock = Label(frame_t_left, font=font_time,
                    bg='black',
                    fg='white')
label_temperature = Label(frame_t_right, font=font_temperature,
                          bg='black',
                          fg='white')
label_location = Label(frame_t_right, font=font_location,
                       bg='black',
                       fg='white')

# Layout Top Left
label_date.pack(side=TOP, anchor=W)
label_clock.pack(side=TOP, anchor=W)

# Layout Top Right
label_location.pack(side=TOP, anchor=E)
weather_image_lg.pack(side=LEFT, anchor=E)
label_temperature.pack(side=TOP, anchor=E)


# Layout Bottom Left
label_news_title.pack(side=TOP, anchor=W)


# Clock function
def tick():
    s = time.strftime(time_format)
    d = time.strftime(date_format)
    if s != label_clock["text"]:
        label_clock["text"] = s
        print("Time:", s)
    if d != label_date["text"]:
        label_date["text"] = d
        print('Date:', d)
    label_clock.after(200, tick)


# Displays Location name and weather data for location
def current_weather():
    # Location request
    location_req_url = "http://freegeoip.net/json/%s" % get_ip()
    r = requests.get(location_req_url)
    location_obj = json.loads(r.text)
    latitude = location_obj['latitude']
    longitude = location_obj['longitude']
    weather_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (weather_api_key, latitude, longitude,
                                                                                  lang, units)
    location = "%s, %s" % (location_obj['city'], location_obj['region_code'])

    # Sets Weather Object
    r = requests.get(weather_url)
    weather_obj = json.loads(r.text)

    fahrenheit = int(weather_obj['currently']['temperature'])
    icon_id = weather_obj['currently']['icon']
    print('Icon ID: ', icon_id)

    if icon_id in weatherIcons and weather_image_lg['image'] != icon_id:
        icon2 = weatherIcons[icon_id]
        w_icon = Image.open(icon2)
        w_icon = w_icon.resize((100, 100), Image.ANTIALIAS)
        w_icon = w_icon.convert('RGB')
        w_photo = ImageTk.PhotoImage(w_icon)

        weather_image_lg.configure(image=w_photo)
        weather_image_lg.icon = w_photo

    format(fahrenheit, '.0f')
    if fahrenheit != label_temperature["text"]:
        label_temperature["text"] = format(fahrenheit, '.0f') + "°"
        print("Temperature:", fahrenheit)
    print('Summary:', weather_obj['currently']['summary'])

    if location != label_location['text']:
        label_location['text'] = location

    label_temperature.after(600000, current_weather)
    weather_image_lg.after(600000, current_weather)
    label_location.after(600000, current_weather)


def get_news():

    for widget in frame_news.winfo_children():
        widget.destroy()
    for i in frame_newspaper.winfo_children():
        i.destroy()
    try:
        feed = feedparser.parse(google_news_url)

        for post in feed.entries[0:5]:
            newspaper_image = Label(frame_newspaper, bg='black', fg='white')
            newspaper_image.configure(image=photo)
            newspaper_image.icon = photo

            label_news = Label(frame_news, bg='black', fg='white', font=font_news)
            label_news['text'] = post['title']
            newspaper_image.pack(side=TOP, anchor=W)
            label_news.pack(side=TOP, anchor=W)
        frame_news.after(600000, get_news)

    except Exception as e:
        traceback.print_exc()
        print("Error: %s. Cannot get news." % e)


def get_ip():
    try:
        ip_url = "http://jsonip.com/"
        req = requests.get(ip_url)
        ip_json = json.loads(req.text)
        return ip_json['ip']
    except Exception as e:
        traceback.print_exc()
        return "Error: %s. Cannot get ip. " % e

# Reference https://developers.google.com/google-apps/calendar/quickstart/python


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def get_calendar():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    for widget in frame_calendar.winfo_children():
        widget.destroy()
    for i in frame_calendar_image.winfo_children():
        i.destroy()
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events[0:5]:
        label_calender_image = Label(frame_calendar_image, bg='black', fg='white')
        label_calender = Label(frame_calendar, font=font_news, bg='black', fg='white')

        label_calender_image.configure(image=photo_calendar)
        label_calender_image.icon = photo_calendar

        start = event['start'].get('dateTime', event['start'].get('date'))

        # TO-DO put in if to check length of test_split

        label_calender['text'] = event['summary'] + ' ' + start
        label_calender.pack(side=TOP, anchor=W)
        label_calender_image.pack(side=TOP, anchor=W)
    label_calender.after(600000, get_calendar)


tick()
get_ip()
current_weather()
get_news()
get_calendar()

frame_t_left.pack(side=LEFT, anchor=N, padx=40, pady=40)
frame_calendar.pack(side=RIGHT, anchor=N)
frame_calendar_image.pack(side=LEFT, anchor=N)
frame_t_right.pack(side=RIGHT, anchor=N, padx=40, pady=40)
frame_b_left.pack(side=BOTTOM, anchor=W, padx=40, pady=40)
frame_news.pack(side=RIGHT, anchor=W)
frame_newspaper.pack(side=LEFT, anchor=W)
frame_top.pack(expand=TRUE, fill=BOTH, side=TOP)
frame_bottom.pack(expand=TRUE, fill=BOTH, side=BOTTOM)
root.mainloop()