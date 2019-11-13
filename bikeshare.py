import time
import pandas as pd
import numpy as np

"""
Cities and corresponding csv files
"""
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# Yearly Months
months =  ['january','february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city = input("Select City you would like to explore (chicago,new york city, washington) ")
    city = city.lower()
    
    while city not in ('chicago','new york city', 'washington') :
        city = input("Please select a valid city name (chicago,new york city, washington) ")
        city = city.lower()
        
    month = input(" Select Month (all, january,february, march, april, may, june, july, august, september, october, november, december)")
    month = month.lower()
    
    while month not in ('all', 'january','february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'):
         month = input(" Select valid option (all, january,february, march, april, may, june, july, august, september, october, november, december)")
         month = month.lower()

    day = input("Select day of the week (all,monday,tuesday,wednesday,thursday,friday,saturday,sunday)")
    day = day.lower()
    
    while day not in ('all','monday','tuesday','wednesday','thursday','friday','saturday','sunday'):
        day = input("Select day of the week (all,monday,tuesday,wednesday,thursday,friday,saturday,sunday)")
        day = day.lower()

    print('-'*40)
    return city, month, day

def display_data(df):
    """
    Asks user to view 5 lines of raw data (yes/no).

    Returns:
        - 5 lines of raw data
        - prompts back for additional 5 lines of raw data
    """

    lower_bound = 0 #initializing the first index
    
    while True:
        choice = input('\nWould you like to view 5 lines of raw bikeshare data? Enter yes or no.\n').lower() #getting user's choice
        
        if choice == 'yes':
            print(df.iloc[lower_bound:lower_bound + 5]) # printing data in specified boundaries
            lower_bound += 5 #incrementing the bound
        else:
            break
        

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
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        month = months.index(month) + 1
        df = df[df['month'] == month]
        
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
   
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    common_month = df['month'].mode()[0]
    print(' Most Common Month is {} \n'.format(months[common_month - 1]))

    common_day = df['day_of_week'].mode()[0]
    print('Most Common day is {} \n'.format(common_day))

    common_start_hour = df['Start Time'].dt.hour.mode()[0]
    print('Most common start hour is {} \n'.format(common_start_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    common_start_station = df['Start Station'].mode()[0]
    print("Most common starting station is {} \n".format(common_start_station))
    
    common_end_station = df['End Station'].mode()[0]
    print("Most common ending station is {} \n".format(common_end_station))

    frequent_combination = df.groupby(['Start Station','End Station']).size().nlargest(1)
    print(" The most frequent Start and End station is {} ".format(frequent_combination))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    print("Total Travel Time is {} \n".format(total_travel_time))

    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time is {} \n".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    user_types = df['User Type'].value_counts()
    print("User Types {} \n".format(user_types))

    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print("Gende Count {} \n".format(gender))

    if 'Birth Year' in df.columns:
        earliest_year_of_birth = df['Birth Year'].min()
        recent_year_of_birth = df['Birth Year'].max()
        common_year_of_birth =  df['Birth Year'].mode()[0]
        
        print("Earliest year of birth {} \n".format(earliest_year_of_birth))
        print("Most Recent year of birth {} \n".format(recent_year_of_birth))
        print("Most common year of birth {} \n".format(common_year_of_birth))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        """
        Checking if data frame is not empty 
        """
        if not df.empty:
            display_data(df)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
        else:
            print("You filtered on empty data")
            
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
