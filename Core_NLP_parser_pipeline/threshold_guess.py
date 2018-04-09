from datetime import datetime
import csv



'''''

Threshold defined as number of users that the current user saw use 3017 at least once assuming users lurk an entire thread until they post in it

'''



with open('postid.date.forum_thread.auth.code.tagged_by_wsj-0-18-bidirectional-distsim.tsv','r+b') as posts_in:

    reader = csv.reader(posts_in, delimiter='\t')

    thread_uniqe_users = {}

    user_threshold = {}



    for (pid, date, forum_thread, user, code, use, tag) in reader:

        thread_uniqe_users.setdefault(forum_thread,set())

        
        if user not in user_threshold.iterkeys():

            user_threshold[user] = len(thread_uniqe_users[forum_thread])
        
        thread_uniqe_users[forum_thread].add(user)


with open('user_thresholds.ssv','a+b') as f:
    f.write('User Threshold\n')

for user, threshold in user_threshold.iteritems():
    
    with open('user_thresholds.ssv','a+b') as f:
        f.write('{} {}\n'.format(user,threshold))