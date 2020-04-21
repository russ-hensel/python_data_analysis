# -*- coding: utf-8 -*-
"""
derived from:
Python: Concordance Programs
http://www.cs.utsa.edu/~wagner/python/concord/concord.html


the plan:

    First Part:

    read in source file, parse out info and clean up twitter text to "words"
    ( part of cleaning involves unicode..., non english words, and conversion to lemmmas )

    write out parsed out data to a 'list' file.

    In first implementations while parsing build a dictionary ( perhaps called c )
    of the words and a line number reference ( in the list file )

    Sort the dict and print out.


    Second part:
        have not looked at yet.

    At some point:

    Eliminate some common english words.


Some more details in each function.

Ideas:
    sort output by number of references
    yamal like list output
    more data in list file
    list 'not' words
    list retreat sources
    list hastags
    tune for speed ( just for fun )
    ......
    write a line based on clean words
    decode senator names

Vivek:
    take a shot at writing out new list file ??
    eliminate common english words
    make a list routine like info about dict  but print word no_of_occurances -- sort by no of references

for lemmas

    spaCy 101: Everything you need to know · spaCy Usage Documentation
    https://spacy.io/usage/spacy-101


clean line
line to words
    clean_word

"""


# con.py: Concordance using a dictionary
import sys
import string
import collections
import spacy          # linguistic module words to lemmas ( might not be correct explain )



#sys.path.append( "D:/Russ/0000/python00/python3/_examples/" )
#import ex_helpers


# --------------- some utilitiy stuff may need to make global

nlp        = spacy.load( 'en_core_web_sm'   )    # example used 'en' but throws error
                                                 # had fight installing

numerals   = set( "0123456789" )   # words do not start with numerals so this will get them out

# also consider  other bad prefixes  like $  but maybe spacy does it all ?


# --------------- print out helper
def  info_about_dict( a_obj, msg = "for a dict:", max_lines = 0 ):
    """
    Print some info about a dict including key value pairs one a line
    up to some max number of lines
    """
    if  isinstance( a_obj, dict ):
        print( f"\nmsg {msg}" )
        #print( f"     Dict: >{a_obj}<" )
        print( "dict list --------->" )
        count_lines   = 0
        for  key, value in a_obj.items():
             print( f"{key}: {value}" )
             count_lines += 1
             if (max_lines != 0 ) and ( count_lines > max_lines ):
                 print( f"hit max lines ({max_lines}), so not all of dict has be printed")
                 return

        #print( f"     dataframe.values: >{a_obj.values}<" )
        # print( f"     a_series.index: >{a_series.index}<" )
    else:
        print( f"\nfor msg = {msg} object is not an instance of Dict" )
    print( "------\n")


# ----------------------------------------
def line_to_words( a_line, use_spacy = True  ):
    """
    break line into clean words -- even lemmas
    return a list or list like thing
    """
    words = a_line.split()       # get word list from line -- this was all original code did
    clean_words   = []
    for i_word in words:
        j_word   = clean_word( i_word )
        if not j_word == "":
            clean_words.append( j_word )

    if use_spacy:   # if using npl spacy....
        "rebuild line, then convert to list again "
        spacy_line  = " ".join( clean_words )
        doc = nlp( spacy_line )
        """
        what is doc?
        """
        # clean_words = doc    # this is not array of words, may need to convert

        npl_words = []
        for token in doc:
            #print( token, token.lemma, token.lemma_)  # debug
            npl_words.append( (token.lemma_) )  # token   just messing with this
        #print( f"npl_words {npl_words}" )  # debug
        clean_words   = npl_words

    return clean_words


# ----------------------------------------
def clean_word( word ):
    """
    clean a word may change to "" if no other clean version --
          so dropping as a word.

    Note eary returns in code

    comments may help define what is 'clean'


    """
    # clean words do not start with punctuation
    word = word.strip( string.punctuation ).lower()
    if len(word) == 0:
         return ""

    # clean words do not start witn numbers
    # ?? why is this code different than above and can they be combined
    if word[0] in numerals:
         return  ""  # or try to strip to find a word

         # insert w and n into c, the concordance
    # clean words do not start witn http, it is a url not a word
    if word.startswith( "http" ):
        return ""

    #..... more "cleaning" is probably needed

    #print( f"word = {word}")
    return word

# ----------------------------------------
def clean_line( line ):
    """
    parse clean and classify the line, return
    classify:   see line_type, and code
    clean:  means clean the line ( some in this code some in function clean_word() )
    note theat for the word ananysis we convert to lowere case

    Return:
       tuple  = ( cleaned_line, line_ref = str_ref, line_type ) # in flux check out the code
    """
    line_type  = "tweet"   # bad   empty, retweet.... working on it
    line       = line.encode( encoding='UTF-8', errors='replace')   # do this in the read?? does not seem to work
    line       = str( line )

    # remove some junk
    line       = line.replace("\n", " ")
    line       = line.replace("/n", " ")  # but still see them

    # this is the parse for the csv
    line_parts  = line.split( ",")  # seems to be way file is delimited this gets us just the tweat

    # if we do not get the required no of parts we "reject" the line
    if len( line_parts )  < 7 :
        line_type  = "bad"
        return( "", "", line_type )
        #print( f"line_parts  {len(line_parts)}" )

    line_ref       = line_parts[6]    # original reference from the download file.
    line_tweet     = line_parts[1]    # the tween part of the line
    if line_tweet.startswith( "RT"):  # be careful where we lower
        line_type  = "retweet"
        # get rid of the RT ??

    line_tweet  = line_tweet.lower()

    return( line_tweet, line_ref, line_type )

# ----------------------------------------
def concord_in_out( fn_src, fn_list ):
    """
    fn_src     file name of the source file
    fn_list    file name of the 'list' file, with line numbers, tweet types .....

    it appears the list is just to number the lines so these can be used later
    return c = concordance is a... dict   {word: [ line references ]}

    """
    line_no          = 0
    concordance      = {}   # concordance see doc string

    file_src  = open( fn_src, 'r', encoding = "utf8", errors='ignore' )

    flist = open( fn_list,'w') # open listing file

    # for line in file_src:
    #     pass

    for line in file_src: # process source file

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

                    if not( word in concordance ): # new entry
                        concordance[word] = [line_no]
                    elif concordance[word][-1] != line_no: # first-time line no
                        concordance[word].append(line_no)

    return concordance


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
    """
    not examined yet

    """
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
    good style say use a main so here it is:
    build concondance
    write 'list' file
    sort and print
    """
    print( "\n\n----------------- start concordance ----------------------" )

    fn_src    = r"D:\Russ\0000\python00\python3\_projects\covid_data\trump\tiny_tweet_download.txt"
    #fn_src    = r"D:\Russ\0000\python00\python3\_projects\covid_data\trump\tweet_download.csv"

    fn_list   = r"D:\Russ\0000\python00\python3\_projects\covid_data\trump\tiny_list.txt"

    concordance  = concord_in_out( fn_src, fn_list )

    # print without sorting
    #info_about_dict( c )

    # try with better names
    # a_dict   = c

    # sort on key and print
    if True:
        a_ordered_dict    = collections.OrderedDict( sorted( concordance.items(), key=lambda a_item: a_item[0])) # items makes dict to tuples
        info_about_dict( a_ordered_dict )

    print( "\n---------------- end concordance ----------------------\n\n" )

    #print ( string.punctuation )

#--------------------------------
if __name__ == "__main__":

    main()



# ======================= eof =======================








