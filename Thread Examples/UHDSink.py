from gnuradio import gr
from gnuradio import audio, analog
from gnuradio import blocks
from gnuradio import fft
from gnuradio import uhd
from gnuradio.fft import window
import threading
import time

class my_top_block(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self)

        self.sample_rate = 5000000
        self.ampl = 0.1
        self.freq = 100000000

        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("", "")),
            uhd.stream_args(
                cpu_format="fc32",
                channels=range(1),
            ),
        )
        self.uhd_usrp_sink_0.set_samp_rate(self.sample_rate)
        self.uhd_usrp_sink_0.set_center_freq(self.freq, 0)
        self.uhd_usrp_sink_0.set_gain(90, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_bandwidth(100e3, 0)
        self.analog_wfm_tx_0 = analog.wfm_tx(
            audio_rate=32000,
            quad_rate=640000,
            tau=75e-6,
            max_dev=75e3,
        )

        self.analog_noise_source_x_0 = analog.noise_source_f(analog.GR_GAUSSIAN, 1, 0)

        def freq_jump():
            while 1:
                if self.freq < 108000000:
                    self.set_freq( self.freq + 5000000)
                else:
                    self.set_freq(88000000)
                print "Jump!"
                time.sleep(0.2)

        jump_thread = threading.Thread(target=freq_jump)

        jump_thread.daemon = True
        jump_thread.start()

        self.connect((self.analog_wfm_tx_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.analog_noise_source_x_0, 0), (self.analog_wfm_tx_0, 0))

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_sink_0.set_center_freq(self.freq, 0)

if __name__ == '__main__':
    try:
        my_top_block().run()
    except [[KeyboardInterrupt]]:
        pass