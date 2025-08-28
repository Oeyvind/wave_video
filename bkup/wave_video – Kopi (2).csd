<Cabbage>
form size(1200, 510), caption("Wave video"), pluginId("wvi1"), guiMode("queue"), colour(30,30,30)
rslider channel("Freq"), bounds(10, 10, 70, 70), text("Freq"), range(20, 20000, 100, 0.35)
rslider channel("Amp"), bounds(70, 10, 70, 70), text("Amp"), range(-96, 24, 0, 0.5)
nslider channel("Wave_exp"), bounds(150, 50, 70, 20), range(0.1, 4, 1), fontSize(14)
button channel("Wave_on"), bounds(150, 10, 70, 30), text("W_On"), colour:0("black"), colour:1("green")
button channel("Wavenote_on"), bounds(230, 20, 70, 50), text("Wn_On"), colour:0("black"), colour:1("green")
button channel("Wavemidi_on"), bounds(310, 20, 70, 50), text("Wm_On"), colour:0("black"), colour:1("green")
gentable bounds(10, 90, 380, 200), channel("wave"), sampleRange(0, 1024), ampRange(-1, 1, 1), outlineThickness(3), tableNumber(1.0), tableGridColour(155, 155, 155, 255) tableBackgroundColour(0,0,0,0) tableColour:0(147, 210, 0, 255)
button channel("Spectrum_on"), bounds(410, 20, 70, 50), text("S_On"), colour:0("black"), colour:1("green")
button channel("Spectrum_midi_on"), bounds(490, 20, 70, 50), text("Sm_On"), colour:0("black"), colour:1("green")
gentable bounds(410, 90, 380, 200), channel("spectrum"), sampleRange(0,16), ampRange(-0, 1, 2), outlineThickness(3), tableNumber(2.0), tableGridColour(155, 155, 155, 255) tableBackgroundColour(0,0,0,0) tableColour:0(147, 210, 0, 255)
button channel("Cepstrum_on"), bounds(810, 20, 70, 50), text("C_On"), colour:0("black"), colour:1("green")
button channel("Cepstrum_midi_on"), bounds(890, 20, 70, 50), text("Cm_On"), colour:0("black"), colour:1("green")
gentable bounds(810, 90, 380, 200), channel("cepstrum"), sampleRange(0, 32), ampRange(-0, 1, 3), outlineThickness(3), tableNumber(3.0), tableGridColour(155, 155, 155, 255) tableBackgroundColour(0,0,0,0) tableColour:0(147, 210, 0, 255)
button channel("Ifft_on"), bounds(410, 320, 70, 50), text("Inv_On"), colour:0("black"), colour:1("green")
button channel("Ifft_midi_on"), bounds(490, 320, 70, 50), text("Invm_On"), colour:0("black"), colour:1("green")

button channel("Peaks_on"), bounds(590, 320, 70, 50), text("Peaks_On"), colour:0("black"), colour:1("green")
gentable bounds(810, 300, 380, 200), channel("inv_fft"), sampleRange(0, 16), ampRange(-1, 1, 4), outlineThickness(3), tableNumber(4.0), tableGridColour(155, 155, 155, 255) tableBackgroundColour(0,0,0,0) tableColour:0(147, 210, 0, 255)
csoundoutput bounds(10, 300, 380, 200)
</Cabbage>
<CsoundSynthesizer>
<CsOptions>
-n -d -m0 -Q0 -+rtmidi=null
</CsOptions>
<CsInstruments>

ksmps = 64
nchnls = 2
0dbfs=1

  giWave ftgen 1, 0, 1024, 7, 0, 1024, -1  ; empty  
  giWave1 ftgen 0, 0, 1024, -2, 0  ; empty  
  giWave2 ftgen 0, 0, 1024, -2, 0  ; empty
  giWaveRaw ftgen 0, 0, 1024, -2, 0  ; empty
  giWaves ftgen 0, 0, 2, -2, giWave1, giWave2
  ;giRawWave ftgen 2, 0, 1024, 7, 0, 1024, -1  ; empty  
  ;giRawWave1 ftgen 0, 0, 1024, -2, 0  ; empty  
  ;giRawWave2 ftgen 0, 0, 1024, -2, 0  ; empty
  ;giRawWaves ftgen 0, 0, 2, -2, giRawWave1, giRawWave2
  giSpectrum ftgen 2, 0, 32, -2, 0  ; empty  
  giCepstrum ftgen 3, 0, 32, -2, 0  ; empty  
  giInvFFT ftgen 4, 0, 16, -2, 0  ; empty  
  gkndx init 0
  gihandle OSCinit 9899 ; set the network port number where we will receive OSC data from Python
  giSigmoRise 	ftgen	0, 0, 256, 19, 0.5, 1, 270, 1				; rising sigmoid
	giSigmoFall 	ftgen	0, 0, 256, 19, 0.5, 1, 90, 1				; falling sigmoid


opcode getNote, i, ii[]
  indx, iNotes[] xin 
  inote = iNotes[indx%lenarray(iNotes)]+(int(indx/lenarray(iNotes))*12)
  xout inote
endop

opcode getWaveAmp, k, iii
  indx, ilen, inum xin 
  kamp = table:k(indx*((1/inum)*ilen), giWave)
  xout kamp
endop

opcode getWaveIndx, i, iii
  indx, ilen, inum xin 
  indx2 = indx*((1/inum)*ilen)
  xout indx2
endop

opcode tablemidi, 0, iiiii[]ii
  ithresh,ichn,indx,itab,iNotes[],ibasenote,inoteactive_tab xin
  k1 = table:k(indx,itab)
  k1diff diff k1
  kmax init 0
  kmax max kmax, k1diff
  kthresh = kmax*ithresh
  kflag lastcycle
  if kflag > 0 then
    k1diff = -1
  endif
  ibasenote = 60
  inum = getNote(indx,iNotes)+ibasenote
  ivel = 100
  kon = 1
  koff = 0
  if k1diff > kthresh then
    ;if table(inum, inoteactive_tab) == 0 then
      midiout 144+ichn-1, ichn, inum, ivel
      tablew kon, inum, inoteactive_tab
    ;endif 
  elseif k1diff < 0 then
    ;if table(inum, inoteactive_tab) == 1 then
      midiout 128+ichn-1, ichn, inum, ivel
      tablew koff, inum, inoteactive_tab
    ;endif
  endif
endop

opcode tablemidi_w, 0, iiiiii[]ii
  ithresh,ichn,indx,indx2,itab,iNotes[],ibasenote,inoteactive_tab xin
  k1 = table:k(indx,itab)
  k1diff diff k1
  kmax init 0
  kmax max kmax, k1diff
  kthresh = kmax*ithresh
  kflag lastcycle
  if kflag > 0 then
    k1diff = -1
  endif
  ibasenote = 60
  inum = getNote(indx2,iNotes)+ibasenote
  ivel = 100
  kon = 1
  koff = 0
  printk2 inum*signum(k1diff)
  if k1diff > kthresh then
    ;if table(inum, inoteactive_tab) == 0 then
      midiout 144+ichn-1, ichn, inum, ivel
      tablew kon, inum, inoteactive_tab
    ;endif 
  elseif k1diff < 0 then
    ;if table(inum, inoteactive_tab) == 1 then
      midiout 128+ichn-1, ichn, inum, ivel
      tablew koff, inum, inoteactive_tab
    ;endif
  endif
endop

instr 1
  kwave_on chnget "Wave_on"
  kwaveon trigger kwave_on, 0.5, 0
  kwaveoff trigger kwave_on, 0.5, 1
  if kwaveon > 0 then
    event "i", 10, 0, -1
  endif
  if kwaveoff > 0 then
    event "i", -10, 0, .1
  endif
  
  kwavenote_on chnget "Wavenote_on"
  kwavenoteon trigger kwavenote_on, 0.5, 0
  kwavenoteoff trigger kwavenote_on, 0.5, 1
  if kwavenoteon > 0 then
    event "i", 11, 0, -1
  endif
  if kwavenoteoff > 0 then
    event "i", -11, 0, .1
  endif

  kspectrum_on chnget "Spectrum_on"
  kspectrumon trigger kspectrum_on, 0.5, 0
  kspectrumoff trigger kspectrum_on, 0.5, 1
  if kspectrumon > 0 then
    event "i", 12, 0, -1
  endif
  if kspectrumoff > 0 then
    event "i", -12, 0, .1
  endif

  kcepstr_on chnget "Cepstrum_on"
  kcepstron trigger kcepstr_on, 0.5, 0
  kcepstroff trigger kcepstr_on, 0.5, 1
  if kcepstron > 0 then
    event "i", 13, 0, -1
  endif
  if kcepstroff > 0 then
    event "i", -13, 0, .1
  endif

  kifft_on chnget "Ifft_on"
  kiffton trigger kifft_on, 0.5, 0
  kifftoff trigger kifft_on, 0.5, 1
  if kiffton > 0 then
    event "i", 14, 0, -1
  endif
  if kifftoff > 0 then
    event "i", -14, 0, .1
  endif

  kwavemidi_on chnget "Wavemidi_on"
  kwavemidion trigger kwavemidi_on, 0.5, 0
  kwavemidioff trigger kwavemidi_on, 0.5, 1
  if kwavemidion > 0 then
    event "i", 21, 0, -1
  endif
  if kwavemidioff > 0 then
    event "i", -21, 0, .1
  endif

  kspectrum_midi_on chnget "Spectrum_midi_on"
  kspectrum_midion trigger kspectrum_midi_on, 0.5, 0
  kspectrum_midioff trigger kspectrum_midi_on, 0.5, 1
  if kspectrum_midion > 0 then
    event "i", 22, 0, -1
  endif
  if kspectrum_midioff > 0 then
    event "i", -22, 0, .1
  endif

  kcepstrum_midi_on chnget "Cepstrum_midi_on"
  kcepstrum_midion trigger kcepstrum_midi_on, 0.5, 0
  kcepstrum_midioff trigger kcepstrum_midi_on, 0.5, 1
  if kcepstrum_midion > 0 then
    event "i", 23, 0, -1
  endif
  if kcepstrum_midioff > 0 then
    event "i", -23, 0, .1
  endif

  kifft_midi_on chnget "Ifft_midi_on"
  kifft_midion trigger kifft_midi_on, 0.5, 0
  kifft_midioff trigger kifft_midi_on, 0.5, 1
  if kifft_midion > 0 then
    event "i", 24, 0, -1
  endif
  if kifft_midioff > 0 then
    event "i", -24, 0, .1
  endif

  kindex init 0
  kvalue init 0
  ktimethen init 0
  nextmsg_wave:
  kmess OSClisten gihandle, "wave_video", "ff", kindex, kvalue ; receive OSC data from Python
  kvalue1 = (kvalue/250) ; scale and offset
  ; fade in and out
  if kindex < 256 then
    kamp table kindex, giSigmoRise
  elseif kindex > 768 then
    kamp table kindex-768, giSigmoFall
  else
    kamp = 1
  endif
  ; raise wave to nth power, shaping
  kexp chnget "Wave_exp"
  if kvalue1 > 0 then
    kvalue1 pow kvalue1, kexp
  else
    kvalue1 = pow(kvalue1*-1, kexp)*-1
  endif
  kvalue1fade = kvalue1;*kamp
  kswitch init 1
  ktab = kswitch == 1 ? giWave1 : giWave2
  ;ktabraw = kswitch == 1 ? giRawWave1 : giRawWave2

  tablewkt kvalue1fade, kindex, ktab
  tablew kvalue1, kindex, giWaveRaw
  if kindex == 1022 then
    kswitch = kswitch == 1 ? 2 : 1
    ktime timeinsts
    kupdate_time limit ktime-ktimethen, 0, 1
    ktimethen = ktime
    event "i", 2, 0, kupdate_time, ktab
  endif
  if kmess == 0 goto done_wave
  kgoto nextmsg_wave 
  done_wave:

  kindex_p init 0
  ksign init 0
  nextmsg_peaks:
  kmess OSClisten gihandle, "wave_peaks", "ff", kindex_p, ksign ; receive OSC data from Python
  if kmess == 0 goto done_peaks
  kamp =-35;table kindex_p, giWaveRaw
  kcps = (((kindex_p/1024)^1.5)*600)+200
  kpan = (ksign*0.5)+0.5
  kpeaks_on chnget "Peaks_on"
  if kpeaks_on > 0 then
    event "i", 3, 0, 0.3, kamp, kcps, kpan 
  endif
  kgoto nextmsg_peaks
  done_peaks:
endin

instr 3
  iamp = ampdbfs(p4)
  icps = p5;*(p6+1)
  ipan = p6
  print ipan
  amp linen 1, 0.01, p3, 0.01
  a1 poscil iamp*amp, icps
  aL = a1*(1-ipan)
  aR = a1*ipan
  outs aR, aR
endin

instr 2
  itab = p4
  ;print p2, itab, p3
  if itab == giWave2 then
    kndx line 0, p3, 1
  else 
    kndx line 1, p3, 0
  endif
  gkndx = kndx
  ftmorf kndx, giWaves, giWave
  cabbageSet "wave", "tableNumber", 1; update table display
  /*
  ;ftmorf kndx, giRawWaves, giRawWave
  konce init 1
  if konce > 0 then
    kArr[] tab2array giWave
    kFFT[] rfft kArr
    kMags[] mags kFFT
    ;kLogs[] = log(kMags)
    ;iampmags = 1/100
    ;kMags *= iampmags
    ;kShape[] = kMags;pow(kMags,0.2)-0.4
    kPows[] = pows(kFFT)
    ispect_amp = 0.04
    kSpec_shape[] = pow(kPows, 0.3)* ispect_amp
    copya2ftab kSpec_shape, giSpectrum
    kMFB[] = log(mfb(kPows,200,5000,32))
    kMfcc[] = dct(kMFB)
    imfcc_amp = 0.01
    kMfcc_shape[] = (kMfcc*imfcc_amp)
    kMfcc_shape = tanh(kMfcc_shape)*0.8
    copya2ftab kMfcc_shape, giCepstrum
    kIFFT[] rifft kArr
    kShape_IFFT[] = kIFFT*4
    copya2ftab kShape_IFFT, giInvFFT
    cabbageSet	"spectrum", "tableNumber", 2	; update table display
    cabbageSet	"cepstrum", "tableNumber", 3	; update table display
    cabbageSet	"inv_fft", "tableNumber", 4	; update table display
    konce = 0
  endif
  */
endin

instr 10
  ; read ftable waveform with oscillator
  kfreq chnget "Freq"
  kamp_dB chnget "Amp"
  kamp = ampdbfs(kamp_dB)
  aphase phasor kfreq
  aphase *= 1024
  a1 table3 aphase, giWave
  a1 *= kamp
  outs a1, a1
endin

instr 11
  iNotes[] fillarray 0,3,5,7,10
  ibasenote = 60
  ilen tableng giWave
  a1 poscil tonek(getWaveAmp(0,ilen,16),2), cpsmidinn(getNote(0,iNotes)+ibasenote)
  a2 poscil tonek(getWaveAmp(1,ilen,16),2), cpsmidinn(getNote(1,iNotes)+ibasenote)
  a3 poscil tonek(getWaveAmp(2,ilen,16),2), cpsmidinn(getNote(2,iNotes)+ibasenote)
  a4 poscil tonek(getWaveAmp(3,ilen,16),2), cpsmidinn(getNote(3,iNotes)+ibasenote)
  a5 poscil tonek(getWaveAmp(4,ilen,16),2), cpsmidinn(getNote(4,iNotes)+ibasenote)
  a6 poscil tonek(getWaveAmp(5,ilen,16),2), cpsmidinn(getNote(5,iNotes)+ibasenote)
  a7 poscil tonek(getWaveAmp(6,ilen,16),2), cpsmidinn(getNote(6,iNotes)+ibasenote)
  a8 poscil tonek(getWaveAmp(7,ilen,16),2), cpsmidinn(getNote(7,iNotes)+ibasenote)
  a9 poscil tonek(getWaveAmp(8,ilen,16),2), cpsmidinn(getNote(8,iNotes)+ibasenote)
  a10 poscil tonek(getWaveAmp(9,ilen,16),2), cpsmidinn(getNote(9,iNotes)+ibasenote)
  a11 poscil tonek(getWaveAmp(10,ilen,16),2), cpsmidinn(getNote(10,iNotes)+ibasenote)
  a12 poscil tonek(getWaveAmp(11,ilen,16),2), cpsmidinn(getNote(11,iNotes)+ibasenote)
  a13 poscil tonek(getWaveAmp(12,ilen,16),2), cpsmidinn(getNote(12,iNotes)+ibasenote)
  a14 poscil tonek(getWaveAmp(13,ilen,16),2), cpsmidinn(getNote(13,iNotes)+ibasenote)
  a15 poscil tonek(getWaveAmp(14,ilen,16),2), cpsmidinn(getNote(14,iNotes)+ibasenote)
  a16 poscil tonek(getWaveAmp(15,ilen,16),2), cpsmidinn(getNote(15,iNotes)+ibasenote)
  asum sum a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16
  asum *= 0.1
  outs asum, asum
endin

instr 12
  iNotes[] fillarray 0,3,5,7,10
  ibasenote = 60
  a1 poscil tonek(table:k(0,giSpectrum),2), cpsmidinn(getNote(0,iNotes)+ibasenote)
  a2 poscil tonek(table:k(1,giSpectrum),2), cpsmidinn(getNote(1,iNotes)+ibasenote)
  a3 poscil tonek(table:k(2,giSpectrum),2), cpsmidinn(getNote(2,iNotes)+ibasenote)
  a4 poscil tonek(table:k(3,giSpectrum),2), cpsmidinn(getNote(3,iNotes)+ibasenote)
  a5 poscil tonek(table:k(4,giSpectrum),2), cpsmidinn(getNote(4,iNotes)+ibasenote)
  a6 poscil tonek(table:k(5,giSpectrum),2), cpsmidinn(getNote(5,iNotes)+ibasenote)
  a7 poscil tonek(table:k(6,giSpectrum),2), cpsmidinn(getNote(6,iNotes)+ibasenote)
  a8 poscil tonek(table:k(7,giSpectrum),2), cpsmidinn(getNote(7,iNotes)+ibasenote)
  a9 poscil tonek(table:k(8,giSpectrum),2), cpsmidinn(getNote(8,iNotes)+ibasenote)
  a10 poscil tonek(table:k(9,giSpectrum),2), cpsmidinn(getNote(9,iNotes)+ibasenote)
  a11 poscil tonek(table:k(10,giSpectrum),2), cpsmidinn(getNote(10,iNotes)+ibasenote)
  a12 poscil tonek(table:k(11,giSpectrum),2), cpsmidinn(getNote(11,iNotes)+ibasenote)
  a13 poscil tonek(table:k(12,giSpectrum),2), cpsmidinn(getNote(12,iNotes)+ibasenote)
  a14 poscil tonek(table:k(13,giSpectrum),2), cpsmidinn(getNote(13,iNotes)+ibasenote)
  a15 poscil tonek(table:k(14,giSpectrum),2), cpsmidinn(getNote(14,iNotes)+ibasenote)
  a16 poscil tonek(table:k(15,giSpectrum),2), cpsmidinn(getNote(15,iNotes)+ibasenote)
  asum sum a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16
  asum *= 0.1
  outs asum, asum
endin

instr 13
  iNotes[] fillarray 0,3,5,7,10
  ibasenote = 60
  a1 poscil tonek(table:k(0,giCepstrum),2), cpsmidinn(getNote(0,iNotes)+ibasenote)
  a2 poscil tonek(table:k(1,giCepstrum),2), cpsmidinn(getNote(1,iNotes)+ibasenote)
  a3 poscil tonek(table:k(2,giCepstrum),2), cpsmidinn(getNote(2,iNotes)+ibasenote)
  a4 poscil tonek(table:k(3,giCepstrum),2), cpsmidinn(getNote(3,iNotes)+ibasenote)
  a5 poscil tonek(table:k(4,giCepstrum),2), cpsmidinn(getNote(4,iNotes)+ibasenote)
  a6 poscil tonek(table:k(5,giCepstrum),2), cpsmidinn(getNote(5,iNotes)+ibasenote)
  a7 poscil tonek(table:k(6,giCepstrum),2), cpsmidinn(getNote(6,iNotes)+ibasenote)
  a8 poscil tonek(table:k(7,giCepstrum),2), cpsmidinn(getNote(7,iNotes)+ibasenote)
  a9 poscil tonek(table:k(8,giCepstrum),2), cpsmidinn(getNote(8,iNotes)+ibasenote)
  a10 poscil tonek(table:k(9,giCepstrum),2), cpsmidinn(getNote(9,iNotes)+ibasenote)
  a11 poscil tonek(table:k(10,giCepstrum),2), cpsmidinn(getNote(10,iNotes)+ibasenote)
  a12 poscil tonek(table:k(11,giCepstrum),2), cpsmidinn(getNote(11,iNotes)+ibasenote)
  a13 poscil tonek(table:k(12,giCepstrum),2), cpsmidinn(getNote(12,iNotes)+ibasenote)
  a14 poscil tonek(table:k(13,giCepstrum),2), cpsmidinn(getNote(13,iNotes)+ibasenote)
  a15 poscil tonek(table:k(14,giCepstrum),2), cpsmidinn(getNote(14,iNotes)+ibasenote)
  a16 poscil tonek(table:k(15,giCepstrum),2), cpsmidinn(getNote(15,iNotes)+ibasenote)
  a17 poscil tonek(table:k(16,giCepstrum),2), cpsmidinn(getNote(16,iNotes)+ibasenote)
  a18 poscil tonek(table:k(17,giCepstrum),2), cpsmidinn(getNote(17,iNotes)+ibasenote)
  a19 poscil tonek(table:k(18,giCepstrum),2), cpsmidinn(getNote(18,iNotes)+ibasenote)
  a20 poscil tonek(table:k(19,giCepstrum),2), cpsmidinn(getNote(19,iNotes)+ibasenote)
  a21 poscil tonek(table:k(20,giCepstrum),2), cpsmidinn(getNote(20,iNotes)+ibasenote)
  a22 poscil tonek(table:k(21,giCepstrum),2), cpsmidinn(getNote(21,iNotes)+ibasenote)
  a23 poscil tonek(table:k(22,giCepstrum),2), cpsmidinn(getNote(22,iNotes)+ibasenote)
  a24 poscil tonek(table:k(23,giCepstrum),2), cpsmidinn(getNote(23,iNotes)+ibasenote)
  a25 poscil tonek(table:k(24,giCepstrum),2), cpsmidinn(getNote(24,iNotes)+ibasenote)
  a26 poscil tonek(table:k(25,giCepstrum),2), cpsmidinn(getNote(25,iNotes)+ibasenote)
  a27 poscil tonek(table:k(26,giCepstrum),2), cpsmidinn(getNote(26,iNotes)+ibasenote)
  a28 poscil tonek(table:k(27,giCepstrum),2), cpsmidinn(getNote(27,iNotes)+ibasenote)
  a29 poscil tonek(table:k(28,giCepstrum),2), cpsmidinn(getNote(28,iNotes)+ibasenote)
  a30 poscil tonek(table:k(29,giCepstrum),2), cpsmidinn(getNote(29,iNotes)+ibasenote)
  a31 poscil tonek(table:k(30,giCepstrum),2), cpsmidinn(getNote(30,iNotes)+ibasenote)
  a32 poscil tonek(table:k(31,giCepstrum),2), cpsmidinn(getNote(31,iNotes)+ibasenote)
  asum sum a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,\
    a11,a12,a13,a14,a15,a16,a17,a18,a19,a20,\ 
    a21,a22,a23,a24,a25,a26,a27,a28,a29,a30,\
    a31, a32
  asum *= 0.05
  outs asum, asum
endin


instr 14
  iNotes[] fillarray 0,3,5,7,10
  ibasenote = 60
  a1 poscil tonek(table:k(0,giInvFFT),2), cpsmidinn(getNote(0,iNotes)+ibasenote)
  a2 poscil tonek(table:k(1,giInvFFT),2), cpsmidinn(getNote(1,iNotes)+ibasenote)
  a3 poscil tonek(table:k(2,giInvFFT),2), cpsmidinn(getNote(2,iNotes)+ibasenote)
  a4 poscil tonek(table:k(3,giInvFFT),2), cpsmidinn(getNote(3,iNotes)+ibasenote)
  a5 poscil tonek(table:k(4,giInvFFT),2), cpsmidinn(getNote(4,iNotes)+ibasenote)
  a6 poscil tonek(table:k(5,giInvFFT),2), cpsmidinn(getNote(5,iNotes)+ibasenote)
  a7 poscil tonek(table:k(6,giInvFFT),2), cpsmidinn(getNote(6,iNotes)+ibasenote)
  a8 poscil tonek(table:k(7,giInvFFT),2), cpsmidinn(getNote(7,iNotes)+ibasenote)
  a9 poscil tonek(table:k(8,giInvFFT),2), cpsmidinn(getNote(8,iNotes)+ibasenote)
  a10 poscil tonek(table:k(9,giInvFFT),2), cpsmidinn(getNote(9,iNotes)+ibasenote)
  a11 poscil tonek(table:k(10,giInvFFT),2), cpsmidinn(getNote(10,iNotes)+ibasenote)
  a12 poscil tonek(table:k(11,giInvFFT),2), cpsmidinn(getNote(11,iNotes)+ibasenote)
  a13 poscil tonek(table:k(12,giInvFFT),2), cpsmidinn(getNote(12,iNotes)+ibasenote)
  a14 poscil tonek(table:k(13,giInvFFT),2), cpsmidinn(getNote(13,iNotes)+ibasenote)
  a15 poscil tonek(table:k(14,giInvFFT),2), cpsmidinn(getNote(14,iNotes)+ibasenote)
  a16 poscil tonek(table:k(15,giInvFFT),2), cpsmidinn(getNote(15,iNotes)+ibasenote)
  asum sum a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16
  asum *= 0.1
  outs asum, asum
endin

; midi out
instr 21
  iNotes[] fillarray 0,3,5,7,10
  ibasenote = 60
  ichn = 1
  ithresh = 0.5
  ilen tableng giWaveRaw
  inoteactive_tab ftgentmp 0, 0, 128, -2, 0
  tablemidi_w(ithresh,ichn,getWaveIndx(0,ilen,16),0,giWaveRaw,iNotes,ibasenote,inoteactive_tab)
  tablemidi_w(ithresh,ichn,getWaveIndx(1,ilen,16),1,giWaveRaw,iNotes,ibasenote,inoteactive_tab)
  tablemidi_w(ithresh,ichn,getWaveIndx(2,ilen,16),2,giWaveRaw,iNotes,ibasenote,inoteactive_tab)
  tablemidi_w(ithresh,ichn,getWaveIndx(3,ilen,16),3,giWaveRaw,iNotes,ibasenote,inoteactive_tab)
  tablemidi_w(ithresh,ichn,getWaveIndx(4,ilen,16),4,giWaveRaw,iNotes,ibasenote,inoteactive_tab)
  tablemidi_w(ithresh,ichn,getWaveIndx(5,ilen,16),5,giWaveRaw,iNotes,ibasenote,inoteactive_tab)
  tablemidi_w(ithresh,ichn,getWaveIndx(6,ilen,16),6,giWaveRaw,iNotes,ibasenote,inoteactive_tab)
  tablemidi_w(ithresh,ichn,getWaveIndx(7,ilen,16),7,giWaveRaw,iNotes,ibasenote,inoteactive_tab)
  tablemidi_w(ithresh,ichn,getWaveIndx(8,ilen,16),8,giWaveRaw,iNotes,ibasenote,inoteactive_tab)
  tablemidi_w(ithresh,ichn,getWaveIndx(9,ilen,16),9,giWaveRaw,iNotes,ibasenote,inoteactive_tab)
  tablemidi_w(ithresh,ichn,getWaveIndx(10,ilen,16),10,giWaveRaw,iNotes,ibasenote,inoteactive_tab)
  tablemidi_w(ithresh,ichn,getWaveIndx(11,ilen,16),11,giWaveRaw,iNotes,ibasenote,inoteactive_tab)
  tablemidi_w(ithresh,ichn,getWaveIndx(12,ilen,16),12,giWaveRaw,iNotes,ibasenote,inoteactive_tab)
  tablemidi_w(ithresh,ichn,getWaveIndx(13,ilen,16),13,giWaveRaw,iNotes,ibasenote,inoteactive_tab)
  tablemidi_w(ithresh,ichn,getWaveIndx(14,ilen,16),14,giWaveRaw,iNotes,ibasenote,inoteactive_tab)
  tablemidi_w(ithresh,ichn,getWaveIndx(15,ilen,16),15,giWaveRaw,iNotes,ibasenote,inoteactive_tab)
endin

instr 22
  iNotes[] fillarray 0,3,5,7,10
  ibasenote = 60
  ichn = 2
  ithresh = 0.1
  inoteactive_tab ftgentmp 0, 0, 128, -2, 0
  tablemidi(ithresh,ichn,0,giSpectrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,1,giSpectrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,2,giSpectrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,3,giSpectrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,4,giSpectrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,5,giSpectrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,6,giSpectrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,7,giSpectrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,8,giSpectrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,9,giSpectrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,10,giSpectrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,11,giSpectrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,12,giSpectrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,13,giSpectrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,14,giSpectrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,15,giSpectrum,iNotes,ibasenote,inoteactive_tab)
  
endin

instr 23
  iNotes[] fillarray 0,3,5,7,10
  ibasenote = 60
  ichn = 3
  ithresh = 0.1
  inoteactive_tab ftgentmp 0, 0, 128, -2, 0
  tablemidi(ithresh,ichn,0,giCepstrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,1,giCepstrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,2,giCepstrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,3,giCepstrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,4,giCepstrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,5,giCepstrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,6,giCepstrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,7,giCepstrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,8,giCepstrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,9,giCepstrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,10,giCepstrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,11,giCepstrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,12,giCepstrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,13,giCepstrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,14,giCepstrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,15,giCepstrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,16,giCepstrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,17,giCepstrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,18,giCepstrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,19,giCepstrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,20,giCepstrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,21,giCepstrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,22,giCepstrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,23,giCepstrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,24,giCepstrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,25,giCepstrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,26,giCepstrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,27,giCepstrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,28,giCepstrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,29,giCepstrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,30,giCepstrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,31,giCepstrum,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,32,giCepstrum,iNotes,ibasenote,inoteactive_tab)
endin

instr 24
  iNotes[] fillarray 0,3,5,7,10
  ibasenote = 60
  ichn = 4
  ithresh = 0.1
  inoteactive_tab ftgentmp 0, 0, 128, -2, 0
  tablemidi(ithresh,ichn,0,giInvFFT,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,1,giInvFFT,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,2,giInvFFT,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,3,giInvFFT,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,4,giInvFFT,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,5,giInvFFT,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,6,giInvFFT,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,7,giInvFFT,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,8,giInvFFT,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,9,giInvFFT,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,10,giInvFFT,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,11,giInvFFT,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,12,giInvFFT,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,13,giInvFFT,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,14,giInvFFT,iNotes,ibasenote,inoteactive_tab)
  tablemidi(ithresh,ichn,15,giInvFFT,iNotes,ibasenote,inoteactive_tab)  
endin

</CsInstruments>  
<CsScore>
i1 0 84600
</CsScore>
</CsoundSynthesizer>