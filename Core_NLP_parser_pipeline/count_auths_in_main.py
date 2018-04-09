from datetime import datetime
import csv
from collections import defaultdict

from datetime import datetime





'''''

Counting number of auths posting in my guess 

'''



'''

with open('correctleangth.posts','r+b') as posts_in:

    reader= csv.reader(posts_in, delimiter='\t')

    for (date, pid, forum, forum_num, thread, thread_num, auth, post_num, post) in reader:

        if 'my-guess-3017' == thread:

            with open('my-guess-3017.thread', 'a+b') as main_out:

                main_out.write('{}\t{}\n'.format(date,auth))

'''

with open('my-guess-3017.thread','r+b') as posts_in:

    reader= csv.reader(posts_in, delimiter='\t')

    CumDays = 0

    auths = set()

    for (date,auth) in reader:

        auths.add(auth)

        if len(auths) == 1:

            prevdate = datetime.strptime(date,"%m/%d/%Y")

            with open('auth_count_main_thread.ssv', 'a+b') as main_out:

                main_out.write('CumDays AuthCount\n0 1\n')

        else:

            currdate = datetime.strptime(date,"%m/%d/%Y")

            if currdate != prevdate:

                CumDays += (datetime.strptime(date,"%m/%d/%Y") - prevdate).days

                prevdate = datetime.strptime(date,"%m/%d/%Y")

                with open('auth_count_main_thread.ssv', 'a+b') as main_out:

                    main_out.write( str(CumDays) + ' ' + str(len(auths)) + '\n')
        














