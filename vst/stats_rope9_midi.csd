<Cabbage>
form size(900, 510), caption("Stats rope"), pluginId("str9"), guiMode("queue"), colour(30,30,30)
rslider channel("Freq_wav"),          bounds(10,  10, 60, 60), text("Freq"), range(20, 300, 100, 0.35)
rslider channel("Amp_wav"),           bounds(70,  10, 60, 60), text("Amp"), range(-50, 6, 0, 3)
rslider channel("detune_wav"),        bounds(130, 10, 60, 60), text("Detune"), range(0, 1, 0.1, 0.35)
button channel("Wave_raw_on"),        bounds(190, 10, 68, 30), text("Wraw_On"), colour:0("black"), colour:1("green")
button channel("Wave_fine_on"),       bounds(260, 10, 70, 30), text("Wfine_On"), colour:0("black"), colour:1("green")

rslider channel("Freq_wavd"),          bounds(10,  80, 60, 60), text("Freq"), range(80, 2000, 100, 0.35)
rslider channel("Amp_wavd"),           bounds(70,  80, 60, 60), text("Amp"), range(-50, 6, 0, 3)
rslider channel("detune_wavd"),        bounds(130, 80, 60, 60), text("Detune"), range(0, 1, 0.1, 0.35)
button channel("Wave_raw_detune_on"), bounds(190, 80, 68, 30), text("Wrawd_On"), colour:0("black"), colour:1("green")
button channel("Wave_fine_detune_on"),bounds(260, 80, 70, 30), text("Wfined_On"), colour:0("black"), colour:1("green")

rslider channel("Freq_fft"),          bounds(10,  150, 60, 60), text("Freq"), range(130, 2000, 100, 0.35)
rslider channel("Amp_fft"),           bounds(70,  150, 60, 60), text("Amp"), range(-50, 6, 0, 3)
rslider channel("detune_fft"),        bounds(130, 150, 60, 60), text("Detune"), range(0, 1, 0.1, 0.35)
rslider channel("chroma_fft"),        bounds(190, 150, 60, 60), text("Chroma"), range(-1, 1, 0.1)
rslider channel("dist_fft"),          bounds(250, 150, 60, 60), text("Dist"), range(0, 1, 0.1, 0.35)
button channel("Fft_bank"),           bounds(320, 150, 70, 30), text("FFT bank"), colour:0("black"), colour:1("green")

rslider channel("Freq_fadr"),         bounds(10,  230, 60, 60), text("Freq"), range(60, 1000, 100, 0.35)
rslider channel("Amp_fadr"),          bounds(70,  230, 60, 60), text("Amp"), range(-50, 6, 0, 3)
rslider channel("detune_fadr"),       bounds(130, 230, 60, 60), text("Detune"), range(0, 1, 0.1, 0.35)
rslider channel("chroma_fadr"),       bounds(190, 230, 60, 60), text("Chroma"), range(-1, 1, 0.1)
rslider channel("dist_fadr"),         bounds(250, 230, 60, 60), text("Dist"), range(0, 1, 0.1, 0.35)
button channel("Fader_bank"),         bounds(320, 230, 70, 30), text("Fader bank"), colour:0("black"), colour:1("green")
  
rslider channel("Grainpitch"),        bounds(10,  300, 60, 60), text("G.pitch"), range(10, 1000, 100, 0.35)
rslider channel("Grainamp"),          bounds(70,  300, 60, 60), text("Amp"), range(-50, 6, 0, 3)
rslider channel("Grate"),             bounds(130, 300, 60, 60), text("G.rate"), range(0.5, 20, 4, 0.35)
rslider channel("Gdur"),              bounds(190, 300, 60, 60), text("G.dur"), range(0.1, 2, 1, 0.35)
rslider channel("G_dist_rate"),       bounds(250, 300, 60, 60), text("Dist_rate"), range(0, 2, 0.1, 0.35)
rslider channel("G_voice_spread"),    bounds(310, 300, 60, 60), text("Voice_spread"), range(0, 7, 0.1, 0.35)
rslider channel("distgrains_ampthresh"), bounds(10, 440, 60, 60), text("M.ampthresh"), range(-50, 0, -5)
rslider channel("distgrains_transpose"), bounds(70, 440, 60, 60), text("M.transpose"), range(-24, 24, 0, 1, 1)
nslider channel("distgrains_midichan"), bounds(130, 440, 50, 40), text("M.chan"), range(1, 16, 1, 1, 1)
button channel("Distance_grain"),     bounds(370, 300, 70, 30), text("Dstnc_grain"), colour:0("black"), colour:1("green")

rslider channel("Grainpitch2"),        bounds(10,  370, 60, 60), text("G.pitch"), range(10, 1000, 100, 0.35)
rslider channel("Grainamp2"),          bounds(70,  370, 60, 60), text("Amp"), range(-50, 6, 0, 3)
rslider channel("Grate2"),             bounds(130, 370, 60, 60), text("G.rate"), range(0.5, 20, 4, 0.35)
rslider channel("Gdur2"),              bounds(190, 370, 60, 60), text("G.dur"), range(0.1, 2, 1, 0.35)
rslider channel("G2_pitchmod"),        bounds(250, 370, 60, 60), text("Pitchmod"), range(0, 2, 1, 0.35)
rslider channel("G2_pitch_spread"),    bounds(310, 370, 60, 60), text("Pitchspread"), range(0, 1, 0.1, 0.35)
rslider channel("G2_ratemod"),         bounds(370, 370, 60, 60), text("Ratemod"), range(0, 2, 1, 0.35)
button channel("Grain2"),              bounds(430, 370, 70, 30), text("Grain2"), colour:0("black"), colour:1("green")

button channel("Noisebank"), bounds(480, 230, 70, 40), text("Noisbnk"), colour:0("black"), colour:1("green")

  kactivity_thresh chnget "stop_activity_thresh"
nslider channel("stop_activity_thresh"), bounds(590, 230, 40, 20), range(0.01, 1, 0.3), fontSize(14)
label bounds(590, 247, 40, 18), fontSize(11), text("stop_thresh")
button channel("Stopchord"), bounds(640, 230, 70, 40), text("Stopchord"), colour:0("black"), colour:1("green")
nslider channel("detune_stopchord"), bounds(715, 230, 40, 20), range(0, 1, 0.1), fontSize(14)
nslider channel("amp_stopchord"), bounds(715, 250, 40, 20), range(-96, -10, -30), fontSize(14)
button channel("stopchord_scalefree"), bounds(640, 273, 50, 25), text("scale"), colour:0("black"), colour:1("green")
button channel("stopchord_minmax"), bounds(695, 273, 60, 25), text("minmax"), colour:0("black"), colour:1("green")

button channel("Stop_LSYS"), bounds(800, 230, 70, 40), text("Stop_LSYS"), colour:0("black"), colour:1("green")

groupbox bounds(480, 10, 410, 205), colour(75,85,90), plant("plant_lsys"), lineThickness("0"){ 
nslider channel("generations"), bounds(5,5,40,20), range(1, 10, 3, 1, 1), fontSize(14)
label bounds(5,22,40,18), text("gens"), fontSize(12), align("left")

nslider channel("gen_interval"), bounds(60,5,40,20), range(-12, 12, 3, 1, 1), fontSize(14)
label bounds(60,22,50,18), text("interval"), fontSize(12), align("left")

combobox channel("root"), bounds(115,5,40,20), range(0, 3, 0, 1, 1), items("A", "B", "C", "D")
label bounds(115,22,50,18), text("root"), fontSize(12), align("left")

nslider channel("tempo"), bounds(170,5,40,20), range(10, 300, 120, 1, 1), fontSize(14)
label bounds(170,22,50,18), text("tempo"), fontSize(12), align("left")

nslider channel("perc_gen"), bounds(225,5,40,20), range(0, 4, 1, 1, 1), fontSize(14)
label bounds(225,22,60,18), text("perc_gen"), fontSize(12), align("left")

label bounds(345,5,60,18), text("midi chan"), fontSize(12), align("left")
label bounds(325,20,30,18), text("gen 1"), fontSize(12), align("left")
label bounds(325,40,30,18), text("gen 2"), fontSize(12), align("left")
label bounds(325,60,30,18), text("gen 3"), fontSize(12), align("left")
label bounds(325,80,30,18), text("gen 4"), fontSize(12), align("left")
nslider channel("midichan_gen1"), bounds(360,20,40,18), range(1, 16, 1, 1, 1), fontSize(14)
nslider channel("midichan_gen2"), bounds(360,40,40,18), range(1, 16, 2, 1, 1), fontSize(14)
nslider channel("midichan_gen3"), bounds(360,60,40,18), range(1, 16, 3, 1, 1), fontSize(14)
nslider channel("midichan_gen4"), bounds(360,80,40,18), range(1, 16, 4, 1, 1), fontSize(14)
label bounds(300,105,100,18), text("drum map (ch 10)"), fontSize(12), align("left")
label bounds(325,120,30,18), text("A"), fontSize(12), align("left")
label bounds(325,140,30,18), text("B"), fontSize(12), align("left")
label bounds(325,160,30,18), text("C"), fontSize(12), align("left")
label bounds(325,180,30,18), text("D"), fontSize(12), align("left")
nslider channel("drum_map_A"), bounds(360,120,40,18), range(1, 127, 60, 1, 1), fontSize(14)
nslider channel("drum_map_B"), bounds(360,140,40,18), range(1, 127, 61, 1, 1), fontSize(14)
nslider channel("drum_map_C"), bounds(360,160,40,18), range(1, 127, 62, 1, 1), fontSize(14)
nslider channel("drum_map_D"), bounds(360,180,40,18), range(1, 127, 63, 1, 1), fontSize(14)

nslider channel("interval0"), bounds(5,50,40,20), range(-12, 12, -5, 1, 1), fontSize(14)
label bounds(5,72,40,18), text("intv A"), fontSize(12), align("left")
nslider channel("interval1"), bounds(60,50,40,20), range(-12, 12, 3, 1, 1), fontSize(14)
label bounds(60,72,50,18), text("intv B"), fontSize(12), align("left")
nslider channel("interval2"), bounds(115,50,40,20), range(-12, 12, 1, 1, 1), fontSize(14)
label bounds(115,72,50,18), text("intv C"), fontSize(12), align("left")
nslider channel("interval3"), bounds(170,50,40,20), range(-12, 12, 12, 1, 1), fontSize(14)
label bounds(170,72,50,18), text("intv D"), fontSize(12), align("left")

texteditor bounds(5,95,45,20), channel("rule0"), colour("black"), caretColour("white"), fontColour("white"), text("BB")
label bounds(5,117,50,18), text("rule A"), fontSize(12), align("left")
texteditor bounds(60,95,45,20), channel("rule1"), colour("black"), caretColour("white"), fontColour("white"), text("C")
label bounds(60,117,50,18), text("rule B"), fontSize(12), align("left")
texteditor bounds(115,95,45,20), channel("rule2"), colour("black"), caretColour("white"), fontColour("white"), text("A")
label bounds(115,117,50,18), text("rule C"), fontSize(12), align("left")
texteditor bounds(170,95,45,20), channel("rule3"), colour("black"), caretColour("white"), fontColour("white"), text("BB")
label bounds(170,117,50,18), text("rule D"), fontSize(12), align("left")
button channel("print_rules"), bounds(235,95,50,18), text("print rules"), colour:0("green"), colour:1("red"), latched(0)

checkbox channel("no_genZ_interval"), bounds(5,145,15,15), value(1)
label bounds(23,144,130,18), text("no interval for gen zero"), fontSize(12), align("left")
checkbox channel("sibling_interval"), bounds(5,165,15,15), value(1)
label bounds(23,164,130,18), text("interval from sibling"), fontSize(12), align("left")
checkbox channel("root_note_sibling"), bounds(5,185,15,15), value(1)
label bounds(23,184,130,18), text("root_note_sibling"), fontSize(12), align("left")
}

csoundoutput bounds(500, 300, 390, 200)
</Cabbage>
<CsoundSynthesizer>
<CsOptions>
-n -d -m0 -M0 -Q0 -+rtmidi=null 
</CsOptions>
<CsInstruments>

ksmps = 64
nchnls = 16
0dbfs=1

massign -1,102
pgmassign -1, -1

  gknum_faders = 10
  gifadertab_size = 16
  giWaveRaw ftgen 1, 0, gifadertab_size,  7, 0, gifadertab_size, -1 
  giWaveRaw1 ftgen 0, 0, gifadertab_size, -2, 0  ; empty  
  giWaveRaw2 ftgen 0, 0, gifadertab_size, -2, 0  ; empty
  giWaveRaws ftgen 0, 0, 2, -2, giWaveRaw1, giWaveRaw2

  gifine_size = 1024
  giWaveFine ftgen 2, 0, gifine_size,  7, 0, gifine_size, -1 
  giWaveFine1 ftgen 11, 0, gifine_size, -2, 0  ; empty  
  giWaveFine2 ftgen 12, 0, gifine_size, -2, 0  ; empty
  giWaveFines ftgen 0, 0, 2, -2, giWaveFine1, giWaveFine2

  gkXpos[] init 32
  gkXdistance[] init 32
  gkZerocross[] init 32
  gkZerocross_distance[] init 32
  gkFftbins[] init 32
  gkPeaks_x[] init 32

  gihandle OSCinit 9899 ; set the network port number where we will receive OSC data from Python

  ; classic waveforms
	giSine		ftgen	0, 0, 65537, 10, 1					; sine wave
	giCosine	ftgen	0, 0, 8193, 9, 1, 1, 90					; cosine wave
	giTri		ftgen	0, 0, 8193, 7, 0, 2048, 1, 4096, -1, 2048, 0		; triangle wave 

	; grain envelope tables
	giSigmoRise 	ftgen	0, 0, 8193, 19, 0.5, 1, 270, 1				; rising sigmoid
	giSigmoFall 	ftgen	0, 0, 8193, 19, 0.5, 1, 90, 1				; falling sigmoid
	giExpFall	ftgen	0, 0, 8193, 5, 1, 8193, 0.00001				; exponential decay
	giTriangleWin 	ftgen	0, 0, 8193, 7, 0, 4096, 1, 4096, 0			; triangular window 

opcode ButtonEvent, 0, kij
  kbutton, instrnum, iparm xin ; iparm is optional p4
  ktrigon trigger kbutton, 0.5, 0
  ktrigoff trigger kbutton, 0.5, 1
  if ktrigon > 0 then
    event "i", instrnum, 0, -1, iparm
  endif
  if ktrigoff > 0 then
    event "i", -instrnum, 0, .1
  endif
endop

opcode EnvFollow, k, kkk
  kval, krise, kfall xin
  kA = 0.001^(1/(krise*kr))
  kB = 0.001^(1/(kfall*kr))
  kfilt init 0
  kfilt = (kval>kfilt?(kval+(kA*(kfilt-kval))):(kval+(kB*(kfilt-kval))))
  kval = kfilt
  xout kfilt
endop   

opcode MinArrayThresh, k, k[]k
  kArr[],kthresh xin
  kndx init 0
  kmin init 9999999
  while kndx < lenarray(kArr) do
    if kArr[kndx] > kthresh then
      kmin min kArr[kndx], kmin
    endif
    kndx += 1
  od
  xout kmin
endop


instr 1
  ; GUI control
  kwave_raw_on chnget "Wave_raw_on"
  ButtonEvent kwave_raw_on, 10.1, giWaveRaw

  kwave_fine_on chnget "Wave_fine_on"
  ButtonEvent kwave_fine_on, 10.2, giWaveFine

  kwave_raw_detune_on chnget "Wave_raw_detune_on"
  ButtonEvent kwave_raw_detune_on, 11.1, giWaveRaw

  kwave_fine_detune_on chnget "Wave_fine_detune_on"
  ButtonEvent kwave_fine_detune_on, 11.2, giWaveFine

  kdistance_grain_on chnget "Distance_grain"
  ButtonEvent kdistance_grain_on, 12

  kgrain2_on chnget "Grain2"
  ButtonEvent kgrain2_on, 13

  kfft_bank_on chnget "Fft_bank"
  ButtonEvent kfft_bank_on, 16, giWaveRaw

  kfader_bank_on chnget "Fader_bank"
  ButtonEvent kfader_bank_on, 17, giWaveRaw

  knoisebank_on chnget "Noisebank"
  ButtonEvent knoisebank_on, 5

  kstopchord_on chnget "Stopchord"
  ButtonEvent kstopchord_on, 18
  
  kstop_lsys_on chnget "Stop_LSYS"
  ButtonEvent kstop_lsys_on, 20

  kpeaks_on chnget "Peaks_on"

  ; OSC receive
  kOSC_received = 0
  
  kfader_ndx init 0
  kfader_val init 0
  k_num_faders init 0
  ktimethen init 0
  nextmsg_faders:
  kmess OSClisten gihandle, "faders", "fff", kfader_ndx, kfader_val, k_num_faders ; receive OSC data from Python
  kOSC_received += kmess
  if kmess == 0 goto done_faders
  kswitch init 0
  ktab_raw table kswitch, giWaveRaws
  
  tablewkt kfader_val, kfader_ndx, ktab_raw
  if kfader_ndx == k_num_faders-1 then
    kswitch = kswitch == 0 ? 1 : 0
    ;printk2 kswitch, 30
    ktime timeinsts
    kupdate_time limit ktime-ktimethen, 0, 5
    ktimethen = ktime
    event "i", 2, 0, kupdate_time, ktab_raw, k_num_faders
  endif
  kgoto nextmsg_faders 
  done_faders:
  
  knumpeaks init 0
  kavg_x_distance init 0
  kavg_x_movement init 0
  nextmsg_peakstats:
    kmess OSClisten gihandle, "peaks_stats", "fff", knumpeaks, kavg_x_distance, kavg_x_movement
    kOSC_received += kmess
    if kmess == 0 goto done_peakstats
    chnset knumpeaks, "numpeaks"
    chnset kavg_x_distance, "avg_x_distance"
    chnset kavg_x_movement, "avg_x_movement"
    kgoto nextmsg_peakstats
  done_peakstats:
  
  kpeak_id init 0
  kpeak_x init 0
  kpeak_y init 0
  kpeak_amp init 0
  kpeak_movement init 0
  kPeaks_active[] init 100
  kpeak_trig trigger kpeaks_on, 0.5, 0
  
  gkPeaks_x *= 0
  kpeaks_indx = 0
  nextmsg_activepeaks:
    kmess OSClisten gihandle, "active_peaks", "fffff", kpeak_id, kpeak_x, kpeak_y, kpeak_amp, kpeak_movement
    kOSC_received += kmess
    if kmess == 0 goto done_activepeaks
      kpeaks_indx limit kpeaks_indx, 0, 31
      gkPeaks_x[kpeaks_indx] = kpeak_x
      kpeaks_indx += 1
      ;kactive4 active 4
      ;Sactive sprintfk "active_peaks %i instr instances%i", kpeak_id, kactive4
      ;puts Sactive, kpeak_id+1
      kamp = (chnget:k("Amp")-15);+abs(kpeak_y)*10
      kcps = (((kpeak_x/1024)^2)*1600)+100
      kpan = (limit(kpeak_y*8, -1, 1)*0.5)+0.5
      kinstr = 4+(kpeak_id*0.001)
      if kpeaks_on > 0 then
        Samp sprintfk "amp_%f", kinstr
        chnset kamp, Samp
        Scps sprintfk "cps_%f", kinstr
        chnset kcps, Scps
        Span sprintfk "pan_%f", kinstr
        chnset kpan, Span
        ; start instr kun hvis den ikke allerede er i kPeaks_active
        if kPeaks_active[kpeak_id] == 0 then
          kcps_base = gkZerocross_distance[0]
          event "i", kinstr, 0, -1, kcps_base
        endif
        kPeaks_active[kpeak_id] = 1 
      endif
      kgoto nextmsg_activepeaks
  done_activepeaks:

  nextmsg_deletepeaks:
    kmess OSClisten gihandle, "deleted_peaks", "f", kpeak_id 
    kOSC_received += kmess
    if kmess == 0 goto done_deletepeaks
      ;Sdelete sprintfk "delete_peaks %i", kpeak_id
      ;puts Sdelete, kpeak_id+1
      k_active = kPeaks_active[kpeak_id]
      if k_active > 0 then
        kinstr = 4+(kpeak_id*0.001)
        event "i", -kinstr, 0, .1 
        kPeaks_active[kpeak_id] = 0
      endif
      kgoto nextmsg_deletepeaks
  done_deletepeaks:
  
  ; housekeeping, all peaks off
  kpeaks_off trigger kpeaks_on, 0.5, 1
  if kpeaks_off > 0 then
    kindex = 0
    while kindex < lenarray(kPeaks_active) do
      if kPeaks_active[kindex] == 1 then
        kinstr = 4+(kindex*0.001)
        event "i", -kinstr, 0, .1
        kPeaks_active[kindex] = 0 
      endif
      kindex += 1
    od
  endif
 
  kxpos init 0
  kxpos_ndx init 0
  nextmsg_xpos:
    kmess OSClisten gihandle, "xpos", "ff", kxpos_ndx, kxpos
    kOSC_received += kmess
    if kmess == 0 goto done_xpos
    if kxpos_ndx == 0 then
      gkXpos *= 0 ; clear memory on new frame
    endif
    gkXpos[kxpos_ndx] = kxpos
    kgoto nextmsg_xpos
  done_xpos:

  kxdistance init 0
  kxdistance_ndx init 0
  nextmsg_xdistance:
    kmess OSClisten gihandle, "xdistance", "ff", kxdistance_ndx, kxdistance
    kOSC_received += kmess
    if kmess == 0 goto done_xdistance
    if kxdistance_ndx == 0 then
      gkXdistance *= 0 ; clear memory on new frame
    endif
    gkXdistance[kxdistance_ndx] = kxdistance
    kgoto nextmsg_xdistance
  done_xdistance:

  kzerocross init 0
  kzerocross_ndx init 0
  nextmsg_zerocross:
    kmess OSClisten gihandle, "zerocross", "ff", kzerocross_ndx, kzerocross
    kOSC_received += kmess
    if kmess == 0 goto done_zerocross
    if kzerocross_ndx == 0 then
      gkZerocross *= 0 ; clear memory on new frame
    endif
    gkZerocross[kzerocross_ndx] = kzerocross
    kgoto nextmsg_zerocross
  done_zerocross:

  kzerocross_distance init 0
  kzerocross_distance_ndx init 0
  nextmsg_zerocross_distance:
    kmess OSClisten gihandle, "zerocross_distance", "ff", kzerocross_distance_ndx, kzerocross_distance
    kOSC_received += kmess
    if kmess == 0 goto done_zerocross_distance
    if kzerocross_distance_ndx == 0 then
      gkZerocross_distance *= 0 ; clear memory on new frame
    endif
    gkZerocross_distance[kzerocross_distance_ndx] = kzerocross_distance
    kgoto nextmsg_zerocross_distance
  done_zerocross_distance:

  kfft_bin init 0
  kfft_bin_ndx init 0
  nextmsg_fft:
    kmess OSClisten gihandle, "fft_bin", "ff", kfft_bin_ndx, kfft_bin
    kOSC_received += kmess
    if kmess == 0 goto done_fft
    if kfft_bin_ndx == 0 then
      gkFftbins *= 0 ; clear memory on new frame
    endif
    gkFftbins[kfft_bin_ndx] = kfft_bin
    kgoto nextmsg_fft
  done_fft:

  kwave_activity init 0
  nextmsg_activity:
    kmess OSClisten gihandle, "activity", "f", kwave_activity
    kOSC_received += kmess
    if kmess == 0 goto done_activity
      chnset kwave_activity, "wave_activity"
    kgoto nextmsg_activity
  done_activity:

  Soscreceived = "OK OSC received"
  kOSC_received limit kOSC_received, 0, 1
  puts Soscreceived, kOSC_received

endin


instr 2
  ;print p3
  itab = p4
  inum_faders = p5
  ;print p2, p3, p4
  if itab == giWaveRaw2 then
    kndx line 0, p3-1/kr, 1
  else 
    kndx line 1, p3-1/kr, 0
  endif
  
  gifine_size = 1024
  istepsize = floor(gifine_size/(inum_faders+1))
  ilaststep = gifine_size-(istepsize*inum_faders)
  giWaveFine1 ftgen 11, 0, gifine_size, 6, 0, istepsize,  table(0,giWaveRaw1),\
                                              istepsize,  table(1,giWaveRaw1),\
                                              istepsize,  table(2,giWaveRaw1),\
                                              istepsize,  table(3,giWaveRaw1),\
                                              istepsize,  table(4,giWaveRaw1),\
                                              istepsize,  table(5,giWaveRaw1),\
                                              istepsize,  table(6,giWaveRaw1),\
                                              istepsize,  table(7,giWaveRaw1),\
                                              istepsize,  table(8,giWaveRaw1),\
                                              istepsize,  table(9,giWaveRaw1),\
                                              ilaststep,  0
  giWaveFine2 ftgen 12, 0, gifine_size, 6, 0, istepsize,  table(0,giWaveRaw2),\
                                              istepsize,  table(1,giWaveRaw2),\
                                              istepsize,  table(2,giWaveRaw2),\
                                              istepsize,  table(3,giWaveRaw2),\
                                              istepsize,  table(4,giWaveRaw2),\
                                              istepsize,  table(5,giWaveRaw2),\
                                              istepsize,  table(6,giWaveRaw2),\
                                              istepsize,  table(7,giWaveRaw2),\
                                              istepsize,  table(8,giWaveRaw2),\
                                              istepsize,  table(9,giWaveRaw2),\
                                              ilaststep,  0
  ftmorf kndx, giWaveRaws, giWaveRaw
  ftmorf kndx, giWaveFines, giWaveFine
  event_i "i", 3, p3, 1/kr, inum_faders
endin

instr 3
  ;print table(512,giWaveFine)
  ;cabbageSet "wave_raw", "tableNumber", 1; update table display
  ;cabbageSet "wave_fine", "tableNumber", 2; update table display
endin

instr 4
  ; peaks sine cluster
  Samp sprintf "amp_%f", p1
  kamp chnget Samp
  Scps sprintf "cps_%f", p1
  kcps chnget Scps
  ;kcps tonek kcps, 10
  Span sprintf "pan_%f", p1
  kpan chnget Span
  kpan tonek kpan, 10
  
  icps = (p4*300)+500
  kcps1 = icps + (kcps*0.2)
  ;puts Samp, 1
  ;printk2 kamp, frac(p1)*2
  ;printk2 kcps, frac(p1)*2
  apan butterlp interp(kpan), 8
  amp linsegr 0, 0.5, 1, 3, 0
  ;amp transegr 0, 0.2, 2, 1, 1, 0, 1, 0.5, 2, 0
  a1 poscil ampdbfs(kamp)*amp, kcps1, -1, -1
  aL = a1*sqrt(1-apan)
  aR = a1*sqrt(apan)
  outs aL, aR
endin

instr 5
  ; noisechord
  ibasenote = 48
  iNotes[] fillarray 0,3,5,7,10
  knumpeaks chnget "numpeaks"
  kavg_x_distance chnget "avg_x_distance"
  kavg_x_movement chnget "avg_x_movement"
  kwave_activity chnget "wave_activity"
  anois rnd31, 1, 1
  ifq1 = cpsmidinn(ibasenote+iNotes[0])
  ifq2 = cpsmidinn(ibasenote+iNotes[1])
  ifq3 = cpsmidinn(ibasenote+iNotes[2])
  ifq4 = cpsmidinn(ibasenote+iNotes[3])
  ifq5 = cpsmidinn(ibasenote+iNotes[4])
  a1 butterbp anois, ifq1, ifq1*0.1
  a2 butterbp anois, ifq2, ifq2*0.1
  a3 butterbp anois, ifq3, ifq3*0.1
  a4 butterbp anois, ifq4, ifq4*0.1
  a5 butterbp anois, ifq5, ifq5*0.1
  iampcurve ftgentmp 0, 0, 1024, 7, 0,171,1,170,0,683,0 ; segm length 1024/6, 6 segments for 5-source fade
  kphasor_freq = (kavg_x_movement/100)*-1
  ;printk2 kphasor_freq
  amp_ndx phasor kphasor_freq
  ;amp_ndx pow amp_ndx, 3
  amp1 table amp_ndx, iampcurve, 1, 0, 1
  amp2 table amp_ndx, iampcurve, 1, 0.2, 1
  amp3 table amp_ndx, iampcurve, 1, 0.4, 1
  amp4 table amp_ndx, iampcurve, 1, 0.6, 1
  amp5 table amp_ndx, iampcurve, 1, 0.8, 1
  asum sum a1*amp1,a2*amp2,a3*amp3,a4*amp4,a5*amp5
  asum *= kwave_activity
  outs asum, asum

endin

instr 10
  ; hsb oscil waveshaped by rope wave
  itab = p4
  print itab
  kfreq chnget "Freq_wav"
  kfreq *= 0.5
  knumpeaks chnget "numpeaks"
  kavg_x_movement chnget "avg_x_movement"
  kdetune chnget "detune_wav"
  ktone = 0.5+(kavg_x_movement*kdetune)
  kbrite = tonek(knumpeaks, 1)
  ioctfn ftgentmp 0, 0, 1024, -19, 1, 0.5, 270, 0.5
  kamp_dB chnget "Amp_wav"
  kamp = ampdbfs(kamp_dB)
  ;a1 poscil kamp, kfreq
  if changed(kfreq) > 0 then
    reinit generator
  endif
  generator:
  ibasfreq = i(kfreq)
  a1L hsboscil kamp, 0.5, kbrite, ibasfreq, giSine, ioctfn
  a1R hsboscil kamp, ktone, kbrite, ibasfreq, giSine, ioctfn
  icenter = 10/16
  a2L tablei a1L*icenter, itab, 1, icenter, 0 ;
  a2R tablei a1R*icenter, itab, 1, icenter, 0 ;
  a2L dcblock a2L ; prevent constant offset
  a2R dcblock a2R ; prevent constant offset
  a2L *= kamp
  a2R *= kamp
  outch 1, a2L*0.3, 2, a2R*0.3
endin

instr 11
  ; detuned sine oscil waveshaped by rope wave
  itab = p4
  print itab
  kfreq chnget "Freq_wavd"
  ;kx_dist = gkZerocross_distance[0]
  ;kfreq *= kx_dist
  kavg_x_movement chnget "avg_x_movement"
  ;kfreq *= (1+kavg_x_movement)
  knumpeaks chnget "numpeaks"
  kdetune chnget "detune_wavd"
  ;kdetune *= kavg_x_movement
  kfreq1 = kfreq+kfreq*(tonek(knumpeaks+1,2))*kdetune
  kfreq2 = kfreq-kfreq*(tonek(knumpeaks+1,0.7))*kdetune
  kamp_dB chnget "Amp_wavd"
  kamp = ampdbfs(kamp_dB)
  a10 poscil kamp, kfreq
  a11 poscil kamp, kfreq1
  a12 poscil kamp, kfreq2
  a1 sum a10,a11,a12
  a1L = (a10+a11)*0.5
  a1R = (a10+a12)*0.5
  a1 *= 0.33
  if itab = 1 then
    icenter = 10/16
  else
    icenter = 0.5
  endif
  a2 tablei a1*icenter, itab, 1, icenter, 0 ;
  a2L tablei a1L*icenter, itab, 1, icenter, 0 ;
  a2R tablei a1R*icenter, itab, 1, icenter, 0 ;
  a2 dcblock a2 ; prevent constant offset
  a2L dcblock a2L ; prevent constant offset
  a2R dcblock a2R ; prevent constant offset
  aleft = a2*0.1+a2L*0.9
  aright = a2*0.1+a2R*0.9
  aleft lpf18 aleft, 100+(tonek(knumpeaks+1,2)*600), 0.3, 0.9
  aright lpf18 aright, 100+(tonek(knumpeaks+1,2)*600), 0.3, 0.9
  outch 3, aleft*0.15, 4, aright*0.15
endin

opcode DistanceGrains, a, k[]kkkkkkkKkiii
  kDistance[], kwavfreq, kgrainrate, kdist_rate, kvoice_spread, kgraindur, kamp_thresh, kamp_env, ktranspose, kchan, ivoice, imaxvoice, iopcode_id xin
  kamp = kDistance[ivoice] > 0 ? 1 : 0
  kamp tonek kamp, 1  

  ; grain rate
  kgrainrate tonek kgrainrate*(1+kDistance[ivoice]*kdist_rate), 1
  async = 0

; grain rate FM
  kGrFmFratio = 1;    chnget "GrFmRatio"
	kGrFmFreq	divz kgrainrate, kGrFmFratio, 1	        ; FM freq for modulating the grainrate 
	kGrFmIndex = 0; chnget "GrFmIndx"      		        ; FM index for modulating the grainrate (normally kept in a 0.0 to 1.0 range)
	iGrFmWave	= giSine				; FM waveform, for modulating the grainrate 
	aGrFmSig	oscil kGrFmIndex, kGrFmFreq, iGrFmWave	; audio signal for frequency modulation of grain rate
	agrainrate	= kgrainrate + (aGrFmSig*kgrainrate)	; add the modulator signal to the grain rate signal

; distribution 
	kdistribution	= 0; chnget "Distribution"			; grain random distribution in time
	idisttab	ftgentmp	0, 0, 16, 16, 1, 16, -10, 0	; probability distribution for random grain masking

; grain shape
	kduration	= divz(1,kgrainrate,1)*kgraindur*1000; 0.5; chnget "Graindur"		

	ienv_attack	= giSigmoRise 			; grain attack shape (from table)
	ienv_decay	= giSigmoFall 			; grain decay shape (from table)
	ksustain_amount	= 0.0					  ; balance between enveloped time(attack+decay) and sustain level time, 0.0 = no time at sustain level
	ka_d_ratio = 0.1;     chnget "Attack"					; balance between attack time and decay time, 0.0 = zero attack time and full decay time
	kenv2amt = 0                    ; amount of secondary enveloping per grain (e.g. for fof synthesis)
	ienv2tab	= giExpFall 				  ; secondary grain shape (from table), enveloping the whole grain if used

; select source waveforms
	kwaveform	= giSine		; source audio waveform 

; original pitch for each waveform, use if they should be transposed individually
; can also be used as a "cycles per second" parameter for single cycle waveforms (assuming that the kwavfreq parameter has a value of 1.0)
	kwavekey1	= 1; chnget "Grainkey1"
	kwavekey2	= 1;chnget "Grainkey2"
	kwavekey3	= 1;chnget "Grainkey3"
	kwavekey4	= 1;chnget "Grainkey4"
	asamplepos	= 0				

; "master" grain pitch (transpose for all 4 source waveforms)
	kwavfreq	= kwavfreq*semitone(ivoice*kvoice_spread)					; transposition factor (playback speed) of audio inside grains, 
  
; pitch sweep
	ksweepshape		= 0.5						; grain wave pitch sweep shape (sweep speed), 0.5 is linear sweep
	iwavfreqstarttab 	ftgentmp	0, 0, 16, -2, 0, 0,   1		; start freq scalers, per grain
	iwavfreqendtab		ftgentmp	0, 0, 16, -2, 0, 0,   1		; end freq scalers, per grain

; FM of grain pitch (playback speed)
	kPtchFmFreq	= 1; chnget "FmFreq"						; FM freq, modulating waveform pitch
	kPtchFmIndex = 0; chnget "FmIndx"						; FM index, modulating waveform pitch
	iPtchFmWave	= giSine						; FM waveform, modulating waveform pitch
	ifmamptab	ftgentmp	0, 0, 16, -2, 0, 0,   1			; FM index scalers, per grain
	ifmenv = -1 					                ; FM index envelope, over each grain (from table)
	kPtchFmIndex = kPtchFmIndex + (kPtchFmIndex*kPtchFmFreq*0.00001) 	; FM index scaling formula
	awavfm oscil	kPtchFmIndex, kPtchFmFreq, iPtchFmWave		; Modulator signal for frequency modulation inside grain

; trainlet parameters
	icosine	= giCosine				; needs to be a cosine wave to create trainlets
  kTrainCpsMult = 1;   chnget "TrCpsMult"                     ; multiplier for  trainlet cps relative to grain rate
	kTrainCps	= kTrainCpsMult*kgrainrate		
	knumpartials= 1;	chnget "TrainPart"					; number of partials in trainlet
	kchroma = 1; chnget "TrainChroma"					; chroma, falloff of partial amplitude towards sr/2

	; gain masking table, amplitude for individual grains
	igainmasks	ftgentmp	0, 0, 16, -2, 0, 0, 1

	; channel masking table, output routing for individual grains (zero based, a value of 0.0 routes to output 1)
	ichanmasks	ftgentmp	0, 0, 16, -2,  0, 0,  0.5
	
	; random masking (muting) of individual grains
	krandommask	=0;chnget "RandMask"

	; wave mix masking. 
  iwaveamptab	ftgentmp 0, 0, 32, -2,   0, 0,  1,0,0,0,0
	ktrainbal = 0; chnget "TrainBal"
	ktrainvol = sqrt(ktrainbal)
	ksinevol = sqrt(1-ktrainbal)*0.25
  tablew ktrainvol, 6, iwaveamptab
  tablew ksinevol, 5, iwaveamptab
  tablew ksinevol, 4, iwaveamptab
  tablew ksinevol, 3, iwaveamptab
  tablew ksinevol, 2, iwaveamptab
; system parameter
	imax_grains	= 100				; max number of grains per k-period
  iopcode_id += 1
  print iopcode_id
        
	a1,a2,a3,a4,a5,a6,a7,a8	partikkel \					; 					
			agrainrate, \						; grains per second			
			kdistribution, idisttab, async, \			; synchronous/asynchronous		
			kenv2amt, ienv2tab, ienv_attack, ienv_decay, \		; grain envelope (advanced)		
			ksustain_amount, ka_d_ratio, kduration, \		; grain envelope 			
			kamp, \							; amp					
			igainmasks, \						; gain masks (advanced)			
			kwavfreq, \						; grain pitch (playback frequency)	
			ksweepshape, iwavfreqstarttab, iwavfreqendtab, \	; grain pith sweeps (advanced)		
			awavfm, ifmamptab, ifmenv, \				; grain pitch FM (advanced)		
			icosine, kTrainCps, knumpartials, kchroma, \		; trainlets				
			ichanmasks, \ 					        ; channel mask (advanced)
			krandommask, \						; random masking of single grains	
			kwaveform, kwaveform, kwaveform, kwaveform, \	; set source waveforms, all set to the live input buffer here
			iwaveamptab, \						; mix source waveforms (remember, we can use different samplepos and transposition for each)
			asamplepos, asamplepos, asamplepos, asamplepos, \	; read position for source waves	
			kwavekey1, kwavekey2, kwavekey3, kwavekey4, \		; individual transpose for each source
			imax_grains, iopcode_id						; system parameter (advanced)
  
  ; midi out
  apulse, aphase partikkelsync iopcode_id
  kSig[] init ksmps
  kSig shiftin apulse
  kpulse = sumarray(kSig) 
  ;Sdebug sprintfk "partikkel %i amp %f pulse %f", iopcode_id, kamp, kpulse
  ;puts Sdebug, kamp+kpulse+1
  kphase downsamp aphase
  if (kpulse > 0) && (kamp_env*kamp > kamp_thresh) then
    knote = (kwavfreq*12)+48
    knote = 12*log2(kwavfreq/440) + 69 + ktranspose
    kvel = 90
    event "i", 202, 0, kgraindur, kvel, knote, kchan
  endif

  if (ivoice < imaxvoice-1) then
    a1 += DistanceGrains(kDistance, kwavfreq, kgrainrate, kdist_rate, kvoice_spread, kgraindur, kamp_thresh, kamp_env, ktranspose, kchan, ivoice+1, imaxvoice, iopcode_id)
  endif
  iampscale = 1/imaxvoice
  xout(a1*iampscale)
endop


instr 12
  ; grain rhythm detuned by peak distances
  kwavfreq chnget "Grainpitch"
  kamp_dB chnget "Grainamp"
  kgrainrate chnget "Grate"
  kx_dist chnget "avg_x_distance"
  kgrainrate *= limit(1-(kx_dist)*2, 0.1, 1)
  kgraindur chnget "Gdur"
  kamp = ampdbfs(kamp_dB)
  kactivity chnget "wave_activity"
  kactivity limit kactivity, 0, 1
  kamp_env EnvFollow kactivity, 0.01, 3
  kamp *= kamp_env
  knumpeaks chnget "numpeaks"
  kwavfreq *= (knumpeaks+1)
  kdist_rate chnget "G_dist_rate"
  kvoice_spread chnget "G_voice_spread"
  kmidi_amp_thresh chnget "distgrains_ampthresh"
  kmidi_amp_thresh ampdbfs kmidi_amp_thresh
  kmidi_transpose chnget "distgrains_transpose"
  kmidi_chan chnget "distgrains_midichan"
  imaxvoice = 5
  iopcode_id1 = 1
  iopcode_id2 = 10  
  a1 DistanceGrains gkXdistance, kwavfreq, kgrainrate, kdist_rate, kvoice_spread, kgraindur, kmidi_amp_thresh, kamp_env, kmidi_transpose, kmidi_chan, 0, imaxvoice, iopcode_id1
  ;a2 DistanceGrains gkZerocross_distance, kwavfreq, kgrainrate, kdist_rate, kvoice_spread, kgraindur, 0, imaxvoice, iopcode_id2
  outch 9, a1*kamp*3, 10, a1*kamp*3
endin

opcode Graincloud, aa, kkkkkkkii
  kwavfreq, kpitchmod, kpitch_spread, kgrainrate, kratemod, kdistribution, kgraindur, ivoice, imaxvoice xin
  kamp = 1

  ; grain rate
  kgrainrate = kgrainrate*(1+(rspline(-0.5, 1, 0.5, 2)*kratemod))
  async = 0

; grain rate FM
  kGrFmFratio = 1;    chnget "GrFmRatio"
	kGrFmFreq	divz kgrainrate, kGrFmFratio, 1	        ; FM freq for modulating the grainrate 
	kGrFmIndex = 0; chnget "GrFmIndx"      		        ; FM index for modulating the grainrate (normally kept in a 0.0 to 1.0 range)
	iGrFmWave	= giSine				; FM waveform, for modulating the grainrate 
	aGrFmSig	oscil kGrFmIndex, kGrFmFreq, iGrFmWave	; audio signal for frequency modulation of grain rate
	agrainrate	= kgrainrate + (aGrFmSig*kgrainrate)	; add the modulator signal to the grain rate signal

; distribution 
	;kdistribution	= 0; chnget "Distribution"			; grain random distribution in time
	idisttab	ftgentmp	0, 0, 16, 16, 1, 16, -10, 0	; probability distribution for random grain masking

; grain shape
	kduration	= divz(1,kgrainrate,1)*kgraindur*1000; 0.5; chnget "Graindur"		

	ienv_attack	= giSigmoRise 			; grain attack shape (from table)
	ienv_decay	= giSigmoFall 			; grain decay shape (from table)
	ksustain_amount	= 0.0					  ; balance between enveloped time(attack+decay) and sustain level time, 0.0 = no time at sustain level
	ka_d_ratio = 0.1;     chnget "Attack"					; balance between attack time and decay time, 0.0 = zero attack time and full decay time
	kenv2amt = 0                    ; amount of secondary enveloping per grain (e.g. for fof synthesis)
	ienv2tab	= giExpFall 				  ; secondary grain shape (from table), enveloping the whole grain if used

; select source waveforms
	kwaveform	= giSine		; source audio waveform 

; original pitch for each waveform, use if they should be transposed individually
; can also be used as a "cycles per second" parameter for single cycle waveforms (assuming that the kwavfreq parameter has a value of 1.0)
	kwavekey1	= 1; chnget "Grainkey1"
	kwavekey2	= 1;chnget "Grainkey2"
	kwavekey3	= 1;chnget "Grainkey3"
	kwavekey4	= 1;chnget "Grainkey4"
	asamplepos	= 0				

; "master" grain pitch (transpose for all 4 source waveforms)
	kwavfreq	= kwavfreq*(1+(rspline(-0.5, 1, 0.5, 2)*kpitchmod))*(1+(ivoice*kpitch_spread))				; transposition factor (playback speed) of audio inside grains, 

; pitch sweep
	ksweepshape		= 0.5						; grain wave pitch sweep shape (sweep speed), 0.5 is linear sweep
	iwavfreqstarttab 	ftgentmp	0, 0, 16, -2, 0, 0,   1		; start freq scalers, per grain
	iwavfreqendtab		ftgentmp	0, 0, 16, -2, 0, 0,   1		; end freq scalers, per grain

; FM of grain pitch (playback speed)
	kPtchFmFreq	= 1; chnget "FmFreq"						; FM freq, modulating waveform pitch
	kPtchFmIndex = 0; chnget "FmIndx"						; FM index, modulating waveform pitch
	iPtchFmWave	= giSine						; FM waveform, modulating waveform pitch
	ifmamptab	ftgentmp	0, 0, 16, -2, 0, 0,   1			; FM index scalers, per grain
	ifmenv = -1 					                ; FM index envelope, over each grain (from table)
	kPtchFmIndex = kPtchFmIndex + (kPtchFmIndex*kPtchFmFreq*0.00001) 	; FM index scaling formula
	awavfm oscil	kPtchFmIndex, kPtchFmFreq, iPtchFmWave		; Modulator signal for frequency modulation inside grain

; trainlet parameters
	icosine	= giCosine				; needs to be a cosine wave to create trainlets
  kTrainCpsMult = 1;   chnget "TrCpsMult"                     ; multiplier for  trainlet cps relative to grain rate
	kTrainCps	= kTrainCpsMult*kgrainrate		
	knumpartials= 1;	chnget "TrainPart"					; number of partials in trainlet
	kchroma = 1; chnget "TrainChroma"					; chroma, falloff of partial amplitude towards sr/2

	; gain masking table, amplitude for individual grains
	igainmasks	ftgentmp	0, 0, 16, -2, 0, 0, 1

	; channel masking table, output routing for individual grains (zero based, a value of 0.0 routes to output 1)
	ichanmasks	ftgentmp	0, 0, 16, -2,  0, 1,  0, 1
	
	; random masking (muting) of individual grains
	krandommask	=0;chnget "RandMask"

	; wave mix masking. 
  iwaveamptab	ftgentmp 0, 0, 32, -2,   0, 0,  1,0,0,0,0
	ktrainbal = 0; chnget "TrainBal"
	ktrainvol = sqrt(ktrainbal)
	ksinevol = sqrt(1-ktrainbal)*0.25
  tablew ktrainvol, 6, iwaveamptab
  tablew ksinevol, 5, iwaveamptab
  tablew ksinevol, 4, iwaveamptab
  tablew ksinevol, 3, iwaveamptab
  tablew ksinevol, 2, iwaveamptab
; system parameter
	imax_grains	= 100				; max number of grains per k-period
        
	a1,a2	partikkel \					; 					
			agrainrate, \						; grains per second			
			kdistribution, idisttab, async, \			; synchronous/asynchronous		
			kenv2amt, ienv2tab, ienv_attack, ienv_decay, \		; grain envelope (advanced)		
			ksustain_amount, ka_d_ratio, kduration, \		; grain envelope 			
			kamp, \							; amp					
			igainmasks, \						; gain masks (advanced)			
			kwavfreq, \						; grain pitch (playback frequency)	
			ksweepshape, iwavfreqstarttab, iwavfreqendtab, \	; grain pith sweeps (advanced)		
			awavfm, ifmamptab, ifmenv, \				; grain pitch FM (advanced)		
			icosine, kTrainCps, knumpartials, kchroma, \		; trainlets				
			ichanmasks, \ 					        ; channel mask (advanced)
			krandommask, \						; random masking of single grains	
			kwaveform, kwaveform, kwaveform, kwaveform, \	; set source waveforms, all set to the live input buffer here
			iwaveamptab, \						; mix source waveforms (remember, we can use different samplepos and transposition for each)
			asamplepos, asamplepos, asamplepos, asamplepos, \	; read position for source waves	
			kwavekey1, kwavekey2, kwavekey3, kwavekey4, \		; individual transpose for each source
			imax_grains						; system parameter (advanced)

  if (ivoice < imaxvoice-1) then
    a1a, a2a Graincloud kwavfreq, kpitchmod, kpitch_spread, kgrainrate, kratemod, kdistribution, kgraindur, ivoice+1, imaxvoice
    a1 += a1a
    a2 += a2a
  endif
  iampscale = 1/(imaxvoice^0.5)
  xout(a1*iampscale, a2*iampscale)
endop

instr 13
  ; async grain cloud
  kFaders[] tab2array giWaveRaw1
  kminfaders minarray kFaders
  kmaxfaders maxarray kFaders
  kavg_x_movement chnget "avg_x_movement"
  kactivity chnget "wave_activity"
  kactivity limit kactivity, 0, 1
  amp_activity follow2 a(kactivity), 0.1, 4
  kwavfreq chnget "Grainpitch2"
  kamp_dB chnget "Grainamp2"
  kgrainrate chnget "Grate2"
  kgraindur chnget "Gdur2"
  kamp = ampdbfs(kamp_dB)  
  imaxvoice = 8
  kactivity_mod EnvFollow kactivity, 5, 1
  kpitchmod chnget "G2_pitchmod"
  kpitchmod *= 1+(kactivity_mod*3)
  kwavfreq *= 1+(kactivity_mod*2)
  kpitch_spread chnget "G2_pitch_spread"
  kratemod chnget "G2_ratemod"
  knumpeaks chnget "numpeaks"
  ; mod mapping
  kamp *= amp_activity
  kdistribution = knumpeaks/7
  kgrainrate *= (1+(kavg_x_movement*2.5))
  kpitch_spread *= kmaxfaders
  kgraindur *= (kminfaders+1)
  a1,a2 Graincloud kwavfreq, kpitchmod, kpitch_spread, kgrainrate, kratemod, kdistribution, kgraindur, 0, imaxvoice
  outch 11, a1*kamp*1.5, 12, a2*kamp*1.5
endin

opcode OscBank, aa, k[]i[]kkkii
  kAmps[], iPitches[], kbasefreq, kchroma, kdetune, ivoice, imaxvoice xin
  if kchroma > 0 then
    kamp = kAmps[ivoice] * (1+((ivoice+1)*kchroma))
  else
    kamp = kAmps[ivoice] + abs(kchroma)
  endif
  ;printk2 kamp, ivoice*2
  kamp tonek kamp, 1  
  kcps = kbasefreq*semitone(iPitches[ivoice])
  kcps = kcps+(kcps*rspline(-kdetune, kdetune, 0.3, 0.9))
  a1 poscil kamp, kcps
  ipan = ivoice/(imaxvoice-1)
  aL = a1*sqrt(1-ipan)
  aR = a1*sqrt(ipan)
  if (ivoice < imaxvoice-1) then
    aLa,aRa OscBank kAmps, iPitches, kbasefreq, kchroma, kdetune, ivoice+1, imaxvoice
    aL += aLa
    aR += aRa
  endif
  xout(aL, aR)
endop

instr 16
  ; oscillator bank, tuned to (penta)scale, mix by 8 first fft bins
  itab = p4
  iPitches[] fillarray 0, 0, 3, 5, 7, 10, 12, 15, 17, 19, 22, 24
  kfreq chnget "Freq_fft"
  kamp_dB chnget "Amp_fft"
  kamp = ampdbfs(kamp_dB)
  kchroma chnget "chroma_fft"
  kdetune chnget "detune_fft"
  kdist chnget "dist_fft"
  imaxvoice = 8
  aL,aR OscBank gkFftbins, iPitches, kfreq, kchroma, kdetune, 1, imaxvoice; start at 1, skipping the DC fft bin
  ;a1 = (tanh(a1)/imaxvoice)*kamp
  aL = aL/imaxvoice
  aR = aR/imaxvoice
  krandfq_flo rspline 0.3,0.6, 0.2, 0.7
  klfo oscil 0.5, krandfq_flo
  klfo += 0.5
  a3L lpf18 aL, 1000+(klfo*400), 0.2, kdist*4
  a3R lpf18 aR, 1000-(klfo*400), 0.2, kdist*4
  outch 5, a3L*kamp, 6, a3R*kamp
endin


instr 17
  ; oscillator bank, tuned to (penta)scale, mix rope fader values
  itab = p4
  iPitches[] fillarray 0, 0, 3, 5, 7, 10, 12, 15, 17, 19, 22, 24
  kFaders[] tab2array giWaveRaw1
  kFaders = kFaders-(sumarray(kFaders)/lenarray(kFaders)) ; center
  kFaders limit kFaders, 0.001, 1
  kFaders -= 0.001
  kFaders = (kFaders^2)*10
  krise = 0.01
  kfall = 3
  kFaders[0] EnvFollow kFaders[0], krise, kfall  
  kFaders[1] EnvFollow kFaders[1], krise, kfall  
  kFaders[2] EnvFollow kFaders[2], krise, kfall  
  kFaders[3] EnvFollow kFaders[3], krise, kfall  
  kFaders[4] EnvFollow kFaders[4], krise, kfall  
  kFaders[5] EnvFollow kFaders[5], krise, kfall  
  kFaders[6] EnvFollow kFaders[6], krise, kfall  
  kFaders[7] EnvFollow kFaders[7], krise, kfall  
  kFaders[8] EnvFollow kFaders[8], krise, kfall  
  kFaders[9] EnvFollow kFaders[9], krise, kfall  
  ;kFaders += 10 ; now it is unipolar
  ;kmin1 minarray kFaders
  ;kmax1 maxarray kFaders
  ;kFaders = (kFaders-kmin1);*divz(1,(kmax1-kmin1),1)
  ;kFaders = (kFaders^2);*kmax1
  
  kmin minarray kFaders
  kmax maxarray kFaders
  ;kprint metro 1
  ;if kprint > 0 then
  ;  ;printarray(kFaders)
  ;  printk2 kmin, 5
  ;  printk2 kmax, 10
  ;endif
  ;kmin1 = minarray(kFaders)
  ;kmax1 = maxarray(kFaders)
  kfreq chnget "Freq_fadr"
  kamp_dB chnget "Amp_fadr"
  kamp = ampdbfs(kamp_dB)
  kdetune chnget "detune_fadr"
  kchroma chnget "chroma_fadr"
  kdist chnget "dist_fadr"
  imaxvoice = 10
  aL,aR OscBank kFaders, iPitches, kfreq, kchroma, kdetune, 0, imaxvoice
  aL = aL/imaxvoice
  aR = aR/imaxvoice
  krandfq_flo rspline 0.3,0.6, 0.2, 0.7
  klfo oscil 0.5, krandfq_flo
  klfo += 0.5
  a3L lpf18 aL, 1000+(klfo*400), 0.2, kdist*4
  a3R lpf18 aR, 1000-(klfo*400), 0.2, kdist*4
  outch 7, a3L*kamp, 8, a3R*kamp
endin


instr 18
  ; stopchord control
  kwave_activity chnget "wave_activity"
  kwave_activity tonek kwave_activity, 1
  kmax_activity init 0
  kmax_activity max kmax_activity, kwave_activity
  kwa_diff diff kwave_activity
  kactivity_thresh chnget "stop_activity_thresh"

  ksig = (kwa_diff < 0) && (kwave_activity < 0.1) && (kmax_activity > kactivity_thresh) ? 1 : 0
  ktrig trigger ksig, 0.5, 0
  
  kmax_x maxarray gkXpos
  kmin_x MinArrayThresh gkXpos, 0
  kmax_z maxarray gkZerocross
  kmin_z MinArrayThresh gkZerocross, 0
  kmaxpeak_x maxarray gkPeaks_x
  kminpeak_x MinArrayThresh gkPeaks_x, 04
  knumpeaks chnget "numpeaks"
  kavg_xpos divz sumarray(gkXpos), knumpeaks, 0.2

  ; selec1 min or max
  kminmax chnget "stopchord_minmax"
  if kminmax > 0 then
    kcps1 delayk kmax_x*0.8, 1
    kcps2 delayk kmax_z*0.8, 1
    kcps3 delayk kmaxpeak_x*0.8, 1
  else
    kcps1 delayk kmin_x, 1
    kcps2 delayk kmin_z, 1
    kcps3 delayk kminpeak_x, 1
  endif
  ; select scale or free
  kscalefree chnget "stopchord_scalefree"
  if ktrig > 0 then
    event "i", 19, 0.2+kavg_xpos, 0.2+kmax_activity, kcps1, kcps2, kcps3, kscalefree
    kmax_activity = 0
  endif 

endin

instr 19
  ; stopchord tone gen
  iscalefree = p7
  iScale[] fillarray 0, 3, 5, 7, 10, 12, 15, 17, 19, 22, 24, 27, 29, 31, 34, 36
  ilenscale lenarray iScale
  if iscalefree > 0 then
    ibasefreq = 220
    icps1 = ibasefreq*semitone(iScale[int(limit(p4*ilenscale-1, 0, ilenscale-1))])
    icps2 = ibasefreq*semitone(iScale[int(limit(p5*ilenscale-1, 0, ilenscale-1))])
    icps3 = ibasefreq*semitone(iScale[int(limit(p6*ilenscale-1, 0, ilenscale-1))])
  else
    icps1 = limit(p4* 400,100, 2000)
    icps2 = limit(p5*1100,100, 2000)
    icps3 = limit(p6*1800,100, 2000)
  endif
  ;print icps1, icps2, icps3
  iamp = ampdbfs(chnget("amp_stopchord"))
  ; random envelope both attack and release
  aenv1   linsegr 0, random(0.05,0.4),   1, 0.1, 0.2, random(0.3,0.5), 0.6, random(2,3.5), 0.01
  aenv2   linsegr 0, random(0.01,0.16), 1, 0.1, 0.2, random(0.3,0.5), 0.6, random(1.8,2.8), 0.01
  aenv3   linsegr 0, random(0.001,0.1), 1, 0.1, 0.2, random(0.3,0.5), 0.6, random(1.4,4.3), 0.01
  amodenv linsegr 1, random(0.01,0.05), 0.1, 1, 0.01, 0.3, 0.01
  kdetune chnget "detune_stopchord"
  kdetune *= 0.1
  kcps1a rspline icps1-(icps1*kdetune), icps1+(icps1*kdetune), 0.25, 0.8
  kcps2a rspline icps2-(icps2*kdetune), icps2+(icps2*kdetune), 0.25, 0.8
  kcps3a rspline icps3-(icps3*kdetune), icps3+(icps3*kdetune), 0.25, 0.8
  kcps1b rspline icps1-(icps1*kdetune), icps1+(icps1*kdetune), 0.25, 0.8
  kcps2b rspline icps2-(icps2*kdetune), icps2+(icps2*kdetune), 0.25, 0.8
  kcps3b rspline icps3-(icps3*kdetune), icps3+(icps3*kdetune), 0.25, 0.8
  a1a poscil aenv1*0.5, kcps1a
  a2a poscil aenv2, kcps2a
  a3a poscil aenv3, kcps3a
  a1b poscil aenv1*0.5, kcps1b
  a2b poscil aenv2, kcps2b
  a3b poscil aenv3, kcps3b
  amod1 = a1a*a2a*amodenv*6
  amod2 = a2b*a3a*amodenv*6
  aleft = a1a+a2a+a3a+amod1
  aright = a1b+a2b+a3b+amod2
  outch 13, aleft*iamp, 14, aright*iamp
endin

instr 20
  ; stopchord LYS
  kwave_activity chnget "wave_activity"
  kwave_activity tonek kwave_activity, 1
  kmax_activity init 0
  kmax_activity max kmax_activity, kwave_activity
  kwa_diff diff kwave_activity
  kactivity_thresh chnget "stop_activity_thresh"

  ksig = (kwa_diff < 0) && (kwave_activity < 0.1) && (kmax_activity > kactivity_thresh) ? 1 : 0
  ktrig trigger ksig, 0.5, 0
  knumpeaks chnget "numpeaks"
  knumpeaks delayk knumpeaks, 1
  ksymbol = knumpeaks%4
  chnset int(ksymbol), "root"

  kFaders[] tab2array giWaveRaw1
  kminfaders minarray kFaders
  kmaxfaders maxarray kFaders
  kmax_x maxarray gkXpos
  kmin_x minarray gkXpos
  kmax_z maxarray gkZerocross
  kmin_z minarray gkZerocross
  kmaxpeak_x maxarray gkPeaks_x
  kminpeak_x minarray gkPeaks_x
  kz0 = gkZerocross[0]
  kz0 delayk kz0, 1
  kmax_x delayk kmax_x, 0.5
  kmin_x delayk kmin_x, 0.5
  kmax_z delayk kmax_z, 0.5
  kmin_z delayk kmin_z, 0.5
  kmaxpeak_x delayk kmaxpeak_x, 0.5
  kminpeak_x delayk kminpeak_x, 0.5
  kmaxfaders delayk kmaxfaders, 1
  ktempo1 = 90
  ktempo2 = 40
  if ktrig > 0 then
    if kmax_x > 0.6 then
      chnset ktempo1, "tempo"
    else
      chnset ktempo2, "tempo"
    endif
    event "i", 102, 0, 1+(kmaxfaders*2), 48+int(kz0*24), 90
    kmax_activity = 0
  endif 

endin



/*
opcode DistanceOscil, a, k[]kkii
  kDistance[], kbasefreq, kdetune, ivoice, imaxvoice xin
  kamp = kDistance[ivoice] > 0 ? 1 : 0
  kamp tonek kamp, 1  
  kcps tonek kbasefreq*(1+kDistance[ivoice]*kdetune), 1
  a1 poscil kamp, kcps
  if (ivoice < imaxvoice-1) then
    a1 += DistanceOscil(kDistance, kbasefreq, kdetune, ivoice+1, imaxvoice)
  endif
  iampscale = 1/imaxvoice
  xout(a1*iampscale)
endop


instr 112
  ; read sine oscil detuned by peak distances
  itab = p4
  print itab
  kfreq chnget "Freq"
  kamp_dB chnget "Amp"
  kamp = ampdbfs(kamp_dB)
  
  knumpeaks chnget "numpeaks"
  kdetune chnget "detune"
  imaxvoice = 4
  a1 DistanceOscil gkXdistance, kfreq, kdetune, 0, imaxvoice
  a2 DistanceOscil gkZerocross_distance, kfreq, kdetune, 0, imaxvoice
  outs a1,a2
endin
*/

#include "lsys_cs_midi.inc"

;***************************************************
instr 202
  print p3,p4,p5,p6
  ; midi  output
    ivel = p4
    inote = p5
    ichan = p6

    idur    = (p3 < 0 ? 999 : p3)  ; use very long duration for negative dur, noteondur will create note off when instrument stops
    idur    = (p3 < 0.05 ? 0.05 : p3)  ; avoid extremely short notes as they won't play

    noteondur ichan, inote, ivel, idur
    
endin
;***************************************************


</CsInstruments>  
<CsScore>
i1 0 84600
</CsScore>
</CsoundSynthesizer>