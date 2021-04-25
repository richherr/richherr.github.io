#!/usr/bin/env python
# coding: utf-8

# # Call Expressions
# 
# *Call expressions* invoke functions, which are named operations. The name of the function appears first, followed by expressions in parentheses. 

# In[1]:


abs(-12)


# In[2]:


round(5 - 1.3)


# In[3]:


max(2, 2 + 3, 4)


# In this last example, the `max` function is *called* on three *arguments*: 2, 5, and 4. The value of each expression within parentheses is passed to the function, and the function *returns* the final value of the full call expression. The `max` function can take any number of arguments and returns the maximum.
# 
# A few functions are available by default, such as `abs` and `round`, but most functions that are built into the Python language are stored in a collection of functions called a *module*. An *import statement* is used to provide access to a module, such as `math` or `operator`.

# In[4]:


import math
import operator
math.sqrt(operator.add(4, 5))


# An equivalent expression could be expressed using the `+` and `**` operators instead.

# In[5]:


(4 + 5) ** 0.5


# Operators and call expressions can be used together in an expression. The *percent difference* between two values is used to compare values for which neither one is obviously `initial` or `changed`. For example, in 2014 Florida farms produced 2.72 billion eggs while Iowa farms produced 16.25 billion eggs (http://quickstats.nass.usda.gov/). The percent difference is 100 times the absolute value of the difference between the values, divided by their average. In this case, the difference is larger than the average, and so the percent difference is greater than 100.

# In[6]:


florida = 2.72
iowa = 16.25
100*abs(florida-iowa)/((florida+iowa)/2)


# Learning how different functions behave is an important part of learning a programming language. A Jupyter notebook can assist in remembering the names and effects of different functions. When editing a code cell, press the *tab* key after typing the beginning of a name to bring up a list of ways to complete that name. For example, press *tab* after `math.` to see all of the functions available in the `math` module. Typing will narrow down the list of options. To learn more about a function, place a `?` after its name. For example, typing `math.log?` will bring up a description of the `log` function in the `math` module.

# In[7]:


get_ipython().run_line_magic('pinfo', 'math.log')


#     log(x[, base])
# 
#     Return the logarithm of x to the given base.
#     If the base not specified, returns the natural logarithm (base e) of x.

# The square brackets in the example call indicate that an argument is optional. That is, `log` can be called with either one or two arguments.

# In[8]:


math.log(16, 2)


# In[9]:


math.log(16)/math.log(2)


# The list of [Python's built-in functions](https://docs.python.org/3/library/functions.html) is quite long and includes many functions that are never needed in data science applications. The list of [mathematical functions in the `math` module](https://docs.python.org/3/library/math.html) is similarly long. This text will introduce the most important functions in context, rather than expecting the reader to memorize or understand these lists.
