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
        
        # # playgrounds
        # query_playground_result = self.google_places.nearby_search(
        #     location=self.full_address, radius = self.radius, types=[types.TYPE_playground])
        # playgrounds = {}
        # for place in query_playground_result.places:
        #     place_latlong = (float(place.geo_location['lat']),float(place.geo_location['lng']))
        #     dist = vincenty(self.latlong, place_latlong).feet  
        #     playgrounds[place.name]= int(dist)
        
        print parks
        print schools
        # print playgrounds
           
        if parks or schools:# or playgrounds:
            self.valid_address=False
        else:
            self.valid_address=True
        locations={}
        
        locations['parks']=parks
        locations['schools']=schools
        # locations['playgrounds']=playgrounds
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

