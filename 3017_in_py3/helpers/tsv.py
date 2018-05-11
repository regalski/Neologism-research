import csv


def tsv_reader(filename,line_num= 0, header=False):

    '''This generates each row in a tab seperated file'''

    with open(filename, 'r') as tsv_file:

        reader = csv.reader(tsv_file, delimiter='\t', quoting = csv.QUOTE_NONE)


        if header == True:
            line_num += 1

        
        while line_num > 1:
        
            next(reader,None)
        
            line_num -= 1
            
                

        for row in reader:            
                
            yield row


