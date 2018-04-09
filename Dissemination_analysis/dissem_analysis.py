
import csv
from datetime import datetime
from collections import defaultdict
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


def counts_for_dissem(file_in,time):

    ''' Counting for calc_denom():
    
    >>> file_in = open('file_in.tsv')
    >>> file_in.readlines()
    ['thread1\tuser1\ta b c\n', 'thread2\tuser2\ta d c\n', 'thread1\tuser2\ta e e']
    
    Produces:
    >>> user, word_count, thread_counts, U_w, T_w, timeseries, N_a = counts_for_dissem('file_in.tsv',0,0)
    >>> user
    array([6., 3.])
    >>> word_count
    a    3.0
    b    1.0
    c    2.0
    d    1.0
    e    2.0
    Name: N_w, dtype: float64
    >>> thread_counts
    array([3., 6.])
    >>> U_w
    a    2
    b    1
    c    2
    d    1
    e    1
    Name: U_w, dtype: int64
    >>> T_w
    a    2
    b    1
    c    2
    d    1
    e    1
    Name: T_w, dtype: int64
    >>> N_a_minus_j
    a    [9.0, 8.0, 7.0]
    b              [9.0]
    c         [9.0, 8.0]
    d              [9.0]
    e         [9.0, 8.0]
    Name: N_a-j, dtype: object
    '''

    user = {}

    thread_counts={}

    word_count={}

    T_w = {}

    U_w = {}

    word_used_by=defaultdict(set)

    word_used_in=defaultdict(set)


    num_of_users_that_used_word_w={}

    num_of_threads_word_w_used_in ={}

    with open(file_in,'r+b') as fakes_in:

        N_a= 0.0
        
        reader= csv.reader(fakes_in,delimiter='\t')


        posts_done = 0



        for (thread, auth, post) in reader:

            post = post.split()

            post_len = float(len(post))                                                     

            user.setdefault(auth,0)           

            user[auth] += post_len     #### <--- counting words contribed by user i

            thread_counts.setdefault(thread,0)

            thread_counts[thread] += post_len ##### <--- counting words contribed by thread i


            for word in post:       #<--- count # of users that used word at least once && # of threads word was used in



                word_count.setdefault(word,0)

                word_count[word] += 1

                N_a += 1


                if auth not in word_used_by.get(word,([])):

                    U_w.setdefault(word,0)
                    
                    U_w[word]+=1
                
                word_used_by[word].add(auth)

                
                if thread not in word_used_in.get(word,([])):   

                    T_w.setdefault(word,0)
                    T_w[word] += 1
                
                word_used_in[word].add(thread)

    word_used_in= None

    word_used_by = None


    user = np.fromiter(user.itervalues(),dtype=float)

    thread_counts = np.fromiter(thread_counts.itervalues(),dtype=float)

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


        >>> user, word_count, thread_counts, U_w, T_w, timeseries, N_a = counts_for_dissem('file_in.tsv',0)
        >>>
        >>> N_a_minus_j = word_count.apply(zero_to_N_w_minus_one,args=([N_a]))
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
    Makes the list of files based on date ranges in the file
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

