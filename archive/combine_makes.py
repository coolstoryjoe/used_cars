import pandas as pd
import os

cwd = os.getcwd()

model_link = str(os.path.join(cwd, 'soup_kitchen', 'models.csv'))
df = pd.read_csv(model_link, header=None, names=['Models'])

# print(df) 
models_dict = {}

for i in df['Models']:
    temp_list = []
    model_link = str(os.path.join(cwd, 'soup_kitchen', str(i + '_makes.csv')))
    if os.path.exists(model_link) == True:
        df = pd.read_csv(model_link, names=['Makes'])
        for j in df['Makes']:
            models_dict[j] = i

df1 = pd.DataFrame.from_dict(models_dict , orient='index').reset_index()
df1.to_csv(str(os.path.join(cwd, 'recipes','makes_models.csv')))
print(df1)

model_link = str(os.path.join(cwd, 'recipes', 'makes_models.csv'))
df = pd.read_csv(model_link,index_col= 0, names = ['Model','Make'] ,header = 0)
print(df)
