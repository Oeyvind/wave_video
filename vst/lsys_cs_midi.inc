
; The rules for the Lindenmayer system are defined in the tables below.
; Symbols (usually notated A,B,C...) are represented by numbers 0, 1, 2 ...
; There is one table (giruleN) for each symbol. Format: size, child1, child2, child3 ...
; This means that an input symbol (parent) 0 generates the output symbols listed as children in girule0.
; We select the rule table by lookup in the girules table.
; In this example, we translate the symbols into melodic intervals, so we also have a table for interval lookup.
; The intervals are listen in order of the symbols (symbol 0 uses the first interval etc).
; Rythm is generated on the basis of the number of children for each branch (parent), and 
; the available time is divided evenly between all children events
                             ; size, child1, child2, ...
girule0 ftgen 0, 0, 8, -2,   3, 2, 0, 1
girule1 ftgen 0, 0, 8, -2,   1, 0
girule2 ftgen 0, 0, 8, -2,   2, 1, 2
girule3 ftgen 0, 0, 8, -2,   1, 0
girules ftgen 0, 0, 8, -2,   girule0,girule1,girule2,girule3
gintervals ftgen 0, 0, 8, -2, -5, -2, 7, 0
gSymbols[] fillarray "A", "B", "C", "D"

instr 101
; gui handling

  ; set LSYS rules
  iset_rule_instr = 112

  Srule0 chnget "rule0"
  if changed(Srule0) > 0 then
    Sscoreline sprintfk {{i %f 0 0.1 0 "%s"}}, iset_rule_instr, Srule0
    scoreline Sscoreline, 1
  endif

  Srule1 chnget "rule1"
  if changed(Srule1) > 0 then
    Sscoreline sprintfk {{i %f 0 0.1 1 "%s"}}, iset_rule_instr, Srule1
    scoreline Sscoreline, 1
  endif

  Srule2 chnget "rule2"
  if changed(Srule2) > 0 then
    Sscoreline sprintfk {{i %f 0 0.1 2 "%s"}}, iset_rule_instr, Srule2
    scoreline Sscoreline, 1
  endif

  Srule3 chnget "rule3"
  if changed(Srule3) > 0 then
    Sscoreline sprintfk {{i %f 0 0.1 3 "%s"}}, iset_rule_instr, Srule3
    scoreline Sscoreline, 1
  endif

  ; set melodic intervals for each symbol
  kinterval0 chnget "interval0"
  kinterval1 chnget "interval1"
  kinterval2 chnget "interval2"
  kinterval3 chnget "interval3"
  tablew kinterval0, 0, gintervals
  tablew kinterval1, 1, gintervals
  tablew kinterval2, 2, gintervals
  tablew kinterval3, 3, gintervals

  kprint_rules chnget "print_rules"
  kprint_trig trigger kprint_rules, 0.5, 0
  if kprint_trig > 0 then
    event "i", 113, 0, 0.1
  endif
endin
alwayson 101

; midi in handling
instr 102
  inum notnum
  ivel veloc
  imidi1_instr = 103
  inst_num = imidi1_instr+(inum*0.001)
  krelease lastcycle
  iactive active imidi1_instr
  iactive1 active imidi1_instr+1
  iactive_ = iactive+iactive1
  print inum, iactive
  event_i "i", imidi1_instr+iactive_, 0, -1, inum, ivel
  if (krelease > 0) then
    event "i", -(imidi1_instr+iactive_), 0, .1
  endif
endin

instr 103
  inote = p4
  ivel = p5
  ivel veloc
  iamp = dbfsamp((ivel/127)^1.1)
  chnset inote, "root_note"
  xtratim 1/kr
  krel release
  ; instrument numbers
  inumlsysplay = 121

  ; play lsystem generator
  event_i "i", inumlsysplay, 0, -1, iamp, inote
  if krel > 0 then
    event "i", -inumlsysplay, 0, .1, iamp, inote
  endif
endin

instr 104
  print p1, p2, p3
  inote = p4
  iroot_note chnget "root_note"
  chnset inote-iroot_note, "second_note_interval" 
  klast lastcycle
  kzero = 0
  if klast > 0 then
    chnset kzero, "second_note_interval"
  endif
endin

instr 105
  print p1, p2, p3
  inote = p4
  iroot_note chnget "root_note"
  chnset inote-iroot_note, "third_note_interval" 
  klast lastcycle
  kzero = 0
  if klast > 0 then
    chnset kzero, "third_note_interval"
  endif
endin


instr 112
  iparent = p4
  Srule strget p5
  Sinfo sprintfk "Set rule %s -> %s", gSymbols[iparent], Srule
  puts Sinfo, 1
  isize strlen Srule
  irule table iparent, girules
  tablew isize, 0, irule 
  index = 1
  while index <= isize do
    Schild strsub Srule, index-1, index
    ichild = 0
    ichild = strcmp(Schild, "A") == 0 ? 0 : ichild
    ichild = strcmp(Schild, "B") == 0 ? 1 : ichild
    ichild = strcmp(Schild, "C") == 0 ? 2 : ichild
    ichild = strcmp(Schild, "D") == 0 ? 3 : ichild
    tablew ichild, index, irule 
    index += 1
  od
  ; clear rest of table
  while index <= ftlen(irule) do
    tablew 0, index, irule 
    index += 1
  od
  print iparent, isize
  
  i1 = 0
  while i1 < 5 do
    print table(i1,irule)
    i1 += 1
  od
  
endin

instr 113
  ; print rules
  SruleA = "rule A: "
  isizeA table 0, girule0
  indxA = 1
  while indxA <= isizeA do
    SruleA strcat SruleA, gSymbols[table(indxA, girule0)]
    indxA += 1
  od
  puts SruleA, 1

  SruleB = "rule B: "
  isizeB table 0, girule1
  indxB = 1
  while indxB <= isizeB do
    SruleB strcat SruleB, gSymbols[table(indxB, girule1)]
    indxB += 1
  od
  puts SruleB, 1

  SruleC = "rule C: "
  isizeC table 0, girule2
  indxC = 1
  while indxC <= isizeC do
    SruleC strcat SruleC, gSymbols[table(indxC, girule2)]
    indxC += 1
  od
  puts SruleC, 1
  SruleD = "rule D: "
  isizeD table 0, girule3
  indxD = 1
  while indxD <= isizeD do
    SruleD strcat SruleD, gSymbols[table(indxD, girule3)]
    indxD += 1
  od
  puts SruleD, 1
endin


; play lsys, control instrument
instr 121
  iamp = p4
  inote = p5
  ;isymbol = floor(chnget("root")+0.5)
  isymbol = chnget("root")-1
  isymbol = isymbol < 0 ? 0 : isymbol
  itempo chnget "tempo"
  idelta = divz(60, itempo, 1)*8
  ilsysinstr = 122+(inote*0.01)
  imelinstr = 131+(inote*0.01)
  imidi_out_instr = 201
  event_i "i", ilsysinstr, 0, idelta, isymbol, inote, 0, imelinstr
  ktime timeinsts
  kretrig init 1
  if (ktime > idelta*kretrig) then
    kretrig += 1
    event "i", ilsysinstr, 0, idelta, isymbol, inote, 0, imelinstr
  endif
  xtratim 1/kr
  krel release
  if krel > 0 then
    turnoff2 ilsysinstr, 4, 0
    turnoff2 imidi_out_instr, 0, 1
    turnoff2 imelinstr, 4, 1
  endif
endin

; lsys generator
instr 122
  idelta = p3
  iparent = p4
  itime times
  ibasepitch = p5
  ithis_gen = p6
  iamp = -20 
  imelinstr = p7
  imax_gen chnget "generations"
  igen_interval chnget "gen_interval"
  index = 0
  imidiinstr = 201
  
  interval2 chnget "second_note_interval" 
  if interval2 != 0 then
    iparent = (wrap(abs(interval2)-1,0,4))
    print iparent
  endif

  event_i "i", imelinstr, 0, p3, iamp, ibasepitch, ithis_gen       
  event_i "i", imidiinstr, 0, p3-(5/kr), iamp, ibasepitch, iparent, ithis_gen
  
  generate:
  if ithis_gen < imax_gen then
    irule table iparent, girules
    irule = irule = 0 ? girule0 : irule ; if parent unknown, use symbol A
    isize table 0, irule
    ichild table index+1, irule
    interval table ichild, gintervals
    ino_genZ_interval chnget "no_genZ_interval"
    interval = (ino_genZ_interval > 0) && (ithis_gen == 0) ? 0 : interval
    isibling_interval chnget "sibling_interval"
    iroot_note_sibling chnget "root_note_sibling"
    if isibling_interval == 1 then
      if iroot_note_sibling == 0 then
        ibasepitch = ibasepitch+interval 
      else
        if index > 0 then
          ibasepitch = ibasepitch+interval
        endif
      endif
      ibasepitch_next = ibasepitch
    else
      ibasepitch_next = ibasepitch+interval
    endif
    Sparent = gSymbols[iparent]
    Schild = gSymbols[ichild]
    Sdebug sprintf "parent %s, to %s, gen %i, size %i, interv %i, base %i, time %.2f", Sparent, Schild, ithis_gen, isize, interval, ibasepitch, itime
    ;puts Sdebug, 1

    inext_gen = ithis_gen+1
    if idelta/isize > 8/kr then
      event_i "i", p1, 0, idelta/isize, ichild, ibasepitch_next+((ithis_gen+1)*igen_interval), inext_gen, imelinstr
    endif
    index += 1
    if index >= isize then
      turnoff
    endif
    ktime timeinsts
    knext = idelta/isize
    if (ktime > knext) then
      reinit generate
    endif
  endif

endin

; global lfo
instr 130
  alfo1 oscil 0.5, 0.09
  alfo1 = alfo1 + 0.5
  chnset alfo1, "lfo1"
  alfo2 oscil 0.5, 0.13
  alfo2 = alfo2 + 0.5
  chnset alfo2, "lfo2"
endin
alwayson 130

; make sound
instr 131

  iamp = ampdbfs(p4)           
  icps = cpsmidinn(p5)		; cps from midi note number
  p3 = p3<0.2?0.2:p3              ; make sure p3 is not too short
  igen = p6


  iattack = 0.001
  idecay = 0.3
  isustain = 0.1
  irelease = 0.1
  amp transegr 0, iattack, 5, 1, idecay, -5, isustain, irelease, -3, 0

  imodindex = 4
  imodratio = 1
  amodamp linsegr 1, 0.3, 1, irelease, 0
  amod oscil3 icps*imodindex*amodamp, icps*imodratio
  acps = icps
  alfo1 chnget "lfo1"
  alfo2 chnget "lfo2"
  aclip = (alfo1*0.2)+0.3
  askew = (alfo2*0.3)-0.5
  asyncin = 0
  iminsweep = 15
  iphase = 0

  a1, async1 squinewave acps, aclip, askew, asyncin, iminsweep, iphase
  a1 = a1*iamp*amp
  idetune = 0.003
  a2a poscil iamp*amp, (icps+amod)*(1+idetune)
  a2b poscil iamp*amp, (icps+amod)*(1-idetune)
  a2 = (a2a+a2b)*0.5
  a3 = (a1+a2)*.5
  ;outch	1, a2, 2, a3

endin

;***************************************************        
instr	201
; midi  output
  ichan_1 chnget "midichan_gen1"
  ichan_2 chnget "midichan_gen2"
  ichan_3 chnget "midichan_gen3"
  ichan_4 chnget "midichan_gen4"
  idrum_gen chnget "perc_gen"
  idrum_map0 chnget "drum_map_A"
  idrum_map1 chnget "drum_map_B"
  idrum_map2 chnget "drum_map_C"
  idrum_map3 chnget "drum_map_D"
	iamp = p4
  idB_range = 70
	ivel = pow((1+(iamp/idB_range)),2) * 127
	inote = p5
  isymbol = p6
  igeneration = p7
  if igeneration == 0 goto end
  ichan = 1
  ichan = igeneration == 1 ? ichan_1 : ichan
  ichan = igeneration == 2 ? ichan_2 : ichan
  ichan = igeneration == 3 ? ichan_3 : ichan
  ichan = igeneration == 4 ? ichan_4 : ichan
	idur = (p3 < 0 ? 999 : p3)	; use very long duration for realtime events, noteondur will create note off when instrument stops
	idur = (p3 < 0.1 ? 0.1 : p3)	; avoid extremely short notes as they won't play
  if ichan == 2 then
    print inote, ichan, igeneration, idur
  endif
	noteondur ichan, inote, ivel, idur
  if igeneration == idrum_gen then
    ichan = 10
    inote = isymbol == 0 ? idrum_map0 : inote
    inote = isymbol == 1 ? idrum_map1 : inote
    inote = isymbol == 2 ? idrum_map2 : inote
    inote = isymbol == 3 ? idrum_map3 : inote
    noteondur ichan, inote, ivel, idur
  endif
  end:
endin
