# handbrake-batch-transcode
Python script to take a directory of video files and transcode them.  For Brian Fowler

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

Also you will need handbrake for transcodey things

### TODO
* Add ability to remove files as they are transcoded to save on disk space
* Actually do the transcoding using HandBrakeCLI
