from helpers.tsv import tsv_reader

import nltk
from nltk.tag import StanfordPOSTagger
import os

import glob

import subprocess

java_path = subprocess.getoutput(['where','java']).split('\n')[0]


files=glob.glob('3*')







#java_path = "C:/ProgramData/Oracle/Java/javapath/java.exe"

os.environ['JAVAHOME']= java_path

mod='C:/Users/fb0619/stanford-postagger-2018-02-27/models/english-bidirectional-distsim.tagger'

jar='C:/Users/fb0619/stanford-postagger-2018-02-27/stanford-postagger.jar'


st= StanfordPOSTagger(mod,jar)




for file in files:


    for post in tsv_reader(file):
        for tup in st.tag(post[0].split(' ')):
            if 'alskj' in tup[0]:
                print(tup)
