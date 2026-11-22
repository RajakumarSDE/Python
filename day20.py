# ============================================================
# THE BIG PICTURE (read this first!)
# Imagine you want to know if you need an umbrella today.
# You could ask a friendly weather helper far away.
# This program is like a messenger:
#   1. You tell it a city name.
#   2. It asks one helper, "Where is this city on the map?"
#   3. It asks another helper, "What's the weather at that spot?"
#   4. It brings the answer back and shows it to you nicely.
# ============================================================

#!/usr/bin/env python3
# ^ This is a tiny note for the computer: "Use Python 3 to read me."
# (It only matters on Mac/Linux. Think of it as a name tag.)

"""Simple command-line weather app using the free Open-Meteo API (no API key needed).

Usage:
    python weather.py Chennai
    python weather.py            # prompts for a city
"""
# ^ This is a "docstring": a label on the box that says what's inside.
#   It doesn't DO anything. It just helps humans understand the program.
#   "API" = a door that one program can knock on to ask another program for stuff.
#   "No API key" = the door is open, so we don't need a secret password.

import json
# ^ Computers send answers in a special text style called JSON.
#   The "json" tool is like a translator that turns it into something Python understands.

import sys
# ^ "sys" lets us talk to the computer system: read what you typed
#   after the program name, and say "I'm done" when we finish.

import urllib.error
# ^ This tool knows the NAMES of things that can go wrong on the internet
#   (like "the wifi is off"). We use it to catch those problems politely.

import urllib.parse
# ^ This tool helps write web addresses correctly,
#   like putting a stamp and the right address on an envelope.

import urllib.request
# ^ This tool actually SENDS the letter to the internet and brings back the reply.

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
# ^ A "variable" is a labeled box that holds something. This box is named GEOCODE_URL.
#   Inside is the address of the helper who knows where cities are on the map.
#   We write it in CAPITALS because it's a constant: it never changes.

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
# ^ The address of the second helper, the one who knows the weather.

# WMO weather interpretation codes -> readable text
# ^ The weather helper doesn't say "rainy". It says a number like 61.
#   So we need a decoder ring to turn numbers into words.
WEATHER_CODES = {
    # ^ A "dictionary": like a real dictionary, you look up one thing (a number)
    #   and it gives you another thing (the meaning). Curly braces { } make one.
    0: "Clear sky",                          # Number 0 means: no clouds, big blue sky
    1: "Mainly clear",                       # Number 1: almost no clouds
    2: "Partly cloudy",                      # Number 2: some clouds, some sun
    3: "Overcast",                           # Number 3: the whole sky is gray
    45: "Fog",                               # Number 45: like walking inside a cloud
    48: "Rime fog",                          # Number 48: icy fog
    51: "Light drizzle",                     # Number 51: tiny sprinkles of rain
    53: "Moderate drizzle",                  # Number 53: medium sprinkles
    55: "Dense drizzle",                     # Number 55: lots of sprinkles
    61: "Light rain",                        # Number 61: gentle rain
    63: "Moderate rain",                     # Number 63: normal rain
    65: "Heavy rain",                        # Number 65: pouring! Bring a big umbrella
    71: "Light snow",                        # Number 71: a few snowflakes
    73: "Moderate snow",                     # Number 73: normal snow
    75: "Heavy snow",                        # Number 75: snowman weather!
    80: "Light rain showers",                # Number 80: quick small rain bursts
    81: "Moderate rain showers",             # Number 81: medium rain bursts
    82: "Violent rain showers",              # Number 82: super strong rain bursts
    95: "Thunderstorm",                      # Number 95: boom and lightning
    96: "Thunderstorm with hail",            # Number 96: thunder plus little ice balls
    99: "Severe thunderstorm with hail",     # Number 99: the scariest storm of all
}
# ^ The closing curly brace says: "The decoder ring is finished."


def fetch_json(url, params):
    # ^ "def" means "I'm teaching the computer a new trick."
    #   The trick is called fetch_json. It needs two things from you:
    #   an address (url) and some extra details (params), like a question.
    #   Think of a trick as a recipe: write it once, use it many times.

    """GET a URL with query parameters and return the parsed JSON."""
    # ^ A label that says what this trick does, in plain words.

    query = urllib.parse.urlencode(params)
    # ^ Turn our question into the special format web addresses understand.
    #   For example, {"name": "Chennai"} becomes "name=Chennai".
    #   It's like folding our question neatly so it fits in the envelope.

    with urllib.request.urlopen(f"{url}?{query}", timeout=10) as response:
        # ^ Send the letter! We glue the address and question together with a "?".
        #   "timeout=10" means: "If nobody answers in 10 seconds, stop waiting."
        #   "with ... as response" means: open the reply, and
        #   automatically close it when we're done (like closing a door behind us).
        return json.load(response)
        # ^ Read the reply, translate it from JSON into Python, and hand it back.
        #   "return" means: "Here's the answer. This trick is finished."


def find_city(name):
    # ^ Teaching a second trick: turn a city NAME into a spot on the map.

    """Look up a city name and return its coordinates and details."""
    # ^ A label: this trick finds where a city lives.

    data = fetch_json(GEOCODE_URL, {"name": name, "count": 1})
    # ^ Use our first trick! Ask the map helper: "Find me this city, but
    #   only give me 1 answer (count = 1)." We keep the reply in a box called data.

    results = data.get("results")
    # ^ Open the reply and take out the part called "results".
    #   ".get" is a polite way to look: if it's missing, we get "nothing"
    #   instead of the program crashing.

    if not results:
        # ^ "if" asks a yes/no question: "Is the results box empty?"
        #   If yes, the helper never heard of that city. Maybe it was spelled wrong.
        raise ValueError(f"Couldn't find a city called '{name}'.")
        # ^ Wave a red flag! "raise" shouts: "Something went wrong!"
        #   We attach a friendly message so you know what happened.

    return results[0]
    # ^ Hand back the first (and only) city. In Python we count from 0, not 1,
    #   so [0] means "the first one in the list."


def get_weather(latitude, longitude):
    # ^ A third trick: given a spot on the map, ask what the weather is.
    #   Latitude = how far up or down on the globe. Longitude = how far left or right.
    #   Together they're like an X on a treasure map.

    """Fetch current conditions and a 3-day forecast."""
    # ^ A label: this trick gets weather for now and the next 3 days.

    return fetch_json(
        # ^ Use our first trick again, and hand back whatever it brings.
        FORECAST_URL,
        # ^ First we say WHO to ask: the weather helper's address.
        {
            # ^ Next comes our shopping list of questions, inside curly braces.
            "latitude": latitude,
            # ^ "Here's the up-and-down part of the spot."
            "longitude": longitude,
            # ^ "Here's the left-and-right part of the spot."
            "current": "temperature_2m,apparent_temperature,relative_humidity_2m,"
                       "wind_speed_10m,weather_code",
            # ^ "Tell me about RIGHT NOW": the temperature, how hot it FEELS,
            #   how damp the air is, how fast the wind blows, and the weather number.
            #   (The "_2m" means measured 2 meters above the ground, about your height!)
            "daily": "weather_code,temperature_2m_max,temperature_2m_min,"
                     "precipitation_probability_max",
            # ^ "Also give me each DAY's summary": the weather number, the hottest
            #   and coldest temperatures, and the biggest chance of rain.
            "timezone": "auto",
            # ^ "Figure out the clock for that city yourself, so the dates match its sunrise."
            "forecast_days": 10,
            # ^ "I only want today plus the next 2 days. That's 3 days total."
        },
        # ^ End of the shopping list.
    )
    # ^ End of our request to the helper.


def describe(code):
    # ^ A tiny trick: turn a weather NUMBER into WORDS using our decoder ring.

    return WEATHER_CODES.get(code, "Unknown")
    # ^ Look up the number in the dictionary.
    #   If the number isn't in the dictionary, say "Unknown" instead of crashing.


def show_weather(city, weather):
    # ^ This trick makes everything look pretty on screen.
    #   It needs the city info and the weather info.

    current = weather["current"]
    # ^ From the big weather reply, grab just the "right now" part
    #   and put it in a box called current, so it's easy to reach.

    units = weather["current_units"]
    # ^ Also grab the units, the little labels like "°C" or "km/h",
    #   so we don't say "25" when we mean "25 degrees".

    place = ", ".join(filter(None, [city["name"], city.get("admin1"), city.get("country")]))
    # ^ Build a nice place name like "Chennai, Tamil Nadu, India".
    #   We gather three pieces: city, state, country.
    #   "filter(None, ...)" throws away any piece that's missing.
    #   ", ".join(...) glues the pieces together with a comma and a space.

    print(f"\nWeather for {place}")
    # ^ "print" shows words on the screen. "\n" means "start on a new line first."
    #   The f before the quote lets us drop {place} right into the sentence.

    print("=" * (len(place) + 12))
    # ^ Draw an underline made of "=" signs.
    #   len(place) counts the letters. We add 12 so the line matches the title's length.

    print(f"Now:        {describe(current['weather_code'])}")
    # ^ Show the weather in words. First we grab the weather NUMBER,
    #   then describe() turns it into words like "Partly cloudy".

    print(f"Temperature: {current['temperature_2m']}{units['temperature_2m']} "
          f"(feels like {current['apparent_temperature']}{units['apparent_temperature']})")
    # ^ Show two temperatures: the real one, and how it FEELS on your skin.
    #   Wind and humidity can make 30 degrees feel like 36. We add the unit label too.

    print(f"Humidity:    {current['relative_humidity_2m']}{units['relative_humidity_2m']}")
    # ^ Show how much water is floating in the air, as a percent.
    #   High humidity feels sticky, like a warm bathroom after a shower.

    print(f"Wind:        {current['wind_speed_10m']} {units['wind_speed_10m']}")
    # ^ Show how fast the wind is blowing, with the unit (like km/h).

    daily = weather["daily"]
    # ^ Now grab the DAY-BY-DAY part of the reply and put it in a box called daily.

    print("\n3-day forecast")
    # ^ Print a heading for the forecast section, on a fresh line.

    print("-" * 14)
    # ^ Draw a short underline made of 14 dashes, one for each letter of the heading.

    for i, day in enumerate(daily["time"]):
        # ^ A "loop": do the same thing again and again, once per day.
        #   "daily['time']" is a list of dates. enumerate gives us two things each lap:
        #   i = which lap we're on (0, 1, 2) and day = the date for that lap.
        #   It's like walking down a row of 3 doors and opening each one.
        print(
            # ^ Show one line of forecast for this day.
            f"{day}: {describe(daily['weather_code'][i]):<22} "
            # ^ Show the date, then the weather in words.
            #   ":<22" means "leave 22 spaces for this part" so every line lines up neatly,
            #   like seats in a classroom.
            f"{daily['temperature_2m_min'][i]}° / {daily['temperature_2m_max'][i]}°C  "
            # ^ Show the coldest and hottest temperature for the day.
            #   The [i] picks the right day's number from each list.
            f"rain chance {daily['precipitation_probability_max'][i]}%"
            # ^ Show how likely rain is, as a percent. 80% means: pack that umbrella!
        )
        # ^ End of this day's line. Then the loop goes back for the next day.

    print()
    # ^ Print an empty line at the end so the answer doesn't touch the next thing on screen.


def main():
    # ^ The "main" trick is the boss. It runs everything above in the right order,
    #   like a teacher telling each student when to talk.

    city_name = " ".join(sys.argv[1:]).strip() or input("Enter a city: ").strip()
    # ^ Figure out which city you want.
    #   sys.argv is everything you typed on the command line.
    #   [1:] skips the first word (the program's own name) and takes the rest.
    #   " ".join(...) glues the words together, so "New York" works with a space.
    #   ".strip()" trims extra spaces from the ends.
    #   "or input(...)" means: if you typed nothing, ASK you with a question instead.

    if not city_name:
        # ^ Ask: "Did you give me an empty answer?"
        print("Please enter a city name.")
        # ^ If so, politely ask for a real one.
        return 1
        # ^ Stop here. The number 1 is a secret code meaning "something went wrong."

    try:
        # ^ "try" means: "Let me TRY this risky stuff. If it breaks, I have a plan."
        #   Like trying to catch a ball: sometimes you miss, so you're ready.
        city = find_city(city_name)
        # ^ Ask the map helper where your city is.
        weather = get_weather(city["latitude"], city["longitude"])
        # ^ Take the city's map spot (up-down and left-right) and ask the weather helper.
    except ValueError as error:
        # ^ PLAN A: if the city couldn't be found, catch that red flag we waved earlier.
        print(error)
        # ^ Show the friendly message, like "Couldn't find a city called 'Chenai'."
        return 1
        # ^ Stop with the "something went wrong" code.
    except (urllib.error.URLError, TimeoutError):
        # ^ PLAN B: if the internet is broken, or the helper took too long to answer.
        print("Couldn't reach the weather service. Check your internet connection.")
        # ^ Tell you what probably happened, in plain words.
        return 1
        # ^ Stop with the "something went wrong" code.

    show_weather(city, weather)
    # ^ Everything worked! Hand the info to our pretty-printer to show you.

    return 0
    # ^ Stop. The number 0 is the secret code for "everything went great!"


if __name__ == "__main__":
    # ^ This asks: "Did someone run this file directly?"
    #   If yes, start the program. If someone only borrowed our tricks for a different
    #   program, don't start anything by surprise. It's like a toy with an ON button
    #   that only works when you press it yourself.
    sys.exit(main())
    # ^ Run the boss (main) and pass its secret code (0 or 1) to the computer,
    #   so the computer knows whether we finished happily or not.