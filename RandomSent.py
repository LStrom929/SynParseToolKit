# Maybe I should print these comments at the onset of the program?

# This tool will select a random .txt file from the glob source
# then select a random sentence from that file.
#
# There are 4 files/bins corresponding to each sentence category: \
# The categories of sentences were selected based on characteristics \
# that represent the breadth of syntactic forms found in the sample medical text.
#
# Short sent 1/"output1"(<11 length): ellipses/domain specific abbreviations + embedded clause(s) (e.g. CP)
# Short sent 2/"output2"(<11 length): grammatically sound/NON-domain abbreviations no embedded clause(s) (e.g. mL/min)
# Long sent 1/"output3"(>=11 length): grammatically sound, embedded clause(s) (e.g. CP) or
# other non-standard syntactic constructions (e.g. multiple ellipses)
# Long sent 2/"output4"(>=11 length): grammatically sound, NO embedded clauses or 
# non-standard syntactic constructions
# Bins 2 and 4 have no embedded clauses--this includes infinitives (see Extended Projection Principle)
#
# The differences in categories were chosen based on common medical sentences and phrases, which are
# compared to controls, i.e. common English sentences.
#
# The program will continue to choose random sentences until each folder is full
# This program is compatible with Python v. 2.7+ (not 3)
# -----------------------------------------------------------------------------

import random
import glob
import sys
import getopt
from nltk import tokenize

# encode for unusual characters in medical text
reload(sys) 
sys.setdefaultencoding('utf8')

bin_size = int(raw_input("Please choose a bin size for the sentences: "))

def pull_file(directory):
    # randomly select a file from given directory

    filelist = glob.glob(directory)
    return filelist[random.randrange(len(filelist))]

def randomize(in_directory):
    # this function will extract a random sentence from the selected file

    random_file = pull_file(in_directory)
    print "Sentence taken from this file: ", random_file, "\n"

    with open(random_file, "rt") as ofile:
        rfile = ofile.read()
    ofile.close()
    
    rrfile = str(rfile.replace("\n", " ")) # the parser won't want newline chars
    tfile = tokenize.sent_tokenize(rrfile) # separate by sentences

    rand_sent = str(random.choice(tfile))
    sent_length = len(rand_sent.split())

    print " ", rand_sent, "\n", "Length of sentence: ", sent_length, "words"

    return {"sent_length":sent_length,"rand_sent":rand_sent}

def get_user_input(program_status):
    # this function will continue the program if the user wishes so

    no_input = True
    while no_input is True:
        user_input2 = raw_input("Would you like to choose another sentence? [y/n] ")

        if user_input2 == 'y':
            no_input = False
            return program_status
        elif user_input2 == 'n':
            no_input = False
            program_status = False
            return program_status
        else:
            print "Please type 'y' or 'n'"
            
def file_length(file):
    # this function returns the number of sentences in a file (bin size) to be used below
    
    with open(file, "rt") as ofile:
        rfile = ofile.read()
        flist = rfile.split('\n')
    ofile.close()
    
    if '' in flist: # including space chars in the list will return an incorrect number of sentences
        flist = [elem for elem in flist if elem != '']
    else:
        pass
    length = len(flist)
    
    # return flist only to check if sent is already in output file
    return {"length":length,"file_list":flist}
    
if __name__ == '__main__': 

    def usage():
        print(sys.argv[0])
        print("\t--input=input directory [must use glob format]")
        print("\t--output1=1st output file [typically .txt]")
        print("\t--output2=2nd output file")
        print("\t--output3=3rd output file")
        print("\t--output4=4th output file")
        print("\tdebug")
        sys.exit(1)

    try:
        (options, args) = getopt.getopt(sys.argv[1:], "",
            ["input=", "output1=", "output2=", "output3=", "output4=", "help", "debug"])

    except getopt.GetoptError:
        print("Invalid option")
        usage()
        sys.exit(1)

    inDirectory = None
    outFile1 = None
    outFile2 = None
    outFile3 = None
    outFile4 = None
    debug = None

    for (opt,val) in options:
        if    opt in ("--input"):	inDirectory = val
        elif  opt in ("--output1"):	outFile1 = val
        elif  opt in ("--output2"):	outFile2 = val
        elif  opt in ("--output3"):	outFile3 = val
        elif  opt in ("--output4"):	outFile4 = val
        elif  opt in ("--help"):	usage(); sys.exit(1)
        elif  opt in ("--debug"):	debug=False

    if inDirectory == None:
        print("ERROR! You must supply the name of a directory of .txt files")
        usage()

    if outFile1 == None:
        print("ERROR! You must supply the name of a directory of a 1st output file")
        usage()

    if outFile2 == None:
        print("ERROR! You must supply the name of a 2nd output file")
        usage()

    if outFile3 == None:
        print("ERROR! You must supply the name of a 3rd output file")
        usage()

    if outFile4 == None:
        print("ERROR! You must supply the name of a 4th output file")
        usage()

    go_again = True

    while go_again is True:
        randomize_dictionary = randomize(inDirectory)
        out1_length = file_length(outFile1)
        out2_length = file_length(outFile2)
        out3_length = file_length(outFile3)
        out4_length = file_length(outFile4)
        
        rand_sent = randomize_dictionary['rand_sent']
        sent_length = randomize_dictionary['sent_length']
        
        # this process will separate the short and long sentences automatically
        
        # do I want to include the sent median code in this program?
        # then I could use the median of medians as a variable in these if statements
        
        # could do most of this with a function...
        
        if sent_length <= 11: # <= median returned from median code???
            print "\n", "To which file would you like to append this sentence?", "\n"
            # Note that these files will vary with user needs
            user_input = raw_input("Please type: 'output1' or 'output2': ")

            if user_input == 'output1':
            
                if out1_length["length"] == bin_size:
                    print "Specified bin size already reached for this file!"
                    go_again = get_user_input(go_again)
                elif rand_sent in out1_length["file_list"]:
                    print "Sentence already exists in that bin!"
                    go_again = get_user_input(go_again)
                else:
                    print "Sentence written to 1st output file."
                    with open(outFile1, 'a') as outf:
                        outf.write(rand_sent+"\n")
                    outf.close()
                    go_again = get_user_input(go_again)

            if user_input == 'output2':
            
                if out2_length["length"] == bin_size:
                    print "Specified bin size already reached for this file!"
                    go_again = get_user_input(go_again)
                elif rand_sent in out2_length["file_list"]:
                    print "Sentence already exists in that bin!"
                    go_again = get_user_input(go_again)
                else:
                    print "Sentence written to 2nd output file."
                    with open(outFile2, 'a') as outf:
                        outf.write(randomize_dictionary['rand_sent']+"\n")
                    outf.close()
                    go_again = get_user_input(go_again)

        if sent_length > 11:
            print "\n", "To which file would you like to append this sentence?", "\n"
            user_input = raw_input("Please type: 'output3' or 'output4': ")

            if user_input == 'output3':
            
                if out3_length["length"] == bin_size:
                    print "Specified bin size already reached for this file!"
                    go_again = get_user_input(go_again)
                elif rand_sent in out3_length["file_list"]:
                    print "Sentence already exists in that bin!"
                    go_again = get_user_input(go_again)
                else:
                    print "Sentence written to 3rd output file."
                    with open(outFile3, 'a') as outf:
                        outf.write(rand_sent+"\n")
                    outf.close()
                    go_again = get_user_input(go_again)

            if user_input == 'output4':
                
                if out4_length["length"] == bin_size:
                    print "Specified bin size already reached for this file!"
                    go_again = get_user_input(go_again)
                elif rand_sent in out4_length["file_list"]:
                    print "Sentence already exists in that bin!"
                    go_again = get_user_input(go_again)
                else:
                    print "Sentence written to 4th output file."
                    with open(outFile4, 'a') as outf:
                        outf.write(rand_sent+"\n")
                    outf.close()
                    go_again = get_user_input(go_again)
                
                
                
                