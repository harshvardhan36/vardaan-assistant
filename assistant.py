import requests
import time
import re
import webbrowser
import random
from datetime import datetime
from serpapi import GoogleSearch

# Casual chat responses
chat_responses = {
    "how are you": ["I'm great, thanks for asking! How about you?", "Doing awesome! What about you?", "Feeling fantastic!"],
    "what's up": ["Not much, just here to help you!", "All good on my end. What about you?", "Ready to assist you, as always!"],
    "tell me about yourself": ["I'm Vardaan, your AI-powered assistant created by Harsh Vardhan.", 
                               "I'm Vardaan, here to make your life easier and more fun!"],
    "thank you": ["You're welcome! 😊", "Happy to help!", "Anytime, my friend!"],
    "who created you": ["I was created by Harsh Vardhan, a brilliant innovator!"]
}

def casual_chat(command):
    for key in chat_responses:
        if key in command:
            return random.choice(chat_responses[key])
    return None

# Predefined knowledge base for quick answers
knowledge_base = {
    "who is your founder": "Harsh Vardhan is my Founder",
}

def check_knowledge_base(query):
    return knowledge_base.get(query.lower(), None)

# Logging function
def log_command(command):
    with open("command_log.txt", "a") as log_file:
        log_file.write(f"{datetime.now()}: {command}\n")

# Function to use SerpAPI for searching
def search_web(query):
    api_key = "dd784d6862e2dd673ae36d850117961e85612399c3e36e1dea7429fb1dbb8915" 
    search = GoogleSearch({
        "q": query,
        "api_key": api_key,
    })
    
    try:
        results = search.get_dict()  # Fetch results
        organic_results = results.get("organic_results", [])
        if organic_results:
            first_result = organic_results[0]
            title = first_result.get("title", "No title available")
            link = first_result.get("link", "No link available")
            return f"Result: {title}\nLink: {link}"
        else:
            return "Sorry, no results found for your query."
    except Exception as e:
        return f"An error occurred: {e}"

# Weather API function
def get_weather(city):
    if not city.strip():  # Check for empty city input
        return "City name cannot be empty. Please try again."
    
    api_key = '234613d877a4fcb4069bcea137035bc4'
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "q=" + city + "&appid=" + api_key + "&units=metric"
    response = requests.get(complete_url)
    
    if response.status_code != 200:
        return f"Error fetching weather data: {response.status_code}"
    
    data = response.json()
    
    if data.get("cod") != "404":
        main_data = data.get("main", {})
        weather_data = data.get("weather", [{}])[0]
        temperature = main_data.get("temp", "N/A")
        pressure = main_data.get("pressure", "N/A")
        humidity = main_data.get("humidity", "N/A")
        weather_description = weather_data.get("description", "N/A")
        return (f"Temperature: {temperature}°C\n"
                f"Pressure: {pressure} hPa\n"
                f"Humidity: {humidity}%\n"
                f"Weather: {weather_description.capitalize()}")
    else:
        return "City not found. Please try again."

# Joke API function
def tell_joke():
    url = "https://v2.jokeapi.dev/joke/Any?type=single"
    try:
        response = requests.get(url)
        joke_data = response.json()
        if joke_data.get('error', False):
            return "Sorry, I couldn't fetch a joke right now."
        else:
            return joke_data['joke']
    except requests.exceptions.RequestException as e:
        return f"Error fetching joke: {e}"

# YouTube search function
def search_youtube(query):
    youtube_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    webbrowser.open(youtube_url)
    return f"Opened YouTube for: {query}"

# Currency Conversion function
def parse_conversion_request(command):
    pattern = r"convert (\d+(\.\d+)?) (\w+) to (\w+)"
    match = re.search(pattern, command.lower())

    if match:
        amount = float(match.group(1))  # Extract the amount
        base_currency = match.group(3).upper()  # Extract the base currency
        target_currency = match.group(4).upper()  # Extract the target currency
        return base_currency, target_currency, amount
    else:
        return None, None, None

def convert_currency(base, target, amount):
    access_key = "fca_live_AmcdFYuscbhyAhRLaRTx48dZ1kSvCSuyRd57ekU1"
    url = f"https://api.freecurrencyapi.com/v1/latest?apikey={access_key}&base_currency={base.upper()}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if request was successful
        data = response.json()
        if target.upper() in data['data']:
            rate = data['data'][target.upper()]
            converted_amount = amount * rate
            return f"{amount} {base.upper()} is equal to {converted_amount:.2f} {target.upper()}"
        else:
            return f"Conversion failed. Target currency '{target.upper()}' not found."
    except requests.exceptions.RequestException as e:
        return f"Error fetching currency data: {e}"

# Command processor
def process_command(command):
    command = command.lower()
    log_command(command)  # Log every command

    # Check knowledge base first
    kb_result = check_knowledge_base(command)
    if kb_result:
        return kb_result

    # Process other commands
    if 'hello' in command:
        return "Hello! How can I assist you today?"
    elif 'your name' in command:
        return "I am Harsh's assistant, Vardaan."
    elif 'time' in command:
        return time.ctime()
    elif 'date' in command:
        return datetime.now().strftime("%Y-%m-%d")
    elif 'weather' in command:
        city = input("Please enter the city name: ")
        return get_weather(city)
    elif 'joke' in command:
        return tell_joke()
    elif 'youtube' in command:
        search_query = input("What do you want to search on YouTube?\nYou: ")
        return search_youtube(search_query)
    elif 'search' in command:
        search_query = input("What do you want to search?\nYou: ")
        return search_web(search_query)
    elif 'convert' in command:
        base_currency, target_currency, amount = parse_conversion_request(command)
        if base_currency and target_currency and amount:
            return convert_currency(base_currency, target_currency, amount)
        else:
            return "Invalid currency conversion request. Please try again."
    elif 'help' in command:
        return ("Here are some things I can do:\n"
                "- Tell the time or date\n"
                "- Fetch the weather for a city\n"
                "- Search the web or YouTube\n"
                "- Tell a joke\n"
                "- Convert currencies\n"
                "- Answer predefined queries (e.g., 'Who is your founder')")
    elif casual_chat(command):
        return casual_chat(command)  # Handle casual conversations
    elif 'exit' in command or 'quit' in command:
        return "Goodbye! Have a great day!"
    else:
        return "Sorry, I didn't understand that command."

# Main assistant function
def start_assistant():
    print("Try help for better understanding!")
    while True:
        command = input("How can I help you? ")
        response = process_command(command)
        print(f"vardaan: {response}")
        if 'exit' in command or 'quit' in command:
            break

# Starting the assistant
if __name__ == "__main__":
    start_assistant()
