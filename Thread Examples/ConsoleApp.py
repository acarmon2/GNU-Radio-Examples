from gnuradio import gr
from gnuradio import audio, analog
from gnuradio import blocks
from gnuradio import fft
from gnuradio.fft import window
import threading
import time

class my_top_block(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self)

        self.sample_rate = 5000000
        self.ampl = 0.1
        self.freq = 144000000

        self.stream = blocks.stream_to_vector_decimator(
            item_size=gr.sizeof_gr_complex,
            sample_rate=self.sample_rate,
            vec_rate=30,
            vec_len=1024,
        )

        self.probe = blocks.probe_signal_vf(1024)
        self.fft = fft.fft_vcc(1024, True, (window.blackmanharris(1024)), True, 1)

        src0 = analog.sig_source_c(self.sample_rate, analog.GR_SIN_WAVE, self.freq, self.ampl)
        dst = audio.sink(self.sample_rate, "")

        self.sqrt = blocks.complex_to_mag_squared(1024)

        def fft_out():
            while 1:
                val = self.probe.level()
                print max(val)
                freq = (val.index(max(val)) - 512) * (self.sample_rate/1024.0)
                print freq
                time.sleep(1)

        fft_thread = threading.Thread(target=fft_out)

        fft_thread.daemon = True
        fft_thread.start()

        self.connect((src0,0),(self.stream, 0))
        self.connect((self.stream, 0),(self.fft, 0))
        self.connect((self.fft, 0),(self.sqrt, 0))
        self.connect((self.sqrt, 0),(self.probe, 0))

if __name__ == '__main__':
    try:
        my_top_block().run()
    except [[KeyboardInterrupt]]:
        pass