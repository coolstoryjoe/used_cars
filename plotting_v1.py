import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib.ticker as ticker
from sklearn.svm import SVR
import numpy as np
import pandas as pd
from models import save_obj, load_obj, dump_csv_single_col, dump_csv, dump_file

# plot the depreciation curve and actual data points of a single car
def plot_graph(age, price):
    X = age.values[:, np.newaxis]
    y = price.values

    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))
    ax.set_xlim(0, 25)
    ax.set_ylim(0, 50000)

    clf = SVR(kernel='rbf', C=5000,  epsilon=0.5)
    clf.fit(X, y)

    plt.plot(X, clf.predict(X), color='g')

    plt.plot(age, price, 'o', color='y')
    
    plt.show()
    return


# plot the depreication curves and data points for two cars
def two_plot_graph(age1, price1, age2, price2):
    clf2 = SVR(kernel='rbf', C=5000,  epsilon=0.1)
    clf = SVR(kernel='rbf', C=5000,  epsilon=0.1)

    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))
    
    ax.set_xlim(0, 25)
    ax.set_ylim(0, 50000)

    X1 = age1.values[:, np.newaxis]
    #y1 = price1.values

    clf.fit(X1, price1)

    plt.plot(X1, clf.predict(X1), color='m')
    plt.plot(age1, price1, 'o', color='m')

    ##########################################

    X2 = age2.values[:, np.newaxis]
    # y2 = price2.values

    clf2.fit(X2, price2)

    plt.plot(X2, clf2.predict(X2), color='y')
    plt.plot(age2, price2, 'o', color='y')

    plt.show()
    return

new_df = load_obj('Toyota_Exaple_DF')
#print(new_df, new_df['model'].unique())

df_4 = new_df[new_df.model == '4Runner']
df_TC = new_df[new_df.model == 'Tacoma']

two_plot_graph(df_4.age, df_4.Price, df_TC.age, df_TC.Price)

# multi_plot_graph(df_4.age, df_4.Price, df_6.age, df_6.Price)
# plot_graph(df.age,df.Price)

def multi_plot_graph(*args):
    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))

    ax.set_xlim(0, 25)
    ax.set_ylim(0, 50000)
    
    for arg in args:
        clf = SVR(kernel='rbf', C=5000,  epsilon=0.1)
    return     

print('now this is updated asdf')