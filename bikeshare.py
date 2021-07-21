import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
DATABASE=CITY_DATA

def get_filters(city, month, day):
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ' '
    while True:
        city = input("What is the city do you want to explore ? Chicago, New York City or Washington!\n").lower()
        if city not in DATABASE:
            print("\n Sorry you did enter an invalid answer. Could you try again please ?\n")
            continue
        else:
            break
    month = ' '
    while True:
        time = input("How would you like to proceed ? per month, day, all or none?\n").lower()
        if time == 'month':
            month = input("Which month you want? January, February, March, April, May or June?\n").lower()
            day = 'all'
            break

        elif time == 'day':
            month = 'all'
            day = input("Which day you want? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday\n").lower()
            break

        elif time == 'all':
            month = input("Which month do you want? January, February, March, April, May or June?\n").lower()
            day = input("Which day do you want? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday\n").lower()
            break
        elif time == 'none':
            month = 'all'
            day = 'all'
            break
        else:
            input("you enter an incorrect word! Please type  again. month, day, all or none?\n")
            break

    print(city)
    print(month)
    print(day)
    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(DATABASE[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        months = ['january', 'feburary', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nstatistics on the most frequent times of travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print(common_month)

    # display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print(common_day_of_week)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print(common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nstatistics on the most popular stations and trip\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print(common_start)

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print(common_end)

    # display most frequent combination of start station and end station trip
    most_freq_station_comb = df['Start Station'] + ' to ' + df['End Station']
    print('The most frequnt combination of start station and end station trip was {}'.format(
        most_freq_station_comb.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("the total travel time :",total_travel_time)

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print("means time of travaelling:",mean_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_counts = df['User Type'].value_counts()
    print("count of user types: ", user_type_counts)

    # Display counts of gender
    if 'Gender' not in df:
        print('Shoot, no gender data for this city :(')
    else:
        gender_of_users = df.groupby('Gender', as_index=False).count()
        print('Number of genders of users mentioned in the data are {}'.format(len(gender_of_users)))
        for i in range(len(gender_of_users)):
            print('{}s - {}'.format(gender_of_users['Gender'][i], gender_of_users['Start Time'][i]))
        print('Gender data for {} users is not available.'.format(
            len(df) - gender_of_users['Start Time'][0] - gender_of_users['Start Time'][1]))

    # Display earliest, most recent, and most common year of birth
    if 'Birth_Year' in df:
        earliest = df['Birth_Year'].min()
        print(earliest)
        recent = df['Birth_Year'].max()
        print(recent)
        common_birth = df['Birth Year'].mode()[0]
        print(common_birth)
    else:
        print("There is no birth year information in this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


""" we can ask the user if he wantes 10 lines of the raw data and more"""


def data(df):
    view_data = (input('\nWould you like to view 10 rows of individual trip data? Enter yes or no\n')).lower()
    start_loc = 0
    while view_data != "no":
        print(df.iloc[start_loc:start_loc + 10])
        start_loc += 10
        view_display = (input("Do you wish to continue?answer by yes or no:\n ")).lower()
        if view_display == "no":
            break

def main():
    city = ""
    month = ""
    day = ""
    while True:
        city, month, day = get_filters(city, month, day)
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()