<CsoundSynthesizer>
<CsOptions>
-otest_midi_partikkel.wav --midioutfile=midi_partikkel.mid
</CsOptions>
<CsInstruments>

	sr = 48000
	ksmps = 10
	nchnls = 2	
	0dbfs = 1

; classic waveforms
	giSine		ftgen	0, 0, 65537, 10, 1					; sine wave
	giCosine	ftgen	0, 0, 8193, 9, 1, 1, 90					; cosine wave
	giTri		ftgen	0, 0, 8193, 7, 0, 2048, 1, 4096, -1, 2048, 0		; triangle wave 

	; grain envelope tables
	giSigmoRise 	ftgen	0, 0, 8193, 19, 0.5, 1, 270, 1				; rising sigmoid
	giSigmoFall 	ftgen	0, 0, 8193, 19, 0.5, 1, 90, 1				; falling sigmoid
	giExpFall	ftgen	0, 0, 8193, 5, 1, 8193, 0.00001				; exponential decay
	giTriangleWin 	ftgen	0, 0, 8193, 7, 0, 4096, 1, 4096, 0			; triangular window 

opcode DistanceGrains, a, k[]kkkkkiii
  kDistance[], kwavfreq, kgrainrate, kdist_rate, kvoice_spread, kgraindur, ivoice, imaxvoice, iopcode_id xin
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
  kinit_mute linseg 0, 1, 0, 0, 1, 1, 1
  apulse, aphase partikkelsync iopcode_id
  kSig[] init ksmps
  kSig shiftin apulse
  kpulse = sumarray(kSig) 
  ;Sdebug sprintfk "partikkel %i amp %f pulse %f", iopcode_id, kamp, kpulse
  ;puts Sdebug, kamp+kpulse+1
  kphase downsamp aphase
  if (kpulse > 0) && (kamp > 0) && (kinit_mute > 0) then
    knote = (kwavfreq*12)+48
    knote = 12*log2(kwavfreq/440) + 69
    kvel = 90
    kchan = iopcode_id < 10 ? 5 : 6
    event "i", 202, 0, kgraindur, kvel, knote, kchan
  endif

  if (ivoice < imaxvoice-1) then
    a1 += DistanceGrains(kDistance, kwavfreq, kgrainrate, kdist_rate, kvoice_spread, kgraindur, ivoice+1, imaxvoice, iopcode_id)
  endif
  iampscale = 1/imaxvoice
  xout(a1*iampscale)
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

gkXdistance[] fillarray 0.2, 0.1, 0.3, 0, 0.08
gkZerocross_distance [] fillarray 0.15, 0, 0.37, 0.14, 0.04
;***************************************************

instr 12
  ; grain rhythm detuned by peak distances
  kwavfreq = 440;chnget "Grainpitch"
  kamp_dB = -1; chnget "Grainamp"
  kgrainrate = 2; chnget "Grate"
  kx_dist = 0.2; chnget "avg_x_distance"
  kgrainrate *= limit(1-(kx_dist)*2, 0.1, 1)
  kgraindur = 0.3; chnget "Gdur"
  kamp = ampdbfs(kamp_dB)
  kactivity = 0.2; chnget "wave_activity"
  kactivity limit kactivity, 0, 1
  kamp_env EnvFollow kactivity, 0.01, 3
  kamp *= kamp_env
  knumpeaks = 4; chnget "numpeaks"
  kwavfreq *= (knumpeaks+1)
  kdist_rate = 0.7; chnget "G_dist_rate"
  kvoice_spread = 0.5; chnget "G_voice_spread"
  imaxvoice = 5
  iopcode_id1 = 1
  iopcode_id2 = 10  
  a1 DistanceGrains gkXdistance, kwavfreq, kgrainrate, kdist_rate, kvoice_spread, kgraindur, 0, imaxvoice, iopcode_id1
  a2 DistanceGrains gkZerocross_distance, kwavfreq*0.5, kgrainrate, kdist_rate, kvoice_spread, kgraindur, 0, imaxvoice, iopcode_id2
  outs a1*kamp*3,a2*kamp*3
endin

;***************************************************
instr 202
  ;print p3,p4,p5,p6
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
;	start	dur	
i12	0 10
e
</CsScore>
</CsoundSynthesizer>
