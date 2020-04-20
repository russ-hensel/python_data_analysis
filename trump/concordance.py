# -*- coding: utf-8 -*-
"""
Python: Concordance Programs
http://www.cs.utsa.edu/~wagner/python/concord/concord.html
"""

# con.py: Concordance using a dictionary
import sys
import string
import collections
import spacy





sys.path.append( "D:/Russ/0000/python00/python3/_examples/" )
import ex_helpers


# --------------- some utilitiy stuff may need to make global

nlp = spacy.load( 'en_core_web_sm'   )    # example use 'en' but throws error


numerals   = set( "0123456789" )   # words do not start with numerals so this will get them out

# also consider  other things like $  but maybe spacy does it all ?


# --------------- print out helper
def  info_about_dict( a_obj, msg = "for a dict:", max_lines = 10 ):
    if  isinstance( a_obj, dict ):
        print( f"\nmsg {msg}" )
        #print( f"     Dict: >{a_obj}<" )
        print( "dict list --------->" )
        count_lines   = 0
        for  key, value in a_obj.items():
             print( f"{key}: {value}" )
             count_lines += 1
             if (max_lines != 0 ) and ( count_lines > max_lines ):
                 print( "hit max lines, so not all of dict has be printed")
                 return

        #print( f"     dataframe.values: >{a_obj.values}<" )
        # print( f"     a_series.index: >{a_series.index}<" )
    else:
        print( f"\nfor msg = {msg} object is not an instance of Dict" )
    print( "------\n")


# ----------------------------------------
def line_to_words( a_line, use_spacy = True  ):
    """
    break line into clean words
    return a list or list like thing
    """
    words = a_line.split()       # get word list from line -- this was all original code did
    clean_words   = []
    for i_word in words:
        j_word   = clean_word( i_word )
        if not j_word == "":
            clean_words.append( j_word )
    if use_spacy:
        spacy_line  = " ".join( clean_words )
        doc = nlp( spacy_line )
        # clean_words = doc    # this is not array of words, may need to convert


    for token in doc:
        print(token, token.lemma, token.lemma_)


    return clean_words


# ----------------------------------------
def clean_word( word ):
    """
    clean word or change to "" if ng

    eary return when fail to clean up
    """
    word = word.strip( string.punctuation ).lower()
    if len(word) == 0:
         return ""

    if word[0] in numerals:
         return  ""  # or try to strip to find a word
         #print( f"word = {word}")
         # insert w and n into c, the concordance

    if word.startswith( "http" ):
        return ""
    return word

# ----------------------------------------
def clean_line( line ):
    """
    clean and classify the line, return
    tuple  = ( cleaned_line, line_ref = str_ref, line_type ) # in flux check it out
    """
    line_type  = "tweet"   # bad   empty, retweet.... working on it
    line       = line.encode( encoding='UTF-8', errors='replace')   # do this in the read?? does not seem to work
    line       = str( line )
    # should these be strip
    line       = line.replace("\n", " ")
    line       = line.replace("/n", " ")  # but still see them
    line_parts  = line.split( ",")  # seems to be way file is delimited this gets us just the tweat
    if len( line_parts )  < 7 :
        line_type  = "bad"
        return( "", "", line_type )
        #print( f"line_parts  {len(line_parts)}" )
    line_ref       = line_parts[6]
    line_tweet     = line_parts[1]
    if line_tweet.startswith( "RT"):  # be careful where we lower
        line_type  = "retweet"
        # get rid of the RT ??

    line_tweet  = line_tweet.lower()

    return( line_tweet, line_ref, line_type )


# ----------------------------------------
def concord_in_out( fn_src, fn_list ):
    """
    it appears the list is just to number the lines so these can be used later
    return c = concordance is a... dict??   {word: [ line references ]}

    """
    line_no   = 0
    c         = {}   # concordance see doc string

    # had some reading problem so modifiee
    #fsrc  = open( fn_src, 'r') # open source file

    fsrc  = open( fn_src, 'r', encoding = "utf8", errors='ignore' )

    flist = open( fn_list,'w') # open listing file

    # for line in fsrc:
    #     pass

    for line in fsrc: # process source file

        line, line_ref, line_type  =  clean_line( line )

        if line_type  == "bad":
            flist.write((' '*5) + line + "\n")
        else:
            line_no += 1
            flist.write(("%4i" % line_no ) + ' ' + line + "\n")
            # print( ">>>>>>>>", line_no, line, flush = True)
            #flist.write( line )

            words = line_to_words( line )  # do not pass back empty words

            #print( f"words = {words}")
            for word in words:

                #word  = clean_word( word )   # move to line_to_words
                if len( word ) > 0:

                    if not( word in c ): # new entry
                        c[word] = [line_no]
                    elif c[word][-1] != line_no: # first-time line no
                        c[word].append(line_no)

    return c


# ----------------------------------------
def concord( filepre ) : # construct concordance
    """
    code in out in file name, this is the orginal
    give a prefix to the two files
    """

    file_src   = f"{filepre}.src.txt"
    file_list  = f"{filepre}.list.txt"
    concord_in_out( file_src, file_list )



# ----------------------------------------
def write_concord( filepre ): # output concordance in good form
    c       = concord(filepre)
    fcon    = open(filepre + ".con.txt",'w') # open concordance file
    ckeys   = c.keys() # get list of keys
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

# write_concord(sys.argv[1]) # uses command line parameter

# ----------------------------------------
def main(  ):
    """
    style say use a main so here it is
    """
    print( "\n\n----------------- start concordance ----------------------" )


    fn_src    = r"D:\Russ\0000\python00\python3\_projects\covid_data\trump\tiny_tweet_download.txt"
    #fn_src    = r"D:\Russ\0000\python00\python3\_projects\covid_data\trump\tweet_download.csv"

    fn_list   = r"D:\Russ\0000\python00\python3\_projects\covid_data\trump\tiny_list.txt"

    c  = concord_in_out( fn_src, fn_list )

    # print without sorting
    #info_about_dict( c )

    # try with better names
    a_dict   = c
    # sort on key


    a_ordered_dict    = collections.OrderedDict( sorted( a_dict.items(), key=lambda a_item: a_item[0])) # items makes dict to tuples
    info_about_dict( a_ordered_dict )


    print( "\n---------------- end concordance ----------------------\n\n" )

    print ( string.punctuation )

#--------------------------------
if __name__ == "__main__":

    main()



# ======================= eof =======================








