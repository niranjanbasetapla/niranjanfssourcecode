
# ENCODING:
def encode(string,selfdelimiting=0):
    
    N=0 ## counts the number of characters read from the source string
    Nruns=0 ## counts the number of runs
    firsttime = 1
    assert(len(string)>0) ## Can't encode an empty string
    for c in string :
        if ( firsttime ) :
            # print the very first character
            if( c == '1' ) or  (c=='0') :
                ans = c ; N+=1
                oldc = c
                r = 1 ## start counting run length
                firsttime = 0 
                pass
            else: ## ignore bogus character
                pass
	else :
            if( (c == '1' ) or (c=='0') ) :
                N+=1
                if ( c != oldc ) :
                    ans = ans + encoded_alpha (r)
                    Nruns +=1
                    oldc = c 
                    r = 1
                    pass
                else:
                    r+=1
                    pass
                pass
            pass
        pass
    ans = ans + encoded_alpha (r) ## report the final run.
    Nruns +=1
    if(selfdelimiting):  ## prepend the number of runs, so the decoder will know when to stop
        ans = encoded_alpha(Nruns) + ans
        pass
    return ans
    pass

from IntegerCodes import dec_to_bin, encoded_alpha, get_alpha_integer, bin_to_dec

## :DECODING: 
def decode(string,selfdelimiting=0):
    """
    general runlength decoder:
    must receive a string of 0 and 1, no other characters

    >>> print decode("11")
    1
    >>> print decode("111111111")
    10101010
    """
    clist = list ( string )
    if(selfdelimiting==0):
        return simpledecode(clist)
    else:
        runs = get_alpha_integer( clist ) ## r is the number of runs
        return smartdecode(clist,runs)
    pass

def smartdecode(clist,runs):
    ans=""
    if(runs>0):
        c=clist.pop(0)
        while ( runs>0 ):
            runs -= 1
            assert ( len(clist) > 0 ) 
            r = get_alpha_integer( clist )
            ans = ans + c*r ## add r copies of the current character
            if ( c=='1' ): c='0' ; pass
            else: c='1' ; pass
            pass
        pass
    return ans

## :DECODING: must receive a string of 0 and 1,
## no other characters
def simpledecode(clist):
    """ SIMPLEDECODE uses 'length of list is zero' to know when to stop """
    ans=""
    if ( len(clist) > 0 ) :
        c=clist.pop(0)
        while 1 :
            r = get_alpha_integer( clist )
            if (r<=0): break
            ans = ans + c*r ## add r copies of the current character
            if ( c=='1' ): c='0' ; pass
            else: c='1' ; pass
            pass
        pass
    return ans

def multiplefiledecode(string):
    """
    assumes that a set of files have been compressed using smartencoding,
    then concatenated
    """
    clist = list ( string )
    files = [] 
    while ( len(clist) > 0 ):
        runs = get_alpha_integer( clist ) ## r is the number of runs
        files.append(  smartdecode(clist,runs) )
        pass
    return files


def test():
    sources = [\
        "010",\
 '0000000000000000100000000000000000001010000000',\
 '1111111111111111111011111111111111111111111001111111',\
 '111111111111111111111111111100000000000000000000000',\
                 "0",\
        "1",\
        "00000000000001111111111111111110000000000000000000000",\
        "000111000"\
        ]
    for smartness in [1,0] :
        print "=============================================="
        print "smartness", smartness
        for source in sources :
            compressed = encode(source,smartness)
            uncompressed = decode(compressed,smartness)
            print
            print "encoding",source,"->", compressed
            print "decoding",uncompressed
            if source!=uncompressed:
                print "ERROR"
                pass
            pass

    print "\n ##demonstrate that the smart decoder can recover multiple files from a single archive"
    smartness=1
    zipfile = ""
    print sources
    for source in sources :
        compressed = encode(source,smartness)
        zipfile = zipfile + compressed
        pass
    print " -> compressed into single file "
    print zipfile
    uncompressed = multiplefiledecode(zipfile)
    print " -> recovered files"
    print uncompressed
    assert sources==uncompressed
    pass

def compress_it( inputfile, outputfile ):
    string = inputfile.read()
    outputfile.write(  encode(string) )
    pass

def uncompress_it( inputfile, outputfile ):
    string = inputfile.read()
    outputfile.write(  decode(string) )
    pass

if __name__ == '__main__':
    import sys
    verbose = 0 
    #    find out the command
    if verbose :
        print "Test has been called with the following argv:" 
        print sys.argv
        pass
    if sys.argv == [''] : ## probably we have been invoked by C-c C-c
        test()
        import doctest
        verbose=1
        if(verbose):
            doctest.testmod(None,None,None,True)
        else:
            doctest.testmod()
            pass
    else : ## read data from stdin and write to stdout
        if (len(sys.argv)==1): ## IRL.py
            print >> sys.stderr, "Compressing"
            compress_it(sys.stdin,sys.stdout)
        else:
            print >> sys.stderr,  "UNCompressing"
            uncompress_it(sys.stdin,sys.stdout)
        pass
    pass

    
