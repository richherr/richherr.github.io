#!/usr/bin/env python
# coding: utf-8

# In[1]:


from datascience import *
import numpy as np
path_data = '../../../assets/data/'
np.set_printoptions(threshold=50)


# In[2]:


nba_salaries = Table.read_table(path_data + 'nba_salaries.csv')
nba = nba_salaries.relabeled("'15-'16 SALARY", 'SALARY')


# # Selecting Rows
# 
# Often, we would like to extract just those rows that correspond to entries with a particular feature. For example, we might want only the rows corresponding to the Warriors, or to players who earned more than $\$10$ million. Or we might just want the top five earners.

# ## Specified Rows
# The Table method `take` does just that – it takes a specified set of rows. Its argument is a row index or array of indices, and it creates a new table consisting of only those rows.
# 
# For example, if we wanted just the first row of `nba`, we could use `take` as follows.

# In[3]:


nba


# In[4]:


nba.take(0)


# This is a new table with just the single row that we specified.
# 
# We could also get the fourth, fifth, and sixth rows by specifying a range of indices as the argument.

# In[5]:


nba.take(np.arange(3, 6))


# If we want a table of the top 5 highest paid players, we can first sort the list by salary and then `take` the first five rows:

# In[6]:


nba.sort('SALARY', descending=True).take(np.arange(5))


# ## Rows Corresponding to a Specified Feature
# More often, we will want to access data in a set of rows that have a certain feature, but whose indices we don't know ahead of time. For example, we might want data on all the players who made more than $\$10$ million, but we don't want to spend time counting rows in the sorted table.
# 
# The method `where` does the job for us. Its output is a table with the same columns as the original but only the rows *where* the feature occurs.
# 
# The first argument of `where` is the label of the column that contains the information about whether or not a row has the feature we want. If the feature is "made more than $\$10$ million", the column is `SALARY`.
# 
# The second argument of `where` is a way of specifying the feature. A couple of examples will make the general method of specification easier to understand.
# 
# In the first example, we extract the data for all those who earned more than $\$10$ million.

# In[7]:


nba.where('SALARY', are.above(10))


# The use of the argument `are.above(10)` ensured that each selected row had a value of `SALARY` that was greater than 10.
# 
# There are 69 rows in the new table, corresponding to the 69 players who made more than $10$ million dollars. Arranging these rows in order makes the data easier to analyze. DeMar DeRozan of the Toronto Raptors was the "poorest" of this group, at a salary of just over $10$ million dollars.

# In[8]:


nba.where('SALARY', are.above(10)).sort('SALARY')


# How much did Stephen Curry make? For the answer, we have to access the row where the value of `PLAYER` is equal to `Stephen Curry`. That is placed a table consisting of just one line:

# In[9]:


nba.where('PLAYER', are.equal_to('Stephen Curry'))


# Curry made just under $\$11.4$ million dollars. That's a lot of money, but it's less than half the salary of LeBron James. You'll find that salary in the "Top 5" table earlier in this section, or you could find it replacing `'Stephen Curry'` by `'LeBron James'` in the line of code above.
# 
# In the code, `are` is used again, but this time with the *predicate* `equal_to` instead of `above`. Thus for example you can get a table of all the Warriors:

# In[10]:


nba.where('TEAM', are.equal_to('Golden State Warriors')).show()


# This portion of the table is already sorted by salary, because the original table listed players sorted by salary within the same team. The `.show()` at the end of the line ensures that all rows are shown, not just the first 10.
# 
# It is so common to ask for the rows for which some column is equal to some value that the `are.equal_to` call is optional. Instead, the `where` method can be called with only a column name and a value to achieve the same effect.

# In[11]:


nba.where('TEAM', 'Denver Nuggets') # equivalent to nba.where('TEAM', are.equal_to('Denver Nuggets'))


# ## Multiple Features
# You can access rows that have multiple specified features, by using `where` repeatedly. For example, here is a way to extract all the Point Guards whose salaries were over $\$15$ million.

# In[12]:


nba.where('POSITION', 'PG').where('SALARY', are.above(15))


# ## General Form
# By now you will have realized that the general way to create a new table by selecting rows with a given feature is to use `where` and `are` with the appropriate condition:
# 
# `original_table_name.where(column_label_string, are.condition)`

# In[13]:


nba.where('SALARY', are.between(10, 10.3))


# Notice that the table above includes Danny Green who made $\$10$ million, but *not* Monta Ellis who made $\$10.3$ million. As elsewhere in Python, the range `between` includes the left end but not the right.

# If we specify a condition that isn't satisfied by any row, we get a table with column labels but no rows.

# In[14]:


nba.where('PLAYER', are.equal_to('Barack Obama'))


# ## Some More Conditions
# Here are some predicates of `are` that you might find useful. Note that `x` and `y` are numbers, `STRING` is a string, and `Z` is either a number or a string; you have to specify these depending on the feature you want.
# 
# | **Predicate**              | Description                              |
# |----------------------------|------------------------------------------|
# | `are.equal_to(Z)`          | Equal to `Z`                             |        
# | `are.above(x)`             | Greater than `x`                         |
# | `are.above_or_equal_to(x)` | Greater than or equal to `x`             |
# | `are.below(x)`             | Less than `x`                            |
# | `are.below_or_equal_to(x)` | Less than or equal to `x`                |
# | `are.between(x, y)`        | Greater than or equal to `x`, and less than `y` |
# | `are.strictly_between(x, y)` | Greater than `x` and less than `y`     |
# | `are.between_or_equal_to(x, y)` | Greater than or equal to `x`, and less than or equal to `y` |
# | `are.containing(S)`        | Contains the string `S`                   |         

# You can also specify the negation of any of these conditions, by using `.not_` before the condition:
# 
# | **Predicate**              | Description                              |
# |----------------------------|------------------------------------------|
# | `are.not_equal_to(Z)`      | Not equal to `Z`                         |    
# | `are.not_above(x)`         | Not above `x`                            |

# ... and so on. The usual rules of logic apply – for example, "not above x" is the same as "below or equal to x".

# We end the section with a series of examples. 

# The use of `are.containing` can help save some typing. For example, you can just specify `Warriors` instead of `Golden State Warriors`:

# In[15]:


nba.where('TEAM', are.containing('Warriors')).show()


# You can extract data for all the guards, both Point Guards and Shooting Guards:

# In[16]:


nba.where('POSITION', are.containing('G'))


# You can get all the players who were not Cleveland Cavaliers and had a salary of no less than $\$20$ million:

# In[17]:


other_than_Cavs = nba.where('TEAM', are.not_equal_to('Cleveland Cavaliers'))
other_than_Cavs.where('SALARY', are.not_below(20))


# The same table can be created in many ways. Here is another, and no doubt you can think of more.

# In[18]:


other_than_Cavs.where('SALARY', are.above_or_equal_to(20))


# As you can see, the use of `where` with `are` gives you great flexibility in accessing rows with features that interest you. Don't hesitate to experiment!
