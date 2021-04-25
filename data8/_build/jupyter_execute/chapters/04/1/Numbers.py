#!/usr/bin/env python
# coding: utf-8

# # Numbers
# 
# Computers are designed to perform numerical calculations, but there are some important details about working with numbers that every programmer working with quantitative data should know. Python (and most other programming languages) distinguishes between two different types of numbers:
# 
# * Integers are called `int` values in the Python language. They can only represent whole numbers (negative, zero, or positive) that don't have a fractional component
# * Real numbers are called `float` values (or *floating point values*) in the Python language. They can represent whole or fractional numbers but have some limitations.
# 
# The type of a number is evident from the way it is displayed: `int` values have no decimal point and `float` values always have a decimal point. 

# In[1]:


# Some int values
2


# In[2]:


1 + 3


# In[3]:


-1234567890000000000


# In[4]:


# Some float values
1.2


# In[5]:


3.0


# When a `float` value is combined with an `int` value using some arithmetic operator, then the result is always a `float` value. In most cases, two integers combine to form another integer, but any number (`int` or `float`) divided by another will be a `float` value. Very large or very small `float` values are displayed using scientific notation.

# In[6]:


1.5 + 2


# In[7]:


3 / 1


# In[8]:


-12345678900000000000.0


# The `type` function can be used to find the type of any number.

# In[9]:


type(3)


# In[10]:


type(3 / 1)


# The `type` of an expression is the type of its final value. So, the `type` function will never indicate that the type of an expression is a name, because names are always evaluated to their assigned values.

# In[11]:


x = 3
type(x) # The type of x is an int, not a name


# In[12]:


type(x + 2.5)


# ## More About Float Values
# 
# Float values are very flexible, but they do have limits. 
# 
# 1. A `float` can represent extremely large and extremely small numbers. There are limits, but you will rarely encounter them.
# 2. A `float` only represents 15 or 16 significant digits for any number; the remaining precision is lost. This limited precision is enough for the vast majority of applications.
# 3. After combining `float` values with arithmetic, the last few digits may be incorrect. Small rounding errors are often confusing when first encountered.
# 
# The first limit can be observed in two ways. If the result of a computation is a very large number, then it is represented as infinite. If the result is a very small number, then it is represented as zero.

# In[13]:


2e306 * 10


# In[14]:


2e306 * 100


# In[15]:


2e-322 / 10


# In[16]:


2e-322 / 100


# The second limit can be observed by an expression that involves numbers with more than 15 significant digits. These extra digits are discarded before any arithmetic is carried out.

# In[17]:


0.6666666666666666 - 0.6666666666666666123456789


# The third limit can be observed when taking the difference between two expressions that should be equivalent. For example, the expression `2 ** 0.5` computes the square root of 2, but squaring this value does not exactly recover 2.

# In[18]:


2 ** 0.5


# In[19]:


(2 ** 0.5) * (2 ** 0.5)


# In[20]:


(2 ** 0.5) * (2 ** 0.5) - 2


# The final result above is `0.0000000000000004440892098500626`, a number that is very close to zero. The correct answer to this arithmetic expression is 0, but a small error in the final significant digit appears very different in scientific notation. This behavior appears in almost all programming languages because it is the result of the standard way that arithmetic is carried out on computers. 
# 
# Although `float` values are not always exact, they are certainly reliable and work the same way across all different kinds of computers and programming languages. 
