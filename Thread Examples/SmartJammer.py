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
        time.sleep(0.1)

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


    # --- Sinks ------

        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("", "")),
            uhd.stream_args(
                cpu_format="fc32",
                channels=range(1),
            ),
        )
        self.uhd_usrp_sink_0.set_samp_rate(self.sample_rate)
        self.uhd_usrp_sink_0.set_center_freq(100000000, 0)
        self.uhd_usrp_sink_0.set_gain(-20, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_bandwidth(100e3, 0)
        self.analog_wfm_tx_0 = analog.wfm_tx(
            audio_rate=32000,
            quad_rate=640000,
            tau=75e-6,
            max_dev=75e3,
        )

        self.analog_noise_source_x_0 = analog.noise_source_f(analog.GR_GAUSSIAN, 1, 0)


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
                print "Index: {} Max: {} Cen Freq: {} Counter: {}".format(val.index(max(val)),max(val),self.freq, self.counter)

                #if self.counter > 0:
                if max(val) > 100:
                    pow_ran = []
                    freq_ran = []
                    for i in val:
                        pow_ran.append(float(i)/max(val))
                    for i in range(1024):
                        freq_ran.append((i*self.sample_rate/1024.0) + (self.freq - (self.sample_rate/2.0)))

                    jam_freq = (self.freq - self.sample_rate/2.0) + (val.index(max(val)) * (self.sample_rate/1024)) 
                    
                    print "Freq to Jam {}".format(jam_freq)

                    #self.set_jam_freq(jam_freq + 1000000)
                    #self.set_gain(50)

                    fig = plt.plot(freq_ran,pow_ran)
                    plt.ylim(-0.3,1.2)
                    plt.xlim(min(freq_ran),max(freq_ran))
                    plt.show()
                    time.sleep(1)

                    #self.set_gain(-20)
                    #self.set_freq(20000000)

                self.counter+=1

                if self.counter == 1:
                    if self.freq < 174000000:
                        self.set_freq(self.freq + self.sample_rate)
                    else:
                        self.set_freq(136000000)
                    self.counter = 0
                    time.sleep(0.1)
                    print "Freq Change!"

                

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


        #self.connect((self.analog_noise_source_x_0, 0), (self.analog_wfm_tx_0, 0))
        #self.connect((self.analog_wfm_tx_0, 0), (self.uhd_usrp_sink_0, 0))
        



    def set_freq(self, freq):
        self.freq = freq
        self.uhd.set_center_freq(self.freq, 0)

    def set_jam_freq(self, freq):
        self.uhd_usrp_sink_0.set_center_freq(freq)

    def set_gain(self, gain):
        self.uhd_usrp_sink_0.set_gain(gain)

if __name__ == '__main__':
    try:
        my_top_block().run()
    except [[KeyboardInterrupt]]:
        pass