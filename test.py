import os, sys
import time
import string
import random
import argparse
import csv

# usage: test.py [--n_range=bottom:step:top] [--repetitions=repetitions] [--output=output]
# usage: test.py [-n bottom:step:top] [-r repetitions] [-o output]

def main(bottom, step, top, r, output):
    if (bottom != None and top != None and step != None):
        n_range = range(bottom, top, step)
    else:
        n_range = range(1, 10, 1)
    if r != None:
        repetitions = r
    else:
        repetitions = 10
    
    times_n = []
    if output != None:
        output_file = output
    else:
        output_file = 'test.csv'
    test_file = 'random-word.test'
    for n in n_range:
        print ('Testing with n='+str(n)+'...')
        times = []
        for j in range(repetitions):
            print(str(j) + ':', end=' ')
            createRandomWord(n, test_file)
            start = time.time()
            #os.system("py blowfish_encrypt.py --test=" + test_file)
            os.system("py pyfish_encrypt.py --test=" + test_file)
            end = time.time()
            times.append(end - start)
        times_n.append(float(sum(times))/float(len(times)))
    eraseRandomWord(test_file)
    writeCSV(n_range, times_n, output_file)

def writeCSV(n_range, times, filename):
    
    with open(filename, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerow(['n','time'])
        i = 0
        for n in n_range:
            spamwriter.writerow([n,times[i]])    
            i += 1

def createRandomWord(n, filename):
    print('\tCreating random word with ' + str(n) + ' characters in ' + filename)
    randomWord = open(filename, 'w')
    randomWord.write(''.join(random.choices(string.ascii_letters + string.digits, k=n)))
    randomWord.close()

def eraseRandomWord(filename):
    os.system("del " + filename)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--n_range')
    parser.add_argument('-r', '--repetitions')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()
    top = bottom = step = repetitions = None
    if (args.n_range):
        n_range_list = args.n_range.split(':')
        top = int(n_range_list[2])
        bottom = int(n_range_list[0])
        step = int(n_range_list[1])
    if (args.repetitions):
        repetitions = int(args.repetitions)
    main(bottom, step, top, repetitions, args.output)