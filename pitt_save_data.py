""" This Script belongs to Anisha Kaul (akaul1)"""
""" Prepared for eduactional purposes"""
""" Fetches Uber Information about Price and Arrival Times Estimates"""

#import libraries
import requests  # For fetching the response off the API
import pprint    # Viewing the contents at the console
from datetime import datetime, timedelta  # For converting the UTC time of the API to local time
import threading # For calling the thread of API request every 20s.
                 # Each request is called using a different thread
import csv       # Saving each API response as a single row of csv data file
import json      # For parsing the response from the Application Program Interface



def request_surge_and_time(start_lat, start_lng, end_lat, end_lng, start_location, end_location, local_time):

  # The URLs defined for the fetching the price estimates
  surge_url = 'https://api.uber.com/v1/estimates/price'
  # The URLs defined for the fetching the times estimates
  time_url = 'https://api.uber.com/v1/estimates/time'
  # The URLs defined for the fetching the product information
  product_url = "https://api.uber.com/v1/products"
  

  # Query parameters for price/surge estimates
  surge_parameters = {
      'server_token': 'W-hVCSnx3xkgr5aKmnB-P1quVgkNGHoPs2GeCQiE',
      'start_latitude' : start_lat, 
      'start_longitude' : start_lng,
      'end_latitude': end_lat, 
      'end_longitude' : end_lng
  }
 
 # Query parameters for eta estimates
  time_parameters = {
    'server_token': 'W-hVCSnx3xkgr5aKmnB-P1quVgkNGHoPs2GeCQiE',
    'start_latitude' : start_lat, 
    'start_longitude' : start_lng
  }

  time_response = requests.get(time_url, params=time_parameters)
  surge_response = requests.get(surge_url, params=surge_parameters)

  # JSON responses of the API requests
  time_data = time_response.json()
  surge_data = surge_response.json()
  
  times = time_data.get("times")
  prices = surge_data.get("prices")

  # The file in which the data has to be saved
  with open('sf_pitt_data.csv', 'a') as csvfile:
    fieldnames = ['time' , 'display_name', 'product_id', 'eta', 'currency_code', 'duration',
                  'start_lat', 'start_lng', 'end_lat', 'end_lng', 'start_location',
                   'end_location', 'distance', 'min_est_fare', 'max_est_fare', 'surge_price', 'minimum_fare' ]
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)    
    array = []
    
    # Make records entries for all the products offered in the location
    for product in times:
      json_v = {}
      
      json_v['time'] = local_time
      json_v['display_name'] = product.get('display_name')
      json_v['product_id'] = product.get('product_id')
      json_v['eta'] = product.get('estimate')
      
      for i in range(0,len(prices)):
        if(prices[i].get('product_id') == product.get('product_id')):
          json_v['currency_code'] = prices[i].get('currency_code')
          json_v['duration'] = prices[i].get('duration')
          json_v['start_lat'] = start_lat
          json_v['start_lng'] = start_lng
          json_v['end_lat'] = end_lat
          json_v['end_lng'] = end_lng
          json_v['start_location'] = start_location
          json_v['end_location'] = end_location
          json_v['distance'] = prices[i].get('distance')
          json_v['min_est_fare'] = prices[i].get('low_estimate')
          json_v['max_est_fare'] = prices[i].get('high_estimate')
          json_v['surge_price'] = prices[i].get('surge_multiplier')
          json_v['minimum_fare'] = prices[i].get('minimum')
          writer.writerow(json_v)
  csvfile.close()

def request_price_estimate():
  # ===================== Pittsburgh Locations =======================
  # Market District Lat Long
  mkt_dist_lat = 40.441287
  mkt_dist_lng = -80.000506

  # Carnegie Mellon University Lat Long
  cmu_lat = 40.443229
  cmu_lng = -79.944137

  # Murray Avenue Lat Long
  murray_lat = 40.437944
  murray_lng = -79.922973

  # Atwood Oakland Lat Long
  atwood_lat = 40.441864
  atwood_lng = -79.956468

  # Steel Plaza Lat Long
  steel_plaza_lat = 40.439859
  steel_plaza_lng = -79.995465

  # Cultural District Lat Long
  cultural_dist_lat = 40.4437
  cultural_dist_lng = -79.9997
  # ===================== San Francisco Locations =======================
  
  # Uber Headquaters Lat Long
  uber_hq_lat = 37.774929
  uber_hq_long = -122.419416

  # Marina Street Lat long
  marina_st_lat = 37.802305
  marina_st_long = -122.431169

  # Freemont Road Lat long
  free_mont_lat = 37.789758
  free_mont_lng = -122.395892

  # Richmond Street Lat long
  richmond_ds_lat = 37.780126
  richmond_ds_lng = -122.480006
  
  utc_time = datetime.now().ctime()
  pitt_time = (datetime.strptime(str(utc_time), '%a %b %d %H:%M:%S %Y') + timedelta(hours= -4) ).ctime()
  sf_time  = (datetime.strptime(str(utc_time), '%a %b %d %H:%M:%S %Y') + timedelta(hours= -7) ).ctime()

  # ======== Requests for Pittsburg locations, Uptown ======
  request_surge_and_time(cmu_lat, cmu_lng, mkt_dist_lat, mkt_dist_lng, "Carnegie Mellon University, Pittsburgh", "Market District, Pittsburgh", pitt_time)
  request_surge_and_time(murray_lat, murray_lng, mkt_dist_lat, mkt_dist_lng, "Murray Avenue, Pittsburgh", "Market District, Pittsburgh", pitt_time)
  request_surge_and_time(atwood_lat, atwood_lng, mkt_dist_lat, mkt_dist_lng, "AtWood Street, Pittsburgh", "Market District, Pittsburgh", pitt_time)
  
  # ======== Requests for Pittsburg locations, Downtown ======
  request_surge_and_time(steel_plaza_lat, steel_plaza_lng, murray_lat, murray_lng, "Steel Plaza, Pittsburgh, Pittsburgh", "Murray Avenue, Pittsburgh", pitt_time)
  request_surge_and_time(cultural_dist_lat, cultural_dist_lng, murray_lat, murray_lng, "Cultural District, Pittsburgh", "Murray Avenue, Pittsburgh", pitt_time)

 
  # ======== Requests for San Francisco locations ======
  request_surge_and_time(uber_hq_lat, uber_hq_long, marina_st_lat, marina_st_long, "Uber Head Quaters, San Francisco", "Marina District",sf_time)
  request_surge_and_time(free_mont_lat, free_mont_lng, richmond_ds_lng, richmond_ds_lng, "Fremont Street, San Francisco", "Richmond District", sf_time)


# Thread generator function that calls the calls for surge price information for all the location afte 20s 
def get_surge_price_and_time_estimate():
  threading.Timer(20.0, get_surge_price_and_time_estimate).start()
  request_price_estimate()

def main():
  get_surge_price_and_time_estimate()

main()
