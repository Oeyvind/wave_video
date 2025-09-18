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


opcode RecursArr, a, k[]ii
  kFreq[], ivoice, imaxvoice xin
  kamp = kFreq[ivoice] > 0 ? 1 : 0
  kamp tonek kamp, 1  
  kcps = kFreq[ivoice]
  printk2 kcps, ivoice*5
  a1 poscil kamp, kcps
  if (ivoice < imaxvoice-1) then
    a1 += RecursArr(kFreq,ivoice+1, imaxvoice)
  endif
  xout(a1)
endop

;***************************************************
instr 1
  iamp = ampdbfs(-9)
  knew linseg 0, 0.5, 0, 0, 500, 1, 500
  kFreq[] fillarray 250,300,0, 0
  kFreq[2] = knew
  imaxvoice = 4
  a1 RecursArr kFreq, 0, imaxvoice 
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
