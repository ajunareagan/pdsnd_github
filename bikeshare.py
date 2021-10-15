import time
import pandas as pd
import numpy as np
import json

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

days=['monday','tuesday','wednesday','thursday','friday','saturday','sunday']

months=['january','february','march','april','may','june']

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
        city=input('Please enter the city you would want to explore! forexample washington, chicago or new york city \n').lower()
        if city in CITY_DATA:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    
    while True:
        month=input('Which month are you interested in (You can type january,february....june or all for none) \n').lower()
        
        if month.isalpha():
            if month in months:
                break
            if month =='all':
                break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
        
    while True:
        day=input('Now provide the day of the week you are intrested in... you can user monday,truesday...sunday \n').lower()
        if day in days:
            break
        if day=='all':
            break

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
    # here i load the datak
    df=pd.read_csv(CITY_DATA[city])
    
    df['Start Time']=pd.to_datetime(df['Start Time'])
    
    df['month']=df['Start Time'].dt.month
    df['day_of_week']=df['Start Time'].dt.weekday_name
    df['hour']=df['Start Time'].dt.hour
    
    #filter by month
    if month!='all':
        month =months.index(month)+1
        df=df[df['month']==month]
        
    #filter by day of week
    if day!='all':
        df=df[df['day_of_week']==day.title()]
        
    return df

def time_statistics(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    mostCommonMonth=df['month'].mode()[0]
    print('The most common month is :{}'.format(months[mostCommonMonth-1]) )

    # TO DO: display the most common day of week
    mostCommonDayOfWeek =df['day_of_week'].mode()[0]
    print('The most common day of the week is: {}'.format(mostCommonDayOfWeek))

    # TO DO: display the most common start hour
    mostCommonStartHour=df['hour'].mode()[0]
    print('The most common start hour is: {}'.format(mostCommonStartHour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_statistics(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_commonly_used_start_station=df['Start Station'].value_counts().idxmax()
    print('The most commonly used start station: ',most_commonly_used_start_station)

    # TO DO: display most commonly used end station
    most_commonly_used_end_station=df['End Station'].value_counts().idxmax()
    print('The most commonly used end station is: ',most_commonly_used_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    most_common_start_and_end_station=df[['Start Station','End Station']].mode().loc[0]
    print('The most frequent start and end station is {}:{}'.format(most_common_start_and_end_station[0],most_common_start_and_end_station[1]))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_statistics(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time=df['Trip Duration'].sum()
    print('The total travel time: ',total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time=df['Trip Duration'].mean()
    print('The mean travel_time is :',mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_statistics(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('Count of user types is:... \n')
    user_type_counts=df['User Type'].value_counts()
    
    #loop through to print the total number of user types
    for index, user_count in enumerate(user_type_counts):
        print(' {}: {}'.format(user_type_counts.index[index],user_count))
    
    print("..........")
 
    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        user_gender_statistics(df)

    # TO DO: Display earliest, most recent, and most common year of birth
    
    if 'Birth Year' in df.columns:
        user_birth_statistics(df)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def user_gender_statistics(df):
    """ function for user gender stats """
    print('Count of gender \n')
    gender_counts=df['Gender'].value_counts()
    #loop through to print the total number of gender
    for index, gender_count in enumerate(gender_counts):
        print(' {}: {}'.format(gender_counts.index[index],gender_count))
    
    print()
   
def user_birth_statistics(df):
    """ function for user birth stats """
    birth_year=df['Birth Year']
    #most common birth year
    most_common_birth_year=birth_year.value_counts().idxmax()
    print('Most common birth year is: ',most_common_birth_year)
    
    #most recent birth year
    most_recent_birth_year=birth_year.max()
    print('The most recent birth year is: ',most_recent_birth_year)
    
    #most earliest birth year
    most_earliest_birth_year =birth_year.min()
    print('Most earliest birth year is: ',most_earliest_birth_year)
    
def calculate_statistics(city,df):
    """ stats on bikeshare users """
    
    #Total Trip duration per gender
    if 'Gender' in df.columns:
        viewData=df.groupby(['Gender'])['Trip Duration'].sum().reset_index(name='Trip Duration')
        print('Trip duration per gender\n')
        print(viewData)
    #number of missing values in the entire sheet
    missing_values=np.count_nonzero(df.isnull())
    print('Number of missing values in the {} dataset:{}'.format(city,missing_values))
    
def display_raw_data(df):
    """ Display raw data (for only 5 rows ) """
    raw_data_lenght=df.shape[0]
    #loop through from 0 to number of  rows in steps of 5
    for i in range(0,raw_data_lenght,5):
        response=input('\n Do you want examin a perticular user data? Type \'yes \'or \'no \'\n')
        if response.lower()!='yes':
            break
            
        data=df.iloc[i: i+5].to_json(orient='records',lines=True).split('\n')
        for row in data:
            passed=json.loads(row)
            j_row=json.dumps(passed,indent=3)
            print(j_row)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_statistics(df)
		
        station_statistics(df)
		
        trip_duration_statistics(df)
		
        user_statistics(df)
        
        calculate_statistics(city,df)
        
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()