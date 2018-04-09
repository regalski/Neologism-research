import re
import csv
import nltk 



'''
If we have to return to this let's make it much prettier.

'''









def count_3017(to_be_counted):
    return len(re.findall('3017',to_be_counted))

def count_alskj(to_be_counted):
    return len(re.findall('alskj',to_be_counted))

def count_codes(code_list):
    return len(code_list.split('.'))




def filter_posts():

    '''
    Filters out posts that are uniteresting into diffrent files. 
    Then sends the remaining posts to the_next_function

    Posts that get filteredout:
        1. Any that occured before the first post in the main 3017 thread
        2. Any that will grind the parser to a halt (mostly Shave journals)
            - tries to save as many of these as possible by removing non-3017 containing sentences and
            the ones that still meet exclusion criteria 
        3. If all 3017 uses in the post were coded as 0 

    '''    
    exclusion_pattern=re.compile('[0-9]{7}|[0-9]{6}-|3017[0-9]')

    with open('3017.res.txt_with_corrected_auths.tsv','r+b') as data_in:

        post_data_in= csv.reader(data_in,delimiter='\t')

        for post in post_data_in:

            if int(post[0])<3140943:

                with open('posts_too_early.tsv','a+b') as too_early:

                    too_early.write('\t'.join(post)+'\n')
            

            elif count_3017(post[-1]) == 1 and len(post[4])==1 and int(post[4])==0:

                with open('code0_posts.txt','a+b') as code0s_out:

                    code0s_out.write(post[-1]+'\n')

            elif len(re.findall(exclusion_pattern,post[-1])) > 0:

                    sents= nltk.sent_tokenize(post[-1])
                    
                    salvaged_sents=[sent for sent in sents if '......' not in sent and '3017' in sent and len(re.findall(exclusion_pattern,sent))==0] 

                    if len(salvaged_sents) > 0:

                        post[-1]= ' '.join(salvaged_sents)

                        yield post

                    else:

                        with open('undesireable_posts.txt','a+b') as bad_bois_out:


                            bad_bois_out.write(post[-1]+'\n')

                            
            else:


                yield post



def normalize_and_psudofy_3017_uses(post_in):

    rep = { "3017'ing": "3017ing",
            "3017'd": "3017ed",
            "3017'ed": "3017ed",
            "3017'ers": "3017ers",
            "3017-ing": "3017ing",
            "3017-ING":'3017ing',
            "3017'er": "3017er",
            "3017's": "3017s",
            "3017-ed": "3017ed", #<-- for this step 3017-ed-> 3017ed is not nesesary but it will be useful to have this set for the dissemination measures.
            "3017-er": "3017er",
            "3017'rs": "3017ers",
            "3017'nd": "3017ed",
            "3017nd": "3017ed",
            "3017ng": "3017ing",
            "3017'in": "3017ing",
            '3017"ing': "3017ing",
            "3017'ning": "3017ing",
            "3017'ng": "3017ing",
            "3017'ners": "3017ers",
            "3017'n": "3017ing",
            "3017'king": "3017ing",
            "3017int": "3017ing",
            "3017(ing": "3017ing",
            "3017-in": "3017ing",
            
            "3017'g": "3017ing",
            "3017-ers": "3017ers",
            "3017`er": "3017er",
            "3017-d": "3017ed",
            }


    rep = dict((re.escape(k), v) for k, v in rep.iteritems())
    pattern = re.compile("|".join(rep.keys()))
    post_in[-1] = pattern.sub(lambda m: rep[re.escape(m.group(0))], post_in[-1])

    post_in[-1]=post_in[-1].replace('3017','alskj')

    post_in[-1] = post_in[-1].replace('alskjingg','alskjing').replace('alskjd','alskjed')
 

    with open('psudofied.tsv','a+b') as fixed_out:
        fixed_out.write('\t'.join(post_in)+'\n')

    with open('./files/'+post_in[0],'a+b') as post_out:
        post_out.write(post_in[-1])

    yield post_in


'''
    This will take as its input what filtered_posts() yields as output.
    It will be a regex that replaces all know variations of each suffix with the non adultered one   
        eg    3017'g ---> 3017ing
    Then it will convert all 3017 instances to alskj
        eg   3017ing ---> alskjing

    Then it will write all the posts to a file for the parser and send its output to make_code_index_file() 

'''

def make_code_index_file(psudofied_line):
    '''
    This will take as its input what normalize_and_psudofy_3017_uses() yields as output.

    first it will use count_3017() and count_codes() compare the two

'''
    psudofied_line[-1]= count_alskj(psudofied_line[-1])

#    print psudofied_line

    
    code_list= psudofied_line[4].split('.')
    line_per_code=[]

    if psudofied_line[-1] > len(code_list):

        while psudofied_line[-1]>len(code_list):      #<--- no reason do do if and while here expept to keep what I am doing clear in my own head.
        
            code_list.append('nocode')
    
    
    elif psudofied_line[-1]< len(code_list):
    
        code_list=['nocode']
    
        with open('too_many_codes.txt','a+b') as too_many_codes:
            too_many_codes.write('Something went wrong at post number {} no worries though they were removed and the post was labeled with "nocode"\n'.format(psudofied_line[0]))
    
    

    for code in code_list:

        line_per_code.append('{}\t{}\t{}\t{}\t{}\n'.format(psudofied_line[0],psudofied_line[1],psudofied_line[2],psudofied_line[3],code))

    for line in line_per_code:
        with open('postid.date.forum_thread.auth.code_PASTE_ME_WITH_TAG_FILE.tsv','a+b') as lines_out:
            lines_out.write(line)
    with open('filelist.txt','a+b') as filenames:
        filenames.write(psudofied_line[0]+'\n')
    

    


for filtered_post in filter_posts():
    for psudofied_post in normalize_and_psudofy_3017_uses(filtered_post):
        make_code_index_file(psudofied_post)
        


