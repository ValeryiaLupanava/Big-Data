#!/opt/anaconda/envs/bd9/bin/python

import sys 
import happybase

def do_map(doc): 
    dict_ = {}
    line = doc.split('\t')
    
    try:
        dict_['UID'] =  int(line[0])
    except:
        return None
    dict_['ts'] =  int(float(line[1]) * 1000) 
    dict_['URL'] = line[2].strip()


    if (dict_['URL'][: 4] == 'http') & (dict_['UID'] % 256 == 97):
        return dict_

        
connection = happybase.Connection('bd-node2.newprolab.com')
connection.open()
table = connection.table('viktorya.mukukenova')

for line in sys.stdin: 
    dictionary = do_map(line) 
    if dictionary is not None:
        table.put(str(dictionary['UID']), {'data:url': dictionary['URL']}, timestamp=dictionary['ts'])

connection.close()

