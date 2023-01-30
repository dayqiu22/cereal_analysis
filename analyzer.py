import pandas as pd
import sys


def main():

    # Ensure correct usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python cereal.py FILENAME")

    # Read cereals into dataframe from file
    cereals = pd.read_csv(sys.argv[1])

    # Read all manufacturers
    mfrs = manufacturers(cereals)

    # Standardize all servings to a weight of 1 ounce per serving
    standardize(cereals)

    # Find the cereal brand with the highest sugar per serving
    print("Cereal brands with the highest sugars per 1 ounce serving:")
    print(max_sugar(cereals))
    print()

    # Find the cereal brand with the highest rating
    print("Cereal brands with the highest ratings:")
    print(max_rating(cereals))
    print()

    # Find the cereal manufacturer with the highest average sugar per serving across products
    print("Cereal manufacturers with the highest average sugars per 1 ounce servings:")
    print(max_sugar_mfr(cereals, mfrs))
    print()

    # Find the cereal manufacturer with the highest average rating across products
    print("Cereal manufacturer with the highest average ratings:")
    print(max_rating_mfr(cereals, mfrs))
    print()


def manufacturers(cereals):
    select = cereals[['mfr']]
    unique = []

    # Loop through each row
    for i in range(select.shape[0]):

        # If manufacturer is not already in the list, append
        if select.iloc[i].mfr not in unique:
            unique.append(select.iloc[i].mfr)

    return unique

def standardize(cereals):
    # Loop through each row
    for i in range(cereals.shape[0]):

        # If serving size is not 1 ounce, adjust all nutritional values and serving size equivalent to 1 ounce
        if cereals.iloc[i].weight != 1:
            multiplier = 1 / cereals.iloc[i].weight

            for j in range(3, 12):
                old = cereals.iloc[i, j]
                cereals.iloc[i, j] = round((old * multiplier), 2)

            for k in range(13, 15):
                old = cereals.iloc[i, k]
                cereals.iloc[i, k] = round((old * multiplier), 2)

def max_sugar(cereals):
    select = cereals[cereals.sugars == cereals.sugars.max()]
    return select[['name', 'sugars']]

def max_rating(cereals):
    select = cereals[cereals.rating == cereals.rating.max()]
    return select[['name', 'rating']]

def max_sugar_mfr(cereals, mfrs):
    averages = []

    # Loop through all manufacturers
    for m in mfrs:

        # Select all cereals made by the current manufacturer
        select = cereals[cereals.mfr == m]

        # Calculate the mean of the sugars column
        averages.append(select.sugars.mean())

    max_avg = max(averages)

    # Since the order of averages and mfrs are the same, the index of the highest average can be used to identify the manufacturer
    max_mfr = mfrs[averages.index(max_avg)]
    return max_mfr

def max_rating_mfr(cereals, mfrs):
    averages = []

    # Loop through all manufacturers
    for m in mfrs:

        # Select all cereals made by the current manufacturer
        select = cereals[cereals.mfr == m]

        # Calculate the mean of the rating column
        averages.append(select.rating.mean())

    max_avg = max(averages)
    # Since the order of averages and mfrs are the same, the index of the highest average can be used to identify the manufacturer
    max_mfr = mfrs[averages.index(max_avg)]
    return max_mfr


if __name__ == "__main__":
    main()
