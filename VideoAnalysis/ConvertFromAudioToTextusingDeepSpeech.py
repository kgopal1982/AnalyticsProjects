#https://www.slanglabs.in/blog/how-to-build-python-transcriber-using-mozilla-deepspeech

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

##############################
#models are downloaded from mozilla deepspeech github link and this is one-time setup
# Install DeepSpeech
# $ pip3 install deepspeech==0.6.0

# # Download and unzip en-US models, this will take a while
# $ mkdir -p ./some/workspace/path/ds06
# $ cd ./some/workspace/path/ds06
# $ curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.6.0/deepspeech-0.6.0-models.tar.gz
# $ tar -xvzf deepspeech-0.6.0-models.tar.gz
# x deepspeech-0.6.0-models/
# x deepspeech-0.6.0-models/lm.binary
# x deepspeech-0.6.0-models/output_graph.pbmm
# x deepspeech-0.6.0-models/output_graph.pb
# x deepspeech-0.6.0-models/trie
# x deepspeech-0.6.0-models/output_graph.tflite

# $ ls -l ./deepspeech-0.6.0-models/

################################

#create a model object using the model files downloaded
import deepspeech
model_file_path = 'deepspeech-0.6.0-models/output_graph.pbmm'
beam_width = 500
model = deepspeech.Model(model_file_path, beam_width)

#add language model for better accuracy:
lm_file_path = 'deepspeech-0.6.0-models/lm.binary'
trie_file_path = 'deepspeech-0.6.0-models/trie'
lm_alpha = 0.75
lm_beta = 1.85
model.enableDecoderWithLM(lm_file_path, trie_file_path, lm_alpha, lm_beta)


#read the audio file


import wave
#fileWithoutExtn = 'What_is_Happiness_Sadhguru'
fileWithoutExtn = 'What_is_Happiness_Sadhguru_imitate_1'
filename = fileWithoutExtn + ".wav"

w = wave.open(filename, 'r')
rate = w.getframerate()
frames = w.getnframes()
buffer = w.readframes(frames)
print("sampling rate of the input file is")
print(rate)
#16000
print("Sampling rate of the model")
print(model.sampleRate())
#16000
print("Buffer type of the file is")
print(type(buffer))

#<class 'bytes'>



#run the below code if the sampling rate of the file is dfferent than 16000 Hz
if (rate != 16000):
    print("The sampling rate is not equal to 16000Hz hence converting")
    converted_filename = 'converted_' + filename
    
    from pydub import AudioSegment as am
    #sound = am.from_file(filename, format='wav', frame_rate=44100)
    sound = am.from_file(filename, format='wav', frame_rate=rate)
    sound = sound.set_frame_rate(16000)
    sound.export(converted_filename, format='wav')
    
    #rate after conversion
    print("sampling rate after conversion")
    w = wave.open(converted_filename, 'r')
    rate = w.getframerate()
    print(rate)
    buffer = w.readframes(frames)
    print("Buffer type of the file is")
    print(type(buffer))
    filename = converted_filename

#the buffer is a byte array, whereas DeepSpeech model expects 16-bit int array. Let’s convert it:
import numpy as np
data16 = np.frombuffer(buffer, dtype=np.int16)
type(data16)

#Run speech-to-text in batch mode to get the text
text = model.stt(data16)

#write to a file
#file1 = open("IMF_Georgieva_COVID-19.txt","w")#write mode 
#file1 = open("obama_wh_last_speech.txt","w")#write mode
#remove extension from the filename before converting to text file
import os
filename1 = os.path.splitext(filename)
filename2 = filename1[0]
filename3 = filename2 + "_" + "using_Local_DeepSpeech_Model"+".txt"
file1 = open(filename3,"w")#write mode 
file1.write(text) 
file1.close() 
