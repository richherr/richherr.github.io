#!/usr/bin/env python
# coding: utf-8

# In[1]:


from datascience import *
path_data = '../../assets/data/'


# # Sequences
# 
# Values can be grouped together into collections, which allows programmers to organize those values and refer to all of them with a single name. By grouping values together, we can write code that performs a computation on many pieces of data at once.
# 
# Calling the function `make_array` on several values places them into an *array*, which is a kind of sequential collection. Below, we collect four different temperatures into an array called `highs`. These are the [estimated average daily high temperatures](http://berkeleyearth.lbl.gov/regions/global-land) over all land on Earth (in degrees Celsius) for the decades surrounding 1850, 1900, 1950, and 2000, respectively, expressed as deviations from the average absolute high temperature between 1951 and 1980, which was 14.48 degrees.

# In[2]:


baseline_high = 14.48
highs = make_array(baseline_high - 0.880, baseline_high - 0.093,
                   baseline_high + 0.105, baseline_high + 0.684)
highs


# Collections allow us to pass multiple values into a function using a single name. For instance, the `sum` function computes the sum of all values in a collection, and the `len` function computes its length. (That's the number of values we put in it.) Using them together, we can compute the average of a collection.

# In[3]:


sum(highs)/len(highs)


# The complete chart of daily high and low temperatures appears below. 
# 
# <h2>Mean of Daily High Temperature</h2>
# 
# ![Mean of Daily High Temperature](../../images/global-land-TMAX-Trend.png)
# 
# <h2>Mean of Daily Low Temperature</h2>
# 
# ![Mean of Daily Low Temperature](../../images/global-land-TMIN-Trend.png)

# 
# ```{toctree}
# :hidden:
# :titlesonly:
# 
# 
# Arrays <1/Arrays>
# Ranges <2/Ranges>
# More on Arrays <3/More_on_Arrays>
# ```
# 
