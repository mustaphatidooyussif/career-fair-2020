import csv
import sys 

"""
Authors: Mustapha Tidoo Yussif and Samuel Atule
"""

class TaskTwo:

    def KMP_search(self, data_file, pattern_file):
        """
        This method implements the Knutt-Morris-Pratt (KMP) algorithm. 
        parametrs:
            :string: original or big string to search from. 
            : sub: substring or pattern searching for. 
        
        return val:
            returns the starting index of where the pattern is found. 
        """
        
        i = 0 #counter for original string. 

        j = 0 # counter for substrng or pattern.

        #read the pattern to a list.
        sub = []
        with open(pattern_file, "r", encoding="utf-8-sig") as f:
            r1 = csv.reader(f)
            for row in r1:
                sub.append(row[0])

        #Create the auxillary array for the pattern. 
        aux = self._build_aux(sub)

        with open(data_file, "r", encoding="utf-8-sig") as f2:
            r2 = csv.DictReader(f2)

            try:
                while True:
                    #if all the characters mathed,
                    row = next(r2)
                    if row["NewConfCases"] == sub[j]:
                        i += 1
                        j += 1 

                        #and j is equal to the total length of the substring. 
                        #a match is found. 
                        if j == len(sub):
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
                print("Match is not found.")
                return None, None 

    def _build_aux(self, sub):
        """
        This method builds the proper prefix array for KMP string searching
        algorithm.

        sub:
            The substring or the pattern to search for. 
        """
        m = len(sub)
        aux = [0] *  m  #create an auxilary array. 

        i = 0
        j = 1

        while (j < m):

            #if both characters match, uppdate value at j and increment both i and j. 
            if sub[i] == sub[j]:
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

if __name__=="__main__":

    try:
        #get files from command line
        covid_data_file = sys.argv[1]
        partial_time_series_file = sys.argv[2]

        country, date  = TaskTwo().KMP_search(covid_data_file, partial_time_series_file)

        #if there is a match,
        #write results to a file
        if country is not None and date is not None:
            output_file = covid_data_file.split(".")[0]
            with open("task2_solution-" + output_file + ".txt", "w") as f2:
                f2.write(country + "\n")
                f2.write(date + "\n")

    except IndexError:
        print("Usage: python task2.py covid_data.csv partial_time_series.csv")