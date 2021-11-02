# -*- coding: utf-8 -*-
"""
Script for calculating Graphic Similarity Scores between low frequency - pseudo word pairs

Created on 2021-11-02 @ 12:59:01

@author: Alex Chalmers & Emily Bellerby
"""
import pandas as pd
import re

# Reading in excel file of dummy data
df = pd.read_excel('dummy_data.xlsx')

# Function for preprocessing of strings to remove any capitalisation and non alphabetic characters
def preprocessing(col):
    subbed_list = []
    for myStr in col:
        lower = myStr.lower()
        regex = re.compile('[^a-zA-Z]')
        # First parameter is the replacement, second parameter is input string
        subbed = regex.sub('', lower)
        subbed_list.append(subbed)
    return subbed_list

# df is preprocessed using preprocessing function
df = df.apply(lambda x: preprocessing(x))

#lists established for collection of calculated scores
f_list = []
v_list = []
c_list = []
a_list = []
t_list = []
b_list = []
e_list = []
GS_list = []

# Looping over the rows of Low frequency - Pseudo word pairs
for index, row in df.iterrows():
    F = 0
    V = 0
    C = 0
    # Looping over the characters of the low frequency words of each row
    for i in range(0, len(row['LowF']), 1):
        # Checking if the character is at least 1 position from the end of the word
        if i < len(row['LowF']) - 1:
            # character pairs split into first and second characters
            first, second = row['LowF'][i:i + 2]
            # check is combination of letters in order they appear
            check = first + second
            # check is combination of letters in reverse order
            check_rev = second + first
            # F score is incremented if letter pair appears in pseudo word
            if check in row['Pseudos']:
                F = F + 1
            # V score is incremented if reversed letter pair appears in pseudo word
            if check_rev in row['Pseudos']:
                V = V + 1

    # get unique characters in low frequency word
    lowFUnique = ''.join(set(row['LowF']))
    # get unique characters in pseudo word
    pseudosUnique = ''.join(set(row['Pseudos']))
    # for each unique character in the low frequency word,
    # C is incremented if it appears in the unique characters of the pseudo word
    for i in range(0, len(lowFUnique), 1):
        if lowFUnique[i] in pseudosUnique:
            C = C + 1
            # count the number of duplicates of each unique letter in both pseudo
            # and low frequency words and increment C if the letter appears in both words more than once
            pseudo_dup = row['Pseudos'].count(lowFUnique[i])
            lowF_dup = row['LowF'].count(lowFUnique[i])
            C = C + min(pseudo_dup, lowF_dup) - 1

    # A is calculated as the average of letters in each word
    A = (len(row['LowF']) + len(row['Pseudos']))/2

    # T is calculated as the ratio of number of letters in the shortest word to the number of letters in the longest word
    T = len(row['LowF']) / len(row['Pseudos']) if len(row['LowF']) < len(row['Pseudos']) else len(row['Pseudos']) / len(row['LowF'])

    # B is 1 if the first letter of the low frequency word is the same as the first letter of the pseudo word, otherwise 0
    B = 1 if row['LowF'][0] == row['Pseudos'][0] else 0

    # E is 1 if the last letter of the low frequency word is the same as the last letter of the pseudo word, otherwise 0
    E = 1 if row['LowF'][-1] == row['Pseudos'][-1] else 0

    # Graphic similarity score is calculated
    GS = 10 * ((50*F + 30*V + 10*C) / A + 5*T + 27*B + 18*E)

    # Each score is appended to respective lists for each low frequency - pseudo word pair
    f_list.append(F)
    v_list.append(V)
    c_list.append(C)
    a_list.append(A)
    t_list.append(T)
    b_list.append(B)
    e_list.append(E)
    GS_list.append(GS)

# The scores are then combined into the original dataframe
print(f_list)
df['F'] = f_list
df['V'] = v_list
df['C'] = c_list
df['A'] = a_list
df['T'] = t_list
df['B'] = b_list
df['E'] = e_list
df['GS'] = GS_list

print(df)