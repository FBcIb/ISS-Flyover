import requests
import json
import datetime
import pprint
import webbrowser 

areacode = str(input('Please enter your area code: '))

# Request LocationKey
url = 'http://dataservice.accuweather.com/locations/v1/postalcodes/US/search?apikey=cJ4IMgmH4SHCATdJzUdsTZN926aUAHFu&q=' + areacode + 'language=en-us&details=false' 
t = requests.get(url)
lockey = t.json()[0]['Key']

# Your lat&long in decimal form - from AccuWeather API
loc = { 
    "lat": t.json()[0]['GeoPosition']['Latitude'],
    "lon": t.json()[0]['GeoPosition']['Longitude'],
    'n': 10   # Number of flyovers to be fetched
}

# Use LocKey to find Weather conditions
weather = 'http://dataservice.accuweather.com/forecasts/v1/daily/1day/' + lockey + '?apikey=cJ4IMgmH4SHCATdJzUdsTZN926aUAHFu&metric=false' 
w = requests.get(weather)

iss_pass = requests.get('http://api.open-notify.org/iss-pass.json', params = loc) # Gives time of next ISS flyover
fo_times = iss_pass.json()['response'] # Extract the flyover times from the json

# Create an array of risetimes for given flyovers
risetimes = []
for d in fo_times:  
    time = d['risetime']
    time = datetime.datetime.fromtimestamp(time) # Convert time into datetime object
    risetimes.append(time.strftime('%m/%d/%Y - %H:%M:%S')) # Format above object into Month-Day-Year Time 

# Create array of hours during sundown - Easily adjusted for seasonal changes
vishours = [] 
for i in range(7):
    vishours.append(i)
for i in range(17,25):
    vishours.append(i)

# Sort for flyovers occurring during visible hours
vis_fo = []
for p in risetimes: 
    hour = int(p[13:15])
    if hour in vishours:
        vis_fo.append(p.strip().split('-'))

# Sorts the visible flyovers into dates via a dict
fo_sorted = {} 
for p in vis_fo:
    if p[0] in fo_sorted:
        fo_sorted[p[0]].append(p[1])
    else:
        fo_sorted[p[0]] = [p[1]]    

# Used to easily read json contents
def jprint(obj):   
    text = json.dumps(obj, indent = 4, sort_keys = True)
    print(text)

# Check City, State of given Address to ensure correct search
city = t.json()[0]['LocalizedName']
state = t.json()[0]['AdministrativeArea']['LocalizedName']
conditions = w.json()['DailyForecasts'][0]['Night']['IconPhrase']

#pprint.pprint(fo_sorted)  # Testing ways to print nicely
#print(json.dumps(fo_sorted, indent=4, sort_keys=True))

#print(*vis_fo, sep = '\n') # More print formatting methods
#print('Flyovers:', *vis_fo, sep = '\n')

# Print out compiled information
print('Flyovers for {0}, {1}:'.format(city, state))
print(json.dumps(fo_sorted, indent=4, sort_keys=True))

if conditions == 'Clear' or conditions == 'Partly Cloudy' or conditions == 'Mostly clear':
    webbrowser.open('https://spotthestation.nasa.gov/')
else:
    print('Poor Viewing Conditions - Expecting: {0}'.format(conditions))

