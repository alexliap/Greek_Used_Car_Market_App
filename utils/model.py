import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from datetime import datetime
from sklearn.tree import DecisionTreeRegressor


def get_prediction(df, brand, model, year, mileage, cc, hp, fuel,
                   transmission):
    dummy = df.query(f'brand == "{brand}"').query(f'model == "{model}"')
    dummy = dummy.query('price != "Ask price"')
    dummy.reset_index(drop = True, inplace = True)
    dummy.drop(['title', 'category', 'location', 'brand',
                'model', 'link', 'town'], axis = 1, inplace = True)
    dummy['price'] = dummy['price'].values.astype('int32')

    fuel_one_hot = OneHotEncoder(drop = 'if_binary').fit_transform(
        dummy['fuel'].values.reshape(-1, 1))
    transmission_one_hot = OneHotEncoder(drop = 'if_binary').fit_transform(
        dummy['transmission'].values.reshape(-1, 1))

    dummy['fuel_type'] = fuel_one_hot.toarray()
    dummy['transmission_type'] = transmission_one_hot.toarray()
    dummy.drop(['fuel', 'transmission'], axis = 1, inplace = True)

    registration_stamp = [datetime.strptime(dummy['registration'][i],
                                            '%m/%Y').year for i in range(len(dummy))]
    dummy['registration_stamp'] = registration_stamp
    dummy.drop('registration', axis = 1, inplace = True)

    x = dummy.iloc[:, 1:]
    y = dummy['price']

    linear = LinearRegression()
    tree = DecisionTreeRegressor(max_depth = 3)

    linear.fit(x, y)
    tree.fit(x, y)
    # Diesel -> 0 | Petrol -> 1
    # Manual -> 1 | Automatic -> 0

    fuel_type = 1 if fuel == 'Petrol' else 0
    transmission_type = 1 if transmission == 'Manual' else 0
    registration = year

    # order -> km, cc, hp, fuel_type, transmission_type, registration_stamp
    ensemble = (linear.predict(np.array([mileage, cc, hp, fuel_type,
                                         transmission_type,
                                         registration]).reshape(1, -1)) +
                tree.predict(np.array([mileage, cc, hp, fuel_type,
                                         transmission_type,
                                         registration]).reshape(1, -1))) / 2

    return np.round(ensemble.item())



