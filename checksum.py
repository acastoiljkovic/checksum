#!/usr/bin/python
# Skripta za generisanje cheksum-e
# ----------------------------------------------------------------------
# Syntax:
#   ./checksum.py [-h] [-a {md5,sha1,sha224,sha254,sha384,sha512}] [-v] 
#   [-f FILE] [-fL FOLDER]
#   -fL FOLDER : moze i putanja do fajla
# ----------------------------------------------------------------------
# Purpose:
#   Generise checksum za folder i za sve clanove tog foldera nad kojima
#   se vrsi backup.
# ----------------------------------------------------------------------
#   Student Name  :  Aleksandar Stoiljković
#   Email         :  aca.stoiljkovic@elfak.rs
#   Profesor Name :  Vladimir Ćirić
# ----------------------------------------------------------------------
# Example:
#   ./checksum.py -a sha254 -vv -f filename -fL /full/path/to/folder -ch 
import hashlib
import os
import time
import argparse

from timeit import default_timer as timer
from datetime import timedelta

# GLOBALNE PROMENLJIVE
# 
HASH_GEN = {}
VERBOSE = 0
CHECK = 0
FILE_NAME = None
FOLDER_NAME = None
HASH_ALG = "md5"

# UCITAVA ARGUMENTE SA KOMANDN LINIJE
#
def inputArguments():
    parser =  argparse.ArgumentParser(
        description="CHECKSUM - HASH GENERATOR",
        prog='Checksum')

    parser.add_argument('-a','--algorithm',
    action='store',
    default='md5',
    type=str,
    choices=['md5','sha1','sha224','sha254','sha384','sha512'],
    help='Choose algorithm for hashing.' )

    parser.add_argument('-v','--verbose',
    action='count',
    default=0,
    help='Verbosely list files and folders processed.')

    parser.add_argument('-f','--file',
    action='store',
    type=str,
    required=True,
    help='Checksum file name. Assuming the file is located in the same directory as the folder for hashing.'
    )

    parser.add_argument('-fL','--folder',
    action='store',
    type=str,
    required=True,
    help='Path to folder or file for hashing.')

    parser.add_argument('-ch','--check',
    action='count',
    default=0,
    help='Check if checksum from file are matching checksum of folder.')

    args = parser.parse_args()

    return args.algorithm, args.verbose,args.file,args.folder,args.check

# PROVERAVA DA LI SU UNETI ARGUMENTI VALIDNI
#
def checkArguments(args):
    global VERBOSE
    global CHECK
    global FILE_NAME
    global FOLDER_NAME
    global HASH_ALG
    HASH_ALG = args[0]
    VERBOSE = args[1]
    FILE_NAME = args[2]
    FILE_NAME += "."
    FILE_NAME += HASH_ALG
    FOLDER_NAME = args[3]
    CHECK = args[4]
    if os.path.exists(FOLDER_NAME):
        if VERBOSE:
            if os.path.isdir(FOLDER_NAME):
                print("Found directory !")
            else:
                print("Found file !")
    else:
        print ("Wrong path to directory !")
        print ("Directory doesn't exists !")
        print ("Closing...")
        quit()
    if os.path.exists(os.path.join(FOLDER_NAME,"..",FILE_NAME)):
        if VERBOSE:
            print("Fund checksum file !")
    elif CHECK:
        print("Checksum file doesn't exists !")
        print ("Closing...")
        quit()
    else:
        if VERBOSE:
            print("Checksum file doesn't exists ")
            print("Creating checksum file ...")
        f = open(os.path.join(FOLDER_NAME,"..",FILE_NAME),"w")
        f.close()    
        if VERBOSE:
            print("Checksum file successful created !")
    return

# KREIRA CHECKSUMU ZA FOLDER I SVE NJEGOVVE CLANOVE
#
def generateCheckSum():
    print("Generating checksum ...")
    
    # POCINJE DA MERI VREME
    #
    start = timer()

    chksum = open(os.path.join(FOLDER_NAME,"..",FILE_NAME),'w');
    chksum.write(returnGeneratedChecksum())
    chksum.close()

    # PREKIDA MERENJE VREMENA
    #
    end = timer()
    
    print("Elapsed time for checksum: "+ str(timedelta(seconds=end-start)))
    print("Checksum generated successful in file: "+FILE_NAME)
    return

# VRACA CHECKSUMU ZA PROSLEDJENI FOLDER/FILE
#
def returnGeneratedChecksum():
    
    if os.path.isdir(FOLDER_NAME):
        try:
            for(path,dirs,files) in os.walk(FOLDER_NAME):
                for fileName in files:
                    if VERBOSE >= 2:
                        print("Hashing: "+fileName)
                    try:
                        fileO = open(os.path.join(path,fileName),'rb')
                    except:
                        fileO.close()
                        continue

                    while 1:
                        # CITAMO U MALIM DELOVIMA DA BI HASHOVAO CEO FAJL
                        #
                        buffer = fileO.read(4096)
                        if not buffer: break
                        HASH_GEN.update(buffer)
                    fileO.close()

        except IOError:
            print("Failed to create checksum !")
            return
    else:
        if VERBOSE >= 2:
            print("Hashing: "+FOLDER_NAME)
        try:
            fileO = open(FOLDER_NAME,'rb')
        except:
            fileO.close()
        while 1:
            # CITAMO U MALIM DELOVIMA DA BI HASHOVAO CEO FAJL
            #
            buffer = fileO.read(4096)
            if not buffer: break
            HASH_GEN.update(buffer)
        fileO.close()
    return HASH_GEN.hexdigest()

# HASH_GEN POSTAVLJA ODREDJENI ALGORITAM
#
def setHashAlgorithm():
    global HASH_GEN

    if HASH_ALG == "md5" :
        HASH_GEN = hashlib.md5()
    elif HASH_ALG == "sha1":
        HASH_GEN = hashlib.sha1()
    elif HASH_ALG == "sha224":
        HASH_GEN = hashlib.sha224()
    elif HASH_ALG == "sha254":
        HASH_GEN = hashlib.sha256()
    elif HASH_ALG == "sha384":
        HASH_GEN = hashlib.sha384()
    elif HASH_ALG == "sha512":
        HASH_GEN = hashlib.sha512()
    else:
        print("Wrong hash algorithm !")
        return

# PROVERAVA DA LI SE CHECKSUMA POKLAPA
#
def checkChecksum():

    # POCNI DA MERIS VREME
    #
    start = timer()
    print("Checking checksum ...")
    file = open(os.path.join(FOLDER_NAME,"..",FILE_NAME),'r')
    
    # HASH GENERISAN OD STANE FUNCKIJE 
    #
    genHash =returnGeneratedChecksum().encode()
    
    # HASH IZVUCEN IZ FAJLA
    #
    fileHash = file.read().encode()

    if genHash == fileHash:
        end = timer()
        print("Checking checksum finished")
        print("Elapsed time: "+str(timedelta(seconds=end-start)))
        print("Checksum are matching !")
        return True
    
    # PREKINI DA MERIS VREME
    #
    end = timer()
    print("Checking checksum finished")
    print("Elapsed time: "+str(timedelta(seconds=end-start)))
    print("Checksum aren't matching !")
    return False

if __name__ == "__main__":
    checkArguments(inputArguments())
    setHashAlgorithm()
    if CHECK:
        checkChecksum()
    else:
        generateCheckSum()