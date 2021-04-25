#!/usr/bin/env python
# coding: utf-8

# In[1]:


from datascience import *
path_data = '../../../assets/data/'
import matplotlib
matplotlib.use('Agg')
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plots
plots.style.use('fivethirtyeight')
import numpy as np


# # Classifying by One Variable
# 
# Data scientists often need to classify individuals into groups according to shared features, and then identify some characteristics of the groups. For example, in the example using Galton's data on heights, we saw that it was useful to classify families according to the parents' midparent heights, and then find the average height of the children in each group.
# 
# This section is about classifying individuals into categories that are not numerical. We begin by recalling the basic use of `group`. 

# ## Counting the Number in Each Category
# The `group` method with a single argument counts the number of rows for each category in a column. The result contains one row per unique value in the grouped column.
# 
# Here is a small table of data on ice cream cones. The `group` method can be used to list the distinct flavors and provide the counts of each flavor.

# In[2]:


cones = Table().with_columns(
    'Flavor', make_array('strawberry', 'chocolate', 'chocolate', 'strawberry', 'chocolate'),
    'Price', make_array(3.55, 4.75, 6.55, 5.25, 5.25)
)
cones


# In[3]:


cones.group('Flavor')


# There are two distinct categories, chocolate and strawberry. The call to `group` creates a table of counts in each category. The column is called `count` by default, and contains the number of rows in each category.
# 
# Notice that this can all be worked out from just the `Flavor` column. The `Price` column has not been used.
# 
# But what if we wanted the total price of the cones of each different flavor? That's where the second argument of `group` comes in.

# ## Finding a Characteristic of Each Category
# The optional second argument of `group` names the function that will be used to aggregate values in other columns for all of those rows. For instance, `sum` will sum up the prices in all rows that match each category. This result also contains one row per unique value in the grouped column, but it has the same number of columns as the original table.
# 
# To find the total price of each flavor, we call `group` again, with `Flavor` as its first argument as before. But this time there is a second argument: the function name `sum`.

# In[4]:


cones.group('Flavor', sum)


# To create this new table, `group` has calculated the sum of the `Price` entries in all the rows corresponding to each distinct flavor. The prices in the three `chocolate` rows add up to $\$16.55$ (you can assume that price is being measured in dollars). The prices in the two `strawberry` rows have a total of $\$8.80$.
# 
# The label of the newly created "sum" column is `Price sum`, which is created by taking the label of the column being summed, and appending the word `sum`. 
# 
# Because `group` finds the `sum` of all columns other than the one with the categories, there is no need to specify that it has to `sum` the prices.
# 
# To see in more detail what `group` is doing, notice that you could have figured out the total prices yourself, not only by mental arithmetic but also using code. For example, to find the total price of all the chocolate cones, you could start by creating a new table consisting of only the chocolate cones, and then accessing the column of prices:

# In[5]:


cones.where('Flavor', are.equal_to('chocolate')).column('Price')


# In[6]:


sum(cones.where('Flavor', are.equal_to('chocolate')).column('Price'))


# This is what `group` is doing for each distinct value in `Flavor`.

# In[7]:


# For each distinct value in `Flavor, access all the rows
# and create an array of `Price`

cones_choc = cones.where('Flavor', are.equal_to('chocolate')).column('Price')
cones_strawb = cones.where('Flavor', are.equal_to('strawberry')).column('Price')

# Display the arrays in a table

grouped_cones = Table().with_columns(
    'Flavor', make_array('chocolate', 'strawberry'),
    'Array of All the Prices', make_array(cones_choc, cones_strawb)
)

# Append a column with the sum of the `Price` values in each array

price_totals = grouped_cones.with_column(
    'Sum of the Array', make_array(sum(cones_choc), sum(cones_strawb))
)
price_totals


# You can replace `sum` by any other functions that work on arrays. For example, you could use `max` to find the largest price in each category:

# In[8]:


cones.group('Flavor', max)


# Once again, `group` creates arrays of the prices in each `Flavor` category. But now it finds the `max` of each array:

# In[9]:


price_maxes = grouped_cones.with_column(
    'Max of the Array', make_array(max(cones_choc), max(cones_strawb))
)
price_maxes


# Indeed, the original call to `group` with just one argument has the same effect as using `len` as the function and then cleaning up the table.

# In[10]:


lengths = grouped_cones.with_column(
    'Length of the Array', make_array(len(cones_choc), len(cones_strawb))
)
lengths


# ## Example: NBA Salaries
# The table `nba` contains data on the 2015-2016 players in the National Basketball Association. We have examined these data earlier. Recall that salaries are measured in millions of dollars.

# In[11]:


nba1 = Table.read_table(path_data + 'nba_salaries.csv')
nba = nba1.relabeled("'15-'16 SALARY", 'SALARY')
nba


# **1.** How much money did each team pay for its players' salaries?
# 
# The only columns involved are `TEAM` and `SALARY`. We have to `group` the rows by `TEAM` and then `sum` the salaries of the groups. 

# In[12]:


teams_and_money = nba.select('TEAM', 'SALARY')
teams_and_money.group('TEAM', sum)


# **2.** How many NBA players were there in each of the five positions?
# 
# We have to classify by `POSITION`, and count. This can be done with just one argument to group:

# In[13]:


nba.group('POSITION')


# **3.** What was the average salary of the players at each of the five positions?
# 
# This time, we have to group by `POSITION` and take the mean of the salaries. For clarity, we will work with a table of just the positions and the salaries.

# In[14]:


positions_and_money = nba.select('POSITION', 'SALARY')
positions_and_money.group('POSITION', np.mean)


# Center was the most highly paid position, at an average of over 6 million dollars.
# 
# If we had not selected the two columns as our first step, `group` would not attempt to "average" the categorical columns in `nba`. (It is impossible to average two strings like "Atlanta Hawks" and "Boston Celtics".) It performs arithmetic only on numerical columns and leaves the rest blank.

# In[15]:


nba.group('POSITION', np.mean)

