import nltk
from nltk.tag import StanfordPOSTagger
import os




java_path = "C:/ProgramData/Oracle/Java/javapath/java.exe"

os.environ['JAVAHOME']= java_path
mod='C:/Users/fb0619/stanford-postagger-2018-02-27/models/english-bidirectional-distsim.tagger'

jar='C:/Users/fb0619/stanford-postagger-2018-02-27/stanford-postagger.jar'

for x in tsv_reader('a.tsv', line_num=3):
    
    print(x)


st= StanfordPOSTagger(mod,jar)


print(st.tag('What is the airspeed of an unladen swallow ?'.split()))