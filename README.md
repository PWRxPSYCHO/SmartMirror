**Version 1.0.0**

# SmartMirror
Raspberrry Pi powered smart mirror inspired by HackerHouseYT Smart Mirror project

Displays News, Google Calendar Feed, Current Weather, 5 Day Weather Forecast, Time, Location, and Date.

**TO-DO:** Make Fullscreen


# Installation and Updating

Download by pressing green button in repo or

If you have [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) installed you can clone the repo:
```
git clone https://github.com/jRosenthal11/SmartMirror.git
```
# Google Calendar Usage
In order to take advantage of the Google Calendar API you will need to go through the setup. I have not figured out how to incorporate and easy API key to the program.

1. Start [here](https://developers.google.com/google-apps/calendar/quickstart/python) this is the quick start guide to get you running
2. Click the Wizard Link and Create a project
3. Create Credentials on API & services page
4. Download the .json files
5. Rename service account key file to `client_secret.json`

Once you have those all setup return back to the [Python Quicksart](https://developers.google.com/google-apps/calendar/quickstart/python) 

Follow along until step 4. Once the web browser opens asking for permission to access your account it worked!
A command prompt window will also appear showing your events.

# Install Your Dependencies
### Currently working on quickstart.py and requirements.txt
Install pip prior to this step

```
sudo pip install -r requirements.txt
```
```
sudo apt-get install python-imaging-tk
```

# Important: Add your API Token

Create a text file and name it `API_Key.txt` and put your API Token from **[DarkSky](https://darksky.net/)** in it.
Then place the text file inside the project folder.

`sudo apt-get install vim` or `sudo apt-get install nano`. You can use `nano` or `vim` to edit the file

```
sudo nano Mirror.py
```
```
vim Mirror.py
```

Open up the project and change the path of the `file_object` to 
``` 
file_object = open("API_KEY.txt")
```
**IF** You get a Json error remove `file_object=open()` line as well as `file_object.close()` and change `weather_api_key` to
`weather_api_key=""` insert your API key in the quotation marks

# Running the Software

To run the application navigate to the project folder and run the following command

```
python3 Mirror.py
```

![Program](Smart_Mirror.png?raw=true "Smart Mirror")
