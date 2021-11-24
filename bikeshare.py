import time
import pandas as pd
import numpy as np
#Making a change to commit it later

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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Enter the city (Chicago, New York City or Washington): ')
        if city.lower() in ['chicago','new york city','washington']:
            print('We are going to see data from',city.title()+'. Good choice!')
            break
        else:
            print('ERROR! Please try again.')

    filters_decision = input('\nDo you want to apply some filters? (Type "yes" or "no"): ')
    if filters_decision.lower() == 'yes' or filters_decision.lower() == 'y':
    # TO DO: get user input for month (all, january, february, ... , june)
        while True:
            month = input('\nEnter the name of the month to filter by, or "All" to apply no month filter (All, January, February, ... , June): ')
            if month.lower() in ['all','january','february', 'march', 'april', 'may', 'june']:
                break
            else:
                print('ERROR! Please try again.')

        # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
        while True:
            day = input('\nEnter the name of the day to filter by, or "All" to apply no day filter (All, Monday, Tuesday, ..., Sunday): ')
            if day.lower() in ['all','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                break
            else:
                print('ERROR! Please try again.')
        print('\n\nOkay! Just to check, you choose...\nMonth: ',month.title(),'\nDay: ',day.title())
    else:
        month = 'all'
        day = 'all'
        
    print('-'*40)
    return city.lower(), month.lower(), day.lower()


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
    df['month'] = pd.DatetimeIndex(df['Start Time']).month
    df['day_of_week'] = pd.DatetimeIndex(df['Start Time']).dayofweek
    ##print (df.head())
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_num = months.index(month)+1 #le sumo 1 porque en la funcion de DatetimeIndex(...).month, los meses van de 1 a 12... Estos index van de 0 a 11.
        # filter by month to create the new dataframe
        df = df[df.month==month_num]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        days=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day_num = days.index(day)
        df = df[df.day_of_week==day_num]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month_size = df['month'].value_counts().size
    if month_size == 1:
        print('The most common month is: obviously %s, because you filtered by month' % (months[df['month'].mode()[0]-1]).title())
    else:
        print('The most common month is:',months[df['month'].mode()[0]-1].title())

    # TO DO: display the most common day of week
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    days_size = df['day_of_week'].value_counts().size
    if days_size == 1:
        print('The most common day is: obviously %s, because you filtered by day' % (days[df['day_of_week'].mode()[0]]).title())
    else:
        print('The most common day is:',days[df['day_of_week'].mode()[0]].title())

    # TO DO: display the most common start hour
    df['hour'] = pd.DatetimeIndex(df['Start Time']).hour
    if month_size == 1 or days_size == 1:
        print('According to your filters, the most common start hour is',str(df['hour'].mode()[0])+':00:00')
    else:
        print('The most common start hour is',str(df['hour'].mode()[0])+':00:00')

    print( "\nThis took %s seconds." % (round(time.time() - start_time,7)) )
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # TO DO: display most commonly used start station
    print('The most commonly used start station is:',df['Start Station'].mode()[0]) #I will not going to show the filters message again (see lines 99 and 107), I think that point is clear.

    # TO DO: display most commonly used end station
    print('The most commonly used end station is:',df['End Station'].mode()[0])

    # TO DO: display most frequent combination of start station and end station trip
    df['Start and End Station'] = df['Start Station'] + '---' + df['End Station']
    print('The most frequent combination of start station and end station trip is:',"'"+str(df['Start and End Station'].mode()[0]).split('---')[0]+"'",'with',"'"+str(df['Start and End Station'].mode()[0]).split('---')[1]+"'")


    print("\nThis took %s seconds." % (round(time.time() - start_time,7)) )
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_hours = int(total_travel_time//3600)
    total_travel_minutes = int((total_travel_time%3600)//60)
    total_travel_seconds = int(((total_travel_time%3600)%60))
    print('The total travel time is',total_travel_hours,'hours,',total_travel_minutes,'minutes and',total_travel_seconds,'seconds.')

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_hours = int(mean_travel_time//3600)
    mean_travel_minutes = int((mean_travel_time%3600)//60)
    mean_travel_seconds = int(((mean_travel_time%3600)%60))
    print('The mean travel time is',mean_travel_hours,'hours,',mean_travel_minutes,'minutes and',mean_travel_seconds,'seconds.')

    print("\nThis took %s seconds." % (round(time.time() - start_time,7)) )
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('Counts of user types:')
    print(df['User Type'].value_counts())

    # TO DO: Display counts of gender
    if 'Gender' in df:
        print('\nCounts of user genders:')
        print(df['Gender'].value_counts())

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print('\nThe oldest user was born in',int(df['Birth Year'].min()),'\nThe youngest user was born in',int(df['Birth Year'].max()),'\nThe most common year of birth is',int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def raw_data(df):
    decision = input('\nDo you want to see raw data? Type "yes" or "no".\n')
    if decision.lower() == 'yes' or decision.lower() == 'y':
        for i in range(len(df)):
            print(df.iloc[i])
            stop = input('\nIf you want to stop seeing raw data, please type "stop". Otherwise, just press Enter.\n')
            if stop.lower() == 'stop':
                break
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter "yes" or "no".\n')
        if restart.lower() != 'yes':
            print('Goodbye!')
            break


if __name__ == "__main__":
	main()
