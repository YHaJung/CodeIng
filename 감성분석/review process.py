
blocks=[]
for block in pd.read_csv('1.csv')['review_list'].values.tolist():
    blocks+=block
a = pd.read_csv('1.csv')['review_list'].values.tolist()
review=[]
for sentence in a:
     review += sentence.replace("'" ,'').replace("[" ,'').replace("]" ,'').split(',')