import requests
import json
import sys
import argparse

def read_next_batch(f, r):
    #    print json.dumps(r.json(), indent=4, sort_keys=True)
    l = len(r.json()['results'])
    actually_read = 0

    for j in range(0, l):
        l2 = len(r.json()['results'][j])
        i = 0
        for key, value in r.json()['results'][j].items():
            f.write('\"' + str(value).replace('"', '\\"') + '\"')
            if(i < l2-1):
                f.write(',')
            i = i + 1
        f.write('\n')
        actually_read = actually_read + 1

    return actually_read

def consume(api_uri, output_file):
    # Fist Request
    r = requests.get(api_uri)

    number_to_read = r.json()['count']

    # Open file for writing
    f = open(output_file,'w')

    # Print File Header
    l = len(r.json()['results']) 
    i = 0

    for key, value in r.json()['results'][0].items():
        f.write('\"' + str(key).replace('"', '\\"') + '\"')
        if(i < l):
            f.write(',')
        i = i + 1

    f.write('\n')

    # Read First Batch of Entries
    actually_read = read_next_batch(f, r)
    print "Read ", actually_read, " of ", number_to_read
    
    while (actually_read < number_to_read):
        next = r.json()['next']
        # print next
        r = requests.get(next)
        read_last = read_next_batch(f, r)
        actually_read = actually_read + read_last
        print "Read ", actually_read, " of ", number_to_read

    # Close open file
    f.close()
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Python script for consuming data made available using L.I.B.R.E | https://github.com/commonwealth-of-puerto-rico/libre')
    parser.add_argument('uri', metavar='uri', nargs=1,
                   help='a uri for the consumer')
    parser.add_argument('-o', '--output_file', metavar='output_file', 
                        default='output.csv',
                   help='an output file for the data.  Defaults to output.csv')

    args = vars(parser.parse_args())

    consume(args['uri'][0], args['output_file'])
#   http://api.estadisticas.gobierno.pr/api/v1/namespaces/comercio_externo/datasets/exportaciones/data/?_format=json
