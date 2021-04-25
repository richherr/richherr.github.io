#!/usr/bin/env python
# coding: utf-8

# In[1]:


from datascience import *
get_ipython().run_line_magic('matplotlib', 'inline')
path_data = '../../../assets/data/'
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import math
from scipy import stats
import numpy as np


# # Bike Sharing in the Bay Area
# 
# We end this chapter by using all the methods we have learned to examine a new and large dataset. We will also introduce `map_table`, a powerful visualization tool.
# 
# The [Bay Area Bike Share](http://www.bayareabikeshare.com/) service published a [dataset](http://www.bayareabikeshare.com/open-data) describing every bicycle rental from September 2014 to August 2015 in their system. There were 354,152 rentals in all. The columns are:
# 
# - An ID for the rental
# - Duration of the rental, in seconds
# - Start date
# - Name of the Start Station and code for Start Terminal
# - Name of the End Station and code for End Terminal
# - A serial number for the bike
# - Subscriber type and zip code

# In[2]:


trips = Table.read_table(path_data + 'trip.csv')
trips


# We'll focus only on the *free trips*, which are trips that last less than 1800 seconds (half an hour). There is a charge for longer trips.
# 
# The histogram below shows that most of the trips took around 10 minutes (600 seconds) or so. Very few took near 30 minutes (1800 seconds), possibly because people try to return the bikes before the cutoff time so as not to have to pay.

# In[3]:


commute = trips.where('Duration', are.below(1800))
commute.hist('Duration', unit='Second')


# We can get more detail by specifying a larger number of bins. But the overall shape doesn't change much.

# In[4]:


commute.hist('Duration', bins=60, unit='Second')


# ## Exploring the Data with `group` and `pivot`
# 
# We can use `group` to identify the most highly used Start Station:

# In[5]:


starts = commute.group('Start Station').sort('count', descending=True)
starts


# The largest number of trips started at the Caltrain Station on Townsend and 4th in San Francisco. People take the train into the city, and then use a shared bike to get to their next destination.

# The `group` method can also be used to classify the rentals by both Start Station and End Station.

# In[6]:


commute.group(['Start Station', 'End Station'])


# Fifty-four trips both started and ended at the station on 2nd at Folsom. A much large number (437) were between 2nd at Folsom and 2nd at Townsend. 
# 
# The `pivot` method does the same classification but displays its results in a contingency table that shows all possible combinations of Start and End Stations, even though some of them didn't correspond to any trips. Remember that the first argument of a `pivot` statement specifies the column labels of the pivot table; the second argument labels the rows.
# 
# There is a train station as well as a Bay Area Rapid Transit (BART) station near Beale at Market, explaining the high number of trips that start and end there.

# In[7]:


commute.pivot('Start Station', 'End Station')


# We can also use `pivot` to find the shortest time of the rides between Start and End Stations. Here `pivot` has been given `Duration` as the optional `values` argument, and `min` as the function which to perform on the values in each cell.

# In[8]:


commute.pivot('Start Station', 'End Station', 'Duration', min)


# Someone had a very quick trip (271 seconds, or about 4.5 minutes) from 2nd at Folsom to Beale at Market, about five blocks away. There are no bike trips between the 2nd Avenue stations and Adobe on Almaden, because the latter is in a different city.

# ## Drawing Maps
# The table `stations` contains geographical information about each bike station, including latitude, longitude, and a "landmark" which is the name of the city where the station is located.

# In[9]:


stations = Table.read_table(path_data + 'station.csv')
stations


# We can draw a map of where the stations are located, using `Marker.map_table`. The function operates on a table, whose columns are (in order) latitude, longitude, and an optional identifier for each point.

# In[10]:


Marker.map_table(stations.select('lat', 'long', 'name'))


# The map is created using [OpenStreetMap](http://www.openstreetmap.org/#map=5/51.500/-0.100), which is an open online mapping system that you can use just as you would use Google Maps or any other online map. Zoom in to San Francisco to see how the stations are distributed. Click on a marker to see which station it is.

# You can also represent points on a map by colored circles. Here is such a map of the San Francisco bike stations.

# In[11]:


sf = stations.where('landmark', are.equal_to('San Francisco'))
sf_map_data = sf.select('lat', 'long', 'name')
Circle.map_table(sf_map_data, color='green')


# ## More Informative Maps: An Application of `join`
# The bike stations are located in five different cities in the Bay Area. To distinguish the points by using a different color for each city, let's start by using group to identify all the cities and assign each one a color.

# In[12]:


cities = stations.group('landmark').relabeled('landmark', 'city')
cities


# In[13]:


colors = cities.with_column('color', make_array('blue', 'red', 'green', 'orange', 'purple'))
colors


# Now we can join `stations` and `colors` by `landmark`, and then select the columns we need to draw a map.

# In[14]:


joined = stations.join('landmark', colors, 'city')
colored = joined.select('lat', 'long', 'name', 'color')
Marker.map_table(colored)


# Now the markers have five different colors for the five different cities.

# To see where most of the bike rentals originate, let's identify the start stations:

# In[15]:


starts = commute.group('Start Station').sort('count', descending=True)
starts


# We can include the geographical data needed to map these stations, by first joining `starts` with `stations`:

# In[16]:


station_starts = stations.join('name', starts, 'Start Station')
station_starts


# Now we extract just the data needed for drawing our map, adding a color and an area to each station. The area is 0.3 times the count of the number of rentals starting at each station, where the constant 0.3 was chosen so that the circles would appear at an appropriate scale on the map.

# In[17]:


starts_map_data = station_starts.select('lat', 'long', 'name').with_columns(
    'colors', 'blue',
    'areas', station_starts.column('count') * 0.3
)
starts_map_data.show(3)
Circle.map_table(starts_map_data)


# That huge blob in San Francisco shows that the eastern section of the city is the unrivaled capital of bike rentals in the Bay Area.
