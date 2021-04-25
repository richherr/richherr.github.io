#!/usr/bin/env python
# coding: utf-8

# In[1]:


from datascience import *
import numpy as np
path_data = '../../../assets/data/'
np.set_printoptions(threshold=50)


# # Sorting Rows
# 
# "The NBA is the highest paying professional sports league in the world," [reported CNN](http://edition.cnn.com/2015/12/04/sport/gallery/highest-paid-nba-players/) in March 2016. The table `nba_salaries` contains the salaries of all National Basketball Association players in 2015-2016.
# 
# Each row represents one player. The columns are:
# 
# | **Column Label**   | Description                                         |
# |--------------------|-----------------------------------------------------|
# | `PLAYER`           | Player's name                                       |
# | `POSITION`         | Player's position on team                           |
# | `TEAM`             | Team name                                           |
# |`'15-'16 SALARY`    | Player's salary in 2015-2016, in millions of dollars|
#  
# The code for the positions is PG (Point Guard), SG (Shooting Guard), PF (Power Forward), SF (Small Forward), and C (Center). But what follows doesn't involve details about how basketball is played.
# 
# The first row shows that Paul Millsap, Power Forward for the Atlanta Hawks, had a salary of almost $\$18.7$ million in 2015-2016.

# In[2]:


# This table can be found online: https://www.statcrunch.com/app/index.php?dataid=1843341
nba_salaries = Table.read_table(path_data + 'nba_salaries.csv')
nba_salaries


# The table contains 417 rows, one for each player. Only 10 of the rows are displayed. The `show` method allows us to specify the number of rows, with the default (no specification) being all the rows of the table.

# In[3]:


nba_salaries.show(3)


# Glance through about 20 rows or so, and you will see that the rows are in alphabetical order by team name. It's also possible to list the same rows in alphabetical order by player name using the `sort` method. The argument to `sort` is a column label or index.

# In[4]:


nba_salaries.sort('PLAYER').show(5)


# To examine the players' salaries, it would be much more helpful if the data were ordered by salary.
# 
# To do this, we will first simplify the label of the column of salaries (just for convenience), and then sort by the new label `SALARY`. 
# 
# This arranges all the rows of the table in *increasing* order of salary, with the lowest salary appearing first. The output is a new table with the same columns as the original but with the rows rearranged.

# In[5]:


nba = nba_salaries.relabeled("'15-'16 SALARY", 'SALARY')
nba.sort('SALARY')


# These figures are somewhat difficult to compare as some of these players changed teams during the season and received salaries from more than one team; only the salary from the last team appears in the table. Point Guard Phil Pressey, for example, moved from Philadelphia to Phoenix during the year, and might be moving yet again to the Golden State Warriors. 
# 
# The CNN report is about the other end of the salary scale – the players who are among the highest paid in the world. 
# 
# To order the rows of the table in *decreasing* order of salary, we must use `sort` with the option `descending=True`.

# In[6]:


nba.sort('SALARY', descending=True)


# Kobe Bryant, in his final season with the Lakers, was the highest paid at a salary of $\$25$ million. Notice that the MVP Stephen Curry doesn't appear among the top 10. He is quite a bit further down the list, as we will see later.

# ## Named Arguments
# 
# The `descending=True` portion of this call expression is called a *named argument*. When a function or method is called, each argument has both a position and a name. Both are evident from the help text of a function or method.

# In[7]:


help(nba.sort)


# At the very top of this `help` text, the *signature* of the `sort` method appears:
# 
#     sort(column_or_label, descending=False, distinct=False)
#     
# This describes the positions, names, and default values of the three arguments to `sort`. When calling this method, you can use either positional arguments or named arguments, so the following three calls do exactly the same thing.
# 
#     sort('SALARY', True)
#     sort('SALARY', descending=True)
#     sort(column_or_label='SALARY', descending=True)
#     
# When an argument is simply `True` or `False`, it's a useful convention to include the argument name so that it's more obvious what the argument value means.
