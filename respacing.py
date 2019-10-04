"""
Created on Wed Oct  2 21:20:06 2019

@author: Wenyi Chu (wc625)
HW1 partner: Qixin Ding (qd49)
"""



# DO NOT CHANGE THIS CLASS
class RespaceTableCell:
    def __init__(self, value, index):
        self.value = value
        self.index = index
        self.validate()

    # This function allows Python to print a representation of a RespaceTableCell
    def __repr__(self):
        return "(%s,%s)"%(str(self.value), str(self.index))

    # Ensure everything stored is the right type and size
    def validate(self):
        assert(type(self.value) == bool), "Values in the respacing table should be booleans."
        assert(self.index == None or type(self.index) == int), "Indices in the respacing table should be None or int"

# Inputs: the dynamic programming table, indices i, j into the dynamic programming table, the string being respaced, and an "is_word" function.
# Returns a RespaceTableCell to put at position (i,j)
def fill_cell(T, i, j, string, is_word):
    if (i==0 and j==0):
        value = True
        index = 0
#        print("Fill (%d,%d) with %r " % (i,j,value) + str(index))
        return RespaceTableCell(value, index)

    if (i==0 and j!=0):
        value = False
        index = None
#        print("Fill (%d,%d) with %r " % (i,j,value) + str(index))
        return RespaceTableCell(value, index)     
   
    if (i!=0 and j==0):
        value = True
        index = 0
#        print("Fill (%d,%d) with %r " % (i,j,value) + str(index))
        return RespaceTableCell(value, index)    
    
    # deal with copy  
    cell = T.get(i-1,j)  
    if (cell.value == True):   
#        print("copycopy from up")
        value = True
        index = cell.index
#        print("Fill (%d,%d) with %r " % (i,j,value) + str(index))
        return RespaceTableCell(True, cell.index)
 

#    print("examine substring")
    substring = string[i-1:j]
#    print(substring)
    
    if (substring == ""):
        value = False
        index = None
#        print("Fill (%d,%d) with %r " % (i,j,value) + str(index))
        return RespaceTableCell(value, index)       
    
    cell = T.get(i,j-len(substring))
#    print("if word? %r" % is_word(substring))
#    print("if prev-cell? %r" % cell.value)
    
    value = (cell.value and is_word(substring))
    if value:
        index = j
    else: 
        index = None

#    print("Fill (%d,%d) with %r " % (i,j,value) + str(index))
    return RespaceTableCell(value, index)
                  
# Inputs: N, the size of the list being respaced
# Outputs: a list of (i,j) tuples indicating the order in which the table should be filled.
def cell_ordering(N):
    result = []
    # N = 19 for the quick example (s="itwasthebestoftimes")
    
    for i in range (N+1):
        base_case_row = (0,i)
        result.append(base_case_row)
    
    for i in range (1,N+1):
        base_case_col = (i,0)
        result.append(base_case_col)

    for i in range (1,N+1):
        for j in range (1,N+1):
            tuple = (i,j)
            result.append(tuple)

    return result

# Input: a filled dynamic programming table.
# (See instructions.pdf for more on the dynamic programming skeleton)
# Return the respaced string, or None if there is no respacing.
def respace_from_table(s, table):
    
    # start from bottom right corner
    new_string = ""
    result_j = []
    
    n = len(s) # in the simple case, n=5
    row = n
    col = n  
    
    while (col > 0):        
        cell = table.get(row,col)
        
        while (cell.value == True):
            row = row - 1
            cell = table.get(row,col)
#            print(row,col,cell.value)
        
#        print("saw first false, jump out, and go left")

        row = row + 1
        result_j.insert(0,col)
        col = col - 1
#        print(row,col,cell.value)  
        
        while (cell.value == False):
            col = col - 1
            cell = table.get(row,col)
#            print(row,col,cell.value)
        
        row = row - 1       
#        print("saw first true, jump out, and go up")

    print("current j = 0")
    print(result_j)

    # add space
    curr = 0
    for c in result_j:
        new_string = new_string + s[curr:c] + " "
        curr = c
    
#    print("done backtrace")
    return (new_string.strip())


if __name__ == "__main__":
    # Example usage.
    from dynamic_programming import DynamicProgramTable
#    s = "itwas"
    s = "itwasthebestoftimes"
    
    
    wordlist = ["of", "it", "the", "best", "times", "was"]
    D = DynamicProgramTable(len(s) + 1, len(s) + 1, cell_ordering(len(s)), fill_cell)
    D.fill(string=s, is_word=lambda w:w in wordlist)
    print respace_from_table(s, D)
    
    
