
#!/bin/bash




##First lets get all the uses and tags into one file  







read -e -p "
Hello, what is the directory I should start with? 

>>>>>" the_directory_in_question 

echo 



export the_directory_in_question



cat $the_directory_in_question* | awk -F'\t' -v OFS='\t' '$2~/alskj/ {print $2,$4}' > uses_and_tags_${the_directory_in_question:0: -1}


#Next lets get all the relevant information togeather!




paste postid.date.forum_thread.auth.code_PASTE_ME_WITH_TAG_FILE.tsv uses_and_tags_${the_directory_in_question:0: -1} > ./comparison_results/postid.date.forum_thread.auth.code.${the_directory_in_question:0: -1}.tsv


python test.py




rm uses_and_tags_${the_directory_in_question:0: -1}

echo 'Done...'

echo