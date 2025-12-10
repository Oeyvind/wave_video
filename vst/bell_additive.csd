<CsoundSynthesizer>
<CsOptions>
</CsOptions>
<CsInstruments>

sr = 48000
ksmps = 10
nchnls = 2	
0dbfs = 1

;xylophone
girtos4        ftgen    0,0,-6,-2,    1,     3.932,     9.538,    16.688,    24.566,    31.147

opcode SineVoice,a,kiii
    kfreq, ivoice, inumvoices, iratios xin
    irto table ivoice,iratios
    kvib_amt = 0.1
    kvib_fq = 0.3+random(0.1,0.2)
    alfo oscil kvib_amt, kvib_fq, -1, random(0,0.7)
    aenv linseg 1, 0.01+((inumvoices-ivoice)/inumvoices)^4, ampdbfs(-12), 1, ampdbfs(-20)
    print 0.01+((inumvoices-ivoice)/inumvoices)^2, irto
    a1 poscil aenv,a(kfreq*irto)*semitone(alfo)
    if ivoice < inumvoices then
     asin SineVoice kfreq, ivoice+1, inumvoices, iratios
     a1 += asin
    endif
    a1 *= (1/inumvoices)
    xout a1
endop

instr 1
    iamp = ampdbfs(-9)
    kfreq = 440
    irel = 0.5
    aenv1 linsegr 0, 0.01, 1, 0.5, ampdbfs(-8), 2, ampdbfs(-15), irel, 0.0001
    a1 SineVoice kfreq, 0, 6, girtos4
    a1 *= aenv1
	outs a1, a1
endin


</CsInstruments>
<CsScore>
;	start	dur	
i1	0	2
i1	3	2
f0 6
e
</CsScore>
</CsoundSynthesizer>
