from django.shortcuts import render  
import requests  
import datetime  

def home(request):  
    # Get the city from POST or set a default value  
    city = request.POST.get('city', 'blantyre')  

    # API Key and URL  
    api_key = 'd82c1f811b5e46c2e6dae343ee21a3b3'  
    url = 'https://api.openweathermap.org/data/2.5/weather'  
    
    # Parameters for the API request  
    params = {'q': city, 'appid': api_key, 'units': 'metric'}  

    try:  
        # Make the API request  
        response = requests.get(url, params=params)  
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)  
        data = response.json()  

        # Check if the API returned a valid response  
        if 'weather' in data and 'main' in data:  
            # Extract weather data  
            description = data['weather'][0]['description']  
            icon = data['weather'][0]['icon']  
            temp = data['main']['temp']  
        else:  
            # Handle case where the city is not found or other errors  
            description = "Weather data not found."  
            icon = None  
            temp = None  

    except requests.exceptions.HTTPError as http_err:  
        description = f"HTTP error occurred: {http_err}"  
        icon = None  
        temp = None  
    except requests.exceptions.RequestException as req_err:  
        description = f"Request error occurred: {req_err}"  
        icon = None  
        temp = None  
    except Exception as e:  
        description = f"An error occurred: {e}"  
        icon = None  
        temp = None  

    # Current date  
    day = datetime.date.today()  

    # Render the template with weather data  
    return render(request, 'weatherapp/index.html', {  
        'city': city,  
        'description': description,  
        'icon': icon,  
        'temp': temp,  
        'day': day  
    })