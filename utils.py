# utils file

import discord
import pandas as pd
import re

# returns if a command exists
def verify_command(commands, cmd):
    if cmd in commands:
        return True
    else: return False

# sorts a dataframe into words said by users and their count
def sort_by_words(df):
    result = pd.DataFrame(columns = ['word', 'author', 'count'])
    for index, row in df.iterrows():
        content = row['content']
        author = row['author']
        for word in str(content).split():
            word = re.sub(r'[^\w\s]', '', word)
            word = word.lower()
            if not word:
                continue
            if ((result['word'] == word) & (result['author'] == author)).any():
                result.loc[(result['word'] == word) & (result['author'] == author), 'count'] += 1
            else:
                result.loc[len(result)] = [word, author, 1]
    return result

# takes in a dataframe DF and an AUTHOR and calculates the percentage of words used replacing the 'count' column
def percentage(df, author):
    authordf = df[df['author'] == author]
    percentdf = pd.DataFrame(columns = ['word', 'percentage', 'author'])
    total = sum(df['count'])
    for index, row in authordf.iterrows():
        percentage = row['count'] / total
        percentdf.loc[len(percentdf)] = [row['word'], percentage, author]
    return percentdf

# when given PERCENTDF, a dataframe with words, authors, and percents, identifies the top 10 words spoken by an author
# that they are at least 3 times more likely to use in their messages
def top_10_words(percentdf, author):
    authordf = percentdf[percentdf['author'] == author]
    top10 = []
    for word in authordf['word']:
        try:
            percentage = authordf[authordf['word'] == word]['percentage'].item()
        except:
            continue
        worddf = percentdf[(percentdf['word'] == word) & (percentdf['author'] != author)]
        boolean = True
        for compare in worddf['percentage']:
            if percentage <= 3*compare:
                boolean = False
                break
        if boolean:
            top10.append(word)
            if len(top10) >= 10:
                return top10
    return top10