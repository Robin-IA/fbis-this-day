"""US style for entry text: "1 November 1979" -> "November 1, 1979", British -> US spelling.

The Documentation-Explorer-Best-Practices rules ask for plain US English with
month-first dates. build_site.py applies conv() to every published text field,
so a drafter writing day-first does not leak into the site."""
import re
M="January|February|March|April|May|June|July|August|September|October|November|December"
UK={"centred":"centered","centre":"center","recognised":"recognized","organised":"organized","organisation":"organization",
 "labour":"labor","defence":"defense","favour":"favor","honour":"honor","programme":"program","travelled":"traveled",
 "colour":"color","rumours":"rumors","rumour":"rumor","offence":"offense","neighbouring":"neighboring","neighbour":"neighbor",
 "towards":"toward","theatre":"theater","harbour":"harbor","armour":"armor","armoured":"armored","behaviour":"behavior",
 "criticised":"criticized","recognise":"recognize","apologised":"apologized","legalised":"legalized","normalised":"normalized",
 "mobilised":"mobilized","characterised":"characterized","emphasised":"emphasized","authorised":"authorized","jeopardised":"jeopardized",
 "endeavour":"endeavor","catalogue":"catalog","analysed":"analyzed","paralysed":"paralyzed","fuelled":"fueled","signalled":"signaled",
 "labelled":"labeled","cancelled":"canceled","modelled":"modeled","counselled":"counseled","whilst":"while","amongst":"among","grey":"gray"}
def comma(m, s):
    rest=s[m.end():m.end()+2]
    return ", " if re.match(r" [A-Za-z0-9(]", rest) else ""
def conv(s):
    if not isinstance(s,str): return s
    out=[]; i=0
    pat=re.compile(r"\b(\d{1,2})(?:(–|-| and | to )(\d{1,2}))? (%s)(?: (\d{4}))?\b"%M)
    def rep(m):
        d1,sep,d2,mon,yr=m.groups()
        days=d1+((sep+d2) if d2 else "")
        if yr:
            return f"{mon} {days}, {yr}"+("," if re.match(r" [A-Za-z0-9(]", m.string[m.end():m.end()+2]) else "")
        return f"{mon} {days}"
    s=pat.sub(rep,s)
    s=s.replace(",,",",")
    for a,b in UK.items():
        s=re.sub(r"\b%s\b"%a,b,s); s=re.sub(r"\b%s\b"%a.capitalize(),b.capitalize(),s)
    return s
