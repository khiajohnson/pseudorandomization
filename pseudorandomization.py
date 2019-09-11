
# coding: utf-8

# ## Pseudorandomization 
# 
# ##### Khia Johnson
# --- 
# This notebook walks you through generating pseudorandomized stimuli lists with some options for customization. Your stimuli should list should be formatted as an Excel or CSV file and have columns for `item` (i.e. filenames), `word` (word/nonword or T/F) and `group` (filler/target/etc.). It's okay if the names and order are different. One of the first things you'll do in this notebook is reformatting. Additional columns may be present and will remain unaffected. You will have the opportunity to rearrange and/or drop columns as needed.
# 
# To use this code, follow the instructions as indicated and run each cell once. The output will be a number of csv files with pseudorandomized order, evenly split between two versions differing in which key response is the correct response. 

# In[1]:


import pandas as pd
import random


# **Import, inspect, and reformat your data**

# In[2]:


# Replace the value with the path to your data (csv or excel file)
path_in = '/Users/khiajohnson/Speech-in-context_docs/CanPL/List.xlsx' 

# Import to a pandas dataframe
if path_in.endswith('csv'):
    stimuli = pd.read_csv(path_in, encoding='utf-8')
else:
    stimuli = pd.read_excel(path_in, encoding='utf-8')

# Inspect the columns and top three rows of your data
stimuli.head(n=3)


# In[3]:


# Rename columns here
stimuli.rename(columns={'item':'item',
                        'is_word':'word',
                        'group':'group',
                        # Add dict entries here
                       }, inplace=True)    

# List the columns you want to keep (in order) here
stimuli = stimuli[['item','group','word']]

# Inspect your dataframe again (this time a random sample of rows)
stimuli.sample(n=3)


# **Set your variables for pseudorandomization here**

# In[4]:


# number of filler items at the beginning
burn_in = 7 

# How are fillers specified in the group column?
filler_spec = 'Filler' 

# How are words specified in the word column?
word_spec = 'Word'

# Which are the two possible key responses?
response_keys = [1,5] 

# How many pseudorandomizations would you like with these settings? 
number_of_lists = 10 

# The directory where you want to save the new CSV files (if unspecified, defaults to current directory)
dir_out = '' 

# The base for the output pseudorandomization filenames
base = 'pseudrand'


# **The following cell contains functions needed for pseudorandomization. Don't change anything here, just run the cell!**

# In[5]:


# pseudorandomizes a pandas dataframe
def gen_psuedorand(df):
    to_fill = df.loc[df['group']==filler_spec].sample(frac=1).to_dict('records')
    targets = df.loc[df['group']!=filler_spec].sample(frac=1).to_dict('records')
    maximum = len(df)
    x = []
    while len(x) < len(targets):
        n = random.choice(range(0,len(df)))
        if (n > burn_in) and (n-1 not in x) and (n not in x) and (n+1 not in x):
            x.append(n)
    x.sort()
    for i in x:
        to_fill.insert(i, targets.pop())
    return pd.DataFrame(to_fill)

# set the correct response to the first option specified
def set_cresp_v1(row):
    if row['word']==word_spec:
        return response_keys[0]
    else:
        return response_keys[1]

# set the correct response to the second option specified
def set_cresp_v2(row):
    if row['word']==word_spec:
        return response_keys[1]
    else:
        return response_keys[0]


# **Double check that you have the right settings. You can rereun any cells that you need to make revisions in.**

# In[6]:


for i in range(int(number_of_lists/2)):
    pseudorandomization = gen_psuedorand(stimuli)
    pseudorandomization.apply(set_cresp_v1, axis=1)
    current_filename = base + '_v1_'+ str(i+1) + '.csv'
    pseudorandomization.to_csv(current_filename)
    print(current_filename, '✓')
        
for i in range(int(number_of_lists/2)):
    pseudorandomization = gen_psuedorand(stimuli)
    pseudorandomization.apply(set_cresp_v2, axis=1)
    current_filename = base + '_v2_'+ str(i+1) + '.csv'    
    pseudorandomization.to_csv(current_filename)    
    print(current_filename, '✓')

