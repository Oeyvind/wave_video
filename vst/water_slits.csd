<Cabbage>
form size(900, 510), caption("Water slits"), pluginId("wsl1"), guiMode("queue"), colour(30,30,30)
groupbox bounds(5, 5, 200, 80), colour(75,85,90), plant("plant_w1"), lineThickness("0"){ 
rslider channel("Freq1_wav"),          bounds(10,  10, 60, 60), text("Freq"), range(20, 300, 100, 0.35)
rslider channel("Amp1_wav"),           bounds(70,  10, 60, 60), text("Amp"), range(-50, 6, 0, 3)
button channel("Wave1_on"),            bounds(130, 10, 68, 30), text("W1_On"), colour:0("black"), colour:1("green")
}
groupbox bounds(5, 90, 200, 80), colour(75,85,90), plant("plant_w1"), lineThickness("0"){ 
rslider channel("Freq2_wav"),          bounds(10,  10, 60, 60), text("Freq"), range(20, 300, 100, 0.35)
rslider channel("Amp2_wav"),           bounds(70,  10, 60, 60), text("Amp"), range(-50, 6, 0, 3)
button channel("Wave2_on"),            bounds(130, 10, 68, 30), text("W1_On"), colour:0("black"), colour:1("green")
}
groupbox bounds(5, 175, 200, 80), colour(75,85,90), plant("plant_w1"), lineThickness("0"){ 
rslider channel("Freq3_wav"),          bounds(10,  10, 60, 60), text("Freq"), range(20, 300, 100, 0.35)
rslider channel("Amp3_wav"),           bounds(70,  10, 60, 60), text("Amp"), range(-50, 6, 0, 3)
button channel("Wave3_on"),            bounds(130, 10, 68, 30), text("W1_On"), colour:0("black"), colour:1("green")
}
groupbox bounds(5, 260, 200, 80), colour(75,85,90), plant("plant_w1"), lineThickness("0"){ 
rslider channel("Freq4_wav"),          bounds(10,  10, 60, 60), text("Freq"), range(20, 300, 100, 0.35)
rslider channel("Amp4_wav"),           bounds(70,  10, 60, 60), text("Amp"), range(-50, 6, 0, 3)
button channel("Wave4_on"),            bounds(130, 10, 68, 30), text("W1_On"), colour:0("black"), colour:1("green")
}
groupbox bounds(5, 345, 200, 80), colour(75,85,90), plant("plant_w1"), lineThickness("0"){ 
rslider channel("Freq5_wav"),          bounds(10,  10, 60, 60), text("Freq"), range(20, 300, 100, 0.35)
rslider channel("Amp5_wav"),           bounds(70,  10, 60, 60), text("Amp"), range(-50, 6, 0, 3)
button channel("Wave5_on"),            bounds(130, 10, 68, 30), text("W1_On"), colour:0("black"), colour:1("green")
}
groupbox bounds(5, 430, 200, 80), colour(75,85,90), plant("plant_w1"), lineThickness("0"){ 
rslider channel("Freq6_wav"),          bounds(10,  10, 60, 60), text("Freq"), range(20, 300, 100, 0.35)
rslider channel("Amp6_wav"),           bounds(70,  10, 60, 60), text("Amp"), range(-50, 6, 0, 3)
button channel("Wave6_on"),            bounds(130, 10, 68, 30), text("W1_On"), colour:0("black"), colour:1("green")
}

csoundoutput bounds(500, 300, 390, 200)
</Cabbage>
<CsoundSynthesizer>
<CsOptions>
-n -d -m0 -M0 -Q0 -+rtmidi=null 
</CsOptions>
<CsInstruments>

ksmps = 64
nchnls = 2
0dbfs=1

;massign -1,102
;pgmassign -1, -1

  gix_size = 1280
  gkSlit1[] init gix_size
  gkSlit2[] init gix_size
  gkSlit3[] init gix_size
  gkSlit4[] init gix_size
  gkSlit5[] init gix_size
  gkSlit6[] init gix_size

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
  kwave1_on chnget "Wave1_on"
  ButtonEvent kwave1_on, 10.1
  kwave2_on chnget "Wave2_on"
  ButtonEvent kwave2_on, 10.2
  kwave3_on chnget "Wave3_on"
  ButtonEvent kwave3_on, 10.3
  kwave4_on chnget "Wave4_on"
  ButtonEvent kwave4_on, 10.4
  kwave5_on chnget "Wave5_on"
  ButtonEvent kwave5_on, 10.5
  kwave6_on chnget "Wave6_on"
  ButtonEvent kwave6_on, 10.6

  ; OSC receive
  kOSC_received = 0
  
  kslit_ndx init 0
  k_ndx init 0
  kx_val init 0
  nextmsg_wave:
  kmess OSClisten gihandle, "wave", "fff", kslit_ndx, k_ndx, kx_val ; receive OSC data from Python
  kOSC_received += kmess
  if kmess == 0 goto done_wave
  gkSlit1[k_ndx] = kx_val
  kgoto nextmsg_wave
  done_wave:
  
  Soscreceived = "OK OSC received"
  kOSC_received limit kOSC_received, 0, 1
  puts Soscreceived, kOSC_received
  chnset kOSC_received, "osc_received"

endin

opcode OscilBank, a, kk[]ii
  kfreq, kAmp[], ivoice, imaxvoice xin
  kamp = kAmp[ivoice]
  kcps = kfreq+(ivoice*20q)
  a1 poscil kamp, kcps
  if (ivoice <= imaxvoice) then
    a1 += OscilBank(kfreq, kAmp, ivoice+1, imaxvoice)
  endif
  xout(a1)
endop

instr 10
  kndx init 0
  iresolution = 3
  iarrsize = floor(gix_size/iresolution)
  kAmps[] init iarrsize
  while kndx < iarrsize-1 do
    kval = gkSlit1[kndx*iresolution]
    kAmps[kndx] = kval
    kndx = kndx+1
  od
  kosc_received chnget "osc_received"
  if changed(kosc_received) > 0 then
    kndx = 0
  endif
  
  kfreq chnget "Freq1_wav"
  iamp = ampdbfs(-10)
  imaxvoice = 30;iarrsize-2
  ivoice = 0
  a1 OscilBank kfreq, kAmps, ivoice, imaxvoice
  kamp_dB chnget "Amp1_wav"
  kamp = (ampdbfs(kamp_dB)*iamp)/imaxvoice
  printk2 kamp
  a1 *= kamp
  outs a1, a1
endin

instr 11
endin



</CsInstruments>  
<CsScore>
i1 0 84600
</CsScore>
</CsoundSynthesizer>