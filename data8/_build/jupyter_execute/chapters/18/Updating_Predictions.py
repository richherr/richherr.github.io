#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib
from datascience import *
path_data = '../../assets/data/'
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plots
import numpy as np
plots.style.use('fivethirtyeight')


# # Updating Predictions
# We know how to use training data to classify a point into one of two categories. Our classification is just a prediction of the class, based on the most common class among the training points that are nearest our new point. 
# 
# Suppose that we eventually find out the true class of our new point. Then we will know whether we got the classification right. Also, we will have a new point that we can add to our training set, because we know its class. This *updates* our training set. So, naturally, we will want to *update our classifier* based on the new training set.
# 
# This chapter looks at some simple scenarios where new data leads us to update our predictions. While the examples in the chapter are simple in terms of calculation, the method of updating can be generalized to work in complex settings and is one of the most powerful tools used for machine learning.

# 
# ```{toctree}
# :hidden:
# :titlesonly:
# 
# 
# A "More Likely Than Not" Binary Classifier <1/More_Likely_than_Not_Binary_Classifier>
# Making Decisions <2/Making_Decisions>
# ```
# 
