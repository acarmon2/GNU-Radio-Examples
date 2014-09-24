#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Jammer
# Generated: Wed Sep 24 08:29:41 2014
##################################################

from gnuradio import analog
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import time
import wx

class Jammer(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Jammer")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 5000000
        self.Freq = Freq = 105.9e6

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(Freq, 0)
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

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_tx_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.analog_noise_source_x_0, 0), (self.analog_wfm_tx_0, 0))



    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

    def get_Freq(self):
        return self.Freq

    def set_Freq(self, Freq):
        self.Freq = Freq
        self.uhd_usrp_sink_0.set_center_freq(self.Freq, 0)

    def change_Freq(self, Freq):
        self.Freq = Freq
        self.uhd_usrp_sink_0.set_center_freq(self.Freq, 0)

class Sweep(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 5000000
        self.Freq = Freq = 105.9e6

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("", "")),
            uhd.stream_args(
                cpu_format="fc32",
                channels=range(1),
            ),
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(Freq, 0)
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

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_tx_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.analog_noise_source_x_0, 0), (self.analog_wfm_tx_0, 0))

    def set_Freq(self, Freq):
        self.Freq = Freq 
        self.uhd_usrp_sink_0.set_center_freq(self.Freq, 0)

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = Sweep()
    while True:
        tb.set_Freq(105.9e6)
        tb.(True)
        time.sleep(0.1)
        tb.stop()
        tb.wait()
        tb.set_Freq(106.9e6)
        tb.Start(True)
        time.sleep(0.1)
        tb.stop()
        tb.wait()
        
        #time.sleep(0.1)    
        #tb.stop()
       
        #tb = Jammer(106.9e6)
        #tb.Start(True)
        #time.sleep(0.1)    
        #tb.stop()
        #tb.wait()
