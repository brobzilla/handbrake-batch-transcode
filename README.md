# handbrake-batch-transcode
Python script to take a directory of video files and transcode them.  For Brian Fowler
I'm hoping this script will run on Linux, Mac, and Windows.

### Usage
Run the script and it takes two parameters the input dir and the output dir.

The script will recursivly search through the input directory and find files with video/* mimetype. The script will preserve the input dir directory structure in the output dir.
```
python BatchTranscode.py <Input Dir> <Output Dir>
```
### Requirements
guessit cuz it helps me figure out what the mimetype is and other things.

```
pip install guessit
```

Also you will need HandBrakeCL for transcodey things.  The Command line version is different from the normal version.

Download CLI here ---> https://handbrake.fr/downloads2.php

### TODO
* Add ability to remove files as they are transcoded to save on disk space
* Actually do the transcoding using HandBrakeCLI
* Add a check to verify HandBrakeCLI is installed and accessabily from this script
