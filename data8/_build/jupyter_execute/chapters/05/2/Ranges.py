#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
path_data = '../../../assets/data/'


# # Ranges
# 
# A *range* is an array of numbers in increasing or decreasing order, each separated by a regular interval. 
# Ranges are useful in a surprisingly large number of situations, so it's worthwhile to learn about them.
# 
# Ranges are defined  using the `np.arange` function, which takes either one, two, or three arguments: a start, and end, and a 'step'.
# 
# If you pass one argument to `np.arange`, this becomes the `end` value, with `start=0`, `step=1` assumed.  Two arguments give the `start` and `end` with `step=1` assumed.  Three arguments give the `start`, `end` and `step` explicitly.
# 
# A range always includes its `start` value, but does not include its `end` value.  It counts up by `step`, and it stops before it gets to the `end`.
# 
#     np.arange(end): An array starting with 0 of increasing consecutive integers, stopping before end.

# In[2]:


np.arange(5)


# Notice how the array starts at 0 and goes only up to 4, not to the end value of 5.

# 
#     np.arange(start, end): An array of consecutive increasing integers from start, stopping before end.

# In[3]:


np.arange(3, 9)


# 
#     np.arange(start, end, step): A range with a difference of step between each pair of consecutive values, starting from start and stopping before end.

# In[4]:


np.arange(3, 30, 5)


# This array starts at 3, then takes a step of 5 to get to 8, then another step of 5 to get to 13, and so on.
# 
# When you specify a step, the start, end, and step can all be either positive or negative and may be whole numbers or fractions. 

# In[5]:


np.arange(1.5, -2, -0.5)


# ## Example: Leibniz's formula for $\pi$

# The great German mathematician and philosopher [Gottfried Wilhelm Leibniz](https://en.wikipedia.org/wiki/Gottfried_Wilhelm_Leibniz) 
# (1646 - 1716) discovered a wonderful formula for $\pi$ as an infinite sum of simple fractions. The formula is
# 
# $$\pi = 4 \cdot \left(1 - \frac{1}{3} + \frac{1}{5} - \frac{1}{7} + \frac{1}{9} - \frac{1}{11} + \dots\right)$$

# Though some math is needed to establish this, we can use arrays to convince ourselves that the formula works. Let's calculate the first 5000 terms of Leibniz's infinite sum and see if it is close to $\pi$.
# 
# $$4 \cdot \left(1 - \frac{1}{3} + \frac{1}{5} - \frac{1}{7} + \frac{1}{9} - \frac{1}{11} + \dots - \frac{1}{9999} \right)$$
# 
# We will calculate this finite sum by adding all the positive terms first and then subtracting the sum of all the negative terms [[1]](#footnotes):
# 
# $$4 \cdot \left( \left(1 + \frac{1}{5} + \frac{1}{9} + \dots + \frac{1}{9997} \right) - \left(\frac{1}{3} + \frac{1}{7} + \frac{1}{11} + \dots + \frac{1}{9999} \right) \right)$$

# The positive terms in the sum have 1, 5, 9, and so on in the denominators. The array `by_four_to_20` contains these numbers up to 17:

# In[6]:


by_four_to_20 = np.arange(1, 20, 4)
by_four_to_20


# To get an accurate approximation to $\pi$, we'll use the much longer array `positive_term_denominators`.

# In[7]:


positive_term_denominators = np.arange(1, 10000, 4)
positive_term_denominators


# The positive terms we actually want to add together are just 1 over these denominators:

# In[8]:


positive_terms = 1 / positive_term_denominators


# The negative terms have 3, 7, 11, and so on on in their denominators. This array is just 2 added to `positive_term_denominators`.

# In[9]:


negative_terms = 1 / (positive_term_denominators + 2)


# The overall sum is

# In[10]:


4 * ( sum(positive_terms) - sum(negative_terms) )


# This is very close to $\pi = 3.14159\dots$. Leibniz's formula is looking good!

# <a id='footnotes'></a>
# ## Footnotes
# [1] Surprisingly, when we add  *infinitely* many fractions, the order can matter! But our approximation to $\pi$ uses only a large finite number of fractions, so it's okay to add the terms in any convenient order.
