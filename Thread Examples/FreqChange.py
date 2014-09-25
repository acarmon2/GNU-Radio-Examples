from gnuradio import gr
from gnuradio import audio, analog
from gnuradio import blocks
from gnuradio import fft
from gnuradio.fft import window
import threading
import time

import matplotlib.pyplot as plt

class my_top_block(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self)

        self.sample_rate = 3000
        self.ampl = 1
        self.freq = 1900
        self.cen_freq = 0
        self.counter = 0

    # --- Sources ----
        self.src0 = analog.sig_source_f(self.sample_rate, analog.GR_COS_WAVE, self.freq, 1, 0)
        self.src1 = analog.sig_source_f(self.sample_rate, analog.GR_COS_WAVE, self.freq/2, 1, 0)

    # --- Audio Out ---

        self.audioOut = audio.sink(32000, "", True) 

    # --- Blocks ----- 

        self.add = blocks.add_vff(1)   #Add Block

        #self.throttle = blocks.throttle(gr.sizeof_float*1, self.sample_rate,True)

        self.streamToVector = blocks.stream_to_vector_decimator(
            item_size=gr.sizeof_float,
            sample_rate=self.sample_rate,
            vec_rate=30,
            vec_len=1024,
        )

        self.fft = fft.fft_vfc(1024, True, (window.blackmanharris(1024)), 1)
        
        self.complexToMag = blocks.complex_to_mag_squared(1024)
        
        self.probe = blocks.probe_signal_vf(1024)

    # --- Functions ----

        def fft_cal():
            while 1:
                val = self.probe.level()
                print "Index: {}".format(val.index(max(val)))
                freq = (val.index(max(val))) * (self.sample_rate/1024.0)
                print freq
                print len(val)
                time.sleep(1)
                
                #self.set_freq(self.freq+100)

                pow_ran = []
                freq_ran = []

                if self.counter:
                    for i in val:
                        pow_ran.append(float(i)/max(val))
                    for i in range(1024):
                        freq_ran.append(i*self.sample_rate/1024.0)

                    fig = plt.plot(freq_ran,pow_ran)
                    plt.ylim(-0.3,1.2)
                    plt.xlim(min(freq_ran),max(freq_ran))
                    plt.show()

                self.counter+=1



    # --- Start Thread ---

        fft_thread = threading.Thread(target=fft_cal)
        fft_thread.daemon = True
        fft_thread.start()

    # --- Conections ---

        #self.connect((self.src0, 0), (self.add, 0))
        #self.connect((self.src1, 0), (self.add, 1))

        #self.connect((self.add, 0), (self.audioOut, 0))
        #self.connect((self.src0, 0), (self.throttle, 0))
        #self.connect((self.throttle, 0), (self.streamToVector, 0))
        self.connect((self.src0, 0), (self.streamToVector, 0))
        self.connect((self.streamToVector, 0), (self.fft, 0))
        self.connect((self.fft, 0),(self.complexToMag, 0))
        self.connect((self.complexToMag, 0),(self.probe, 0))


    def set_freq(self, freq):
        self.freq = freq
        self.src0.set_frequency(self.freq)


if __name__ == '__main__':
    try:
        my_top_block().run()
    except [[KeyboardInterrupt]]:
        pass