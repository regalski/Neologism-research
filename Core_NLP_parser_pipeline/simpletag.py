import csv

with open('postid.date.forum_thread.auth.code.tagged_by_wsj-0-18-bidirectional-distsim.tsv','r+b') as in_file:
    reader=csv.reader(in_file,delimiter='\t')

    for x in reader:
        x[-1]= x[-1][:2]

        with open('simp.tags.tsv','a+b') as out:
            out.write('\t'.join(x)+'\n')