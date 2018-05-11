from dissem_analysis_3 import *
import tqdm
import multiprocessing 
import glob
import os

import datetime

files = glob.glob('files\\*')[0:2]


file_in=files[0]



user, word_count, thread_counts, U_w, T_w, timeseries, N_a = counts_for_dissem(file_in)


word_count = word_count.apply(zero_to_N_w_minus_one,args=[N_a])

print('first')
start = datetime.datetime.now()

word_count = word_count.apply(calc_denom, args=(user,))

print((datetime.datetime.now()-start).seconds)









'''
#print(os.cpu_count())


def _apply_df(fargs):
    df, func, kwargs = fargs
    return df.apply(func, **kwargs)

def apply_by_multiprocessing(df, func, **kwargs):
    workers = kwargs.pop('workers')
    pool = multiprocessing.Pool(processes=workers)
    result = pool.map(_apply_df, [(d, func, kwargs)
            for d in np.array_split(df, workers)])
    pool.close()
    return pd.concat(list(result))
print('top level run')
    
if __name__ == '__main__':

    files = glob.glob('files\\*')[0:2]

    file_in=files[0]

    user, word_count, thread_counts, U_w, T_w, timeseries, N_a = counts_for_dissem(file_in)


    word_count = word_count.apply(zero_to_N_w_minus_one,args=[N_a])
    
    
    print('first')
    
    start = datetime.datetime.now()
    
    
    print((datetime.datetime.now()-start).microseconds)
    
    print('second')
    
    start = datetime.datetime.now()
    
    apply_by_multiprocessing(word_count, calc_denom, args=(user,), workers=4)

    print((datetime.datetime.now()-start).seconds)
    

'''


'''
if __name__ == '__main__':      
    with Pool(4) as p:
        print(type(p.map(counts_for_dissem,files)))
'''

