from gnuradio import gr
from gnuradio import audio, analog
from gnuradio import blocks
from gnuradio import fft
from gnuradio import uhd
from gnuradio.fft import window
import threading
import time

import matplotlib.pyplot as plt

class my_top_block(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self)

        self.sample_rate = 5000000
        self.ampl = 1
        self.freq = 144000000
        self.counter = 0

    # --- Sources ----

        self.uhd = uhd.usrp_source(
            ",".join(("", "")),
            uhd.stream_args(
                cpu_format="fc32",
                channels=range(1),
            ),
        )
        self.uhd.set_samp_rate(self.sample_rate)
        self.uhd.set_center_freq(self.freq, 0)
        self.uhd.set_gain(0, 0)
        self.uhd.set_antenna("RX2", 0)

    # --- Blocks -----

        self.throttle = blocks.throttle(gr.sizeof_gr_complex*1, self.sample_rate,True)

        self.streamToVector = blocks.stream_to_vector_decimator(
            item_size=gr.sizeof_gr_complex,
            sample_rate=self.sample_rate,
            vec_rate=30,
            vec_len=1024,
        )

        self.fft = fft.fft_vcc(1024, True, (window.blackmanharris(1024)), 1)
        
        self.complexToMag = blocks.complex_to_mag_squared(1024)
        
        self.probe = blocks.probe_signal_vf(1024)

    # --- Functions ----

        def fft_cal():
            while 1:
                val = self.probe.level()
                print "Index: {} Max: {}".format(val.index(max(val)),max(val))

                if max(val):
                    pow_ran = []
                    freq_ran = []
                    for i in val:
                        pow_ran.append(float(i)/max(val))
                    for i in range(1024):
                        freq_ran.append((i*self.sample_rate/1024.0) + (self.freq - (self.sample_rate/2.0)) )
                    fig = plt.plot(freq_ran,pow_ran)
                    plt.ylim(-0.3,1.2)
                    plt.xlim(min(freq_ran),max(freq_ran))
                    plt.show()
                    time.sleep(1)

                

    # --- Start Thread ---

        fft_thread = threading.Thread(target=fft_cal)
        fft_thread.daemon = True
        fft_thread.start()

    # --- Conections ---

        self.connect((self.uhd, 0), (self.throttle, 0))
        self.connect((self.throttle, 0), (self.streamToVector, 0))
        self.connect((self.streamToVector, 0), (self.fft, 0))
        self.connect((self.fft, 0),(self.complexToMag, 0))
        self.connect((self.complexToMag, 0),(self.probe, 0))


    def set_freq(self, freq):
        self.freq = freq
        self.uhd.set_center_freq(self.freq, 0)


if __name__ == '__main__':
    try:
        my_top_block().run()
    except [[KeyboardInterrupt]]:
        pass