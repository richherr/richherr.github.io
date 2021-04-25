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


# # Joining Tables by Columns
# Often, data about the same individuals is maintained in more than one table. For example, one university office might have data about each student's time to completion of degree, while another has data about the student's tuition and financial aid.
# 
# To understand the students' experience, it may be helpful to put the two datasets together. If the data are in two tables, each with one row per student, then we would want to put the columns together, making sure to match the rows so that each student's information remains on a single row.
# 
# Let us do this in the context of a simple example, and then use the method with a larger dataset.

# The table `cones` is one we have encountered earlier. Now suppose each flavor of ice cream comes with a rating that is in a separate table.

# In[2]:


cones = Table().with_columns(
    'Flavor', make_array('strawberry', 'vanilla', 'chocolate', 'strawberry', 'chocolate'),
    'Price', make_array(3.55, 4.75, 6.55, 5.25, 5.75)
)
cones


# In[3]:


ratings = Table().with_columns(
    'Kind', make_array('strawberry', 'chocolate', 'vanilla'),
    'Stars', make_array(2.5, 3.5, 4)
)
ratings


# Each of the tables has a column that contains ice cream flavors: `cones` has the column `Flavor`, and `ratings` has the column `Kind`. The entries in these columns can be used to link the two tables.
# 
# The method `join` creates a new table in which each cone in the `cones` table is augmented with the Stars information in the `ratings` table.  For each cone in `cones`, `join` finds a row in `ratings` whose `Kind` matches the cone's `Flavor`. We have to tell `join` to use those columns for matching.

# In[4]:


rated = cones.join('Flavor', ratings, 'Kind')
rated


# Each cone now has not only its price but also the rating of its flavor.
# 
# In general, a call to `join` that augments a table (say `table1`) with information from another table (say `table2`) looks like this:
# 
#     table1.join(table1_column_for_joining, table2, table2_column_for_joining)
# 
# The new table `rated` allows us to work out the price per star, which you can think of as an informal measure of value. Low values are good – they mean that you are paying less for each rating star.

# In[5]:


rated.with_column('$/Star', rated.column('Price') / rated.column('Stars')).sort(3)


# Though strawberry has the lowest rating among the three flavors, the less expensive strawberry cone does well on this measure because it doesn't cost a lot per star.

# **Side note.** Does the order we list the two tables matter? Let's try it.  As you see it, this changes the order that the columns appear in, and can potentially changes the order of the rows, but it doesn't make any fundamental difference.

# In[6]:


ratings.join('Kind', cones, 'Flavor')


# Also note that the join will only contain information about items that appear in both tables. Let's see an example. Suppose there is a table of reviews of some ice cream cones, and we have found the average review for each flavor.

# In[7]:


reviews = Table().with_columns(
    'Flavor', make_array('vanilla', 'chocolate', 'vanilla', 'chocolate'),
    'Stars', make_array(5, 3, 5, 4)
)
reviews


# In[8]:


average_review = reviews.group('Flavor', np.average)
average_review


# We can join `cones` and `average_review` by providing the labels of the columns by which to join.

# In[9]:


cones.join('Flavor', average_review, 'Flavor')


# Notice how the strawberry cones have disappeared. None of the reviews are for strawberry cones, so there is nothing to which the `strawberry` rows can be joined. This might be a problem, or it might not be - that depends on the analysis we are trying to perform with the joined table.
