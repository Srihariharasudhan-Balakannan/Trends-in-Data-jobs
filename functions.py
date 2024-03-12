# imports
from geopy.geocoders import Nominatim

# function to sort dictionary passed based on the values in descending order and returns first n ket value pairs
def sort_dict_by_value(dictionary, descending=True, n=None):
    sorted_dict = dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=descending))
    if n is not None:
        sorted_dict = dict(list(sorted_dict.items())[:n])
    return sorted_dict

# function to roll up job data and return it as required individual dictionaries
def roll_up_data(job_lst):
    company_dict    = {}
    skill_dict      = {}
    location_dict   = {}
    job_type_dict   = {}
    experience_dict = {
        'entry level' : 0, 
        'mid level': 0,
        'senior level': 0
    }
    for l in job_lst:
        for key, value in l.items():
            if key == 'company_name':
                try:
                    company_dict[value] += 1
                except:
                    company_dict[value] = 1
            elif key == 'skills':
                for v in value:
                    try:
                        skill_dict[v] += 1
                    except:
                        skill_dict[v] = 1
            elif key == 'locations':
                for v in value:
                    try:
                        location_dict[v] += 1
                    except:
                        location_dict[v] = 1
            elif key == 'job_types':
                    for v in value:
                        try:
                            job_type_dict[v] += 1
                        except:
                            job_type_dict[v] = 1
            elif key == 'experience':
                if value < 3:
                    experience_dict['entry level'] +=1
                elif value >=3 and value <= 5:
                    experience_dict['mid level'] +=1
                else:
                    experience_dict['senior level'] +=1
    company_dict  = sort_dict_by_value(company_dict, descending=True, n=10)
    skill_dict    = sort_dict_by_value(skill_dict, descending=True, n=10)
    location_dict = sort_dict_by_value(location_dict, descending=True, n=10)
    return company_dict, skill_dict, location_dict, job_type_dict, experience_dict

# function to convert keys and values of a dictionary as two separate lists 
def dict_to_lst(my_dict):
    keys_list = list(my_dict.keys())
    values_list = list(my_dict.values())
    return keys_list, values_list

# function to get co-ordinates of location passed as string 
def get_coordinates(location):
    try:
        geolocator = Nominatim(user_agent="MyApp")
        data = geolocator.geocode(location)
        return data.latitude, data.longitude
    except:
        return -1, -1
    
# function to get latitude of location passed as a string 
def get_latitude(location):
    try:
        geolocator = Nominatim(user_agent="MyApp")
        data = geolocator.geocode(location)
        return data.latitude
    except:
        return -1
    
# function to get the longitude of location passed as a string 
def get_longitude(location):
    try:
        geolocator = Nominatim(user_agent="MyApp")
        data = geolocator.geocode(location)
        return data.longitude
    except:
        return -1

# function to add co-ordinates to pandas data-frame and column name containing location string passed as arguments
def add_coordinates(df, col_name):
    df['latitude'] = df.apply(lambda x: get_latitude(x[col_name]), axis=1)
    df['longitude'] = df.apply(lambda x: get_longitude(x[col_name]), axis=1)
    res_df = df[(df['latitude'] > 0) & (df['longitude'] > 0)]
    return res_df
