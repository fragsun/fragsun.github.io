# -*- coding:UTF-8 -*-

import time

def compare_file(sourceFile,targetFile):
    compareResult = True
    try:
        sf =  open(sourceFile,'r')
        tf = open(targetFile,'r')
        lf = open('compare_log.txt','a')
    except Exception as e:
        print(e)
    for nuLine,sLine in enumerate(sf):
        sLine = sLine.rstrip('\n')
        try:
            tLine = tf.next().rstrip('\n')
        except StopIteration:
            tLine = '---none---'
        if tLine == sLine:
            continue
        else:
            compareResult = False
            fileTimestrp = time.strftime('%Y%m%d %H:%M:%S',time.localtime())
            lf.write('\n[%s] Found difference at %d line! \nSource line is: \'%s\'\nTarget line is: \'%s\'\n'%(fileTimestrp,nuLine+1,sLine,tLine))
    sf.close()
    tf.close()
    if compareResult:
        fileTimestrp = time.strftime('%Y%m%d %H:%M:%S',time.localtime())
        lf.write('\n[%s] Compare over, no difference found.\n'%fileTimestrp)
    lf.close()
    return compareResult



if __name__=='__main__':
    a = list()
    a = compare_file('F:\\python\\test\\ippbx\\UCA\\testcase_1.py','F:\\python\\test\\ippbx\\UCA\\testcase_1.py')
    print a
