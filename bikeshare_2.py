import time
import datetime
import pandas as pd
import numpy as np
from difflib import get_close_matches

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['sunday', 'monday','tuesday','wednesday','thursday','friday','saturday']

def validate_city(city): 
    """
    This function checks if the user entered city is available in the dictionary
    Args:
        city
    Returns:
        True --> if the city is present
        False --> if the city is not present
    """
    if city in CITY_DATA:
        return True
    else:
        return False

def validate_month(month):
    """
    This function checks if the user entered month is available for analysis
    Args:
        month
    Returns:
        True --> month is present
        False -->month is not present
    """
    if month in months or month == 'all':
        return True
    else:
        return False

def validate_day(day):
    """
    This function checks if the user entered day is a valid one
    Args:
        day
    Returns:
        True --> entered day is correct
        False -->entered day value is a garbage
    """
    if day in days or day == 'all':
        return True
    else:
        return False

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print('Hello! Let\'s explore some US bikeshare data!')
    print("+++++++++++++++++++++++++++++++++++++++++++++\n")

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print("Please select a city 'Chicago/New York City/Washington'")
    global city
    city = input("City: ").lower()
    #validate the city input
    while (validate_city(city) == False):
        #check for minor spelling mistakes and get the close match for the input
        if len(get_close_matches(city,CITY_DATA.keys()))>0:
            confirmation = input("Did you mean '%s' instead? Type yes/no: " % get_close_matches(city,CITY_DATA.keys())[0].title())
            if confirmation.lower() == 'yes':
                city = get_close_matches(city,CITY_DATA.keys())[0]
            else:
                city = input("Please enter a valid city 'chicago/new york city/washington': ")
        else:
            print(" \n")
            city = input("Please enter a valid city 'chicago/new york city/washington': ")

        
    # get user input for month (all, january, february, ... , june)
    print("\nPlease select a month for analysis january to june")
    print("type 'all' if you want to view data for all months")
    month = input("Month: ").lower()
    while(validate_month(month) == False):
        #check for minor spelling mistakes and get the close match for the input
        if len(get_close_matches(month,months))>0:
            confirmation = input("Did you mean '%s' instead? Type yes/no: " % get_close_matches(month,months)[0].title())
            if confirmation.lower() == 'yes':
                month = get_close_matches(month,months)[0]
            else:
                month = input("Please enter a valid month january to june: ")
        else:
            month = input("Please enter a valid month january to june: ")
        

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print("\nPlease select a day for analysis ex: sunday/monday")
    print("type 'all' if you want to view data for all days")
    day = input("Day: ").lower()
    while(validate_day(day) == False):
        #check for minor spelling mistakes and get the close match for the input
        if len(get_close_matches(day,days))>0:
            confirmation = input("Did you mean '%s' instead? Type yes/no: " % get_close_matches(day,days)[0].title())
            if confirmation.lower() == 'yes':
                day = get_close_matches(day,days)[0]
            else:
                day = input("Please enter a valid day: ")
        else:
            day = input("Please enter a valid day: ")
    
    print("\n")
    print("******************************************************************")
    print("                Displaying analysis for")
    print("                CITY : ", city.title())
    print("                MONTH: ", month.title())
    print("                DAY  : ", day.title())
    print("******************************************************************")

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
        # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month)+1    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_format(hour):
    """
    This function converts the 24Hr format to 12Hr format
    Args:
        hour in 24hr format
    Returns:
        hour --> in 12hr format
        notation --> am/pm
    """    
    if hour == 0:
        notation = 'am'
        hour = 12
    elif 1 <= hour < 12:
        notation = 'am'
    elif 13 <= hour < 24:
        notation = 'pm'
        hour = hour - 12
    else:
        #return 12noon as 12pm
        notation = 'pm'    
    return hour, notation


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    Args:
        bikeshare dataframe
    Returns:
        none    
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = months[(df["month"].value_counts().index[0] - 1)]
    print("Month --> {}".format(most_common_month.upper()))    

    # display the most common day of week
    most_common_day = df["day_of_week"].value_counts().index[0]
    print("Day   --> {}".format(most_common_day.upper()))

    # display the most common start hour
    most_common_starthour = df["Start Time"].dt.hour.value_counts().index[0]
    '''
    for debugging purpose
    print(df["Start Time"].dt.hour.value_counts())
    '''
    #most_common_starthour = int(df["Start Time"].dt.hour.mode())
    hour, notation = time_format(most_common_starthour)
    print("Hour  --> {}{}".format(hour, notation))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)

def create_trippoints(df):
    """
    This function creates a 'journey' column that concatenates
    "start Station" with 'End Station'
    Args:
        bikeshare dataframe
    Returns:
        none
    """

    df['journey'] = df['Start Station'].str.cat(df['End Station'], sep=' TO ')

def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    Args:
        bikeshare dataframe
    Returns:
        none    
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_startstation = df["Start Station"].value_counts().index[0]
    print("Start station --> {}".format(most_common_startstation))
    
    #print(df["Start Station"].value_counts())

    # display most commonly used end station
    most_common_endstation = df["End Station"].value_counts().index[0]
    print("End Station   --> {}".format(most_common_endstation))
    #print(df["End Station"].value_counts())

    # display most frequent combination of start station and end station trip
    create_trippoints(df)
    most_pop_trip = df['journey'].mode().value_counts().index[0]
    print('Popular Trip  --> {}.'.format(most_pop_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def trip_duration_stats(df):
    """
    Finds and prints the total trip duration and average trip duration in
       hours, minutes, and seconds.
    Args:
        bikeshare dataframe
    Returns:
        none
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    minute, second = divmod(total_duration, 60)
    hour, minute = divmod(minute, 60)
    print('Total trip duration --> {} hours, {} minutes and {}'
          ' seconds.'.format(hour, minute, second))

    # display mean travel time
    average_duration = round(df['Trip Duration'].mean())
    m, s = divmod(average_duration, 60)
    if m > 60:
        h, m = divmod(m, 60)
        print('Average trip duration --> {} hours, {} minutes and {}'
              ' seconds.'.format(h, m, s))
    else:
        print('Average trip duration --> {} minutes and {} seconds.'.format(m, s))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def user_stats(df):
    """Displays statistics on bikeshare users.
    Args:
        bikeshare dataframe
    Returns:
        none    
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df["User Type"].value_counts()
    print(user_type)
    global city
    if "Gender" in df.columns:        
        # Display counts of gender
        gender_type = df["Gender"].value_counts()
        print(gender_type)
    else:
        print("Gender data not available for the city ", city)

    if "Birth Year" in df.columns:
        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = str(int(df['Birth Year'].min()))
        print("Earliest Birth Year: "+ earliest_birth_year)
        
        most_recent_birth_year = str(int(df['Birth Year'].max()))
        print("Most Recent Birth Year: " + most_recent_birth_year)
        
        most_common_birth_year = str(int(df['Birth Year'].mode()))
        print("Most Common Birth Year: " + most_common_birth_year)
    else:
        print("Birth Year data not available for the city ", city)
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        #print(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
