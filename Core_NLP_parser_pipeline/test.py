
import csv


import sys
import os





def code_tag_pair_checker(tagger):

    tagger=tagger[:-1]

    file_in= './comparison_results/postid.date.forum_thread.auth.code.'+ tagger +'.tsv'


    d={
        'CD': ['1','12'],
        'JJ': ['2','3'],
        'NN': ['5','6','8','9','13'],
        'VB': ['11'],
                
        }

    pairs=[]

    all_codes=[]


    with open(file_in,'r+b') as codes_and_tags_in:

        let_us_see= csv.reader(codes_and_tags_in,delimiter='\t')






        for line in let_us_see:

            for tag, codes in d.iteritems():

                if line[-3] in codes:

                    pairs.append(tag + '\t' + line[-1][:2])

                    all_codes.append(tag)



    unique_pairs= set(pairs)

    unique_codes= sorted(set(all_codes))


    unsorted_lines=[]

    with open('./comparison_results/wurms_code_aggrement_with_uses_' + tagger + '.txt','a+b') as count_out:
    

        for pair in sorted(unique_pairs):


                pair_count=pairs.count(pair)

                pair= pair.split('\t')

                #if pair[0] in unique_codes:

                code_count = all_codes.count(pair[0])


                if pair[0]==pair[1]:


                    unsorted_lines.append( 'CORRECT' + '\t' +'\t'.join(pair) + '\t'+ str(pair_count)+'/'+str(code_count)+ '\t' + str(float(pair_count)/float(code_count)*100)+'%' + '\n\n')

                else:

                        
                    unsorted_lines.append( 'INCORRECT' + '\t' + '\t'.join(pair) + '\t'+ str(pair_count)+'/'+str(code_count)+ '\t' + str(float(pair_count)/float(code_count)*100)+'%' + '\n\n') 

        sorted_lines= sorted(unsorted_lines)

        for line in sorted_lines:

            count_out.write(line)




code_tag_pair_checker(os.getenv('the_directory_in_question'))



