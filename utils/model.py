import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from datetime import datetime
from sklearn.tree import DecisionTreeRegressor


def get_prediction(df, brand, model, year, mileage, cc, hp, fuel,
                   transmission):
    """
    Takes in features of a seller's car to give a suggestions about how much
    he should sell it.
    :param df: Dataframe data
    :param brand: Seller's car brand
    :param model: Seller's car model
    :param year: Seller's car registration year
    :param mileage: Seller's car mileage
    :param cc: Seller's car displacement
    :param hp: Seller's car horsepower
    :param fuel: Seller's car fuel type
    :param transmission: Seller's car transmission
    :return: suggested price (int)
    """

    """
    Create df by quering brand and model.
    Ignoring rows where price equals 'Ask price'.
    Dropping columns we will not use for training
    And converting price column to int.
    """
    dummy = df.query(f'brand == "{brand}"').query(f'model == "{model}"')
    dummy = dummy.query('price != "Ask price"')
    dummy.reset_index(drop = True, inplace = True)
    dummy.drop(['title', 'category', 'location', 'brand',
                'model', 'link', 'town'], axis = 1, inplace = True)
    dummy['price'] = dummy['price'].values.astype('int32')
    """
    Prepare fuel and transmission columns to use them for training.
    We proceed with one-hot encoding.
    """
    fuel_one_hot = OneHotEncoder(drop = 'if_binary').fit_transform(
        dummy['fuel'].values.reshape(-1, 1))
    transmission_one_hot = OneHotEncoder(drop = 'if_binary').fit_transform(
        dummy['transmission'].values.reshape(-1, 1))

    dummy['fuel_type'] = fuel_one_hot.toarray()
    dummy['transmission_type'] = transmission_one_hot.toarray()
    dummy.drop(['fuel', 'transmission'], axis = 1, inplace = True)
    """
    Extract the registration year from registration column.
    Then drop the registration column.
    """
    registration_stamp = [datetime.strptime(dummy['registration'][i],
                                            '%m/%Y').year for i in range(len(dummy))]
    dummy['registration_stamp'] = registration_stamp
    dummy.drop('registration', axis = 1, inplace = True)
    """
    Split data to input and target.
    """
    x = dummy.iloc[:, 1:]
    y = dummy['price']

    linear = LinearRegression()
    tree = DecisionTreeRegressor(max_depth = 3)

    linear.fit(x, y)
    tree.fit(x, y)
    # Diesel -> 0 | Petrol -> 1
    # Manual -> 1 | Automatic -> 0
    """
    Here we process the information the seller gives us in order to give a 
    suggestion.
    """
    fuel_type = 1 if fuel == 'Petrol' else 0
    transmission_type = 1 if transmission == 'Manual' else 0
    registration = year
    """
    Here we combine the 2 models' prediction in order to generalize better.
    """
    # order -> km, cc, hp, fuel_type, transmission_type, registration_stamp
    ensemble = (linear.predict(np.array([mileage, cc, hp, fuel_type,
                                         transmission_type,
                                         registration]).reshape(1, -1)) +
                tree.predict(np.array([mileage, cc, hp, fuel_type,
                                         transmission_type,
                                         registration]).reshape(1, -1))) / 2

    return np.round(ensemble.item())
