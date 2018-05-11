
import csv
from datetime import datetime
from collections import defaultdict
from collections import Counter
import numpy as np
import pandas as pd







def zero_to_N_w_minus_one(N_w,N_a):   

    '''This produces an array from 0 to N_w-1
        it will be applied to a pandas series
        that has as its index the words and
        as its values the number of times that word
        was used.
    '''

    return N_a - np.arange(0,N_w)     ###!! prifile if using a list compression is faster
                                      ###!! because iterating over a list should be faster than over array
                                      ###!! in calc_denom
 
def zero_to_N_w_minus_one_list(N_w,N_a):   #<---Using lists is faster!

    '''This produces an array from 0 to N_w-1
        it will be applied to a pandas series
        that has as its index the words and
        as its values the number of times that word
        was used.
    '''

    return [N_a - x for x in  xrange(0,N_w)]


def counts_for_dissem(file_in,time=0):





    prelim_count = {}
        
    with open(file_in,'r') as fakes_in:

        reader= csv.reader(fakes_in,delimiter='\t')


        posts_done = 0



        for (thread, auth, post) in reader:

            post = post.split()

            for word in post:

                prelim_count.setdefault(word,[[],[],0])

                prelim_count[word][0].append(auth)

                prelim_count[word][1].append(thread)

                prelim_count[word][2] += 1

    words = { 
            
            k:[ v[0], v[1], len(set(v[0])), len(set(v[1])), v[2]] 
            
            for k, v in prelim_count.items() 

            if v[2] >= 5

            }

    prelim_count= None
    

    U_w = { k: v[2] for k,v in words.items()}

    T_w = { k: v[3] for k,v in words.items()}

    user = Counter()

    thread_counts = Counter()

    for used_in_by in words.values():

        user += Counter(used_in_by[0])
        thread_counts += Counter(used_in_by[1])

    word_count = { k: v[-1] for k,v in words.items()}

    words = None

    ##need to calc N_a
    N_a = sum(user.values())

    a = sum(thread_counts.values())
    b= sum(word_count.values())

    if a == b == N_a:
        pass
    else:
        print('Problem with N_a == sum(thread_counts) == sum(user)')


    user = np.fromiter(user.values(),dtype=float)

    thread_counts = np.fromiter(thread_counts.values(),dtype=float)

    word_count = pd.Series(word_count,name='N_w')



    U_w = pd.Series(U_w,name='U_w')
    T_w = pd.Series(T_w,name='T_w')
    
    timeseries = pd.Series(time,index=T_w.index)

    return user, word_count, thread_counts, U_w, T_w, timeseries, N_a

def calc_denom(count,vec):

    ''' Applied to a pandas series
        the elements of which are arrays
        produced by zero_to_N_w_minus_one() calculates
        the denominator for equation 1 of
        Altmann et al. (2011) 


        >>> user, word_count, thread_counts, U_w, T_w, N_a_minus_j = counts_for_dissem('file_in.tsv',0)
        >>>
        >>> T_denom = N_a_minus_j.apply(calc_denom,args=(thread_counts,))
        >>>
        >>> U_denom = N_a_minus_j.apply(calc_denom,args=(user,))
        >>>
        
        Then using the numerators already collected we calculate the
        dissemination across users and threads.

        >>> df = pd.concat([ U_w/U_denom, T_w/T_denom, word_count,timeseries],axis=1)
        >>>
        >>> df.columns = ['D_u','D_t','N_w','time']
        >>>
        >>> print df
                D_u       D_t  N_w  time
        a  1.142857  1.142857  3.0     0
        b  1.000000  1.000000  1.0     0
        c  1.333333  1.333333  2.0     0
        d  1.000000  1.000000  1.0     0
        e  0.666667  0.666667  2.0     0
    '''

    denom = 1
    for x in count:

        denom = denom*((x-vec)/x)

    return np.sum(1-denom)


def file_in_list():

    '''
    Makes the list of files in based on date ranges in the file
    names that were produced in post.normalizer.py
    
    >>> outertime = 0
    >>> for file_in in file_in_list():
    >>>     counts_for_dissem(file_in,outertime)
    >>>     outertime +=1
    '''

    date_ranges=[]

    for x in range(11,18):

         if x == 11:

             date_ranges.append([datetime.strptime('20'+ str(x) + '0601',"%Y%m%d"), datetime.strptime('20'+ str(x) + '1231',"%Y%m%d")])
         
         elif x == 17:

            date_ranges.append([datetime.strptime('20'+ str(x) + '0101',"%Y%m%d"), datetime.strptime('20'+ str(x) + '0601',"%Y%m%d")])

         else:

             date_ranges.append([datetime.strptime('20'+ str(x) + '0101',"%Y%m%d"), datetime.strptime('20'+ str(x) + '0601',"%Y%m%d")])
             date_ranges.append([datetime.strptime('20'+ str(x) + '0602',"%Y%m%d"), datetime.strptime('20'+ str(x) + '1231',"%Y%m%d")])


    for date_range in date_ranges:

        yield datetime.strftime(date_range[0],'%Y%m%d') + '-' + datetime.strftime(date_range[1],'%Y%m%d') + '_thread_auth_normalizedPosts.tsv'

