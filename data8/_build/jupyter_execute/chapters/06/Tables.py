#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
np.set_printoptions(threshold=50)
path_data = '../../assets/data/'


# # Tables
# 
# Tables are a fundamental object type for representing data sets. A table can be viewed in two ways:
# * a sequence of named columns that each describe a single aspect of all entries in a data set, or
# * a sequence of rows that each contain all information about a single entry in a data set.
# 
# In order to use tables, import all of the module called `datascience`, a module created for this text.

# In[2]:


from datascience import *


# Empty tables can be created using the `Table` function. An empty table is useful because it can be extended to contain new rows and columns.

# In[3]:


Table()


# The `with_columns` method on a table constructs a new table with additional labeled columns. Each column of a table is an array. To add one new column to a table, call `with_columns` with a label and an array. (The `with_column` method can be used with the same effect.)
# 
# Below, we begin each example with an empty table that has no columns. 

# In[4]:


Table().with_columns('Number of petals', make_array(8, 34, 5))


# To add two (or more) new columns, provide the label and array for each column. All columns must have the same length, or an error will occur.

# In[5]:


Table().with_columns(
    'Number of petals', make_array(8, 34, 5),
    'Name', make_array('lotus', 'sunflower', 'rose')
)


# We can give this table a name, and then extend the table with another column.

# In[6]:


flowers = Table().with_columns(
    'Number of petals', make_array(8, 34, 5),
    'Name', make_array('lotus', 'sunflower', 'rose')
)

flowers.with_columns(
    'Color', make_array('pink', 'yellow', 'red')
)


# The `with_columns` method creates a new table each time it is called, so the original table is not affected. For example, the table `flowers` still has only the two columns that it had when it was created.

# In[7]:


flowers


# Creating tables in this way involves a lot of typing. If the data have already been entered somewhere, it is usually possible to use Python to read it into a table, instead of typing it all in cell by cell.
# 
# Often, tables are created from files that contain comma-separated values. Such files are called CSV files.
# 
# Below, we use the Table method `read_table` to read a CSV file that contains some of the data used by Minard in his graphic about Napoleon's Russian campaign. The data are placed in a table named `minard`.

# In[8]:


minard = Table.read_table(path_data + 'minard.csv')
minard


# We will use this small table to demonstrate some useful Table methods. We will then use those same methods, and develop other methods, on much larger tables of data.

# <h2>The Size of the Table</h2>
# 
# The method `num_columns` gives the number of columns in the table, and `num_rows` the number of rows.

# In[9]:


minard.num_columns


# In[10]:


minard.num_rows


# <h2>Column Labels</h2>
# 
# The method `labels` can be used to list the labels of all the columns. With `minard` we don't gain much by this, but it can be very useful for tables that are so large that not all columns are visible on the screen.

# In[11]:


minard.labels


# We can change column labels using the `relabeled` method. This creates a new table and leaves `minard` unchanged.

# In[12]:


minard.relabeled('City', 'City Name')


# However, this method does not change the original table. 

# In[13]:


minard


# A common pattern is to assign the original name `minard` to the new table, so that all future uses of `minard` will refer to the relabeled table.

# In[14]:


minard = minard.relabeled('City', 'City Name')
minard


# <h2>Accessing the Data in a Column</h2>
# 
# We can use a column's label to access the array of data in the column.

# In[15]:


minard.column('Survivors')


# The 5 columns are indexed 0, 1, 2, 3, and 4. The column `Survivors` can also be accessed by using its column index.

# In[16]:


minard.column(4)


# The 8 items in the array are indexed 0, 1, 2, and so on, up to 7. The items in the column can be accessed using `item`, as with any array.

# In[17]:


minard.column(4).item(0)


# In[18]:


minard.column(4).item(5)


# <h2>Working with the Data in a Column</h2>
# 
# Because columns are arrays, we can use array operations on them to discover new information. For example, we can create a new column that contains the percent of all survivors at each city after Smolensk.

# In[19]:


initial = minard.column('Survivors').item(0)
minard = minard.with_columns(
    'Percent Surviving', minard.column('Survivors')/initial
)
minard


# To make the proportions in the new columns appear as percents, we can use the method `set_format` with the option `PercentFormatter`. The `set_format` method takes `Formatter` objects, which exist for dates (`DateFormatter`), currencies (`CurrencyFormatter`), numbers, and percentages.

# In[20]:


minard.set_format('Percent Surviving', PercentFormatter)


# <h2>Choosing Sets of Columns</h2>
# 
# The method `select` creates a new table that contains only the specified columns.

# In[21]:


minard.select('Longitude', 'Latitude')


# The same selection can be made using column indices instead of labels.

# In[22]:


minard.select(0, 1)


# The result of using `select` is a new table, even when you select just one column.

# In[23]:


minard.select('Survivors')


# Notice that the result is a table, unlike the result of `column`, which is an array.

# In[24]:


minard.column('Survivors')


# Another way to create a new table consisting of a set of columns is to `drop` the columns you don't want.

# In[25]:


minard.drop('Longitude', 'Latitude', 'Direction')


# Neither `select` nor `drop` change the original table. Instead, they create new smaller tables that share the same data. The fact that the original table is preserved is useful! You can generate multiple different tables that only consider certain columns without worrying that one analysis will affect the other.

# In[26]:


minard


# All of the methods that we have used above can be applied to any table.

# 
# ```{toctree}
# :hidden:
# :titlesonly:
# 
# 
# Sorting Rows <1/Sorting_Rows>
# Selecting Rows <2/Selecting_Rows>
# Example: Population Trends <3/Example_Trends_in_the_Population_of_the_United_States>
# Example: Trends in Gender <4/Example_Gender_Ratio_in_the_US_Population>
# ```
# 
