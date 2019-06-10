'''
This program uses Porcupine / requires numpy; soundfile; pyaudioc

To create a new wakeword
tools/optimizer/${SYSTEM}/${MACHINE}/pv_porcupine_optimizer -r resources/ -w ${WAKE_WORD} \-p ${TARGET_SYSTEM} -o ${OUTPUT_DIRECTORY}


cd tools/optimizer/windows/amd64/
pv_porcupine_optimizer -r <resources full path folder> -w "Hey Atlas" -p windows -o <where you want your file to go>

In the above example replace ${SYSTEM} and ${TARGET_SYSTEM} with current and target (runtime) operating systems (linux, mac, or windows). 
${MACHINE} is the CPU architecture of current machine (x86_64 or i386). ${WAKE_WORD} is the chosen wake word. 
Finally, ${OUTPUT_DIRECTORY} is the output directory where keyword file will be stored.
'''

#OS Specific Libraries
import argparse
import os
import platform
import struct
import sys
from datetime import datetime
from threading import Thread

#Required Libraries
import numpy as np
import pyaudio
import soundfile

#Speech Recognition Library
import speech_recognition as sr

#Porcupine Library
sys.path.append(os.path.join(os.path.dirname(__file__), 'Porcupine-master/binding/python')) #This path points to the library
from porcupine import Porcupine

class PorcupineDemo(Thread):

    def __init__(
            self,
            library_path,
            model_file_path,
            keyword_file_paths,
            sensitivities,
            input_device_index=None,
            output_path=None):
        super(PorcupineDemo, self).__init__()

        self._library_path = library_path
        self._model_file_path = model_file_path
        self._keyword_file_paths = keyword_file_paths 
        self._sensitivities = sensitivities
        self._input_device_index = input_device_index

        self._output_path = output_path
        if self._output_path is not None:
            self._recorded_frames = []

    def run(self):
            """
            Creates an input audio stream, initializes wake word detection (Porcupine) object, and monitors the audio
            stream for occurrences of the wake word(s). It prints the time of detection for each occurrence and index of
            wake word.
            """

            num_keywords = len(self._keyword_file_paths)

            keyword_names =\
                [os.path.basename(x).replace('.ppn', '').replace('_tiny', '').split('_')[0] for x in self._keyword_file_paths]

            print('listening for:')
            for keyword_name, sensitivity in zip(keyword_names, sensitivities):
                print('- %s (sensitivity: %f)' % (keyword_name, sensitivity))

            porcupine = None
            pa = None
            audio_stream = None
            try:
                porcupine = Porcupine(
                    library_path=self._library_path,
                    model_file_path=self._model_file_path,
                    keyword_file_paths=self._keyword_file_paths,
                    sensitivities=self._sensitivities)

                pa = pyaudio.PyAudio()
                audio_stream = pa.open(
                    rate=porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=porcupine.frame_length,
                    input_device_index=self._input_device_index)

                while True:
                    pcm = audio_stream.read(porcupine.frame_length)
                    pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

                    if self._output_path is not None:
                        self._recorded_frames.append(pcm)

                    result = porcupine.process(pcm)
                    if num_keywords == 1 and result:
                        print('[%s] detected keyword' % str(datetime.now()))

                        import speech_recognition as sr

                        r = sr.Recognizer() #speech recognizer instance

                        #Start using microphone args - device_index=n
                        #sr.Microphone.list_microphone_names()
                        #print the microphones
                        with sr.Microphone() as source:
                            print("Say Something...")
                            #Adjust for all the background audio
                            r.adjust_for_ambient_noise(source, duration=1)
                            #Listen to audio and cut
                            audio = r.listen(source)

                        try: #sphinx speech recognizer method
                            print("You said: " + r.recognize_sphinx(audio))

                        except sr.UnknownValueError:
                            print("Could no understand audio")

                        except sr.RequestError as e:
                            print(f"Sphinx error: {e}")

                        #RequestError may be thrown if quota limits are met, 
                        # the server is unavailable, or there is no internet connection.

            except KeyboardInterrupt:
                print('stopping ...')
            finally:
                if porcupine is not None:
                    porcupine.delete()

                if audio_stream is not None:
                    audio_stream.close()

                if pa is not None:
                    pa.terminate()

                if self._output_path is not None and len(self._recorded_frames) > 0:
                    recorded_audio = np.concatenate(self._recorded_frames, axis=0).astype(np.int16)
                    soundfile.write(self._output_path, recorded_audio, samplerate=porcupine.sample_rate, subtype='PCM_16')


def _default_library_path(): #TODO: When deploying modify this to the propper settings (might not work in jetson)
    system = platform.system()
    machine = platform.machine()

    if system == 'Darwin':
        return os.path.join(os.path.dirname(__file__), '../../lib/mac/%s/libpv_porcupine.dylib' % machine)
    elif system == 'Linux':
        if machine == 'x86_64' or machine == 'i386':
            return os.path.join(os.path.dirname(__file__), '../../lib/linux/%s/libpv_porcupine.so' % machine)
        else:
            raise Exception('cannot autodetect the binary type. Please enter the path to the shared object using --library_path command line argument.')
    elif system == 'Windows':
        if platform.architecture()[0] == '32bit':
            return os.path.join(os.path.dirname(__file__), '..\\..\\lib\\windows\\i686\\libpv_porcupine.dll')
        else:
            return os.path.join(os.path.dirname(__file__), 'Porcupine-master\\lib\\windows\\amd64\\libpv_porcupine.dll')
    raise NotImplementedError('Porcupine is not supported on %s/%s yet!' % (system, machine))


if __name__ == '__main__':

    keyword_file_paths = "Porcupine-master\Atlas_Wake_Word\Hey_Atlas_windows.ppn"

    keyword_file_paths = [x.strip() for x in keyword_file_paths.split(',')]

    sensitivities = 0.5

    if isinstance(sensitivities, float):
            sensitivities = [sensitivities] * len(keyword_file_paths)
    else:
        sensitivities = [float(x) for x in sensitivities.split(',')]

    PorcupineDemo(
        library_path=_default_library_path(),
        model_file_path=os.path.join(os.path.dirname(__file__), 'Porcupine-master/lib/common/porcupine_params.pv'),
        keyword_file_paths=keyword_file_paths,
        sensitivities=sensitivities, #number between 0 and 1
        output_path=None,
        input_device_index=None).run()
