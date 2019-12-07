# checksum
Python script for generating checksum

# Syntax:
   ./checksum.py [-h] [-a {md5,sha1,sha224,sha254,sha384,sha512}] [-v] 
   [-f FILE] [-fL FOLDER]
   \n
   -fL FOLDER  : also support if path leads to file
   -f FILE     : file extension is equal to hashing algorithm

# Example:
   ./checksum.py -a sha254 -vv -f filename -fL /full/path/to/folder -ch 
