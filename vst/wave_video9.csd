<Cabbage>
form size(500, 510), caption("Wave video"), pluginId("wvi9"), guiMode("queue"), colour(30,30,30)
rslider channel("Freq"), bounds(10, 10, 70, 70), text("Freq"), range(20, 20000, 100, 0.35)
rslider channel("Amp"), bounds(70, 10, 70, 70), text("Amp"), range(-96, 24, 0, 0.5)
button channel("Sparks"), bounds(150, 20, 70, 50), text("Sparks"), colour:0("black"), colour:1("green")

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


instr 1
  ksparks_on chnget "Sparks"
  ;ksparks_ton trigger ksparks_on, 0.5, 0
  ;ksparks_toff trigger ksparks_on, 0.5, 1
  ;if ksparks_ton > 0 then
  ;  event "i", 101, 0, -1
  ;endif
  ;if ksparks_toff > 0 then
  ;  event "i", -101, 0, .1
  ;endif
  
  kOSC_received = 0
  kframerate init 1
  ksize init 1
  kndx init 0
  kx init 0
  ky init 0
  ktimethen init 0
  nextmsg_xy:
  kmess OSClisten gihandle, "wave_video_xy", "fffff", kframerate, ksize, kndx, kx, ky ; receive OSC data from Python
  kOSC_received += kmess
  if kmess == 0 goto done_xy
    kamp = (chnget:k("Amp")-15)
    kcps = (((kx/144)^2)*chnget:k("Freq"))+100
    kpan = (limit(ky/108, -1, 1)*0.5)+0.5
    if ksparks_on > 0 then
      idur = 0.1
      kinstr = 4
      kdly = random(0,1/kframerate)
      ;Stest sprintfk "fps %f, size%i, ndx %i, x %i, y %i, dly %f", kframerate, ksize, kndx, kx, ky, kdly
      ;puts Stest, kndx+1
      event "i", kinstr, kdly, idur, kamp, kcps, kpan
    endif
    kgoto nextmsg_xy
  done_xy:

endin

instr 4
  iamp = p4
  icps = p5
  ipan = p6
  amp expon 1, p3, 0.0001
  a1 poscil ampdbfs(iamp)*amp, icps
  aL = a1*sqrt(1-ipan)
  aR = a1*sqrt(ipan)
  outs aL, aR
endin

</CsInstruments>  
<CsScore>
i1 0 84600
</CsScore>
</CsoundSynthesizer>