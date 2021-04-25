#!/usr/bin/env python
# coding: utf-8

# # Strings
# 
# Much of the world's data is text, and a piece of text represented in a computer is called a *string*. A string can represent a word, a sentence, or even the contents of every book in a library. Since text can include numbers (like this: 5) or truth values (True), a string can also describe those things.
# 
# The meaning of an expression depends both upon its structure and the types of values that are being combined. So, for instance, adding two strings together produces another string. This expression is still an addition expression, but it is combining a different type of value.

# In[1]:


"data" + "science"


# Addition is completely literal; it combines these two strings together without regard for their contents. It doesn't add a space because these are different words; that's up to the programmer (you) to specify.

# In[2]:


"data" + " " + "science"


# Single and double quotes can both be used to create strings: `'hi'` and `"hi"` are identical expressions. Double quotes are often preferred because they allow you to include apostrophes inside of strings.

# In[3]:


"This won't work with a single-quoted string!"


# Why not? Try it out.

# The `str` function returns a string representation of any value. Using this function, strings can be constructed that have embedded values.

# In[4]:


"That's " + str(1 + 1) + ' ' + str(True)


# 
# ```{toctree}
# :hidden:
# :titlesonly:
# 
# 
# String Methods <1/String_Methods>
# ```
# 
