"""
Authors: Mustapha Tidoo Yussif and Samuel Atule
"""
import csv 
import math 
import sys
from datetime import datetime

class TaskOne:
    def __init__(self, data):
        #finding overall death rate
        self.total_confirmed_deaths = 0
        self.total_confirmed_cases = 0

        #Keep count of infections and deaths 
        self.confirmed_deaths_by_country = data["init_confirmed_deaths"]
        self.confirmed_cases_by_country = data["init_confirmed_cases"]

        self.num_days = 1
        self.recent_week_infections = [None] 
        self.recent_week_infections[0] = data["init_confirmed_cases"]

        #finding  trends
        self.recent_week_dates = [None]
        self.recent_week_dates[0] = data["init_date"]

        self.positive_trend_countries = []
        self.negative_trend_countries = []

        self.steepest_increase = -1
        self.steepest_increase_country = data["init_country_name"]

        self.steepest_decrease = 1
        self.steepest_decrease_country =  data["init_country_name"]

        self.earliest_peak_country = data["init_country_name"]
        self.earliest_peak_date = datetime.strptime(data["init_date"], '%m/%d/%Y')

        
        #Initialize higest infection count and corresponding country
        self.highest_infection = 0.0
        self.highest_infection_country =  data["init_country_name"]
        
        #Initialize second higest infection count and corresponding country
        self.second_highest_infection = 0.0
        self.second_highest_infection_country =  data["init_country_name"]


        #innitialize the highest infection rate and country
        self.highest_infection_rate = 0.0
        self.highest_infection_rate_country = data["init_country_name"]

        #innitialize the highest death rate and country
        self.highest_death_rate = 0.0
        self.highest_death_rate_country = data["init_country_name"]


    def update_totals(self, x, y):

        """
        Updates the total number of confirmed cases 
        and confirmed deaths.
        """
        self.total_confirmed_deaths += float(x) 
        self.total_confirmed_cases += float(y) 

    def get_total_deaths(self):
        return self.total_confirmed_deaths 

    def get_total_cases(self):
        return self.total_confirmed_cases 

    def update_by_country(self, x, y):
        """
        Accumulates the number of confirmed cases and 
        deaths for each country. 
        """
        self.confirmed_cases_by_country += float(x) 
        self.confirmed_deaths_by_country += float(y)

    def update_recent_week_data_by_country(self, case, date):
        """
        Gets the most recent one week confirmed cases and dates.
        """
        self.recent_week_infections.insert(0, float(case))
        self.recent_week_dates.insert(0, date)

    def cor_coefficient(self, X, Y, n):
        """
        Finds the correlation coefficient between X and Y. 
        It helps us determine the trends in the new confirmed cases. 
        """
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

    def update_trend(self, pos_country = None, neg_country = None):

        #Adds country with the number of new infections per day on the rise. 
        if pos_country is not None:
            self.positive_trend_countries.append(pos_country)

         #Adds country with the number of new infections per day decreasing. 
        if neg_country is not None:
            self.negative_trend_countries.append(neg_country)

    def find_steepest_increase(self, pos_corr, country):
        """
        Updates country witht the speepest increase.

        params:
            pos_corr: positve correlation coefficient. 
            country: name of the country. 
        """
        if  corr > self.steepest_increase:
            self.steepest_increase =  pos_corr
            self.steepest_increase_country = country

    def find_steepest_decrease(self, neg_corr, country):
        """
        Updates country witht the speepest decrease.
        """
        if  corr < self.steepest_decrease:
            self.steepest_decrease =  neg_corr
            self.steepest_decrease_country = country
    
    def findPeakElement(self, nums):
        """
        Finds the first the index of the first peak element.

        params:
            nums: list of the most recent one week new infection cases. 
        """
        for i in range(len(nums)-1):
            if nums[i] > nums[i+1]:
                return i
            
        return len(nums)-1

    def find_earliest_peak_country(self, peak_index, country):
        """
        Method to find the country tha has the earlies peak in new confirmed infections. 

        params:
            peak_index: index of the peak element. 
            country: the name of the country. 
        """
        peak_date= datetime.strptime(self.recent_week_dates[peak_index], '%m/%d/%Y')
        if peak_date < self.earliest_peak_date:
            self.earliest_peak_date = peak_date
            self.earliest_peak_country = country

    def find_top_2(self, cur_count, cur_country):
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
        if self.highest_infection < cur_count:

            self.second_highest_infection = self.highest_infection
            self.second_highest_infection_country = self.highest_infection_country

            self.highest_infection = cur_count
            self.highest_infection_country = cur_country

        #if the current number of infections is less than or equal to current highest,
        else:
            #if the current number of infections is greater than the current second highest,
            #update the second highest number of infections and country. 
            if self.second_highest_infection < cur_count:
                self.second_highest_infection = cur_count
                self.second_highest_infection_country = cur_country


    def calculate_rate(self, a, b):
        """
        This method finds the ratio of a to b. 
            a: numerator.
            b: denominator.
        """
        return a/float(b)

    def update_highest_infection_rate(self, cur_rate, cur_country):
        """
        Update the highest  infection rate and country.
        """
        #if current rate is greater than current highest rate.
        if cur_rate > self.highest_infection_rate:
            self.highest_infection_rate = cur_rate
            self.highest_infection_rate_country = cur_country

    def update_highest_death_rate(self, cur_rate, cur_country):
        """
        Update the highest  death rate and country.
        """
        #if current rate is greater than current highest rate.
        if cur_rate > self.highest_death_rate:
            self.highest_death_rate = cur_rate
            self.highest_death_rate_country = cur_country

if __name__=="__main__":

    try:

        #get files from command line
        covid_data_file = sys.argv[1]
        population_data_file = sys.argv[2]

        population = {}
        with open(population_data_file, "r") as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                population[row["Country"]] = row["Population"]

        with open(covid_data_file, "r", encoding="utf-8-sig") as f2:
            reader2 = csv.DictReader(f2)
            next_country = next(reader2)

            init_data = {
                "init_country_name": next_country["CountryExp"],
                "init_confirmed_cases": float(next_country["NewConfCases"]),
                "init_confirmed_deaths": float(next_country["NewDeaths"]),
                "init_date": next_country["DateRep"]
            }
            
            t = TaskOne(init_data)

            for row in reader2:

                #if the country is the same, keep counting infection and deaths 
                #for the country 
                if row["CountryExp"] == next_country["CountryExp"]:
                    t.update_by_country(row["NewConfCases"], row["NewDeaths"])

                    #Append only the most recent one week
                    if t.num_days < 7:
                        t.update_recent_week_data_by_country(row["NewConfCases"], row["DateRep"])
                        t.num_days += 1 
                else:

                    #find overall deaths and infections
                    t.update_totals(t.confirmed_cases_by_country, t.confirmed_deaths_by_country)

                    ################## positive trends countries 
                    num_recent_inf = len(t.recent_week_infections)

                    #ignore countries with less than 7 infection records
                    #and countries that have the same new infections case throughout the week.
                    # e. g [1,1,1,1,1,1,1]
                    if num_recent_inf == 7 and \
                        not all(t.recent_week_infections[i] == t.recent_week_infections[i+1] for i in range(num_recent_inf-1)):

                        days_in_week = list(range(1,8))
                        corr = t.cor_coefficient(days_in_week, t.recent_week_infections, num_recent_inf)

                        #check correlation coefficient.
                        if corr > 0:
                            t.update_trend(pos_country = next_country["CountryExp"], neg_country = None)

                            #update the country with the steepest increase. 
                            if corr > t.steepest_increase:
                                t.find_steepest_increase(corr, next_country["CountryExp"])

                        elif corr < 0:
                            t.update_trend(pos_country = None, neg_country = next_country["CountryExp"])

                            #update the country with the steepest decrease. 
                            if corr < t.steepest_decrease:
                                t.find_steepest_decrease(corr, next_country["CountryExp"])

                            ###############################country that peak earliest############
                            peak_index = t.findPeakElement(t.recent_week_infections)
                            t.find_earliest_peak_country(peak_index, next_country["CountryExp"])

                    
                    ############# Highest infection and country##############
                    #Update the current highest and second higest infection and deaths

                    t.find_top_2(t.confirmed_cases_by_country, next_country["CountryExp"])

                    
                    if next_country["CountryExp"] in population: #TODO: COrrect this. too inefficient. use try and catch
                        #######################infection rate##############
                                    
                        inf_rate = t.calculate_rate(t.confirmed_cases_by_country, population[next_country["CountryExp"]])

                        t.update_highest_infection_rate(inf_rate, next_country["CountryExp"])
                    
                        #######################death rate##############
                        death_rate = t.calculate_rate(t.confirmed_deaths_by_country, population[next_country["CountryExp"]])
                        t.update_highest_death_rate(death_rate, next_country["CountryExp"])

                    ##############################Overal death rate@####################
                    t.overall_death_rate = t.calculate_rate(t.total_confirmed_cases, t.total_confirmed_deaths)

                    #move to the next country
                    next_country = row
                    t.confirmed_cases_by_country = float(next_country["NewConfCases"]) #for next country
                    t.confirmed_deaths_by_country = float(next_country["NewDeaths"]) #for next country
                    t.num_days = 1
                    t.recent_week_infections = [None]
                    t.recent_week_infections[0] = float(next_country["NewConfCases"])

                    t.recent_week_dates = [None]
                    t.recent_week_dates[0] = next_country["DateRep"]

        #write results to a file
        output_file = population_data_file.split(".")[0]
        with open("task1_solution-" + output_file + ".txt", "w") as f2:
            f2.write(t.highest_infection_country + "," +str(t.highest_infection) + "\n")
            f2.write(t.second_highest_infection_country + "," + str(t.second_highest_infection) + "\n")
            f2.write(t.highest_infection_rate_country + "," + str(t.highest_infection_rate) + "\n")
            f2.write(str(t.overall_death_rate)  + "\n")
            f2.write(t.highest_death_rate_country + "," + str(t.highest_death_rate) + "\n")
            f2.write(",".join(t.positive_trend_countries) + "\n")
            f2.write(str(t.steepest_increase_country)  + "\n")
            f2.write(",".join(t.negative_trend_countries) + "\n")
            f2.write(t.steepest_decrease_country  + "\n")
            f2.write(t.earliest_peak_country + "," + t.earliest_peak_date.strftime("%d-%b-%Y") + "\n")

    except IndexError:
        print("Usage: python task1.py covid_data.csv population_data.csv")