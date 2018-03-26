from googleplaces import GooglePlaces, types, lang
from geopy.distance import vincenty
from geopy.geocoders import Nominatim
import googlemaps



class Places(object):
    def __init__(self,addr):        
        self.api_key = 'AIzaSyA0gO64fjVBIhWSgTlyUEzihiTXPnXsh0Y'
        self.gmaps = googlemaps.Client(key=self.api_key)
        print self.gmaps
        self.location = self.gmaps.geocode(addr)[0]
        # for key, value in self.location.iteritems():
            # print key, ':', value
        
        self.latlong = (float(self.location['geometry']['location']['lat']),float(self.location['geometry']['location']['lng']))
        # print self.latlong
        if 'bounds' in self.location['geometry']:
            self.geocode_bounds = self.location['geometry']['bounds']  
        else:
            self.geocode_bounds = None
        self.full_address = self.location['formatted_address']
        
        # allowable distance in meters
        self.radius = 152.4
        self.valid_address=None

    def __str__(self):
        return self.full_address
    
#This is based on a singular lat-long for both locations. Not exact and may not be admissable for the state    
    def restrictive_locations(self):
        self.google_places = GooglePlaces(self.api_key)
        # Parks
        
        query_park_result = self.google_places.nearby_search(
            location=self.full_address, radius = self.radius, types=[types.TYPE_PARK])
        parks = {}
        print query_park_result
        for place in query_park_result.places:
            # print place
            place_latlong = (float(place.geo_location['lat']),float(place.geo_location['lng']))
            dist = vincenty(self.latlong, place_latlong).feet  
            parks[place.name]= int(dist)

        
        # Schools
        query_school_result = self.google_places.nearby_search(
            location=self.full_address, radius = self.radius, types=[types.TYPE_SCHOOL])
        schools = {}
        for place in query_school_result.places:
            place_latlong = (float(place.geo_location['lat']),float(place.geo_location['lng']))
            dist = vincenty(self.latlong, place_latlong).feet  
            schools[place.name]= int(dist)
        
        print parks
        print schools   
        if parks or schools:
            self.valid_address=False
        else:
            self.valid_address=True
        locations={}
        
        locations['parks']=parks
        locations['schools']=schools
        return locations

# This will be a much more accurate calculation based on the bounds of both properties
    def get_least_dist():
        pass
        # print type(self.geocode_bounds['northeast']['lat'])
        # print type(self.geocode_bounds['northeast']['lng'])


    def get_corners(self):
        max_lng=None
        min_lng=None
        max_lat=None
        min_lat=None
        for key, value in self.geocode_bounds.iteritems():
            print key,value



# # location = raw_input('Please enter the location you would like to search:')
# location = '532 N. Albany Ave.'
# # You may prefer to use the text_search API, instead.


# query_park_result = google_places.nearby_search(
#         location=location, radius = 200,
#         types=[types.TYPE_PARK])

# query_school_result = google_places.nearby_search(
#         location=location, radius = 200,
#         types=[types.TYPE_SCHOOL])


# # If types param contains only 1 item the request to Google Places API
# # will be send as type param to fullfil:
# # http://googlegeodevelopers.blogspot.com.au/2016/02/changes-and-quality-improvements-in_16.html



# if query_school_result.has_attributions:
#     print query_school_result.html_attributions


# for place in query_school_result.places:
#     print place.name
#     print place.geo_location















# if query_park_result.has_attributions:
#     print query_park_result.html_attributions


# for place in query_park_result.places:
#     # Returned places from a query are place summaries.
#     print place.name
#     print place.geo_location
#     # print place.place_id

    # # The following method has to make a further API call.
    # place.get_details()
    # # Referencing any of the attributes below, prior to making a call to
    # # get_details() will raise a googleplaces.GooglePlacesAttributeError.
    # print place.details # A dict matching the JSON response from Google.
    # print place.local_phone_number
    # print place.international_phone_number
    # print place.website
    # print place.url

    # # Getting place photos

    # for photo in place.photos:
    #     # 'maxheight' or 'maxwidth' is required
    #     photo.get(maxheight=500, maxwidth=500)
    #     # MIME-type, e.g. 'image/jpeg'
    #     photo.mimetype
    #     # Image URL
    #     photo.url
    #     # Original filename (optional)
    #     photo.filename
    #     # Raw image data
    #     photo.data


# # Are there any additional pages of results?
# if query_result.has_next_page_token:
#     query_result_next_page = google_places.nearby_search(
#             pagetoken=query_result.next_page_token)


# # Adding and deleting a place
# try:
#     added_place = google_places.add_place(name='Mom and Pop local store',
#             lat_lng={'lat': 51.501984, 'lng': -0.141792},
#             accuracy=100,
#             types=types.TYPE_HOME_GOODS_STORE,
#             language=lang.ENGLISH_GREAT_BRITAIN)
#     print added_place.place_id # The Google Places identifier - Important!
#     print added_place.id

#     # Delete the place that you've just added.
#     google_places.delete_place(added_place.place_id)
# except GooglePlacesError as error_detail:
#     # You've passed in parameter values that the Places API doesn't like..
#     print error_detail