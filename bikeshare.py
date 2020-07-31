##################################################################################################
#  Name : Diana Aranha
#  Project 2 : 
#  Due Date  : July 15, 2019
##################################################################################################
import time
import sys
import pandas as pd 
import numpy as np
import datetime
import json
from prettytable import PrettyTable

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

quit1 = False

def check_Valid_Input(inputMsg, nameList,name,limit):
    """
    This function is used to process the validity of input typed by user
    for the city, month and day.  
    It is invoked 3 times:
    a. first for city, 
    b. second for the month and
    c. third for the day

    Asks user to specify a city, month, and day for error checking

    Inputs:
        (str)  inputMsg - Specific to data entry (as numeric character) for the city, month and day
        (list) nameList - list representing the city names, month names and day names
        (str)  name     - string representing the string "city" or "month" or "day"
        (int)  limit    - beyond the acceptable numeric input (error input by user) that will raise a
                          ValueError exception

    Returns:
        (str) itemName - name of the city or month or day selected by user input, to filter the dataset
    """

    process = True
    quit1 = False

    while process or quit1:
        try:
            nameStr = input(inputMsg)
            # for input, only numeric is valid
            if nameStr not in ['0','1','2','3','4','5','6','7','8','9']:
                raise TypeError
            else:
                nameInt = int(nameStr)

            #print ('nameInt : ', nameInt)
            #Invalid numbers do not correspond to the items in name_Array

            if nameInt >= limit or nameInt < 0:
                raise ValueError  # for invalid numeric input
            elif nameInt == 0:
                print ('User quits the program')
                process = False
                quit1 = True
                sys.exit(0)       # raises exception; see sys.exit(1) below        
            else:
                # we get one of the items in name_Array - we have a match, so we quit the while loop 
                # itemName for specific element in the list for the city or the month or the day               
                itemName = nameList[nameInt - 1]
                process = False
                quit1 = False
                print()
                print(name + ' selected : ', itemName)
                print()
        except TypeError:
            print("Error : Input must be numeric : You typed : " + nameStr)
        except ValueError:
            print("Invalid selection for " + name + " : " + str(nameInt))            
        except:
            print("You have selected  : " + str(nameInt) + " to quit")
            sys.exit(1)   # exit the program
    return  itemName

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    print('=============================================\n')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # call function check_Valid_Input to process the city
    
    cityInputMsg = "Please Enter a number related to a City : \n\n" \
                   "1=Chicago, 2=New York City OR 3=Washington  OR 0=quit\n"

    cityNameList = ['Chicago', 'New York City', 'Washington']
    city = check_Valid_Input (cityInputMsg, cityNameList, "city", 4) 

    # get user input for month (all, january, february, ... , june)
    # call function check_Valid_Input to process the month
    monthInputMsg = "Please Enter a number related to a Month :\n\n" \
                    "1=January, 2=February, 3=March, 4=April, 5=May, 6=June, 7=All OR 0=quit\n"                   
 
    monthNameList = ['January','February','March','April','May','June','All']  
    month = check_Valid_Input (monthInputMsg, monthNameList, "month", 8)

     # get user input for day of the week
    # call function check_Valid_Input to process the day   
    dayInputMsg = "Please Enter a number related to a day of the week :\n\n" \
                  "1-Monday, 2=Tuesday, 3=Wednesday, 4=Thursday, 5=Friday, 6=Saturday, 7=Sunday OR 8=ALL OR 0=quit\n"

    dayList = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday', 'All']
    day = check_Valid_Input (dayInputMsg, dayList, "day", 9)   

    print('-'*80)
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

    cityStr = "city : " + city + " | "
    monthStr = "months : " + month + " | "
    dayStr = "days : " + day

    print ("\n *** Processing Bike Share Data using Filters : {}".format(cityStr + monthStr + dayStr) + " ***\n")
    print ('-'*80)    

    print ('\n\n---------- Basic Statistics of the dataset for : ' + city + ' when file is loaded -------------------------------\n\n', \
          df.describe(include='all'))

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time']   = pd.to_datetime(df['End Time'])

    # dt.weekday_name does not work with Python version 3.7.6 so the day_name was obtained and 
    # the weekend was filtered out
    # extract month and day of week from Start Time to create new columns
    df['week_day'] = df['Start Time'].dt.day_name()

    filter1 = df['Start Time'].dt.day_name() != "Saturday"
    filter2 = df['Start Time'].dt.day_name() != "Sunday"

    df.where(filter1 & filter2, inplace = True)   
   
    # extract month
    df['month']      = df['Start Time'].dt.month
    df['month_name'] = df['Start Time'].dt.month_name()    
    df['start_hour'] = df['Start Time'].dt.hour    

    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int

        months = ['January', 'February', 'March', 'April', 'May', 'June']       
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        #print ('Filter by Day : ', day.title())

        # filter by day of week to create the new dataframe
        #df = df[df['day_of_week'] == day.title()]
        
        df = df[df['week_day'] == day.title()]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\n----------------- Calculating The Most Frequent Times of Travel...  ----------------------\n')

    start_time = time.time()  

    # Time Stats in tabular form
    ts = PrettyTable()
    ts.field_names = ["Most Common Month","Most Common Day","Most Common Start Hour"]

    # ts.add_row([df2['month_name'].value_counts().idxmax(), df2['day_of_week'].value_counts().idxmax(), df2['start_hour'].value_counts().idxmax()])
    # ts.add_row([df2.loc[:,'month_name'].mode()[0], df2.loc[:,'day_of_week'].mode()[0], df2['start_hour'].mode()[0]])

    ts.add_row([df['month_name'].mode()[0], df['week_day'].mode()[0], df['start_hour'].mode()[0]])
    print(ts)      

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\n-------------------- Calculating The Most Popular Stations and Trip... ---------------------\n')
    print()

    start_time = time.time()    

    freq_Start_End_Stn_Combo = df['Start Station'] + ' ' + df['End Station']
    trips = freq_Start_End_Stn_Combo.value_counts()

    # Station Stats in tabular formdf['Start Station'] + ' ' + df['End Station']
    ss = PrettyTable()
    ss.field_names = ["Most Common Start Station ","Most Common End Station","Frequent Start - End Station Combo"]

    # display  most frequent start-end station combinations 
    ss.add_row([df['Start Station'].value_counts().idxmax(), df['End Station'].value_counts().idxmax(), trips.idxmax()])
    
    #ss.add_row([df['Start Station'].mode()[0], df['End Station'].mode()[0], trips.head()])  
    #ss.add_row([df['Start Station'].value_counts().head(1), df['End Station'].value_counts().head(1), trips.head()])

    print(ss)   
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*70)

def trip_duration_stats(df):
    """
       Displays statistics on 
       a. the total and average trip duration.
       b. Min, Max and Mean Trip duration
       c. Trip duration for each User Type
    """
  
    print ('\n-------------------- Calculating Trip Duration... -----------------------------------\n')    
    print ()

    start_time = time.time()    

    """ Method 1 """
    #total_travel_time = df['Trip Duration'].sum() /60 /60 /24
    #avg_travel_time = df['Trip Duration'].mean() / 60
    #min_travel_time = df['Trip Duration'].min() / 60
    #max_travel_time = df['Trip Duration'].max() / 60    

    # display trip duration -- total and avg time in tabular form
    #td = PrettyTable()
    #td.field_names = ["Total Travel Time", "Average Travel Time","Minimum Travel Time", "Max Travel Time"]   
    #td.add_row([total_travel_time, avg_travel_time, min_travel_time, max_travel_time])
    #print(td)
    
    # Method 2 : Alternate way to calculate Travel Time, total time and avg time using numpy

    df['Trip Time'] = df['End Time'] - df['Start Time']
    tot_trip_time = np.sum(df['Trip Time'])

    tot_Days = str(tot_trip_time).split()[0]
    avg_trip_time = np.mean(df['Trip Time'])
    avg_trip_round = round(avg_trip_time.total_seconds()/60)   

    tx = PrettyTable()
    tx.field_names = ["Total Trip Time", "Average Trip Time (Minutes)", "Total Trip Days"]
    tx.add_row ([tot_trip_time, avg_trip_round, tot_Days])
    print(tx)

    # get max, min, mean trip duration
    print('\n\n')

    ty = PrettyTable()
    ty.field_names = ["Min Trip Duration", "Max Trip Duration", "Mean Trip Duration"]
    ty.add_row ([df['Trip Duration'].min(), df['Trip Duration'].max(), round(df['Trip Duration'].mean())])
    print(ty)

    # get trip duration for each user type  

    print ('\n ------- Trip Duration for each User Type -------\n\n', \
            df.groupby(['User Type']).sum()['Trip Duration']) 
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*70)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\n----------------------- Calculating User Stats ...  -------------------------------------------\n')
    start_time = time.time()   

    # ----------------------------------------- U S E R T Y P E ---------------------------------------------    

    print ("-----------------------  U S E R  T Y P E   I N F O ---------------------------------------------")

    print ("\nMissing values in User Type : ",df['User Type'].isnull().sum())  
    
    # Display counts of user types in a tabular form
    y1 = PrettyTable()
    y1.field_names = ["User Type"]
    y1.add_row (([df["User Type"].value_counts(ascending=False, dropna=True)]))    
    print(y1)

    # ---------------------------------------------------- G E N D E R ---------------------------------    
    if 'Gender' in df.columns:
        print ()
        print ("-----------------------  G E N D E R   I N F O ----------------------------------------")
        print ()
        print ("\nMissing Values in Gender : ", df['Gender'].isnull().sum())
        print ("\nSum of Males and Females : ", df['Gender'].notnull().sum())
        print ()       

        # Display counts of gender in a tabular form
        x1 = PrettyTable()
        x1.field_names = ["Gender"]        
        x1.add_row([df['Gender'].value_counts(ascending=False, dropna=True)])
        print(x1)       
        
        print ('\n\n---------- Group by User Type and Gender including missing values : ----------------------\n', \
               df.groupby(['User Type','Gender'])['Gender'].count())
       
    else:
        print ("\n ********** Washington File does not have Gender Data **********\n")

    # -------------------------------------- B I R T H  Y E A R ----------------------------------------------          

    # Washington bikeshare file lacks the Birth Year and Gender columns
    #
    if 'Birth Year' in df.columns:
        print ()
        print ("-----------------------  B I R T H  Y E A R   I N F O ---------------------------------------------")
        print ("\nMissing Birth year values : ", df['Birth Year'].isnull().sum(axis=0))
        print ("\nNo. of Birth year values : ", df['Birth Year'].notnull().sum(axis=0))
        print ()

        # Display earliest, most recent, and most common year of birth
        # drop the rows with missing values 

        df3 = df['Birth Year'].dropna()      
        df3['Birth Year'] = df3.astype('int64')   #Change Birth Year from float to integer    

        # Birth Year data in tabular form
        by = PrettyTable()
        by.field_names = ["Earliest Birth Year", "Most Recent Birth Year", "Most Common Birth Year"]
        by.add_row([df3['Birth Year'].min(), df3['Birth Year'].max(), df3['Birth Year'].mode()[0]])
        print(by)   

    else:
        print ("\n ********** Washington File does not have Birth Year Data **********\n")      

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*70)

def show_raw_data(df):
    """ Prints raw data for bikeshare """

    rows = df.shape[0]

    # start from 0 to total rows and increment by 5
    for idx in range(0, rows, 5):
        yes = input('\n Show Trip data? Enter yes or no\n')
        if yes.lower() != 'yes':
            break

        # get raw data and change to json
        data_in_row = df.iloc[idx: idx + 5].to_json(orient='records', lines=True).split('\n')

        for currRow in data_in_row:
            # display data for each user
            row1 = json.loads(currRow)
            row_in_json = json.dumps(row1, indent=4)
            print (row_in_json)   

def main():
    while True:        
        city, month, day = get_filters()           
        df = load_data(city, month, day)       

        show_raw_data(df)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
