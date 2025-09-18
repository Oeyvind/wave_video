<CsoundSynthesizer>
<CsOptions>
-odac
</CsOptions>
<CsInstruments>

sr = 48000
ksmps = 10
nchnls = 2	
0dbfs = 1

opcode Recursion, a, iip
  //input: frequency, number of partials, this partial (default=1)
  iFreq, iNumParts, iThisPart xin
  //amplitude decreases for higher partials
  iAmp = 1/iNumParts/iThisPart
  //apply small frequency deviation except for the first partial
  iFreqMult = (iThisPart == 1) ? 1 : iThisPart*random:i(0.95,1.05)
  //create this partial
  aOut = poscil:a(iAmp,iFreq*iFreqMult)
  //add the other partials via recursion
  if (iThisPart < iNumParts) then
    aOut += Recursion(iFreq,iNumParts,iThisPart+1)
  endif
  xout(aOut)
endop


opcode RecursArr, a, i[]i
  iFreq[], ivoice xin
  iamp = 1  
  icps = iFreq[ivoice]
  a1 poscil iamp, icps
  if (iFreq[ivoice+1] > 0) then
    a1 += RecursArr(iFreq,ivoice+1)
  endif
  xout(a1)
endop

;***************************************************
instr 1
  iamp = ampdbfs(-9)
	iFreq[] fillarray 250,300,500, 0
	a1 RecursArr iFreq, 0
	a1 *= iamp
  outs a1, a1
endin


</CsInstruments>
<CsScore>
;	start	dur	
i1	0	2
e
</CsScore>
</CsoundSynthesizer>
