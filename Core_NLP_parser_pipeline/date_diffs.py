from datetime import datetime
import csv



'''''
produces table

Use daysSincePrev CumDays POS UseOfPOS 


'''



with open('simp.tags.tsv','r+b') as posts_in:

    reader= csv.reader(posts_in, delimiter='\t')


    pos= {}

    i = 1

    for (pid, date, forum_thread, auth, code, use, tag) in reader:

        if tag not in pos.keys():

            pos[tag] = 0 


        date= date.split('/')
        
        month, day, year = date
        
        if len(day)<2:
        
                day= '0' + day   ### <--- found out later that 0 padding is not needed.
        
        if len(month)<2:
        
                month= '0' + month
        
        if i==1:

                cumdays = 0 
        
                prevdate = datetime.strptime(''.join((month,day,year)),"%m%d%Y")

                pos[tag] += 1

                days_since_prev = 0

                print i, (prevdate-prevdate).days, cumdays, tag, pos[tag]
        
                

                with open('use.days_since_prev.cumdays.pos.pos_count.tsv', 'a+b') as counts_out:
                    counts_out.write('Use DaysSincePrev CumDays POS UseOfPOS\n' + '{} {} {} {} {}\n'.format(i,days_since_prev, cumdays, tag, pos[tag]))

                i+=1

        else:
            
            currdate = datetime.strptime(''.join((month,day,year)),"%m%d%Y")

            cumdays += (currdate-prevdate).days

            pos[tag] += 1

            days_since_prev = (currdate-prevdate).days
            

            print i, (currdate-prevdate).days, cumdays, tag, pos[tag] 

            i+=1
            
            prevdate = currdate

            with open('use.days_since_prev.cumdays.pos.pos_count.tsv', 'a+b') as counts_out:

                counts_out.write('{} {} {} {} {}\n'.format(i,days_since_prev, cumdays, tag, pos[tag]))