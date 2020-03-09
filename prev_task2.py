import csv
import sys 
from os.path import isfile

"""
Authors: Mustapha Tidoo Yussif and Samuel Atule
"""

class TaskTwo:

    def __init__(self):
        self._pattern = []
        self._pattern_len = 0

    def create_pattern(self, pattern_file):
        """
        This method constructs a list from the partial data file.
        The list is used as a pattern for searching.
        :return:
            Modifies the contents of self._pattern & self._pattern_ln
        """

        with open(pattern_file, encoding="utf-8-sig") as r:
            partial_data = csv.reader(r)
            self._pattern = [row[0] for row in partial_data]

        self._pattern_len = len(self._pattern)


    def KMP_search(self, data_file):
        """
        This method implements the Knutt-Morris-Pratt (KMP) algorithm. 
        
        :param data_file: substring or pattern searching for. 
        :return::
            returns the country and the date where th pattern is found. 
        """
        
        i = 0 #counter for original string. 

        j = 0 # counter for substrng or pattern.

        #Create the auxillary array for the pattern. 
        aux = self._build_proper_prefix()

        with open(data_file, "r", encoding="utf-8-sig") as f2:
            r2 = csv.DictReader(f2)

            try:
                while True:
                    #if all the characters mathed,
                    row = next(r2)
                    if row["NewConfCases"] == self._pattern[j]:
                        i += 1
                        j += 1 

                        #and j is equal to the total length of the substring. 
                        #a match is found. 
                        if j == self._pattern_len:
                            return row["CountryExp"], row["DateRep"]

                    #if there is a mismatch, two conditions are handled.  
                    #(whether the mismatch occured at the start or not)
                    else:
                        if j == 0:
                            # Move to the next character in only the original string. 
                            i += 1 
                        else:
                            # aux[i-1] gives the index from where to start the comparison
                            #after the mismatch. 
                            j = aux[j - 1]

            except StopIteration:
                return "not", "found" 

    def _build_proper_prefix(self):

        """
        This method builds the proper prefix array as specified by the KMP string searching
        algorithm.
        
        # 1. Initialize a list of the same size as the pattern to search with zeroes. 
        # 2. Initialize iterators for the string to search from and pattern to search for. 
        #3. If a character at index j matches with with another at index i, set the prefix
        #at i to plus 1 to prefix at j and increment both i and j. 
        #4. otherise, 
        # a. if j is not at the beginning of the pattern, get the suffix
        # of the position immediately before j and continue matching.
        # b. otherwise, set the suffix at the current index, i to zero.
        # index 0 is a special case of b.


        :return: The suffix to be used for computing the kmp pattern skip indices
        """
        aux = [0] *  self._pattern_len  #create an auxilary array.

        i = 0
        j = 1

        while (j < self._pattern_len):

            #if both characters match, uppdate value at j and increment both i and j. 
            if self._pattern[i] == self._pattern[j]:
                aux[j] = aux[i] + 1

                i += 1
                j += 1 
            else:
                #if both characters do not match, check
                #if not at the starting index, i = index of previous character
                if i != 0:
                    i = aux[i-1]

                #copy i to cell j.
                else:
                    aux[j] = i 
                    j += 1

        return aux 

    def output_results(self, country, date, filename):
        """
        This method writes the results of the task 2(the country and date)
        where the pattern occured into a file. 

        :param country: the name of the country. 
        :param date: the name where the pattern occured. 
        :param filename: the name of the input file. 

        """
        output_file = filename.split(".")[0]
        with open("task2_solution-" + output_file + ".txt", "w") as f2:
            f2.write(country + "\n")
            f2.write(date + "\n")

    def task2(self, data_file, pattern_file):
        """
        This calls the atomic functions, arrange them in order to comple find the 
        pattern. 
        :param data_file: The file containing the covid-19 data. 
        :param pattern_file: The file containing the partial time series. 
        :return:
            Writes a file task2_results-<data_file> to the folder containing this file.
        """

        if isfile(data_file) and isfile(pattern_file):
            self.create_pattern(pattern_file)
            country, date = self.KMP_search(data_file)
            self.output_results(country, date, data_file)
        else:
            exit("Error: check files you passed")

if __name__=="__main__":

    try:
        #get files from command line
        covid_data_file = sys.argv[1]
        partial_time_series_file = sys.argv[2]

        task2 = TaskTwo()
        task2.task2(covid_data_file, partial_time_series_file)

    except IndexError:
        print("Usage: python task2.py covid_data.csv partial_time_series.csv")