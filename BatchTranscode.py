import sys, time
from subprocess import Popen
from os import walk, path, makedirs, utime
from guessit import guess_file_info

AVCONV = "avconv"

class TransCoder(object):

    def __init__(self, outputroot):
        """ This is basically a constructor."""
        self.setOutputRoot(outputroot)
        self.verifyOutputDir(outputroot)
        self.__tmp = open(path.join(outputroot, "log"), 'w')

    def close(self):
        self.__tmp.close();

    def setOutputRoot(self, outputroot):
        """ set the outroot for the transcoder """
        self.__output_root = outputroot

    def setFilename(self, filename, input_dir):
        """ Set the filename to be transcoded """
        # Remove the part of the dir  from the input root to the actual file.
        shortend_filename = filename[(len(input_dir)+1):]
        # split it and get the two parts.
        head, tail = path.split(shortend_filename)

        # trim off the extension and add .mkv so the new file will be that.
        self.__output_filename = path.splitext(tail)[0] + ".mkv"
        # Take output root plus the other dirs inside the root.
        self.__output_dir = path.join(self.__output_root,head)
        # input filename == filename.
        self.__input_filename = filename;
        # input == input ;)
        self.__input_dir = input_dir

    def doTranscode(self):
        """ Actually transcode the file using handbrake commandline """

        # Verify output dir exisits if not create it.
        self.verifyOutputDir(self.__output_dir)

        # Join new file name and output dir to get full output.
        outfile = path.join(self.__output_dir,self.__output_filename)

        # Take the input dir and filename to get inputfile.
        infile = path.join(self.__input_dir, self.__input_filename)

        # Capture the time we started
        start = time.time()


        print "transcoding %s to %s" \
                % (infile, outfile)

        # Debugging command
        #self.touch(outfile)

        # Trying to do this:
        # avconv -i <input> -map 0:0 -map 0:1 -map 0:1 -c:v copy -c:a:0 aac -c:a:1 ac3 <output>
        print "Check %s for log " % self.__tmp.name
        po = Popen([AVCONV, '-i', infile,
            '-map', '0:0', '-map', '0:1', '-map', '0:1',
            '-c:v', 'copy', '-c:a:0', 'aac', '-c:a:1', 'ac3',
            '-strict', 'experimental',
            outfile], stderr=self.__tmp, stdout=self.__tmp)

        while po.poll() == None:
            time.sleep(1)
            sys.stdout.write('.')
            sys.stdout.flush()
        print('')

        #get total time
        secs = time.time() - start
        hrs = int(secs) / 3600
        min = int(secs) % 3600 / 60
        sec = int(secs) % 60

        print 'Transcoded %s (%d:%d:%d total time)' % (outfile, hrs, min, sec)



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
        encoder.setFilename(filename,input_dir)
        encoder.doTranscode();

    encoder.close();
