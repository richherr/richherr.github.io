#!/usr/bin/env python
# coding: utf-8

# In[1]:


from datascience import *
import numpy as np
path_data = '../../../assets/data/'
import matplotlib
matplotlib.use('Agg')
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plots
plots.style.use('fivethirtyeight')


# In[2]:


# As of Jan 2017, this census file is online here: 
data = 'http://www2.census.gov/programs-surveys/popest/datasets/2010-2015/national/asrh/nc-est2015-agesex-res.csv'

# A local copy can be accessed here in case census.gov moves the file:
# data = path_data + 'nc-est2015-agesex-res.csv'

full_census_table = Table.read_table(data)
full_census_table

partial_census_table = full_census_table.select('SEX', 'AGE', 'POPESTIMATE2010', 'POPESTIMATE2014')
partial_census_table

us_pop = partial_census_table.relabeled('POPESTIMATE2010', '2010').relabeled('POPESTIMATE2014', '2014')


# # Example: Trends in Gender
# 
# We are now equipped with enough coding skills to examine features and trends in subgroups of the U.S. population. In this example, we will look at the distribution of males and females across age groups. We will continue using the `us_pop` table from the previous section.

# In[3]:


us_pop


# As we know from having examined this dataset earlier, a [description of the table](http://www2.census.gov/programs-surveys/popest/datasets/2010-2015/national/asrh/nc-est2015-agesex-res.pdf) appears online. Here is a reminder of what the table contains. 
# 
# Each row represents an age group. The `SEX` column contains numeric codes: `0` stands for the total, `1` for male, and `2` for female. The `AGE` column contains ages in completed years, but the special value `999` represents the entire population regardless of age. The rest of the columns contain estimates of the US population.

# ## Understanding `AGE` = 100
# As a preliminary, let's interpret data in the final age category in the table, where `AGE` is 100. The code below extracts the rows for the combined group of men and women (`SEX` code 0) for the highest ages.

# In[4]:


us_pop.where('SEX', are.equal_to(0)).where('AGE', are.between(97, 101))


# Not surprisingly, the numbers of people are smaller at higher ages – for example, there are fewer 99-year-olds than 98-year-olds. 
# 
# It does come as a surprise, though, that the numbers for `AGE` 100 are quite a bit larger than those for age 99. A closer examination of the documentation shows that it's because the Census Bureau used 100 as the code for everyone aged 100 or more. 
# 
# The row with `AGE` 100 doesn't just represent 100-year-olds – it also includes those who are older than 100. That is why the numbers in that row are larger than in the row for the 99-year-olds.

# ## Overall Proportions of Males and Females
# We will now begin looking at gender ratios in 2014. First, let's look at all the age groups together. Remember that this means looking at the rows where the "age" is coded 999. The table `all_ages` contains this information. There are three rows: one for the total of both genders, one for males (`SEX` code 1), and one for females (`SEX` code 2).

# In[5]:


us_pop_2014 = us_pop.drop('2010')
all_ages = us_pop_2014.where('AGE', are.equal_to(999))
all_ages


# Row 0 of `all_ages` contains the total U.S. population in each of the two years. The United States had just under 319 million in 2014.
# 
# Row 1 contains the counts for males and Row 2 for females. Compare these two rows to see that in 2014, there were more females than males in the United States. 
# 
# The population counts in Row 1 and Row 2 add up to the total population in Row 0. 
# 
# For comparability with other quantities, we will need to convert these counts to percents out of the total population. Let's access the total for 2014 and name it. Then, we'll show a population table with a proportion column. Consistent with our earlier observation that there were more females than males, about 50.8% of the population in 2014 was female and about 49.2% male in each of the two years. 

# In[6]:


pop_2014 = all_ages.column('2014').item(0)
all_ages.with_column(
    'Proportion', all_ages.column('2014')/pop_2014
).set_format('Proportion', PercentFormatter)


# ## Proportions of Boys and Girls among Infants

# When we look at infants, however, the opposite is true. Let's define infants to be babies who have not yet completed one year, represented in the row corresponding to `AGE` 0. Here are their numbers in the population. You can see that male infants outnumbered female infants.

# In[7]:


infants = us_pop_2014.where('AGE', are.equal_to(0))
infants


# As before, we can convert these counts to percents out of the total numbers of infants. The resulting table shows that in 2014, just over 51% of infants in the U.S. were male. 

# In[8]:


infants_2014 = infants.column('2014').item(0)
infants.with_column(
    'Proportion', infants.column('2014')/infants_2014
).set_format('Proportion', PercentFormatter)


# In fact, it has long been observed that the proportion of boys among newborns is slightly more than 1/2. The reason for this is not thoroughly understood, and [scientists are still working on it](http://www.npr.org/sections/health-shots/2015/03/30/396384911/why-are-more-baby-boys-born-than-girls).

# ## Female:Male Gender Ratio at Each Age ###

# We have seen that while there are more baby boys than baby girls, there are more females than males overall. So it's clear that the split between genders must vary across age groups.
# 
# To study this variation, we will separate out the data for the females and the males, and eliminate the row where all the ages are aggregated and `AGE` is coded as 999.
# 
# The tables `females` and `males` contain the data for each the two genders.

# In[9]:


females_all_rows = us_pop_2014.where('SEX', are.equal_to(2))
females = females_all_rows.where('AGE', are.not_equal_to(999))
females


# In[10]:


males_all_rows = us_pop_2014.where('SEX', are.equal_to(1))
males = males_all_rows.where('AGE', are.not_equal_to(999))
males


# The plan now is to compare the number of women and the number of men at each age, for each of the two years. Array and Table methods give us straightforward ways to do this. Both of these tables have one row for each age.

# In[11]:


males.column('AGE')


# In[12]:


females.column('AGE')


# For any given age, we can get the Female:Male gender ratio by dividing the number of females by the number of males. To do this in one step, we can use `column` to extract the array of female counts and the corresponding array of male counts, and then simply divide one array by the other. Elementwise division will create an array of gender ratios for all the years.

# In[13]:


ratios = Table().with_columns(
    'AGE', females.column('AGE'),
    '2014 F:M RATIO', females.column('2014')/males.column('2014')
)
ratios


# You can see from the display that the ratios are all around 0.96 for children aged nine or younger. When the Female:Male ratio is less than 1, there are fewer females than males. Thus what we are seeing is that there were fewer girls than boys in each of the age groups 0, 1, 2, and so on through 9. Moreover, in each of these age groups, there were about 96 girls for every 100 boys.

# So how can the overall proportion of females in the population be higher than the males? 
# 
# Something extraordinary happens when we examine the other end of the age range. Here are the Female:Male ratios for people aged more than 75.

# In[14]:


ratios.where('AGE', are.above(75)).show()


# Not only are all of these ratios greater than 1, signifying more women than men in all of these age groups, many of them are considerably greater than 1. 
# 
# - At ages 89 and 90 the ratios are close to 2, meaning that there were about twice as many women as men at those ages in 2014.
# - At ages 98 and 99, there were about 3.5 to 4 times as many women as men. 
# 
# If you are wondering how many people there were at these advanced ages, you can use Python to find out:

# In[15]:


males.where('AGE', are.between(98, 100))


# In[16]:


females.where('AGE', are.between(98, 100))


# The graph below shows the gender ratios plotted against age. The blue curve shows the 2014 ratio by age.
# 
# The ratios are almost 1 (signifying close to equal numbers of males and females) for ages 0 through 60, but they start shooting up dramatically (more females than males) starting at about age 65.
# 
# That females outnumber males in the U.S. is partly due to the marked gender imbalance in favor of women among senior citizens.

# In[17]:


ratios.plot('AGE')

