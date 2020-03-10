import csv
import sys 
from os.path import isfile

"""
Authors: Mustapha Tidoo Yussif and Samuel Atule
class of 2020
"""

class TaskTwo:

    def __init__(self):
        self._pattern = []
        self._pattern_len = 0

        self.good_suffix_table = [] #suffix table as required by boyer moore algorithm. 
        
        self.bad_match_table = {}  # values to be used for skipping in case of mismatches
                                    #as required by the boyer moore algorithm. 

    def create_pattern(self, pattern_file):
        """
        This method constructs a list from the partial data file.
        The list is used as a pattern for searching.

        :param pattern_file: the name of the file containing the partial 
        time series data. 
        :return:
            Modifies the contents of self._pattern & self._pattern_len
        """

        with open(pattern_file, encoding="utf-8-sig") as r:
            partial_data = csv.reader(r)
            self._pattern = [row[0] for row in partial_data]

        self._pattern_len = len(self._pattern)


    def read_covid_data(self, data_file):
        """
        This method reads the data from the covid_data.csv file into two list. 
        The infections list contains the new infection cases in the file and the
        info list contains the correspoding dates and country for the case. 

        :param data_file: the name of the covid_fie. 
        :return:
          :infections: a list of all infection cases in the file. 
          :info: a list containing (country, data) corresponding to the case. 
        """
        infections = []
        info = []
        with open(data_file, encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                infections.append(row["NewConfCases"])
                info.append((row["CountryExp"], row["DateRep"]))

        return infections, info


    def KMP_search(self, data_file):
        """
        This method implements the Knutt-Morris-Pratt (KMP) algorithm. 
        
        :param data_file: the name of the covid_data file. 
        :return:
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



    def boyer_more_search(self, values):
        """
        This method implements the Boyer-Moore string matching algorithm. 

        :param values: this is a list containing all the new infection 
                      cases recorder till date. 

        :return:
          returns the position where a match is found.
        """
        ln = len(values)
        index = 0

        while index <= ln - self._pattern_len:
            j = self._pattern_len - 1

            while j >= 0 and self._pattern[j] == values[index + j]:
                j = j - 1

            if j < 0:
                return index + self._pattern_len - 1
            else:
                mismatch = values[index + j]
                # mismatched items which do not exist in pattern has an occurrence value of -1.
                step = -1
                try:
                    step = self.bad_match_table[mismatch]
                except KeyError:
                    pass

                # avoid backward steps in case step is bigger than unmatched_index
                step = max(1, j - step)
                index = index + max(step, self.good_suffix_table[j + 1])

        return -1

    def find_pattern(self, data_file, pattern_file, algorithm):
        """
        This method calls the string matching functions based. If the 
        algorithm is set to kmp, the KMP algorithm is called to 
        find the string matching. This approach is used when the length 
        of the pattern is shorter. The Boyer-moore algorithm is called 
        otherwise. And that one is suitable for longer patterns. 

        :param data_file: the name of the covid data file. 
        :param pattern_file: name of the partial time series file.
        :param algorithm: the algorithm to call. 
        """
        if algorithm == "kmp":
            country, date = self.KMP_search(data_file)
            self.output_results(country, date, data_file)
        else:
            infec, info = self.read_covid_data(data_file)
            self._build_good_suffix_table()
            self._build_bad_match_table()
            index = self.boyer_more_search(infec)
            if index > 0:
                self.output_results(info[index][0], info[index][1], data_file)
            else:
                self.output_results("not", "found", data_file)


    def _build_bad_match_table(self):
        """
        A method for pre-processing the skip values for
        the bad match rule of Boyer-Moore's algorithm
        :return:
        Modifies the contents of self._bad_item_skips by setting them
            to the proper.
        """
        # keep values to be used for skipping in case of mismatches.
        # subsequent occurrences of an item in the pattern  override previous ones
        for i in range(self._pattern_len):
            self.bad_match_table[self._pattern[i]] = i


    def _build_good_suffix_table(self):
        """
        A method for preprocessing the skip values for the 
        boyer moore algorithm when there is a match. 
        """
        ln = self._pattern_len

        # tables for skip distances and borders
        self.good_suffix_table = [0] * (ln + 1)
        borders = [0] * (ln + 1)

        s = ln
        m = ln + 1

        # the first item on the right end has maximum
        borders[s] = m

        while s > 0:
            while m <= ln and self._pattern[s - 1] != self._pattern[m - 1]:

                if self.good_suffix_table[m] == 0:
                    self.good_suffix_table[m] = m - s

                m = borders[m]

            s = s - 1
            m = m - 1
            borders[s] = m

        # Working with the so called case2 of the good suffix table.
        k = borders[0]
        for i in range(ln):
            if self.good_suffix_table[i] == 0:
                self.good_suffix_table[i] = k

            if i == k:
                k = borders[i]


    def output_results(self, country, date, filename):
        """
        This method writes the results of the task 2(the country and date)
        where the pattern occured into a file. 

        :param country: the name of the country. 
        :param date: the name where the pattern occured. 
        :param filename: the name of the input file. 

        """
        output_file = filename.split("\\")[-1].split(".")[-2]
        with open("output/task2_solution-" + output_file + ".txt", "w") as f2:
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

            #if the length of the pattern string is less than 15,
            #call KMP
            if self._pattern_len < 15:
                self.find_pattern(data_file, pattern_file, "kmp")
            else:
                self.find_pattern(data_file, pattern_file, "bm")
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