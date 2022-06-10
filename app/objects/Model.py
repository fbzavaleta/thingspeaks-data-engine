from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import numpy as np
import pandas as pd 

class Model:
    def __init__(self, df):
        self.X = df.drop(columns='label')
        self.y = df['label']
    
    def criarModel(self):
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.3, random_state=42)
        lr = LinearRegression()
        lr.fit(X_train, y_train)


        intercept = lr.intercept_
        coef = lr.coef_

        y_pred = lr.predict(X_test)
        df_test = pd.DataFrame({'atual': y_test, 'predicted': y_pred})

        print('-------------------------------- model results ------------------------------------')
        print('r2 score:', metrics.r2_score(y_test, y_pred))
        print('mean absolute error:', metrics.mean_absolute_error(y_test, y_pred))
        print('mean squared error:', metrics.mean_squared_error(y_test, y_pred))
        print('root mean squared error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))


        return lr, df_test