# python-CI-template
Python CI template for EC500 Software Engineering

Exercise-2 Part-1:
It took about fifty-eight seconds to encode a one minute forty seconds video from avi to mp4 at thirty frames per second with 1 Mbps and resolution being 480p. And after varying the bit rate to two Mbps and resolution to 720p, it took about eighty-seven seconds for the same input video. This statistics is with one worker thread working on encoding. On four cores with four worker threads working on encoding four videos(same size) in parallel, it took about five minutes and thirty seconds. This is about thirty seconds of speedup achieved.   

Exercise-2 Part-2:
Job file contains the details of the task. Tasks are loaded from the job file in the main program. User is required to enter the number of worker threads to launch. Tasks are appended in a task queue from the job file. Once a task under execution is completed, next task is considered for execution from the queue. 

Unit test include two tests for now. First is to check if the video actually got created after encoding. Second check is to see if the entire was encoded or not. This is done by checking comparing the video lengths of the input video and the encoded video. Few other tests could be to verify the resolution, check the frame rate, quality of the encoded video etc. 

