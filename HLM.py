from pyo import *
import random
import time
import numpy as np

s = Server(winhost="asio").boot()
s.setMidiInputDevice(99) # Open all input devices.

'''
different classes
'''


#______________________________________________________________________________________________________________________________________________________________________________
class WTRand():
    """
        randomly generated wavetable
        WTRand(freq=440, mul=1)
        out(ch=1):
            1 or 2 channels
        setNewWaves(type=3)
            set new type:
                1-Cosine Logaritmic
                2-Cosine
                3-Curve
                4-Exponential
                5-Linear
                6-Logaritmic
        setPointer(pointer)
            set pointer between 0-1 on table
        setMul(mul)
            set volume
        setFreq(freq)
            set oscillator frequency
    """
    def __init__(self, freq=440, mul=1, pointer=0, type=2):

        self.freq = freq
        self.mul = mul
        self.RandFreq = 1
        self.pointer = Sig(pointer)
        self.type = type
        self.wavetable = NewTable(8192/44100)

        self.wave_1 = self.new_wave(self.type)
        self.wave_2 = self.new_wave(self.type)
        self.wave_3 = self.new_wave(self.type)
        self.wave_4 = self.new_wave(self.type)
        self.wave_5 = self.new_wave(self.type)
        self.wave_6 = self.new_wave(self.type)
        self.wave_7 = self.new_wave(self.type)
        self.wave_8 = self.new_wave(self.type)

        self.morph = TableMorph(self.pointer, self.wavetable, [self.wave_1, self.wave_2, self.wave_3, self.wave_4, self.wave_5, self.wave_6, self.wave_7, self.wave_8])
        self.osc = Osc(self.wavetable, self.freq, mul=self.mul)

    # waves construction
    def new_wave(self, type):

        self.type = type
        self.liste = [(0,0)]

        for i in range(1,11):
            x = random.uniform((i*682),((i+1)*682))
            y = random.uniform(0,1)
            self.liste.append((x,y))

        self.liste.append((8192,0))

        if self.type == 1:
            self.wave = CosLogTable(self.liste)
        if self.type == 2:
            self.wave = CosTable(self.liste)
        if self.type == 3:
            self.wave = CurveTable(self.liste)
        if self.type == 4:
            self.wave = ExpTable(self.liste)
        if self.type == 5:
            self.wave = LinTable(self.liste)
        if self.type == 6:
            self.wave = LogTable(self.liste)

        return self.wave

    def out(self, ch=1):
        if ch == 1 :
            return self.osc.out()
        elif ch == 2 :
            self.mix = Mix(self.osc, 2)
            return self.mix.out()


    def setNewWaves(self, type=3):
        self.wavetable = NewTable(8192/44100)
        self.wave_1 = self.new_wave(self.type)
        self.wave_2 = self.new_wave(self.type)
        self.wave_3 = self.new_wave(self.type)
        self.wave_4 = self.new_wave(self.type)
        self.wave_5 = self.new_wave(self.type)
        self.wave_6 = self.new_wave(self.type)
        self.wave_7 = self.new_wave(self.type)
        self.wave_8 = self.new_wave(self.type)
        self.morph = TableMorph(self.pointer, self.wavetable, [self.wave_1, self.wave_2, self.wave_3, self.wave_4, self.wave_5, self.wave_6, self.wave_7, self.wave_8])
        self.osc = Osc(self.wavetable, self.freq, mul=self.mul).out()
        
        

    def setPointer(self, pointer):
        self.pointer = Sig(pointer)

    def setMul(self, mul):
        self.osc.setMul(mul)

    def setFreq(self, freq):
        self.osc.setFreq(freq)

#______________________________________________________________________________________________________________________________________________________________________________
# wavetable from buffer record
class WTLive(WTRand):

    """
    does not work

    """

    def __init__(self, freq=440, mul=1):

        self.freq = freq
        self.mul = mul

        self.input = Input()
        self.dur = 8192/44100

        self.wavetable = NewTable(self.dur)

        self.wave_1 = NewTable(self.dur)
        self.wave_2 = NewTable(self.dur)
        self.wave_3 = NewTable(self.dur)
        self.wave_4 = NewTable(self.dur)
        self.wave_5 = NewTable(self.dur)
        self.wave_6 = NewTable(self.dur)
        self.wave_7 = NewTable(self.dur)
        self.wave_8 = NewTable(self.dur)

        self.r1 = TableRec(self.input, self.wave_1, .001)
        self.r2 = TableRec(self.input, self.wave_2, .001)
        self.r3 = TableRec(self.input, self.wave_3, .001)
        self.r4 = TableRec(self.input, self.wave_4, .001)
        self.r5 = TableRec(self.input, self.wave_5, .001)
        self.r6 = TableRec(self.input, self.wave_6, .001)
        self.r7 = TableRec(self.input, self.wave_7, .001)
        self.r8 = TableRec(self.input, self.wave_8, .001)

        self.pointer = Randi()
        self.morph = TableMorph(self.pointer, self.wavetable, [self.wave_1, self.wave_2, self.wave_3, self.wave_4, self.wave_5, self.wave_6, self.wave_7, self.wave_8])
        self.osc = Osc(self.wavetable, self.freq, mul=self.mul)


    # recording
    def rec(self, interval=0.1):
        self.interval = interval 
        
        self.r1.play()
        time.sleep(self.interval)
        self.r2.play()
        time.sleep(self.interval)
        self.r3.play()
        time.sleep(self.interval)
        self.r4.play()
        time.sleep(self.interval)
        self.r5.play()
        time.sleep(self.interval)
        self.r6.play()
        time.sleep(self.interval)
        self.r7.play()
        time.sleep(self.interval)
        self.r8.play()
 
        
#______________________________________________________________________________________________________________________________________________________________________________

class CloudOsc():
    """
        cloud oscillator
        CloudOsc(dens=40, dist=10, freq=110, waveform=7, mul=1)
        waveform :
            0 Saw up 
            1 Saw down
            2 Square
            3 Triangle
            4 Pulse
            5 Bipolar pulse
            6 Sample and hold
            7 Modulated Sine(default)
        out(selfch=1)
            1 or 2 channels
        setFreq(freq)
            set new frequency
    """
    def __init__(self, dens=40, dist=10, freq=110, waveform=7, mul=1):
        
        self.dens = dens
        self.dist = dist
        self.freq = freq
        self.waveform = waveform
        self.mul = mul

        self.freq_list = []
        for i in range (0,self.dens) :
            self.freq_list.append(self.freq + i*self.dist)

        vol = (1*self.mul)/self.dens

        self.osc = LFO(self.freq_list, type=self.waveform, mul=vol)


    def out(self, ch=1):
        if ch == 1 :
            return self.osc
        elif ch == 2 :
            self.mix = Mix(self.osc, 2)
            return self.mix

    def setFreq(self, freq):
        self.freq = freq
        self.freq_list.clear()
        for i in range (0,self.dens) :
            self.freq_list.append(self.freq + i*self.dist)
        self.osc.setFreq(self.freq_list)
        

#______________________________________________________________________________________________________________________________________________________________________________

class Entropie:
    """
        random signal destroyer
            Entropie(res=.01, length=1, sub=.3, floor=0, mul=.5 )
            e = Entropie()
            met = Metro(.5).play()
            new_a = TrigFunc(met, e.new, arg=None)
            osc = LFO(freq=300, sharp=0.50, type=0, mul=e.val, add=0).mix(2).out()
        new()
            new signal
    """
    def __init__(self, res=.01, length=1, sub=.3, floor=0, mul=.5 ):
        
        self.res = res
        self.range = int(1/res * length)

        self.mul = mul
        self.add = sub
        self.floor = floor
        
        self.list = []        
        self.new()

        self.val = SigTo(self.mul, self.res)

        self.i = 0
        self.met_appamp = Metro(self.res).play()
        self.app = TrigFunc(self.met_appamp, self.appamp, arg=None)
        self.n_step = int((self.mul-self.floor)/self.add)

    def new(self):
        self.list.clear()
        self.i = 0
        for i in range(self.range):
            self.list.append(self.mul)

    def appamp(self):
        if self.list[self.i] >0:
            self.list[self.i] -= self.add
            if self.list[self.i] < 0:
                self.list[self.i] = 0
        self.val.value = random.choice(self.list)
        self.i += 1
        if self.i == self.range:
          self.i = 0

            
#______________________________________________________________________________________________________________________________________________________________________________

class EntropieRegen:
    """
        random signal destroyer and regenerator (lfo like)
            Entropie(res=.01, length=1, sub=.3, floor=0, mul=.5 )
            e = Entropie()
            met = Metro(.5).play()
            new_a = TrigFunc(met, e.new, arg=None)
            osc = LFO(freq=300, sharp=0.50, type=0, mul=e.val, add=0).mix(2).out()
        new()
            new signal
    """
    def __init__(self, res=.01, length=1, sub=.3, floor=0, mul=.5 ):
        
        self.res = res
        self.range = int(1/res * length)

        self.mul = mul
        self.add = sub
        self.floor = floor
        
        self.list = []        
        self.new()

        self.val = SigTo(self.mul, self.res)

        self.i = 0
        self.met_appamp = Metro(self.res).play()
        self.app = TrigFunc(self.met_appamp, self.appamp, arg=None)
        self.n_step = int((self.mul-self.floor)/self.add)

    def new(self):
        self.list.clear()
        self.i = 0
        for i in range(self.range):
            self.list.append(self.mul)

    def appamp(self):
        self.list[self.i] -= self.add
        self.val.value = random.choice(self.list)
        self.i += 1
        if self.i == self.range:
          self.i = 0

#______________________________________________________________________________________________________________________________________________________________________________

class RandLoopSeq:
    """
        random looping sequence
            RandRepSeq(len=16, tempo=180, loop=4, scale="major", root=60)
            scales = { "major":      [0, 2, 4, 5, 7, 9, 11],
                        "minorH":     [0, 2, 3, 5, 7, 8, 11],
                        "minorM":     [0, 2, 3, 5, 7, 9, 11],
                        "ionian":     [0, 2, 4, 5, 7, 9, 11],
                        "dorian":     [0, 2, 3, 5, 7, 9, 10],
                        "phrygian":   [0, 1, 3, 5, 7, 8, 10],
                        "lydian":     [0, 2, 4, 6, 7, 9, 11],
                        "mixolydian": [0, 2, 4, 5, 7, 9, 10],
                        "aeolian":    [0, 2, 3, 5, 7, 8, 10],
                        "locrian":    [0, 1, 3, 5, 6, 8, 10],
                        "wholeTone":  [0, 2, 4, 6, 8, 10],
                        "majorPenta": [0, 2, 4, 7, 9],
                        "minorPenta": [0, 3, 5, 7, 10],
                        "egyptian":   [0, 2, 5, 7, 10],
                        "majorBlues": [0, 2, 5, 7, 9],
                        "minorBlues": [0, 3, 5, 8, 10],
                        "minorHungarian": [0, 2, 3, 6, 7, 8, 11]
                      }
            new()
                new sequence
    """
    def __init__(self, len=16, tempo=180, loop=4, scale="major", root=120):
        
        self.len = len
        self.tempo = 30/tempo
        self.loop = loop
        self.root = root
        self.freq = SigTo(440)

        self.scale = []
        self.scales = { "major":      [0, 2, 4, 5, 7, 9, 11],
                        "minorH":     [0, 2, 3, 5, 7, 8, 11],
                        "minorM":     [0, 2, 3, 5, 7, 9, 11],
                        "ionian":     [0, 2, 4, 5, 7, 9, 11],
                        "dorian":     [0, 2, 3, 5, 7, 9, 10],
                        "phrygian":   [0, 1, 3, 5, 7, 8, 10],
                        "lydian":     [0, 2, 4, 6, 7, 9, 11],
                        "mixolydian": [0, 2, 4, 5, 7, 9, 10],
                        "aeolian":    [0, 2, 3, 5, 7, 8, 10],
                        "locrian":    [0, 1, 3, 5, 6, 8, 10],
                        "wholeTone":  [0, 2, 4, 6, 8, 10],
                        "majorPenta": [0, 2, 4, 7, 9],
                        "minorPenta": [0, 3, 5, 7, 10],
                        "egyptian":   [0, 2, 5, 7, 10],
                        "majorBlues": [0, 2, 5, 7, 9],
                        "minorBlues": [0, 3, 5, 8, 10],
                        "minorHungarian": [0, 2, 3, 6, 7, 8, 11]
                      }
        self.degree = self.scales[scale]
        self.buildScale()
        self.seq = []
        self.freq_seq = []
        self.new()

        self.met = Metro(self.tempo).play()
        self.trig = Trig()
        self.seq_trig = Trig()
        self.loop_trig = Trig()
        self.iter = TrigFunc(self.met, self.read)

        self.counter = 0
        self.loop_counter = 0


    def buildScale(self):
        for i in range(len(self.degree)):
            self.scale.append(self.root + self.degree[i])

    def new(self):
        self.seq.clear()
        self.freq_seq.clear()
        for i in range(self.len):
            val = random.choice([0,1])
            pit = random.choice(self.scale)
            self.seq.append(val)
            self.freq_seq.append(pit)
        self.counter = 0

    def read(self):
        if self.seq[self.counter] == 1:
            self.freq = self.freq_seq[self.counter]
            self.trig.play()
        self.counter += 1
        if self.counter == self.len:
            self.counter = 0
            self.loop()

    def loop(self):
        self.loop_counter += 1
        self.seq_trig.play()
        if self.loop_counter == self.loop:
            self.change()
            self.loop_counter = 0
            self.loop_trig.play()
 
    def change(self):
        index = random.randint(0,self.len-1)
        if self.seq[index] == 0:
            self.seq[index] = 1
            self.freq_seq[index] = random.choice(self.scale)
        else:
            self.seq[index] = 0
        
#______________________________________________________________________________________________________________________________________________________________________________


class ComplexRandLoopSeq:
    """
        random looping sequence
            RandRepSeq(len1=2, len2=3, len3=4, tempo=180, loop=4, scale="major", root=60)
            scales = { "major":      [0, 2, 4, 5, 7, 9, 11],
                        "minorH":     [0, 2, 3, 5, 7, 8, 11],
                        "minorM":     [0, 2, 3, 5, 7, 9, 11],
                        "ionian":     [0, 2, 4, 5, 7, 9, 11],
                        "dorian":     [0, 2, 3, 5, 7, 9, 10],
                        "phrygian":   [0, 1, 3, 5, 7, 8, 10],
                        "lydian":     [0, 2, 4, 6, 7, 9, 11],
                        "mixolydian": [0, 2, 4, 5, 7, 9, 10],
                        "aeolian":    [0, 2, 3, 5, 7, 8, 10],
                        "locrian":    [0, 1, 3, 5, 6, 8, 10],
                        "wholeTone":  [0, 2, 4, 6, 8, 10],
                        "majorPenta": [0, 2, 4, 7, 9],
                        "minorPenta": [0, 3, 5, 7, 10],
                        "egyptian":   [0, 2, 5, 7, 10],
                        "majorBlues": [0, 2, 5, 7, 9],
                        "minorBlues": [0, 3, 5, 8, 10],
                        "minorHungarian": [0, 2, 3, 6, 7, 8, 11]
                      }
            new()
                new sequence
    """
    def __init__(self, len=16, len1=2, len2=3, len3=4, tempo=180, loop=4, scale="major", root=60):
        
        self.len = len
        self.len1 = len1
        self.len2 = len2
        self.len3 = len3
        self.tempo = 30/tempo
        self.loop = loop
        self.root = root
        self.freq = SigTo(440)

        self.scale = []
        self.scales = { "major":      [0, 2, 4, 5, 7, 9, 11, 12],
                        "minorH":     [0, 2, 3, 5, 7, 8, 11, 12],
                        "minorM":     [0, 2, 3, 5, 7, 9, 11, 12],
                        "ionian":     [0, 2, 4, 5, 7, 9, 11, 12],
                        "dorian":     [0, 2, 3, 5, 7, 9, 10, 12],
                        "phrygian":   [0, 1, 3, 5, 7, 8, 10, 12],
                        "lydian":     [0, 2, 4, 6, 7, 9, 11, 12],
                        "mixolydian": [0, 2, 4, 5, 7, 9, 10, 12],
                        "aeolian":    [0, 2, 3, 5, 7, 8, 10, 12],
                        "locrian":    [0, 1, 3, 5, 6, 8, 10, 12],
                        "wholeTone":  [0, 2, 4, 6, 8, 10, 12, 12],
                        "majorPenta": [0, 2, 4, 7, 9, 12, 14, 12],
                        "minorPenta": [0, 3, 5, 7, 10, 12, 15, 12],
                        "egyptian":   [0, 2, 5, 7, 10, 12, 14, 12],
                        "majorBlues": [0, 2, 5, 7, 9, 12, 14, 12],
                        "minorBlues": [0, 3, 5, 8, 10, 12, 15, 12],
                        "minorHungarian": [0, 2, 3, 6, 7, 8, 11, 12]
                      }

        self.degree = self.scales[scale]
        self.buildScale()
        self.seq = [] # note on or off
        self.seq1 = []
        self.seq2 = []
        self.seq3 = []        
        #self.freq_seq = []
        self.new()

        self.met = Metro(self.tempo).play()
        self.trig = Trig()
        self.seq_trig = Trig()
        self.loop_trig = Trig()
        self.iter = TrigFunc(self.met, self.read)

        self.counter = 0
        self.counter1 = 0
        self.counter2 = 0
        self.counter3 = 0
        self.loop_counter = 0


    def buildScale(self):
        for i in range(len(self.degree)):
            self.scale.append(self.root + self.degree[i])

    def new(self):
        self.seq1.clear()
        for i in range(self.len1):
            val = random.choice([0,1])
            self.seq1.append(val)
        self.seq2.clear()
        for i in range(self.len2):
            val = random.choice([0,1])
            self.seq2.append(val)
        self.seq3.clear()
        for i in range(self.len3):
            val = random.choice([0,1])
            self.seq3.append(val)
        self.seq.clear()
        #self.freq_seq.clear()
        for i in range(self.len):
            val = random.choice([0,1])
            #pit = random.choice(self.scale)
            self.seq.append(val)
            #self.freq_seq.append(pit)
        self.counter = 0
        self.counter1 = 0
        self.counter2 = 0
        self.counter3 = 0
        

    def read(self):
        if self.seq[self.counter] == 1:
            note = self.seq1[self.counter1] + self.seq2[self.counter2]*2 + self.seq3[self.counter3]*4
            self.freq = self.scale[note]
            self.trig.play()

        self.counter += 1
        self.counter1 += 1
        self.counter2 += 1
        self.counter3 += 1
        if self.counter1 == self.len1:
            self.counter1 = 0
        if self.counter2 == self.len2:
            self.counter2 = 0
        if self.counter3 == self.len3:
            self.counter3 = 0
        if self.counter == self.len:
            self.counter = 0
            self.loop()

    def loop(self):
        self.loop_counter += 1
        self.seq_trig.play()
        if self.loop_counter == self.loop:
            self.change()
            self.loop_counter = 0
            self.loop_trig.play()
 
    def change(self):
        index = random.randint(0,self.len-1)
        if self.seq[index] == 0:
            self.seq[index] = 1
            choice = random.choice([1,2,3])
            if choice == 1:
                ind = index % self.len1
                if self.seq1[ind] == 0:
                    self.seq1[ind] = 1
                else:
                    self.seq1[ind] = 0
            elif choice == 2:
                ind = index % self.len2
                if self.seq2[ind] == 0:
                    self.seq2[ind] = 1
                else:
                    self.seq2[ind] = 0
            elif choice == 3:
                ind = index % self.len3
                if self.seq3[ind] == 0:
                    self.seq3[ind] = 1
                else:
                    self.seq3[ind] = 0
        else:
            self.seq[index] = 0
        
#______________________________________________________________________________________________________________________________________________________________________________


class CellAuto:
    """
    Cellular automata
        CellAuto(self, size=17, tempo=660, root=220, mulx=10, muly=20)
        play()
            start cellular automata
        new()
            new random grid
        getValues()
            return list of values
        getCellNb()
            return total number of cell 
            (total possible number of values in the list)
    """

    def __init__(self, size=17, tempo=660, root=60, mulx=1, muly=1.595):
        
        self.size = size
        self.tempo = 60/tempo
        self.root = root
        self.mulx = mulx
        self.muly = muly

        self.total_size = self.size*self.size

        self.values = []
        for i in range(self.total_size):
            self.values.append(0)

        self.metro = Metro(self.tempo)
        self.trig = TrigFunc(self.metro, self.gof)
        self.grid = np.random.choice([0,0,0,0,0,1], (self.size,self.size))


    def gof(self):
    
        self.values.clear()

        for x in range (self.size):

            for y in range (self.size):

                if x == 0:
                    if y == 0:
                        self.around = self.grid[x,y+1]+self.grid[x+1,y]+self.grid[x+1,y]
                    elif y == self.grid[0].size-1:
                        self.around = self.grid[x,y-1]+self.grid[x+1,y-1]+self.grid[x+1,y]
                    else:
                        self.around = self.grid[x,y-1]+self.grid[x,y+1]+self.grid[x+1,y-1]+self.grid[x+1,y]+self.grid[x+1,y+1]

                elif x == self.grid[0].size-1:
                    if y == 0:
                        self.around = self.grid[x-1,y]+self.grid[x-1,y+1]+self.grid[x,y+1]
                    elif y == self.grid[0].size-1:
                        self.around = self.grid[x-1,y-1]+self.grid[x-1,y]+self.grid[x,y-1]
                    else:
                        self.around = self.grid[x-1,y-1]+self.grid[x-1,y]+self.grid[x-1,y+1]+self.grid[x,y-1]+self.grid[x,y+1]

                elif y == 0:
                    self.around = self.grid[x-1,y]+self.grid[x-1,y+1]+self.grid[x,y+1]+self.grid[x+1,y]+self.grid[x+1,y+1]

                elif y == self.grid[0].size-1:
                    self.around = self.grid[x-1,y-1]+self.grid[x-1,y]+self.grid[x,y-1]+self.grid[x+1,y-1]+self.grid[x+1,y]

                else:
                    self.around = self.grid[x-1,y-1]+self.grid[x-1,y]+self.grid[x-1,y+1]+self.grid[x,y-1]+self.grid[x,y+1]+self.grid[x+1,y-1]+self.grid[x+1,y]+self.grid[x+1,y+1]

                # life and death 

                if self.grid[x,y] == 0:
                    if self.around == 3:
                        self.grid[x,y] = 1
                        self.values.append(self.root+((x+1)*self.mulx * self.muly**(y+1)))

                else:
                    if self.around < 1 or self.around > 3:
                        self.grid[x,y] = 0
                    else:
                        self.values.append(self.root+((x+1)*self.mulx * self.muly**(y+1)))

                self.values = self.values
    
    def new(self):
        self.grid = np.random.choice([0,0,0,0,0,1], (self.size,self.size))

    def play(self):
        self.metro.play()

    def getValues(self):
        return self.values

    def getCellNb(self):
        return self.total_size


#____________________________________________________________________________________________
class TripleChaos:
    """
        3 x 3 non-linear ordinary differential equations
            TripleChaos(type=1, pitch=.5, chaos1=.5, chaos2=.5, chaos3=.5, amp1=.5, amp2=.5, amp3=.5, stereo=False)
            type: 1: Rossler
                  2: Lorenz
                  3: ChenLee  
            pitch, chaos and mul : between 0 and 1
            stereo : True or False
    setPitch(pitch)
        set osc1 pitch
    setChaos1(chaos)
        set chaos of osc1
    setChaos2(chaos)
        set chaos of osc2
    setChaos3(chaos)
        set chaos of osc3
    setMul1(mul)
        set volume of osc1
    setMul2(mul)
        set volume of osc2
    setMul3(mul)
        set volume of osc3
    out()
        output osc3
    ctrl()
        display sliders for each available parameters
    setThresh(thresh)
        set threshold for trig (accessible via TripleChaos.trig)
    """
    def __init__(self, system=1, pitch=.5, chaos1=.5, chaos2=.5, chaos3=.5, amp1=.5, amp2=.5, amp3=.5, stereo=False, thresh=.5):
        
        self.system = system
        self.pitch = pitch 
        self.chaos1 = chaos1 
        self.chaos2 = chaos2 
        self.chaos3 = chaos3 
        self.amp1 = amp1 
        self.amp2 = amp2 
        self.amp3 = amp3 
        self.stereo = stereo
        self.thresh = thresh

        if self.system == 1:
            self.osc1 = Rossler(self.pitch, self.chaos1, mul=self.amp1) 
            self.osc2 = Rossler(self.osc1, self.chaos2, mul=self.amp2)
            self.osc3 = Rossler(self.osc1+self.osc2, self.chaos3, self.stereo, self.amp3)

        if self.system == 2:
            self.osc1 = Lorenz(self.pitch, self.chaos1, mul=self.amp1) 
            self.osc2 = Lorenz(self.osc1, self.chaos2, mul=self.amp2)
            self.osc3 = Lorenz(self.osc1+self.osc2, self.chaos3, self.stereo, self.amp3)

        if self.system == 3:
            self.osc1 = ChenLee(self.pitch, self.chaos1, mul=self.amp1) 
            self.osc2 = ChenLee(self.osc1, self.chaos2, mul=self.amp2)
            self.osc3 = ChenLee(self.osc1+self.osc2, self.chaos3, self.stereo, self.amp3)

        self.trig = Thresh(self.osc3, self.thresh)

    def setPitch(self, pitch):
        self.pitch = pitch
        self.osc1.setPitch(self.pitch)

    def setChaos1(self, chaos):
        self.chaos1 = chaos
        self.osc1.setChaos(self.chaos1)

    def setChaos2(self, chaos):
        self.chaos2 = chaos
        self.osc2.setChaos(self.chaos2)

    def setChaos3(self, chaos):
        self.chaos3 = chaos
        self.osc3.setChaos(self.chaos3)

    def setMul1(self, mul):
        self.amp1 = mul
        self.osc1.setMul(self.amp1)

    def setMul2(self, mul):
        self.amp2 = mul
        self.osc2.setMul(self.amp2)

    def setMul3(self, mul):
        self.amp3 = mul
        self.osc3.setMul(self.amp3)

    def setThresh(self, thresh):
        self.trig.setThreshold(thresh)

    def out(self):
        self.osc3.out()

    def ctrl(self):
        self.osc1.ctrl()
        self.osc2.ctrl()
        self.osc3.ctrl()

    def mod(self):
        return self.osc3
            


#_________________________________________________________________________________________________________

osc = TripleChaos(2, stereo=True)
#osc.out()
osc.ctrl()
met=Metro().play()
table = LinTable([(0,0),(100,.5),(5000,0)])
env = TrigEnv(osc.trig, table)
sine = Sine(220, mul=env).out()




s.gui(locals())