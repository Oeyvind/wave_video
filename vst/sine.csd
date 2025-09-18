<CsoundSynthesizer>
<CsOptions>
-odac
</CsOptions>
<CsInstruments>

	sr = 48000
	ksmps = 10
	nchnls = 2	
	0dbfs = 1

	giSine		ftgen	0, 0, 65536, 10, 1				; sine wave
	giSquare	ftgen	0, 0, 128, 7, 1, 64, 1, 0, -1, 64, -1				; sine wave

;***************************************************
	instr 1
        iamp    = ampdbfs(-9)
	kenv	linseg 0, 1, 1, p3-1, 0	
	a1	oscili kenv*iamp, 1500, giSine
	a2	oscili kenv*iamp, 1500, giSine
        a3      = (a1+a2)*0.5
		outs a3, a3
	endin


</CsInstruments>
<CsScore>
;	start	dur	
i1	0	2
e
</CsScore>
</CsoundSynthesizer>
