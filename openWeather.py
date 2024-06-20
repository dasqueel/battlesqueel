import os
import requests
import pprint

fbs_stadiums_dict = {
    'Air Force': {'latitude': 38.999, 'longitude': -104.8614},
    'Akron': {'latitude': 41.0778, 'longitude': -81.5158},
    'Alabama': {'latitude': 33.208, 'longitude': -87.5505},
    'Appalachian State': {'latitude': 36.2137, 'longitude': -81.6805},
    'Arizona': {'latitude': 32.2284, 'longitude': -110.9515},
    'Arizona State': {'latitude': 33.4231, 'longitude': -111.9308},
    'Arkansas': {'latitude': 36.0686, 'longitude': -94.1786},
    'Arkansas State': {'latitude': 35.8467, 'longitude': -90.6678},
    'Army': {'latitude': 41.381, 'longitude': -73.964},
    'Auburn': {'latitude': 32.6029, 'longitude': -85.4893},
    'Ball State': {'latitude': 40.2067, 'longitude': -85.407},
    'Baylor': {'latitude': 31.5489, 'longitude': -97.115},
    'Boise State': {'latitude': 43.603, 'longitude': -116.205},
    'Boston College': {'latitude': 42.3355, 'longitude': -71.1688},
    'Bowling Green': {'latitude': 41.3764, 'longitude': -83.6262},
    'Buffalo': {'latitude': 43.0015, 'longitude': -78.7897},
    'BYU': {'latitude': 40.2518, 'longitude': -111.6493},
    'California': {'latitude': 37.8719, 'longitude': -122.2591},
    'Central Michigan': {'latitude': 43.5906, 'longitude': -84.773},
    'Charlotte': {'latitude': 35.3096, 'longitude': -80.7401},
    'Cincinnati': {'latitude': 39.131, 'longitude': -84.5167},
    'Clemson': {'latitude': 34.6786, 'longitude': -82.8436},
    'Coastal Carolina': {'latitude': 33.7934, 'longitude': -79.0074},
    'Colorado': {'latitude': 40.009, 'longitude': -105.266},
    'Colorado State': {'latitude': 40.576, 'longitude': -105.0838},
    'Connecticut': {'latitude': 41.808, 'longitude': -72.2555},
    'Duke': {'latitude': 36.0014, 'longitude': -78.9382},
    'East Carolina': {'latitude': 35.5977, 'longitude': -77.3659},
    'Eastern Michigan': {'latitude': 42.2431, 'longitude': -83.6245},
    'Florida': {'latitude': 29.6494, 'longitude': -82.3481},
    'Florida Atlantic': {'latitude': 26.3781, 'longitude': -80.1014},
    'Florida International': {'latitude': 25.756, 'longitude': -80.377},
    'Florida State': {'latitude': 30.4383, 'longitude': -84.2906},
    'Fresno State': {'latitude': 36.813, 'longitude': -119.746},
    'Georgia': {'latitude': 33.9508, 'longitude': -83.3741},
    'Georgia Southern': {'latitude': 32.4258, 'longitude': -81.781},
    'Georgia Tech': {'latitude': 33.772, 'longitude': -84.393},
    'Hawaii': {'latitude': 21.2958, 'longitude': -157.818},
    'Houston': {'latitude': 29.7227, 'longitude': -95.3414},
    'Illinois': {'latitude': 40.1019, 'longitude': -88.2355},
    'Indiana': {'latitude': 39.1806, 'longitude': -86.5283},
    'Iowa': {'latitude': 41.6611, 'longitude': -91.5445},
    'Iowa State': {'latitude': 42.016, 'longitude': -93.6358},
    'Kansas': {'latitude': 38.9543, 'longitude': -95.2558},
    'Kansas State': {'latitude': 39.2025, 'longitude': -96.5933},
    'Kent State': {'latitude': 41.148, 'longitude': -81.3454},
    'Kentucky': {'latitude': 38.0221, 'longitude': -84.5056},
    'Liberty': {'latitude': 37.3501, 'longitude': -79.1787},
    'Louisiana': {'latitude': 30.2135, 'longitude': -92.0198},
    'Louisiana Monroe': {'latitude': 32.531, 'longitude': -92.078},
    'Louisiana Tech': {'latitude': 32.529, 'longitude': -92.6507},
    'Louisville': {'latitude': 38.2181, 'longitude': -85.7584},
    'LSU': {'latitude': 30.4119, 'longitude': -91.1851},
    'Marshall': {'latitude': 38.4211, 'longitude': -82.4231},
    'Maryland': {'latitude': 38.9905, 'longitude': -76.9495},
    'Memphis': {'latitude': 35.1495, 'longitude': -89.9375},
    'Miami (FL)': {'latitude': 25.957, 'longitude': -80.239},
    'Miami (OH)': {'latitude': 39.5069, 'longitude': -84.7458},
    'Michigan': {'latitude': 42.2658, 'longitude': -83.7485},
    'Michigan State': {'latitude': 42.7311, 'longitude': -84.4875},
    'Middle Tennessee': {'latitude': 35.8461, 'longitude': -86.3628},
    'Minnesota': {'latitude': 44.976, 'longitude': -93.2293},
    'Mississippi State': {'latitude': 33.461, 'longitude': -88.794},
    'Missouri': {'latitude': 38.943, 'longitude': -92.329},
    'Navy': {'latitude': 38.984, 'longitude': -76.4845},
    'Nebraska': {'latitude': 40.8206, 'longitude': -96.7054},
    'Nevada': {'latitude': 39.546, 'longitude': -119.818},
    'New Mexico': {'latitude': 35.084, 'longitude': -106.651},
    'North Carolina': {'latitude': 35.907, 'longitude': -79.050},
    'North Texas': {'latitude': 33.210, 'longitude': -97.152},
    'Northern Illinois': {'latitude': 41.933, 'longitude': -88.765},
    'Northwestern': {'latitude': 42.063, 'longitude': -87.688},
    'Notre Dame': {'latitude': 41.6983, 'longitude': -86.2335},
    'Ohio': {'latitude': 39.330, 'longitude': -82.101},
    'Ohio State': {'latitude': 40.0017, 'longitude': -83.0197},
    'Oklahoma': {'latitude': 35.2043, 'longitude': -97.4421},
    'Oklahoma State': {'latitude': 36.125, 'longitude': -97.066},
    'Old Dominion': {'latitude': 36.886, 'longitude': -76.305},
    'Ole Miss': {'latitude': 34.365, 'longitude': -89.538},
    'Oregon': {'latitude': 44.052, 'longitude': -123.086},
    'Oregon State': {'latitude': 44.565, 'longitude': -123.281},
    'Penn State': {'latitude': 40.812, 'longitude': -77.856},
    'Pittsburgh': {'latitude': 40.443, 'longitude': -79.961},
    'Purdue': {'latitude': 40.423, 'longitude': -86.921},
    'Rice': {'latitude': 29.718, 'longitude': -95.403},
    'Rutgers': {'latitude': 40.506, 'longitude': -74.454},
    'San Diego State': {'latitude': 32.773, 'longitude': -117.071},
    'San Jose State': {'latitude': 37.337, 'longitude': -121.882},
    'SMU': {'latitude': 32.840, 'longitude': -96.784},
    'South Carolina': {'latitude': 34.000, 'longitude': -81.034},
    'South Florida': {'latitude': 27.975, 'longitude': -82.503},
    'Southern Methodist': {'latitude': 32.840, 'longitude': -96.784},
    'Southern Mississippi': {'latitude': 31.329, 'longitude': -89.334},
    'Stanford': {'latitude': 37.434, 'longitude': -122.161},
    'Syracuse': {'latitude': 43.037, 'longitude': -76.138},
    'TCU': {'latitude': 32.709, 'longitude': -97.361},
    'Temple': {'latitude': 39.977, 'longitude': -75.158},
    'Tennessee': {'latitude': 35.955, 'longitude': -83.925},
    'Texas': {'latitude': 30.283, 'longitude': -97.732},
    'Texas A&M': {'latitude': 30.609, 'longitude': -96.340},
    'Texas State': {'latitude': 29.888, 'longitude': -97.929},
    'Texas Tech': {'latitude': 33.590, 'longitude': -101.875},
    'Toledo': {'latitude': 41.654, 'longitude': -83.614},
    'Troy': {'latitude': 31.808, 'longitude': -85.973},
    'Tulane': {'latitude': 29.940, 'longitude': -90.120},
    'Tulsa': {'latitude': 36.154, 'longitude': -95.945},
    'UAB': {'latitude': 33.524, 'longitude': -86.812},
    'UCF': {'latitude': 28.607, 'longitude': -81.197},
    'UCLA': {'latitude': 34.073, 'longitude': -118.447},
    'UNLV': {'latitude': 36.104, 'longitude': -115.168},
    'USC': {'latitude': 34.014, 'longitude': -118.287},
    'Utah': {'latitude': 40.760, 'longitude': -111.850},
    'Utah State': {'latitude': 41.740, 'longitude': -111.810},
    'UTEP': {'latitude': 31.772, 'longitude': -106.507},
    'UTSA': {'latitude': 29.463, 'longitude': -98.512},
    'Vanderbilt': {'latitude': 36.144, 'longitude': -86.805},
    'Virginia': {'latitude': 38.033, 'longitude': -78.507},
    'Virginia Tech': {'latitude': 37.222, 'longitude': -80.422},
    'Wake Forest': {'latitude': 36.127, 'longitude': -80.251},
    'Washington': {'latitude': 47.654, 'longitude': -122.304},
    'Washington State': {'latitude': 46.731, 'longitude': -117.154},
    'West Virginia': {'latitude': 39.649, 'longitude': -79.956},
    'Western Kentucky': {'latitude': 36.985, 'longitude': -86.455},
    'Western Michigan': {'latitude': 42.283, 'longitude': -85.615},
    'Wisconsin': {'latitude': 43.070, 'longitude': -89.412},
    'Wyoming': {'latitude': 41.312, 'longitude': -105.580},
    'Jacksonville State': {'latitude': 33.8203, 'longitude': -85.7664},
    'Kennesaw State': {'latitude': 34.0290, 'longitude': -84.5676},
    'New Mexico State': {'latitude': 32.2835, 'longitude': -106.7519},
    'South Alabama': {'latitude': 30.6975, 'longitude': -88.1816},
    'Georgia State': {'latitude': 33.7358, 'longitude': -84.3896},
    'James Madison': {'latitude': 38.4393, 'longitude': -78.8769},
    'UMass': {'latitude': 42.3900, 'longitude': -72.5301}
}

openWeatherKey = os.getenv('openWeatherKey')
# print(openWeatherKey)
team = 'Wyoming'
lat=fbs_stadiums_dict[team]['latitude']
lon=fbs_stadiums_dict[team]['longitude']

url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={openWeatherKey}&units=imperial'
response = requests.get(url)

json = response.json()
wind = json['wind']
main = json['main']
weather = json['weather']

pprint.pprint(main)
pprint.pprint(wind)
pprint.pprint(weather)

# dicts = [wind, main]
# for d in weather: dicts.append(d)

# print(dicts)
# combined_dict = {}
# for d in dicts:
#     combined_dict.update(d)

# pprint.pprint(combined_dict)

def createStadiumMap():
    import folium

    # Create a map centered in the USA
    map_fbs = folium.Map(location=[39.8283, -98.5795], zoom_start=4)

    # Add stadiums to the map
    for school, coords in fbs_stadiums_dict.items():
        folium.Marker(
            location=[coords['latitude'], coords['longitude']],
            popup=school,
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(map_fbs)

    # Save the map to an HTML file
    map_fbs.save('fbs_stadiums_map.html')
