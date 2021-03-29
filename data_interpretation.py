import pandas as pd

df = pd.read_csv('data.csv')

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