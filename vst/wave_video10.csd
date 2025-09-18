<Cabbage>
form size(500, 510), caption("Wave video"), pluginId("wv10"), guiMode("queue"), colour(30,30,30)
rslider channel("Freq"), bounds(10, 10, 70, 70), text("Freq"), range(20, 20000, 100, 0.35)
rslider channel("Amp"), bounds(70, 10, 70, 70), text("Amp"), range(-96, 24, 0, 0.5)
button channel("Sparks"), bounds(150, 20, 70, 50), text("Sparks"), colour:0("black"), colour:1("green")
button channel("Spect"), bounds(230, 20, 70, 50), text("Spect"), colour:0("black"), colour:1("green")

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

  ;gkndx init 0
  gihandle OSCinit 9899 ; set the network port number where we will receive OSC data from Python
  giSigmoRise 	ftgen	0, 0, 256, 19, 0.5, 1, 270, 1				; rising sigmoid
  giSigmoFall 	ftgen	0, 0, 256, 19, 0.5, 1, 90, 1				; falling sigmoid
  giSpect ftgen 0, 0, 32, 2, 0 ; "spectrum" from rope x,y coordinates

instr 1
  ksparks_on chnget "Sparks"
  kspect_on chnget "Spect"
  kspect_ton trigger kspect_on, 0.5, 0
  kspect_toff trigger kspect_on, 0.5, 1
  if kspect_ton > 0 then
    event "i", 5, 0, -1
  endif
  if kspect_toff > 0 then
    event "i", -5, 0, .1
  endif
  
  kOSC_received = 0
  kframerate init 0
  kx init 0
  ky init 0
  ktimethen init 0
  nextmsg_xy:
  kmess OSClisten gihandle, "wave_video_xy", "fff", kframerate, kx, ky ; receive OSC data from Python
  kOSC_received += kmess
  if kmess == 0 goto done_xy
    if (ky > 0) && ksparks_on > 0 then
      kamp = (chnget:k("Amp")-15)
      kcps = (((kx/36)^2)*chnget:k("Freq"))+100
      kpan = (limit(ky/27, -1, 1)*0.5)+0.5 
      idur = 0.3
      kinstr = 4
      kdly = random(0, 1/kframerate);(kx/36)/kframerate
      ;Stest sprintfk "fps %f, size%i, ndx %i, x %i, y %i, dly %f", kframerate, ksize, kndx, kx, ky, kdly
      ;puts Stest, kndx+1
      event "i", kinstr, kdly, idur, kamp, kcps, kpan
    endif
    if kspect_on > 0 then
      tablew ky/36, kx, giSpect
    endif
    kgoto nextmsg_xy
  done_xy:

endin

instr 4
  iamp = p4
  icps = p5
  ipan = p6
  amp expseg 0.001, 0.01, 1, p3-0.01, 0.0001
  a1 poscil ampdbfs(iamp)*amp, icps
  aL = a1*sqrt(1-ipan)
  aR = a1*sqrt(ipan)
  outs aL, aR
endin

instr 5
  indx = 1
  imax = 28
  while indx < imax do
    event_i "i", 6+(indx*0.01), 0, -1, indx-1
    indx += 1
  od
  xtratim 1/kr
  kflag release
  printk2 kflag
  if kflag > 0 then
    kndx = 0
    while kndx < imax do
      event "i", -(6+kndx*0.01), 0, .1
      kndx += 1
    od 
  endif
endin

instr 6
  indx = p4
  kamp table indx, giSpect
  kfreq = chnget:k("Freq")*(indx+1)
  kamp0 = ampdbfs(chnget:k("Amp"))
  amp interp kamp0*kamp
  amp butterhp amp, 0.4
  amp butterlp amp, 20
  a1 poscil amp, kfreq
  outs a1,a1
endin

</CsInstruments>  
<CsScore>
i1 0 84600
</CsScore>
</CsoundSynthesizer>