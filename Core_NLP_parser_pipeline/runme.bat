java -cp "..\..\stanford-corenlp-full-2018-01-31\*" -Xmx1g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos -pos.model ..\..\stanford-corenlp-full-2018-01-31\models\wsj-0-18-bidirectional-distsim.tagger -filelist ..\filelist.txt -outputFormat conll -outputDirectory ..\tagged_by_wsj-0-18-bidirectional-distsim

