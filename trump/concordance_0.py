# -*- coding: utf-8 -*-
"""
original code

"""



# con.py: Concordance using a dictionary
import sys
import string

def build_concord( filepre ): #
    """
    build concordance
    args: filepre  -- filename of input
    returns: c - concordance a dictionary


    """
    n = 0
    c = {}
    fsrc  = open(filepre + ".src.txt",'r') # open source file
    flist = open(filepre + ".list.txt",'w') # open listing file

    for line in fsrc: # process source file
        if len(line) == 1: # don't number empty lines
            flist.write((' '*5) + line)
        else:
            n += 1
            flist.write(("%4i" % n) + ' ' + line)
            wp = line.split()
            for w in wp:
                w = w.strip(string.punctuation).lower()
                if len(w) > 0:
                    # insert w and n into c, the concordance
                    if not(w in c): # new entry
                        c[w] = [n]
                    elif c[w][-1] != n: # first-time line no
                        c[w].append(n)
    return c

def write_concord(filepre): # output concordance in good form
    c = build_concord(filepre)
    fcon = open(filepre + ".con.txt",'w') # open concordance file
    ckeys = c.keys() # get list of keys
    ckeys.sort() # sort list of keys in place
    for j in range(0,len(ckeys)): # print in sorted order
        y = 15
        fcon.write(("%4i" % j) + ' ')
        fcon.write(str(ckeys[j]) + ' '*(15-len(ckeys[j])))
        x = 0
        for i in c[ckeys[j]]: # print list of line nos
            x += len(str(i)) + 1
            if x < 100: # max line length
                fcon.write(str(i) + " ")
            else:
                x = len(str(i))
                fcon.write('\n' + ' '*(y+5) + str(i) + " ")
        fcon.write('\n')




# to run from command line use:
#    where sys.argv[1] = source_file_name
#
#write_concord( sys.argv[1] ) # uses command line parameter


def main():
    pass
    print( "i am main " )

    prefix_for_files = "trump"
    write_concord( prefix_for_files  ) # uses command line parameter
    #write_concord( sys.argv[1] ) # uses command line parameter

#--------------------------------
if __name__ == "__main__":

    main()






