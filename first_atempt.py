import csv 
import math 

def cor_coefficient(X, Y, n):
    sum_X = 0
    sum_Y = 0
    sum_XY = 0
    squareSum_X = 0
    squareSum_Y = 0

    for i in range(n):
        # sum of X
        sum_X = sum_X + X[i] 
          
        # sum of Y
        sum_Y = sum_Y + Y[i] 
          
        # sum of X[i] * Y[i]. 
        sum_XY = sum_XY + X[i] * Y[i] 
          

        squareSum_X = squareSum_X + X[i] * X[i] 
        squareSum_Y = squareSum_Y + Y[i] * Y[i] 
    
    # use formula for calculating correlation  
    # coefficient. 
    numerator = (n * sum_XY - sum_X * sum_Y)
    denominator = math.sqrt(
                            (n * squareSum_X - sum_X * sum_X)* 
                            (n * squareSum_Y - sum_Y * sum_Y)
                            )
    try:
        corr = numerator/ denominator
        return corr

    except ZeroDivisionError:
        print("Zero division is not allowed")


def findPeakElement(nums):
    l = 0 
    r = len(nums) -1 
    while l < r:
        mid = (l + r)//2

        # If middle element is greater than  
        # its right neighbour, then left half must  
        # have a peak element 
        if nums[mid] > nums[mid + 1]:
            r = mid
        else:
            # If middle element is less than  
            # its right neighbour, then right half must  
            # have a peak element 
            l = mid + 1

    return l


class TaskOne:

    def __init__(self):
        pass 

def calculate_rate(a, b):
    """
    This method finds the ratio of a to b. 
        a: numerator.
        b: denominator.
    """
    return a/b

def update_highest_rate(cur_rate, cur_country, cur_highest_rate, highest_rate_Country):
    """
    Update the highest rate (infection/death) and country.
    """
    #if current rate is greater than current highest rate.
    if cur_rate > cur_highest_rate:
        cur_highest_rate = cur_rate
        highest_rate_Country = cur_country
    return cur_highest_rate, highest_rate_Country


def find_top_2(top_1, top_1_country, top_2, top_2_country, cur_count, cur_country):
    """
    It finds the highest and the second highest infections and the corresponding 
    countries.

    params:
        top_1: current highest number of infections. 
        top_1_country: country with the current highest infections. 
        top_2: current second highest number of infections.
        top_2_country: country with the current second highest infections. 
        cur_count: current number of infections. 
        cur_country: current country. 
    """
    #if the current number of infections is greater than the current highest,
    # copy current highest to second highest 
    #and update the current highest. 
    if top_1 < cur_count:

        top_2 = top_1
        top_2_country = top_1_country

        top_1 = cur_count
        top_1_country = cur_country

    #if the current number of infections is less than or equal to current highest,
    else:
        #if the current number of infections is greater than the current second highest,
        #update the second highest number of infections and country. 
        if top_2 < cur_count:
            top_2 = cur_count
            top_2_country = cur_country

    return {
        "top_1": top_1,
        "top_1_country": top_1_country,
        "top_2": top_2,
        "top_2_country": top_2_country
    } 

population = {}
with open("population_data.csv", "r") as f:
    reader = csv.DictReader(f)
    count = 0
    for row in reader:
        population[row["Country"]] = row["Population"]

with open("covid_data.csv", "r", encoding="utf-8-sig") as f2:
    reader2 = csv.DictReader(f2)
    next_country = next(reader2)

    #Initialize higest infection count and corresponding country
    highest_infection = 0.0
    highest_country =  next_country["CountryExp"]
    
    #Initialize second higest infection count and corresponding country
    second_highest_infection = 0.0
    second_highest_country =  next_country["CountryExp"]

    #Keep count of infections and deaths 
    confirmed_cases = float(next_country["NewConfCases"])
    confirmed_deaths = float(next_country["NewDeaths"])

    #innitialize the highest infection rate and country
    highest_infection_rate = 0.0
    highest_infection_rate_country = ""

    #innitialize the highest death rate and country
    highest_death_rate = 0.0
    highest_death_rate_country = ""

    #finding overall death rate
    total_deaths = float(next_country["NewDeaths"])
    total_infections = float(next_country["NewConfCases"])

    #finding positive trends
    recent_week_infections = [None] 
    recent_week_infections[0] = float(next_country["NewConfCases"])

    num_days = 1

    positive_trend_countries = []
    steepest_increase = 0.0
    steepest_increase_country = next_country["CountryExp"]

    negative_trend_countries = []
    steepest_decrease = 0.0
    steepest_derease_country = next_country["CountryExp"]

    peak_dates = [None]
    peak_dates[0] = next_country["DateRep"]
    earliest_peak = 8 
    earliest_peak_country = next_country["CountryExp"]
    earliest_peak_date = next_country["DateRep"]

    c = 0
    for row in reader2:
        #find overal deaths
        total_deaths += float(row["NewDeaths"])
        total_infections += float(row["NewConfCases"])
        

        #if the country is the same, keep counting infection and deaths 
        #for the country 
        if row["CountryExp"] == next_country["CountryExp"]:
            confirmed_cases += float(row["NewConfCases"])
            confirmed_deaths += float(row["NewDeaths"])

            #Append only the most recent one week
            if num_days < 7:
                recent_week_infections.insert(0, float(row["NewConfCases"]))
                peak_dates.insert(0, row["DateRep"])
                num_days += 1 
        else:
            c +=confirmed_cases
            print(next_country["CountryExp"], confirmed_cases, confirmed_deaths)
            ################## positive trends countries 
            num_recent_inf = len(recent_week_infections) 

            #ignore countries with less than 7 infection records
            #and countries that have the same new infections case throughout the week.
            # e. g [1,1,1,1,1,1,1]
            if num_recent_inf == 7 and \
                not all(recent_week_infections[i] == recent_week_infections[i+1] for i in range(num_recent_inf-1)):

                days_in_week = list(range(1,8))
                corr = cor_coefficient(days_in_week, recent_week_infections, num_recent_inf)

                #check correlation coefficient.
                if corr > 0:
                    positive_trend_countries.append(next_country["CountryExp"])

                    #update the country with the steepest increase. 
                    if corr > steepest_increase:
                        steepest_increase = corr
                        steepest_increase_country = next_country["CountryExp"]

                elif corr < 0:
                    negative_trend_countries.append(next_country["CountryExp"])

                    #update the country with the steepest decrease. 
                    if corr < steepest_decrease:
                        steepest_decrease = corr
                        steepest_decrease_country = next_country["CountryExp"]

                    ###############################country that peak earliest############
                    peak_index = findPeakElement(recent_week_infections)
                    if earliest_peak > peak_index:
                        earliest_peak = peak_index
                        earliest_peak_country = next_country["CountryExp"]
                        earliest_peak_date = peak_dates[peak_index]

            
            ############# Highest infection and country##############
            #Update the current highest and second higest infection and deaths

            ans = find_top_2(highest_infection, highest_country, 
                       second_highest_infection, second_highest_country, 
                       confirmed_cases, next_country["CountryExp"])

            highest_infection = ans["top_1"]
            highest_country =  ans["top_1_country"]
            
            second_highest_infection =  ans["top_2"]
            second_highest_country = ans["top_2_country"]

            # if highest_infection < confirmed_cases:
            #     #confirmed infections
            #     second_highest_infection = highest_infection
            #     second_highest_country = highest_country

            #     highest_infection = confirmed_cases
            #     highest_country = next_country["CountryExp"]

            # else:
            #     if second_highest_infection < confirmed_cases:
            #         second_highest_infection = confirmed_cases
            #         second_highest_country = next_country["CountryExp"]

            
            if next_country["CountryExp"] in population: #TODO: COrrect this. too inefficient. use try and catch
                #######################infection rate##############
                            
                inf_rate = calculate_rate(confirmed_cases, float(population[next_country["CountryExp"]]))

                highest_infection_rate, highest_infection_rate_country = update_highest_rate(
                                                                                inf_rate, next_country["CountryExp"], 
                                                                                highest_infection_rate,
                                                                                 highest_infection_rate_country)
            

                #######################death rate##############
                
                death_rate = calculate_rate(confirmed_deaths, float(population[next_country["CountryExp"]]))
                highest_death_rate, highest_death_rate_country = update_highest_rate(
                                                                                death_rate, next_country["CountryExp"], 
                                                                                highest_death_rate,
                                                                                highest_death_rate_country)
                
            ##############################Overal death rate@####################
            overall_death_rate = calculate_rate(total_deaths, total_infections)

            #move to the next country
            next_country = row
            confirmed_cases = float(next_country["NewConfCases"]) #for next country
            confirmed_deaths = float(next_country["NewDeaths"]) #for next country
            num_days = 1
            recent_week_infections = [None] 
            recent_week_infections[0] = float(next_country["NewConfCases"])

            peak_dates = [None] 
            peak_dates[0] = float(next_country["NewConfCases"])

    print(total_deaths, c)
    print("Inf: {}, {}".format(highest_infection_rate, highest_infection_rate_country))
    print("Death: {}, {}".format(highest_death_rate, highest_death_rate_country))
    print("Overall {}".format(overall_death_rate))
    print("Steepest increase: {}, {}".format(steepest_increase_country, steepest_increase))
    print("Steepest decrease: {}, {}".format(steepest_decrease_country, steepest_decrease))
    print("Earliest peak: {}, {}, {}".format(earliest_peak_country, earliest_peak_date, earliest_peak))
