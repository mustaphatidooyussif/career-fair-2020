import csv
import sys 

"""
Authors: Mustapha Tidoo Yussif and Samuel Atule
"""

class TaskTwo:

    def KMP_search(self, string, sub):
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

        aux = self._build_aux(sub)
        n = len(string) 

        while (i < n):

            #if all the characters mathed,
            if string[i] == sub[j]:
                i += 1
                j += 1 

                #and j is equal to the total length of the substring. 
                #a match is found. 
                if j == len(sub):
                    return (i-j)

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

        #read the covid data file 
        confirmed_cases = []
        infor = []
        with open(covid_data_file, "r", encoding="utf-8-sig") as f:
            reader1 = csv.DictReader(f)
            for row in reader1:
                confirmed_cases.append(row["NewConfCases"])
                infor.append((row["CountryExp"], row["DateRep"]))

        #read the partial time series data
        pattern = []
        with open(partial_time_series_file, "r", encoding="utf-8-sig") as f1:
            reader2 = csv.reader(f1)
            for row in reader2:
                pattern.append(row[0])

        index = TaskTwo().KMP_search(confirmed_cases, pattern)

        #write results to a file
        output_file = partial_time_series_file.split(".")[0]
        with open("task2_solution-" + output_file + ".txt", "w") as f2:
            f2.write(infor[index][0] + "\n")
            f2.write(infor[index][1] + "\n")

    except IndexError:
        print("Usage: python task2.py covid_data.csv partial_time_series.csv")