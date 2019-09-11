
# coding: utf-8

# ## Pseudorandomization 
# 
# ##### Khia Johnson

import pandas as pd
import random

# Replace the value with the path to your data (csv or excel file)
path_in = '/Users/khiajohnson/Speech-in-context_docs/CanPL/List.xlsx' 

# Import to a pandas dataframe
if path_in.endswith('csv'):
    stimuli = pd.read_csv(path_in, encoding='utf-8')
else:
    stimuli = pd.read_excel(path_in, encoding='utf-8')

# Rename columns here
stimuli.rename(columns={'item':'item',
                        'is_word':'word',
                        'group':'group',
                        # Add dict entries here
                       }, inplace=True)    

# List the columns you want to keep (in order) here
stimuli = stimuli[['item','group','word']]

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

# function to pseudorandomize a pandas dataframe
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

# functions for pandas apply to set the correct response
def set_cresp_v1(row):
    if row['word']==word_spec:
        return response_keys[0]
    else:
        return response_keys[1]

def set_cresp_v2(row):
    if row['word']==word_spec:
        return response_keys[1]
    else:
        return response_keys[0]

# Generate CSV files with pseudorandomizations per the specified settings
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

