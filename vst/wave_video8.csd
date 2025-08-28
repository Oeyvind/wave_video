<Cabbage>
form size(500, 510), caption("Wave video"), pluginId("wvi8"), guiMode("queue"), colour(30,30,30)
rslider channel("Freq"), bounds(10, 10, 70, 70), text("Freq"), range(20, 20000, 100, 0.35)
rslider channel("Amp"), bounds(70, 10, 70, 70), text("Amp"), range(-96, 24, 0, 0.5)
button channel("Wave_fade_on"), bounds(150, 20, 70, 50), text("W_On"), colour:0("black"), colour:1("green")
gentable bounds(10, 90, 380, 200), channel("wave_raw"), sampleRange(0, 1024), ampRange(-1, 1, 1), outlineThickness(3), tableNumber(1.0), tableGridColour(155, 155, 155, 255) tableBackgroundColour(0,0,0,0) tableColour:0(147, 210, 0, 255)
;button channel("Wave_raw_on"), bounds(410, 20, 70, 50), text("Wf_On"), colour:0("black"), colour:1("green")
;gentable bounds(410, 90, 380, 200), channel("wave_fade"), sampleRange(0,1024), ampRange(-1, 1, 2), outlineThickness(3), tableNumber(2.0), tableGridColour(155, 155, 155, 255) tableBackgroundColour(0,0,0,0) tableColour:0(147, 210, 0, 255)
;button channel("Wavenote_on"), bounds(230, 20, 70, 50), text("Wn_On"), colour:0("black"), colour:1("green")
;button channel("Wavemidi_on"), bounds(310, 20, 70, 50), text("Wm_On"), colour:0("black"), colour:1("green")
button channel("Peaks_on"), bounds(400, 20, 70, 50), text("Peaks_On"), colour:0("black"), colour:1("green")
button channel("Print"), bounds(400, 80, 70, 50), text("Print"), colour:0("black"), colour:1("green")

button channel("Noisebank"), bounds(400, 140, 70, 50), text("Noisbnk"), colour:0("black"), colour:1("green")

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

  giWaveFade ftgen 1, 0, 1024, 7, 0, 1024, -1  ; empty  
  giWaveFade1 ftgen 0, 0, 1024, -2, 0  ; empty  
  giWaveFade2 ftgen 0, 0, 1024, -2, 0  ; empty
  giWaveFades ftgen 0, 0, 2, -2, giWaveFade1, giWaveFade2
  giWaveRaw ftgen 2, 0, 1024,  7, 0, 1024, -1 
  giWaveRaw1 ftgen 0, 0, 1024, -2, 0  ; empty  
  giWaveRaw2 ftgen 0, 0, 1024, -2, 0  ; empty
  giWaveRaws ftgen 0, 0, 2, -2, giWaveRaw1, giWaveRaw2
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
  kamp = table:k(indx*((1/inum)*ilen), giWaveRaw)
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
  kwave_fade_on chnget "Wave_fade_on"
  kwavefadeon trigger kwave_fade_on, 0.5, 0
  kwavefadeoff trigger kwave_fade_on, 0.5, 1
  if kwavefadeon > 0 then
    event "i", 10.1, 0, -1, giWaveFade
  endif
  if kwavefadeoff > 0 then
    event "i", -10.1, 0, .1
  endif
  
  knoisebank_on chnget "Noisebank"
  knoisebankon trigger knoisebank_on, 0.5, 0
  knoisebankoff trigger knoisebank_on, 0.5, 1
  if knoisebankon > 0 then
    event "i", 5, 0, -1
  endif
  if knoisebankoff > 0 then
    event "i", -5, 0, .1
  endif

  kwave_raw_on chnget "Wave_raw_on"
  kwaverawon trigger kwave_raw_on, 0.5, 0
  kwaverawoff trigger kwave_raw_on, 0.5, 1
  if kwaverawon > 0 then
    event "i", 10.2, 0, -1, giWaveRaw
  endif
  if kwaverawoff > 0 then
    event "i", -10.2, 0, .1
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

  kwavemidi_on chnget "Wavemidi_on"
  kwavemidion trigger kwavemidi_on, 0.5, 0
  kwavemidioff trigger kwavemidi_on, 0.5, 1
  if kwavemidion > 0 then
    event "i", 21, 0, -1
  endif
  if kwavemidioff > 0 then
    event "i", -21, 0, .1
  endif

  kOSC_received = 0
  kindex init 0
  kvalue init 0
  ktimethen init 0
  nextmsg_wave:
  kmess OSClisten gihandle, "wave_video", "ff", kindex, kvalue ; receive OSC data from Python
  kOSC_received += kmess
  ; fade in and out
  if kindex < 256 then
    kamp table kindex, giSigmoRise
  elseif kindex > 768 then
    kamp table kindex-768, giSigmoFall
  else
    kamp = 1
  endif
  kvaluefade = kvalue*kamp
  kswitch init 1
  ktab_raw = kswitch == 1 ? giWaveRaw1 : giWaveRaw2
  ktab_fade = kswitch == 1 ? giWaveFade1 : giWaveFade2
  
  tablewkt kvalue, kindex, ktab_raw
  tablewkt kvaluefade, kindex, ktab_fade
  if kindex == 1022 then
    kswitch = kswitch == 1 ? 2 : 1
    ktime timeinsts
    kupdate_time limit ktime-ktimethen, 0, 5
    ktimethen = ktime
    event "i", 2, 0, kupdate_time, kswitch
  endif
  if kmess == 0 goto done_wave
  kgoto nextmsg_wave 
  done_wave:
  
  kpeaks_on chnget "Peaks_on"
  knumpeaks init 0
  kavg_x_distance init 0
  ksum_x_movement init 0
  kavg_x_movement init 0
  nextmsg_peaksummary:
    kmess OSClisten gihandle, "peaks_summary", "ffff", knumpeaks, kavg_x_distance, kavg_x_movement, ksum_x_movement
    kOSC_received += kmess
    chnset knumpeaks, "numpeaks"
    chnset kavg_x_distance, "avg_x_distance"
    chnset kavg_x_movement, "avg_x_movement"
    chnset ksum_x_movement, "sum_x_movement"
  if kmess == 0 goto done_peaksummary
  done_peaksummary:

  kpeak_id init 0
  kpeak_x init 0
  kpeak_y init 0
  kpeak_amp init 0
  kpeak_movement init 0
  kPeaks_active[] init 100
  nextmsg_activepeaks:
    kmess OSClisten gihandle, "active_peaks", "fffff", kpeak_id, kpeak_x, kpeak_y, kpeak_amp, kpeak_movement
    kOSC_received += kmess
    if kmess == 0 goto done_activepeaks
      ;Sactive sprintfk "active_peaks %i", kpeak_id
      ;puts Sactive, kpeak_id+1
      kamp = (chnget:k("Amp")-15);+abs(kpeak_y)*10
      kcps = (((kpeak_x/1024)^2)*1600)+100
      kpan = (limit(kpeak_y*8, -1, 1)*0.5)+0.5
      kinstr = 4+(kpeak_id*0.001)
      if kpeaks_on > 0 then
        Samp sprintfk "amp_%f.4", kinstr
        chnset kamp, Samp
        Scps sprintfk "cps_%f.4", kinstr
        chnset kcps, Scps
        Span sprintfk "pan_%f.4", kinstr
        chnset kpan, Span
        ; start instr kun hvis den ikke allerede er i kPeaks_active
        if kPeaks_active[kpeak_id] == 0 then
          event "i", kinstr, 0, -1
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
  
  kprintbutton chnget "Print"
  printarray(kPeaks_active, kprintbutton)
  kprint_trig trigger kprintbutton, 0.5, 0
  if kprint_trig > 0 then
    kindex = 0
    while kindex < lenarray(kPeaks_active) do
      if kPeaks_active[kindex] == 1 then
        printk2 kindex, 20
      endif
      kindex += 1
    od
  endif
  ktest active 4
  printk2 ktest*kprintbutton
  Soscreceived = "OK OSC received"
  kOSC_received limit kOSC_received, 0, 1
  puts Soscreceived, kOSC_received
endin


instr 2
  ;print p3
  iswitch = p4
  ;print p2, itab, p3
  if iswitch == 1 then
    kndx line 0, p3-1/kr, 1
  else 
    kndx line 1, p3-1/kr, 0
  endif
  gkndx = kndx
  ftmorf kndx, giWaveRaws, giWaveRaw
  ftmorf kndx, giWaveFades, giWaveFade
  ;kupdate metro 4
  ;if kupdate > 0 then
  ;  event "i", 3, 0, 1/kr
  ;endif
  event_i "i", 3, 0, 1/kr
endin

instr 3
  ;cabbageSet "wave_raw", "tableNumber", 1; update table display
  ;cabbageSet "wave_fade", "tableNumber", 2; update table display
endin

instr 4
  Samp sprintf "amp_%f.4", p1
  kamp chnget Samp
  Scps sprintf "cps_%f.4", p1
  kcps chnget Scps
  kcps tonek kcps, 10
  Span sprintf "pan_%f.4", p1
  kpan chnget Span
  kpan tonek kpan, 10
  apan butterlp interp(kpan), 8
  amp linsegr 0, 0.15, 1, 0.5, 0
  ;amp transegr 0, 0.2, 2, 1, 1, 0, 1, 0.5, 2, 0
  a1 poscil ampdbfs(kamp)*amp, kcps, -1, -1
  aL = a1*sqrt(1-apan)
  aR = a1*sqrt(apan)
  outs aL, aR
endin

instr 5
  ibasenote = 48
  iNotes[] fillarray 0,3,5,7,10
  knumpeaks chnget "numpeaks"
  kavg_x_distance chnget "avg_x_distance"
  kavg_x_movement chnget "avg_x_movement"
  ksum_x_movement chnget "sum_x_movement"
  ;printk2 ksum_x_movement
  ;printk2 kavg_x_movement, 20
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
  ;ksum_x_movement tonek ksum_x_movement, 20
  kphasor_freq = (ksum_x_movement/100)*-1
  printk2 kphasor_freq
  amp_ndx phasor kphasor_freq
  ;amp_ndx pow amp_ndx, 3
  amp1 table amp_ndx, iampcurve, 1, 0, 1
  amp2 table amp_ndx, iampcurve, 1, 0.2, 1
  amp3 table amp_ndx, iampcurve, 1, 0.4, 1
  amp4 table amp_ndx, iampcurve, 1, 0.6, 1
  amp5 table amp_ndx, iampcurve, 1, 0.8, 1
  asum sum a1*amp1,a2*amp2,a3*amp3,a4*amp4,a5*amp5
  outs asum, asum

endin

instr 10
  ; read ftable waveform with oscillator
  itab = p4
  kfreq chnget "Freq"
  kamp_dB chnget "Amp"
  kamp = ampdbfs(kamp_dB)
  aphase phasor kfreq
  aphase *= 1024
  a1 table3 aphase, itab
  a1 *= kamp
  outs a1, a1
endin

instr 11
  iNotes[] fillarray 0,3,5,7,10
  ibasenote = 60
  ilen tableng giWaveRaw
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


</CsInstruments>  
<CsScore>
i1 0 84600
</CsScore>
</CsoundSynthesizer>