"""Parse public Azure Status History PIRs from HTML, without tenant credentials."""
import datetime as dt
import html
import re
from html.parser import HTMLParser

HISTORY_URL = 'https://azure.status.microsoft/en-us/status/history'
TRACKING = re.compile(r'\bTracking\s*ID\s*:\s*([A-Z0-9]{3,}-[A-Z0-9]{2,})\b', re.I)
DATE = re.compile(r'\b(\d{1,2}/\d{1,2}/20\d{2})\b')

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts=[]
        self.hidden=0
    def handle_starttag(self, tag, attrs):
        if tag in ('script','style','noscript'):
            self.hidden+=1
        if tag in ('h1','h2','h3','h4','h5','p','div','section','article','li','br','tr'):
            self.parts.append('\n')
    def handle_endtag(self, tag):
        if tag in ('script','style','noscript'):
            self.hidden=max(0,self.hidden-1)
        if tag in ('h1','h2','h3','h4','h5','p','div','section','article','li','tr'):
            self.parts.append('\n')
    def handle_data(self,data):
        if not self.hidden:
            self.parts.append(data)

def parse_history(raw_html):
    p=TextExtractor()
    p.feed(raw_html.decode('utf-8', errors='replace') if isinstance(raw_html,bytes) else raw_html)
    lines=[re.sub(r'\s+',' ',html.unescape(line)).strip() for line in ''.join(p.parts).splitlines()]
    lines=[x for x in lines if x]
    positions=[i for i,line in enumerate(lines) if TRACKING.search(line)]
    incidents=[]
    for ix,pos in enumerate(positions):
        match=TRACKING.search(lines[pos]); tracking=match.group(1).upper()
        before=lines[max(0,pos-18):pos]
        title=next((line for line in reversed(before) if re.search(r'Post.Incident Review|\bPIR\b',line,re.I)),None)
        if not title:
            continue
        date_string=next((m.group(1) for line in reversed(before) if (m:=DATE.search(line))),None)
        if not date_string:
            continue
        try:
            date=dt.datetime.strptime(date_string,'%m/%d/%Y').replace(tzinfo=dt.timezone.utc).strftime('%Y-%m-%dT00:00:00Z')
        except ValueError:
            continue
        end=positions[ix+1] if ix+1<len(positions) else len(lines)
        for j in range(pos+1,end):
            if re.search(r'Post.Incident Review|\bPIR\b',lines[j],re.I) and j>pos+2:
                end=j;break
        body=lines[pos+1:end]
        start=next((i+1 for i,line in enumerate(body) if line.lower().startswith('what happened')),0)
        stop=next((i for i in range(start,len(body)) if body[i].lower().startswith(('what went wrong','how did we respond','how are we making'))),len(body))
        impact=' '.join(body[start:stop])[:5000]
        region_scope=(title+' '+impact[:2800]).lower()
        italy=bool(re.search(r'\bitaly north\b|\bitalynorth\b',region_scope))
        germany=bool(re.search(r'\bgermany west central\b|\bgermanywestcentral\b|\bfrankfurt\b',region_scope))
        incidents.append({
            'id':'pir:'+tracking, 'tracking_id':tracking,'title':title,'description':impact,
            'link':HISTORY_URL,'when':date,'italy':italy,'germany':germany,
            'source':'Azure Status History (PIR pubblica)','kind':'pir',
            'impact_minutes':None,'impact_precision':'not_region_specific',
        })
    return list({x['id']:x for x in incidents}.values())
