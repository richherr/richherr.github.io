#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib
#matplotlib.use('Agg')
path_data = '../../../assets/data/'
from datascience import *
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plots
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math
import scipy.stats as stats
plots.style.use('fivethirtyeight')


# # Rows of Tables
# Now that we have a qualitative understanding of nearest neighbor classification, it's time to implement our classifier.
# 
# Until this chapter, we have worked mostly with single columns of tables. But now we have to see whether one *individual* is "close" to another. Data for individuals are contained in *rows* of tables.
# 
# So let's start by taking a closer look at rows.

# In[2]:


def standard_units(x):
    return (x - np.mean(x))/np.std(x)


# Here is the original table `ckd` containing data on patients who were tested for chronic kidney disease.

# In[3]:


ckd = Table.read_table(path_data + 'ckd.csv').relabeled('Blood Glucose Random', 'Glucose')


# The data corresponding to the first patient is in row 0 of the table, consistent with Python's indexing system. The Table method `row` accesses the row by taking the index of the row as its argument:

# In[4]:


ckd.row(0)


# Rows have their very own data type: they are *row objects*. Notice how the display shows not only the values in the row but also the labels of the corresponding columns.
# 
# Rows are in general **not arrays**, as their elements can be of different types. For example, some of the elements of the row above are strings (like `'abnormal'`) and some are numerical. So the row can't be converted into an array.
# 
# However, rows share some characteristics with arrays.  You can use `item` to access a particular element of a row. For example, to access the Albumin level of Patient 0, we can look at the labels in the printout of the row above to find that it's item 3:

# In[5]:


ckd.row(0).item(3)


# ## Converting Rows to Arrays (When Possible)
# Rows whose elements are all numerical (or all strings) can be converted to arrays.  Converting a row to an array gives us access to arithmetic operations and other nice NumPy functions, so it is often useful.
# 
# Recall that in the previous section we tried to classify the patients as 'CKD' or 'not CKD', based on two attributes `Hemoglobin` and `Glucose`, both measured in standard units. 

# In[6]:


ckd = Table().with_columns(
    'Hemoglobin', standard_units(ckd.column('Hemoglobin')),
    'Glucose', standard_units(ckd.column('Glucose')),
    'Class', ckd.column('Class')
)

color_table = Table().with_columns(
    'Class', make_array(1, 0),
    'Color', make_array('darkblue', 'gold')
)
ckd = ckd.join('Class', color_table)
ckd


# Here is a scatter plot of the two attributes, along with a red point corresponding to Alice, a new patient. Her value of hemoglobin is 0 (that is, at the average) and glucose 1.1 (that is, 1.1 SDs above average).

# In[7]:


alice = make_array(0, 1.1)
ckd.scatter('Hemoglobin', 'Glucose', group='Color')
plots.scatter(alice.item(0), alice.item(1), color='red', s=30);


# To find the distance between Alice's point and any of the other points, we only need the values of the attributes:

# In[8]:


ckd_attributes = ckd.select('Hemoglobin', 'Glucose')


# In[9]:


ckd_attributes


# Each row consists of the coordinates of one point in our training sample. **Because the rows now consist only of numerical values**, it is possible to convert them to arrays.  For this, we use the function `np.array`, which converts any kind of sequential object, like a row, to an array. (Our old friend `make_array` is for *creating* arrays, not for *converting* other kinds of sequences to arrays.)

# In[10]:


ckd_attributes.row(3)


# In[11]:


np.array(ckd_attributes.row(3))


# This is very handy because we can now use array operations on the data in each row.

# ## Distance Between Points When There are Two Attributes
# The main calculation we need to do is to find the distance between Alice's point and any other point. For this, the first thing we need is a way to compute the distance between any pair of points. 
# 
# How do we do this?  In 2-dimensional space, it's pretty easy.  If we have a point at coordinates $(x_0,y_0)$ and another at $(x_1,y_1)$, the distance between them is
# 
# $$
# D = \sqrt{(x_0-x_1)^2 + (y_0-y_1)^2}
# $$
# 
# (Where did this come from?  It comes from the Pythogorean theorem: we have a right triangle with side lengths $x_0-x_1$ and $y_0-y_1$, and we want to find the length of the hypotenuse.)
# 
# 

# In the next section we'll see that this formula has a straightforward extension when there are more than two attributes. For now, let's use the formula and array operations to find the distance between Alice and the patient in Row 3.

# In[12]:


patient3 = np.array(ckd_attributes.row(3))
alice, patient3


# In[13]:


distance = np.sqrt(np.sum((alice - patient3)**2))
distance


# We're going to need the distance between Alice and a bunch of points, so let's write a function called `distance` that computes the distance between any pair of points. The function will take two arrays, each containing the $(x, y)$ coordinates of a point.  (Remember, those are really the Hemoglobin and Glucose levels of a patient.)

# In[14]:


def distance(point1, point2):
    """Returns the Euclidean distance between point1 and point2.
    
    Each argument is an array containing the coordinates of a point."""
    return np.sqrt(np.sum((point1 - point2)**2))


# In[15]:


distance(alice, patient3)


# We have begun to build our classifier: the `distance` function is the first building block. Now let's work on the next piece.

# ## Using `apply` on an Entire Row
# Recall that if you want to apply a function to each element of a column of a table, one way to do that is by the call `table_name.apply(function_name, column_label)`. This evaluates to an array consisting of the values of the function when we call it on each element of the column. So each entry of the array is based on the corresponding row of the table.
# 
# If you use `apply` without specifying a column label, then the entire row is passed to the function. Let's see how this works on a very small table `t` containing the information about the first five patients in the training sample.

# In[16]:


t = ckd_attributes.take(np.arange(5))
t


# Just as an example, suppose that for each patient we want to know how unusual their most unusual attribute is.  Concretely, if a patient's hemoglobin level is further from the average than her glucose level, we want to know how far it is from the average.  If her glucose level is further from the average than her hemoglobin level, we want to know how far that is from the average instead.
# 
# That's the same as taking the maximum of the absolute values of the two quantities. To do this for a particular row, we can convert the row to an array and use array operations.

# In[17]:


def max_abs(row):
    return np.max(np.abs(np.array(row)))


# In[18]:


max_abs(t.row(4))


# And now we can apply `max_abs` to each row of the table `t`:

# In[19]:


t.apply(max_abs)


# This way of using `apply` will help us create the next building block of our classifier.

# ## Alice's $k$ Nearest Neighbors
# If we want to classify Alice using a k-nearest neighbor classifier, we have to identify her $k$ nearest neighbors. What are the steps in this process? Suppose $k = 5$. Then the steps are:
# - **Step 1.** Find the distance between Alice and each point in the training sample.
# - **Step 2.** Sort the data table in increasing order of the distances.
# - **Step 3.** Take the top 5 rows of the sorted table.
# 
# Steps 2 and 3 seem straightforward, provided we have the distances. So let's focus on Step 1.
# 
# Here's Alice:

# In[20]:


alice


# What we need is a function that finds the distance between Alice and another point whose coordinates are contained in a row. The function `distance` returns the distance between any two points whose coordinates are in arrays. We can use that to define `distance_from_alice`, which takes a row as its argument and returns the distance between that row and Alice.

# In[21]:


def distance_from_alice(row):
    """Returns distance between Alice and a row of the attributes table"""
    return distance(alice, np.array(row))


# In[22]:


distance_from_alice(ckd_attributes.row(3))


# Now we can `apply` the function `distance_from_alice` to each row of `ckd_attributes`, and augment the table `ckd` with the distances. Step 1 is complete!

# In[23]:


distances = ckd_attributes.apply(distance_from_alice)
ckd_with_distances = ckd.with_column('Distance from Alice', distances)


# In[24]:


ckd_with_distances


# For Step 2, let's sort the table in increasing order of distance:

# In[25]:


sorted_by_distance = ckd_with_distances.sort('Distance from Alice')
sorted_by_distance


# Step 3: The top 5 rows correspond to Alice's 5 nearest neighbors; you can replace 5 by any other positive integer.

# In[26]:


alice_5_nearest_neighbors = sorted_by_distance.take(np.arange(5))
alice_5_nearest_neighbors


# Three of Alice's five nearest neighbors are blue points and two are gold. So a 5-nearest neighbor classifier would classify Alice as blue: it would predict that Alice has chronic kidney disease.
# 
# The graph below zooms in on Alice and her five nearest neighbors. The two gold ones just inside the circle directly below the red point. The classifier says Alice is more like the three blue ones around her.

# In[27]:


plots.figure(figsize=(8,8))
plots.scatter(ckd.column('Hemoglobin'), ckd.column('Glucose'), c=ckd.column('Color'), s=40)
#ckd.scatter('Hemoglobin', 'Glucose', group='Color')
plots.scatter(alice.item(0), alice.item(1), color='red', s=40)
radius = sorted_by_distance.column('Distance from Alice').item(4)+0.014
theta = np.arange(0, 2*np.pi+1, 2*np.pi/200)
plots.plot(radius*np.cos(theta)+alice.item(0), radius*np.sin(theta)+alice.item(1), color='g', lw=1.5);
plots.xlim(-2, 2.5)
plots.ylim(-2, 2.5);


# We are well on our way to implementing our k-nearest neighbor classifier. In the next two sections we will put it together and assess its accuracy.
