import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington)
    city = input('For which city do you want to receive information? Enter "chicago", "new york city" or "washington".\n').lower()
    while str(city) != "chicago" and str(city) != "new york city" and str(city) != "washington":
        print('If you want to terminate the query, enter "exit".\n')
        city = input('Invalid input. Please enter one of the following city names: "chicago", "new york city" or "washington".\n').lower()
        if str(city) == "exit":
            quit()

    # get user input for month (all, january, february, ... , june)
    global month_options
    month_options = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = input('For which month do you want to receive information? Enter a month name between january and june or write "all".\n').lower()
    if str(month) == "exit":
            quit()
    while str(month) not in month_options:
        city = input('Invalid input. Please enter one of the following expressions: {}.\n'.format(month_list)).lower()
        if str(month) == "exit":
            quit()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_options = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = input('For which day of the week do you want to receive information? Enter a day name e.g. "thursday" or simply write "all".\n').lower()
    if str(day) == "exit":
            quit()
    while str(day) not in day_options != "all":
        day = input('Invalid input. Please enter one of the following expressions: {}.\n'.format(day_list)).lower()
        if str(day) == "exit":
            quit()

    print('-'*40)
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

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day_of_Week'] = df['Start Time'].dt.weekday_name
    df['Start Hour'] = df['Start Time'].dt.hour
    df['Stop Hour'] = df['End Time'].dt.hour
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        global month_number
        month_number = months.index(month) + 1
        df = df[df['Month'] == month_number]
    if day != 'all':
        df = df[df['Day_of_Week'] == day.title()]
    return df

def time_stats(df, month, day, city):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    month_count = {}
    # differentiating between broad scrope (all months) and narrow scope (particular month)
    if str(month) == 'all':
        i = 1
        for month_name in month_options[1:]:
            month_count[month_name] = df[df['Month'] == i]['Month'].count()
            i += 1
        v = list(month_count.values())
        k = list(month_count.keys())
        max_month = k[v.index(max(v))]
        max_month_count = max(v)
        print("In {}, {} is the most common month with a total of {} bike rentals.".format(city.capitalize(), max_month.capitalize(), max_month_count))
        if str(day) == 'all':
            day_count = df['Day_of_Week'].value_counts()
            max_day = day_count.index.tolist()[0]
            max_day_count = day_count[max_day]
            print('{} is the most frequent day of travel in {} with a total of {} bike rentals.'.format(max_day, city.capitalize(), max_day_count))

            hour_count = df['Start Hour'].value_counts()
            max_hour = hour_count.index.tolist()[0]
            max_hour_count = hour_count[max_hour]
            print('Overall, {}:00 is the most common time of travel in {} with a total of {} bike rentals.'.format(max_hour, city.capitalize(), max_hour_count))
    else:
        if str(day) == 'all':
            day_count = df['Day_of_Week'].value_counts()
            max_day = day_count.index.tolist()[0]
            max_day_count = day_count[max_day]
            print('During {}, {} is the most frequent day of travel in {} with a total of {} bike rentals.'.format(month, max_day, city.capitalize(), max_day_count))

            hour_count = df['Start Hour'].value_counts()
            max_hour = hour_count.index.tolist()[0]
            max_hour_count = hour_count[max_hour]
            print('During {}, the most common time of travel in {} is {}:00 with a total of {} bike rentals.'.format(month, city.capitalize(), max_hour, max_hour_count))
        else:
            hour_count = df['Start Hour'].value_counts()
            max_hour = hour_count.index.tolist()[0]
            max_hour_count = hour_count[max_hour]
            print('For {}s during {}, the most common time of travel in {} is {}:00 with a total of {} bike rentals.'.format(day, month, city.capitalize(), max_hour, max_hour_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_count = df['Start Station'].value_counts()
    max_start = start_count.index.tolist()[0]
    max_start_count = start_count[max_start]

    # display most commonly used end station
    end_count = df['End Station'].value_counts()
    max_end = end_count.index.tolist()[0]
    max_end_count = end_count[max_end]

    # display most frequent combination of start station and end station trip
    combinations = df.groupby(['Start Station', 'End Station']).size().reset_index().rename(columns={0:'count'})
    combinations_sorted = combinations.sort_values('count', ascending=False)
    show_first_five = input('Do you want to see the 5 most frequent combinations of start stations and end stations? Enter "yes" to see the corresponding data or "no" to skip .\n').lower()
    if str(show_first_five) == 'yes':
        print(combinations_sorted.head(5))

    # ask user for input to trigger print of further results
        more_detail = input('Do you want to see more combinations? Enter "yes" to see 5 additional lines. Otherwise, enter "no" to proceed.\n').lower()
        while str(more_detail) != 'yes' and str(more_detail) != 'no':
            more_detail = input('Invalid input. Please enter "yes" or "no".\n').lower()
        i = 5
        j = 5
        while i < len(combinations_sorted) and str(more_detail) == 'yes':
            print(combinations_sorted.iloc[i:i+j])
            more_detail = input('Do you want to see more combinations? Enter "yes" to see 5 additional lines. Otherwise, enter "no" to proceed.\n').lower()
            while str(more_detail) != 'yes' and str(more_detail) != 'no':
                more_detail = input('Invalid input. Please enter "yes" or "no".\n').lower()
            if str(more_detail) == 'yes':
                i = i + j

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df, city):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    time_sum = df['Trip Duration'].agg(np.sum)
    days = (time_sum % (60 * 60 * 24))
    print('The total travel time for the selected timeframe in {} is {} days or {} seconds.\n'.format(city.capitalize(), days, time_sum))

    # display mean travel time
    time_mean = df['Trip Duration'].mean()
    mean_2_d = round(time_mean, 2)
    print('The average travel time for the selected timeframe in {} is {} seconds.\n'.format(city.capitalize(), mean_2_d))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city, ):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    # display counts of user types
    sub_count = df[df['User Type'] == 'Subscriber']['User Type'].value_counts()[0]
    cust_count = df[df['User Type'] == 'Customer']['User Type'].value_counts()[0]
    print('For the selected timeframe in {}, a total of {} users are subscribers and {} are customers.\n.'.format(city.capitalize(), sub_count, cust_count))

    # display counts of gender (no data available for the washington dataset)
    if str(city) == 'chicago' or str(city) == 'new york city':
        female_sum = df[df['Gender'] == 'Female']['Gender'].value_counts()[0]
        male_sum = df[df['Gender'] == 'Male']['Gender'].value_counts()[0]
        NaN_sum = df['Gender'].isnull().sum()

        print('From all users for the selected timeframe in {}, a total of {} users are female, {} are male and {} did not specify their gender.\n'.format(city.capitalize(), female_sum, male_sum, NaN_sum))



    # display earliest, most recent, and most common year of birth
    try:
        earliest_date = df['Birth Year'].min()
        recent_date = df['Birth Year'].max()
        count_date = df['Birth Year'].value_counts()
        common_date = count_date.index.tolist()[0]
        print(' The earliest year of birth is {}.\n The most recent year of birth is {}.\n The most common year of birth is {}.\n'.format(earliest_date, recent_date, common_date))

    # no data on birth year available for the washington dataset. Therefore, an except statement must be incorporated
    except KeyError:
        print("No information on the earliest, most recent and most common year of birth can be provided for the washington dataset.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, month, day, city)
        station_stats(df)
        trip_duration_stats(df, city)
        user_stats(df, city)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
