# -*- coding: utf-8 -*-
"""
in python lots of things are like lists:


str             strings or text, as lists they are letters                        immutable     ordered
list            the work horse in python, contents may be anything                mutable       ordered
dict            dictionaries, like lists but key: value pairs.  Index by the key  mutable       not ordered
tuple           like a list but immutable                                         immutable     ordered
set             a list with no duplicates                                         mutable       not ordered
OrderedDict     a dict but you can count on staying in order built                mutable       ordered
range()         more or less a list of integers                                   xxx           orderedish
random()        sort of list_like -- infinite or indefinate                       xxx           xxx



More in the collections module, also see generators and itterables



"""

"""

What is list like?
    There are lots of variations and exceptions but:

    Works in a for loop:

        for i_item in list_like_thing:
            print( "process i_item"    )

    has a length   len( list_like_thing )

    can index into it   list_like_thing[ some_index ]

    may have extended indexing: slices   [1:3:-1]

    can convert between types:   a_list   = list( a_tuple )



Might want to add some actual code examples


"""

