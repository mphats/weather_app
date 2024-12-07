from django.shortcuts import render  
import requests  
import datetime  

def home(request):  
    # Default city  
    default_city = 'blantyre'  
    city = request.POST.get('city', default_city)  # Get the city from POST or default to 'blantyre'  

    # API Key and URL  
    api_key = 'd82c1f811b5e46c2e6dae343ee21a3b3'  # Replace with your actual API key  
    url = 'https://api.openweathermap.org/data/2.5/weather'  
    
    # Parameters for API request  
    params = {'q': city, 'appid': api_key, 'units': 'metric'}  

    # Initialize variables for weather data  
    description = ""  
    icon = None  
    temp = None  

    try:  
        # Make the API request  
        response = requests.get(url, params=params)  
        response.raise_for_status()  # Check for HTTP errors  
        data = response.json()  

        # Validate and extract weather data  
        if 'weather' in data and 'main' in data:  
            description = data['weather'][0]['description']  
            icon = data['weather'][0]['icon']  
            temp = data['main']['temp']  
        else:  
            description = "Weather data not found. Please check the city name."  

    except requests.exceptions.HTTPError as http_err:  
        description = f"HTTP error occurred: {http_err}"  
    except requests.exceptions.RequestException as req_err:  
        description = f"Request error occurred: {req_err}"  
    except Exception as e:  
        description = f"An unexpected error occurred: {e}"  

    # Current date  
    day = datetime.date.today().strftime("%A, %B %d, %Y")  # Format the date for better readability  

    # Render the template with weather data  
    return render(request, 'weatherapp/index.html', {  
        'city': city,  
        'description': description,  
        'icon': icon,  
        'temp': temp,  
        'day': day  
    })