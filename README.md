# ISS-Flyover
Quick simple program for checking the visibility of ISS flyovers within the next 24 hours.  Returns the projected weather report if conditions are poor or opens the NASA ISS tracking page if conditions are clear.

# Dependencies:
requests

json

datetime

pprint (optional - for print formatting)

webbrowser

AccuWeather API key (obtained here: https://developer.accuweather.com/ and stored in iss_flyover_config)


# Notes:
Subject to future change as Nathan Bergey, whose ISS tracking is used (source: http://open-notify.org/ and github: https://github.com/open-notify/Open-Notify-API), plans to disable ISS pass predictions.
