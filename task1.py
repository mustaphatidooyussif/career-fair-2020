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
        self.total_confirmed_deaths = data["init_confirmed_deaths"]
        self.total_confirmed_cases = data["init_confirmed_cases"]

        #Keep count of infections and deaths 
        self.confirmed_deaths_by_country = data["init_confirmed_deaths"]
        self.confirmed_cases_by_country = data["init_confirmed_cases"]

        self.num_days = 1
        self.recent_week_infections = [None] 
        self.recent_week_infections[0] = data["init_confirmed_cases"]

        #finding  trends
        # self.recent_week_dates = [None]
        # self.recent_week_dates[0] = data["init_date"]

        self.positive_trend_countries = []
        self.negative_trend_countries = []

        self.steepest_increase = -1
        self.steepest_increase_country = data["init_country_name"]

        self.steepest_decrease = 1
        self.steepest_decrease_country =  data["init_country_name"]

        self.earliest_peak_country = data["init_country_name"]
        self.earliest_peak_date = datetime.strptime(data["init_date"], '%m/%d/%y')

        
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


        self.last_peak_value = 0
        self.last_peak_country = ""
        self.last_peak_date = ""

    def update_totals(self, x, y):

        """
        Updates the total number of confirmed cases 
        and confirmed deaths.
        """
        self.total_confirmed_cases += float(x) 
        self.total_confirmed_deaths += float(y) 

    def update_by_country(self, x, y):
        """
        A method for accumulating the new confirmed infection cases and confirmed 
        deaths for each country.
        :param x: the new confirmed infection case for the country on a particular date.  
        :param y: the new confirmed death recorded for the country on a particular date. 
        :return : 
            None
        """
        self.confirmed_cases_by_country += float(x) 
        self.confirmed_deaths_by_country += float(y)

    def update_recent_week_data_by_country(self, case):
        """
        Gets the most recent one week confirmed cases and dates.
        """
        self.recent_week_infections.insert(0, float(case))

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
        This method Updates country with the speepest decrease. 
        """
        if  corr < self.steepest_decrease:
            self.steepest_decrease =  neg_corr
            self.steepest_decrease_country = country
    

    def find_last_peak_by_country(self, a, b, cur_country, cur_date):
        """
        This method is supposed to find the earliest peak date. However, the 
        date is read in reverse chronological with the most recent date 
        being read first. As the result, the last peak in this case, becomes
        the earliest peak. It keeps comparing and updating the peak and peak date
        till the last peak. 

        :param a: the current new infection case recorded for the country. 
        :param b: the new new infection case recorded for the country. 
        :param cur_country: the name of the country. eg. Afghanistan. 
        :param cur_date: the current date of the new infection case. 
        """
        if a > b:
            self.last_peak_value = a
            self.last_peak_country = cur_country
            self.last_peak_date = datetime.strptime(cur_date, "%m/%d/%y")

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
             
        :param cur_count: current number of infections for the country on a particular date.  
        :param cur_country: the name of the current country. 
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
        :param a: numerator.
        :param b: denominator.
        """
        return a/float(b)

    def update_highest_infection_rate(self, cur_rate, cur_country):
        """
        This method updates the highest  infection rate and the country with the 
        highest infection rate. There is a global variable `highest_infection_rate`
        that keeps track of the highest infection rate. When a new infection rate 
        `cur_rate` is calculated, it is compared with it and update the highest 
        infection rate if it `cur_rate` is greater. 

        :param cur_rate: the infection rate of each country.
        :param cur_country: the name of the country whose infection rate is passed along. 
        """
        #if current rate is greater than current highest rate.
        if cur_rate > self.highest_infection_rate:
            self.highest_infection_rate = cur_rate
            self.highest_infection_rate_country = cur_country

    def update_highest_death_rate(self, cur_rate, cur_country):
        """
        This method updates the highest  death rate and the country with the 
        highest death rate. There is a global variable `highest_death_rate`
        that keeps track of the highest infection rate. When a new death rate 
        `cur_rate` is calculated, it is compared with it and update the `highest_death_rate`
        rate if it `cur_rate` is greater. 

        :param cur_rate: the death rate of each country.
        :param cur_country: the name of the country whose death rate is passed along. 
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

            #get the first row
            next_country = next(reader2)

            init_data = {
                "init_country_name": next_country["CountryExp"],
                "init_confirmed_cases": float(next_country["NewConfCases"]),
                "init_confirmed_deaths": float(next_country["NewDeaths"]),
                "init_date": next_country["DateRep"]
            }
            
            # Initialize the class. 
            t = TaskOne(init_data)

            possible_earliest_peak = 0
            possible_earliest_peak_country = ""
            possible_earliest_peak_date = ""

            previous = next_country

            for row in reader2:
                #find overall deaths and infections
                t.update_totals(row["NewConfCases"], row["NewDeaths"])

                #if the country is the same, keep counting infection and deaths 
                #for the country 
                if row["CountryExp"] == next_country["CountryExp"]:
                    t.update_by_country(row["NewConfCases"], row["NewDeaths"])

                    #update the earliest peak for each country. 
                    current = row
                    t.find_last_peak_by_country(
                        previous["NewConfCases"], current["NewConfCases"], 
                        previous["CountryExp"], previous["DateRep"])

                    previous = current

                    #Append only the most recent one week
                    if t.num_days < 7:
                        t.update_recent_week_data_by_country(row["NewConfCases"])
                        t.num_days += 1 

                else:
                    ################## positive trends countries 
                    num_recent_inf = len(t.recent_week_infections)

                    #ignore countries with less than 7 infection records
                    #and countries that have the same new infections case throughout the week.
                    # e. g [1,1,1,1,1,1,1]
                    if num_recent_inf == 7 and \
                        not all(t.recent_week_infections[i] == t.recent_week_infections[i+1] for i in range(num_recent_inf-1)):

                        days_in_week = list(range(1,8))
                        corr = t.cor_coefficient(days_in_week, t.recent_week_infections, num_recent_inf)

                        #both negative and positive peaks 

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

                            
                            if t.earliest_peak_date > t.last_peak_date:
                                t.earliest_peak_date = t.last_peak_date
                                t.earliest_peak_country = t.last_peak_country 

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

                    #move to the next country
                    next_country = row
                    t.confirmed_cases_by_country = float(next_country["NewConfCases"]) #for next country
                    t.confirmed_deaths_by_country = float(next_country["NewDeaths"]) #for next country
                    t.num_days = 1
                    t.recent_week_infections = [None]
                    t.recent_week_infections[0] = float(next_country["NewConfCases"])

            ##############################Overal death rate@####################
            t.overall_death_rate = t.calculate_rate(t.total_confirmed_cases, t.total_confirmed_deaths)

        #write results to a file
        output_file = covid_data_file.split(".")[0]
        with open("task1_solution-" + output_file + ".txt", "w") as f2:
            f2.write("(a) " + t.highest_infection_country + ", " +str(t.highest_infection) + "\n")
            f2.write("(b) " + t.second_highest_infection_country + ", " + str(t.second_highest_infection) + "\n")
            f2.write("(c) " +t.highest_infection_rate_country + ", " + str(t.highest_infection_rate) + "\n")
            f2.write("(d) " +str(t.overall_death_rate)  + "\n")
            f2.write("(e) " +t.highest_death_rate_country + ", " + str(t.highest_death_rate) + "\n")
            f2.write("(f) " + ",".join(t.positive_trend_countries) + "\n")
            f2.write("(g) " + str(t.steepest_increase_country)  + "\n")
            f2.write("(h) " +",".join(t.negative_trend_countries) + "\n")
            f2.write("(i) " + t.steepest_decrease_country  + "\n")
            f2.write("(j) " +t.earliest_peak_country + ", " + t.earliest_peak_date.strftime("%m/%d/%y") + "\n")

    except IndexError:
        print("Usage: python task1.py covid_data.csv population_data.csv")