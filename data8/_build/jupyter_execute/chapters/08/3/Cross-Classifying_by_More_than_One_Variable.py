#!/usr/bin/env python
# coding: utf-8

# In[1]:


from datascience import *
path_data = '../../../assets/data/'
import numpy as np

import matplotlib
matplotlib.use('Agg')
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plots
plots.style.use('fivethirtyeight')


# # Cross-Classifying by More than One Variable
# 
# When individuals have multiple features, there are many different ways to classify them. For example, if we have a population of college students for each of whom we have recorded a major and the number of years in college, then the students could be classified by major, or by year, or by a combination of major and year.
# 
# The `group` method also allows us to classify individuals according to multiple variables. This is called *cross-classifying*.

# ## Two Variables: Counting the Number in Each Paired Category
# The table `more_cones` records the flavor, color, and price of six ice cream cones.

# In[2]:


more_cones = Table().with_columns(
    'Flavor', make_array('strawberry', 'chocolate', 'chocolate', 'strawberry', 'chocolate', 'bubblegum'),
    'Color', make_array('pink', 'light brown', 'dark brown', 'pink', 'dark brown', 'pink'),
    'Price', make_array(3.55, 4.75, 5.25, 5.25, 5.25, 4.75)
)

more_cones


# We know how to use `group` to count the number of cones of each flavor:

# In[3]:


more_cones.group('Flavor')


# But now each cone has a color as well. To classify the cones by both flavor and color, we will pass a list of labels as an argument to `group`. The resulting table has one row for every *unique combination* of values that appear together in the grouped columns. As before, a single argument (a list, in this case, but an array would work too) gives row counts.

# Although there are six cones, there are only four unique combinations of flavor and color. Two of the cones were dark brown chocolate, and two pink strawberry.

# In[4]:


more_cones.group(['Flavor', 'Color'])


# ## Two Variables: Finding a Characteristic of Each Paired Category
# A second argument aggregates all other columns that are not in the list of grouped columns.

# In[5]:


more_cones.group(['Flavor', 'Color'], sum)


# **Three or More Variables.** You can use `group` to classify rows by three or more categorical variables. Just include them all in the list that is the first argument. But cross-classifying by multiple variables can become complex, as the number of distinct combinations of categories can be quite large. 

# ## Pivot Tables: Rearranging the Output of `group`
# Many uses of cross-classification involve just two categorical variables, like `Flavor` and `Color` in the example above. In these cases it is possible to display the results of the classification in a different kind of table, called a *pivot table*. Pivot tables, also known as *contingency tables*, make it easier to work with data that have been classified according to two variables.
# 
# Recall the use of `group` to count the number of cones in each paired category of flavor and color:

# In[6]:


more_cones.group(['Flavor', 'Color'])


# The same data can be displayed differenly using the Table method `pivot`. Ignore the code for a moment, and just examine the table of outcomes.

# In[7]:


more_cones.pivot('Flavor', 'Color')


# Notice how this table displays all nine possible pairs of flavor and color, including pairs like "dark brown bubblegum" that don't exist in our data. Notice also that the count in each pair appears in the body of the table: to find the number of light brown chocolate cones, run your eye along the row `light brown` until it meets the column `chocolate`.
# 
# The `group` method takes a list of two labels because it is flexible: it could take one or three or more. On the other hand, `pivot` always takes two column labels, one to determine the columns and one to determine the rows.

# **`pivot`** 
# 
# The `pivot` method is closely related to the `group` method: it groups together rows that share a combination of values. It differs from `group` because it organizes the resulting values in a grid. The first argument to `pivot` is the label of a column that contains the values that will be used to form new columns in the result. The second argument is the label of a column used for the rows. The result gives the count of all rows of the original table that share the combination of column and row values.
# 
# Like `group`, `pivot` can be used with additional arguments to find characteristics of each paired category. An optional third argument called `values` indicates a column of values that will replace the counts in each cell of the grid. All of these values will not be displayed, however; the fourth argument `collect` indicates how to collect them all into one aggregated value to be displayed in the cell.
# 
# An example will help clarify this. Here is `pivot` being used to find the total price of the cones in each cell.  

# In[8]:


more_cones.pivot('Flavor', 'Color', values='Price', collect=sum)


# And here is `group` doing the same thing.

# In[9]:


more_cones.group(['Flavor', 'Color'], sum)


# Though the numbers in both tables are the same, table produced by `pivot` is easier to read and lends itself more easily to analysis. The advantage of `pivot` is that it places grouped values into adjacent columns, so that they can be combined and compared.

# ## Example: Education and Income of Californian Adults
# The State of California's Open Data Portal is a rich source of information about the lives of Californians. It is our source of a [dataset](http://data.ca.gov/dataset/ca-educational-attainment-personal-income) on educational attainment and personal income among Californians over the years 2008 to 2014. The data are derived from the U.S. Census Current Population Survey.
# 
# For each year, the table records the `Population Count` of Californians in many different combinations of age, gender, educational attainment, and personal income. We will study only the data for the year 2014.

# In[10]:


full_table = Table.read_table(path_data + 'educ_inc.csv')
ca_2014 = full_table.where('Year', are.equal_to('1/1/14 0:00')).where('Age', are.not_equal_to('00 to 17'))
ca_2014


# Each row of the table corresponds to a combination of age, gender, educational level, and income. There are 127 such combinations in all! 
# 
# As a first step it is a good idea to start with just one or two variables. We will focus on just one pair: educational attainment and personal income. 

# In[11]:


educ_inc = ca_2014.select('Educational Attainment', 'Personal Income', 'Population Count')
educ_inc


# Let's start by looking at educational level alone. The categories of this variable have been subdivided by the different levels of income. So we will group the table by `Educational Attainment` and `sum` the `Population Count` in each category.

# In[12]:


education = educ_inc.select('Educational Attainment', 'Population Count')
educ_totals = education.group('Educational Attainment', sum)
educ_totals


# There are only four categories of educational attainment. The counts are so large that is is more helpful to look at percents. For this, we will use the function `percents` that we defined in an earlier section. It converts an array of numbers to an array of percents out of the total in the input array.

# In[13]:


def percents(array_x):
    return np.round( (array_x/sum(array_x))*100, 2)


# We now have the distribution of educational attainment among adult Californians. More than 30% have a Bachelor's degree or higher, while almost 16% lack a high school diploma.

# In[14]:


educ_distribution = educ_totals.with_column(
    'Population Percent', percents(educ_totals.column(1))
)
educ_distribution


# By using `pivot`, we can get a contingency table (a table of counts) of adult Californians cross-classified by `Educational Attainment` and `Personal Income`.

# In[15]:


totals = educ_inc.pivot('Educational Attainment', 'Personal Income', values='Population Count', collect=sum)
totals


# Here you see the power of `pivot` over other cross-classification methods. Each column of counts is a distribution of personal income at a specific level of educational attainment. Converting the counts to percents allows us to compare the four distributions.

# In[16]:


distributions = totals.select(0).with_columns(
    "Bachelor's degree or higher", percents(totals.column(1)),
    'College, less than 4-yr degree', percents(totals.column(2)),
    'High school or equivalent', percents(totals.column(3)),
    'No high school diploma', percents(totals.column(4))   
    )

distributions


# At a glance, you can see that over 35% of those with Bachelor's degrees or higher had incomes of $\$75,000$ and over, whereas fewer than 10% of the people in the other education categories had that level of income. 
# 
# The bar chart below compares the personal income distributions of adult Californians who have no high school diploma with those who have completed a Bachelor's degree or higher. The difference in the distributions is striking. There is a clear positive association between educational attainment and personal income.

# In[17]:


distributions.select(0, 1, 4).barh(0)

