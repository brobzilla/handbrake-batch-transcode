import sys
from os import walk, path, makedirs, utime
from guessit import guess_file_info

HANDBRAKE = "HandBrakeCLI"

class TransCoder(object):

    def __init__(self, dirname):
        """ This is basically a constructor."""
        self.setOutputDir(dirname)

    def setOutputDir(self, dirname):
        """ set the outdir for the transcoder """
        self.__dir = dirname

    def setFilename(self, output_extension, filename):
        """ Set the filename to be transcoded """
        self.__filename = filename
        self.__output_ext = output_extension

    def doTranscode(self):
        """ Actually transcode the file using handbrake commandline """
        print "transcoding %s with handbrake to %s/%s/%s" \
                % (self.__filename, self.__dir, self.__output_ext, self.__filename)

        self.verifyOutputDir(path.join(self.__dir,self.__output_ext))
        outputname = path.join(self.__dir,self.__output_ext,self.__filename)

        # Debugging command
        #self.touch(outputname)

        # Capture the time we started
        start = time.time()

        tmp = os.tmpfile()
        po = Popen((HANDBRAKE, '-i%s' % (infile), '-t%s' % (title), '-o%s' % (outfile),
                        '-f av_mkv',
                        '-effmpeg', '-m', '-b2048', '-p',         #video options
                                    '-B256', '-R48', '-66ch') , stderr=tmp)   #audio options
        while po.poll() == None:
            time.sleep(60)
                sys.stdout.write('.')
                sys.stdout.flush()
                sys.stdout.write('n')

                #get total time
                secs = time.time() - start
                hrs = int(secs) / 3600
                min = int(secs) % 3600 / 60
                sec = int(secs) % 60

                print 'Transcoded file (%d:%d:%d total time)' % (hrs, min, sec)



    def verifyOutputDir(self, dirname):
        """ Verify that output dir exists """
        print "Verifing output dir %s" % dirname
        if (not path.exists(dirname)):
            print "Path doesn't exist"
            makedirs(dirname)

    def touch(self, fname, times=None):
        """ Utility method to just touch files in the output dir to verify
            script is preserving the directory structure correctly 
        """
        with open(fname, 'a'):
            utime(fname, times)


class FileNameGrabber(list):

    def __init__(self, inputDir, *args):
        """ This is basically a constructor."""
        # The list of files in the dir.
        list.__init__(self, *args)
        # Input dir
        self.__input_dir = inputDir

    def getFileNames(self):
        """ This method will get all the file names in the __input_dir.
            Checks mimetype before adding it to the list.
        """
        for (dirpath, dirnames, filenames) in walk(self.__input_dir):
            for filename in filenames:
                name = path.join(dirpath, filename)
                info = guess_file_info(name)
                if ('mimetype' in info.keys() and info['mimetype'].startswith('video')):
                    self.append(name)
                else:
                   print "Skipping %s because mimetype wasn't determined" % name

    def size(self):
        """ Return the number of elements in the dir."""
        return len(self)

    def __str__(self):
        """ return a string of all the file names found."""
        output = "\nMy Files are: "
        for i in self:
            output += "\n " + i
        return output

    def __repr__(self):
        return self.__str__()


# Pythonic thing that is the main entrance point to python script.
if __name__=="__main__":
    if len(sys.argv) != 3:
           print( "Usage: " + sys.argv[0] + " <Input Dir> <Output Dir>")
           sys.exit(1)

    # Grab the Command line params
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    print "Input Dir = ", input_dir
    print "Output Dir = ", output_dir

    # Create the grabber and kick off the search.
    grabber = FileNameGrabber(input_dir)
    grabber.getFileNames();
    print "How many files did I get? ", grabber.size()

    # Create the transcoder and loop through files to transcode.
    encoder = TransCoder(output_dir)
    for filename in grabber:
        shortend_filename = filename[(len(input_dir)+1):]
        head, tail = path.split(shortend_filename)
        encoder.setFilename(head,tail)
        encoder.doTranscode();
