import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Returns filters from the following functions:
        get_city() - asks user to enter name of the city to analyze
        get_month() - asks user to enter name of the month to filter by, or "all" to apply no month filter
        get_day() - asks user to enter name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city = get_city()
    month = get_month()
    day = get_day()
    return city, month, day


def get_city():
    """
    Asks user to enter the name of the city to analyze.
    Returns name of the city.
    """
    city_list = ['Chicago', 'New York City', 'Washington']
    city =  None
    while city not in city_list:
        try:
            city = input('Type Chicago, New York City, or Washington: ').title()
            if city not in city_list:
                print('Oops! That\'s not one of the three cities. Try again.')
        except:
            continue
        print(('You have chosen {}.').format(city))
    return city


def get_month():
    """
    Asks user to enter the name of the month to analyze, or "all" to apply no month filter.
    Returns name of the month to analyze or "all".
    """
    month_list = ['All', 'January', 'February', 'March', 'April', 'May', 'June']
    month = None
    while month not in month_list:
        try:
            month = input('Type \'all\' or a month between January and June: ').title()
            if month not in month_list:
                print('Oops! Please type \'all\' or a month between January and June.')
        except:
            continue
        print(('You have chosen: {}').format(month))
    return month


def get_day():
    """
    Asks user to enter the name of the day of the week to analyze, or "all" to apply no day filter.
    Returns name of the day to analyze or "all".
    """
    day_list = ['All', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    day = None
    while day not in day_list:
        try:
            day = input('Type \'all\' or a day of the week: ').title()
            if day not in day_list:
                print('Oops! Please type \'all\' or a day of the week.')
        except:
            continue
        print(('You have chosen: {}').format(day))
    return day


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
    if city == 'Chicago':
        filename = 'chicago.csv'
    elif city == 'New York City':
        filename = 'new_york_city.csv'
    else:
        filename = 'washington.csv'
    df = pd.read_csv(filename)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    if month != 'All':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'All':
        df = df[df['day_of_week'] == day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', popular_month)

    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular Day:', popular_day)

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    pop_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', pop_start_station)

    pop_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', pop_end_station)

    popular_trip = (df['Start Station'] + ' to ' + df['End Station']).mode()[0]
    print('Most Popular Trip:', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    travel_time = df['Trip Duration'] / 60
    print('Total Travel Time in Minutes:\n', travel_time)

    average_trip = travel_time.mean()
    print('Average Travel Time:', average_trip, ' minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))


def user_stats(df, city):
    """
    Displays statistics on bikeshare user type.
    Displays statistics on bikeshare user genders for cities other than Washington.
    Displays statistics on bikeshare user birth years for cities other than Washington.
    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
        (str) city - city as selected by user
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print(user_types)

    if city != 'Washington':
        user_gender = df['Gender'].value_counts()
        print(user_gender)
    else:
        print('No gender data available for this city.')

    if city != 'Washington':
        oldest = int(df['Birth Year'].min())
        youngest = int(df['Birth Year'].max())
        pop_birth_year = int(df['Birth Year'].mode())
        print('Earliest Birth Year:', oldest,
              '\nMost Recent Birth Year:', youngest,
              '\nMost Common Birth Year:', pop_birth_year)
    else:
        print('No birth year data available for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))


def view_data(df):
    """
    Asks user whether they want to view raw data.
    Continues providing raw data in rows of 5 until user enters 'no.'
    """
    get_data = input('\nWould you like to view the raw data? Enter yes or no.\n')
    i = 5
    while get_data.lower() != 'no':
        print(df.iloc[i-5:i])
        i += 5
        get_data = input('\nContinue? Enter yes or no.\n')
        continue


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        view_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
