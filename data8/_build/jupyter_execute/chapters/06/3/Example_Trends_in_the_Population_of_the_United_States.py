#!/usr/bin/env python
# coding: utf-8

# In[1]:


from datascience import *
import numpy as np
path_data = '../../../assets/data/'
np.set_printoptions(threshold=50)


# # Example: Population Trends
# 
# We are now ready to work with large tables of data. The file below contains "Annual Estimates of the Resident Population by Single Year of Age and Sex for the United States." Notice that `read_table` can read data directly from a URL.

# In[2]:


# As of Jan 2017, this census file is online here: 
data = 'http://www2.census.gov/programs-surveys/popest/datasets/2010-2015/national/asrh/nc-est2015-agesex-res.csv'

# A local copy can be accessed here in case census.gov moves the file:
# data = path_data + 'nc-est2015-agesex-res.csv'

full_census_table = Table.read_table(data)
full_census_table


# Only the first 10 rows of the table are displayed. Later we will see how to display the entire table; however, this is typically not useful with large tables.
# 
# a [description of the table](http://www2.census.gov/programs-surveys/popest/datasets/2010-2015/national/asrh/nc-est2015-agesex-res.pdf) appears online. The `SEX` column contains numeric codes: `0` stands for the total, `1` for male, and `2` for female. The `AGE` column contains ages in completed years, but the special value `999` is a sum of the total population. The rest of the columns contain estimates of the US population.
# 
# Typically, a public table will contain more information than necessary for a particular investigation or analysis. In this case, let us suppose that we are only interested in the population changes from 2010 to 2014. Let us `select` the relevant columns.

# In[3]:


partial_census_table = full_census_table.select('SEX', 'AGE', 'POPESTIMATE2010', 'POPESTIMATE2014')
partial_census_table


# We can also simplify the labels of the selected columns.

# In[4]:


us_pop = partial_census_table.relabeled('POPESTIMATE2010', '2010').relabeled('POPESTIMATE2014', '2014')
us_pop


# We now have a table that is easy to work with. Each column of the table is an array of the same length, and so columns can be combined using arithmetic. Here is the change in population between 2010 and 2014.

# In[5]:


us_pop.column('2014') - us_pop.column('2010')


# Let us augment `us_pop` with a column that contains these changes, both in absolute terms and as percents relative to the value in 2010.

# In[6]:


change = us_pop.column('2014') - us_pop.column('2010')
census = us_pop.with_columns(
    'Change', change,
    'Percent Change', change/us_pop.column('2010')
)
census.set_format('Percent Change', PercentFormatter)


# **Sorting the data.** Let us sort the table in decreasing order of the absolute change in population.

# In[7]:


census.sort('Change', descending=True)


# Not surprisingly, the top row of the sorted table is the line that corresponds to the entire population: both sexes and all age groups. From 2010 to 2014, the population of the United States increased by about 9.5 million people, a change of just over 3%.
# 
# The next two rows correspond to all the men and all the women respectively. The male population grew more than the female population, both in absolute and percentage terms. Both percent changes were around 3%.
# 
# Now take a look at the next few rows. The percent change jumps from about 3% for the overall population to almost 30% for the people in their late sixties and early seventies. This stunning change contributes to what is known as the greying of America.
# 
# By far the greatest absolute change was among those in the 64-67 agegroup in 2014. What could explain this large increase? We can explore this question by examining the years in which the relevant groups were born.
# 
# - Those who were in the 64-67 age group in 2010 were born in the years 1943 to 1946. The attack on Pearl Harbor was in late 1941, and by 1942 U.S. forces were heavily engaged in a massive war that ended in 1945. 
# 
# - Those who were 64 to 67 years old in 2014 were born in the years 1947 to 1950, at the height of the post-WWII baby boom in the United States. 
# 
# The post-war jump in births is the major reason for the large changes that we have observed.
