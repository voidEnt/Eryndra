#!/usr/bin/env python3
"""Independent static checks for MAP-001 pass 01; never substitutes for MZ editor-open.
Usage: python validate_candidate.py candidate.json SampleGenerated.zip
"""
import collections, hashlib, json, pathlib, sys, zipfile
map_path, archive = map(pathlib.Path, sys.argv[1:3])
m = json.loads(map_path.read_text())
z = zipfile.ZipFile(archive)
tilesets = json.loads(z.read(next(n for n in z.namelist() if n.endswith('/data/Tilesets.json'))))
flags = tilesets[4]['flags']
checks = []
def check(name, passed, details=None):
    checks.append({'check':name,'status':'PASS' if passed else 'FAIL','details':details})
check('canvas', m.get('width')==29 and m.get('height')==21)
check('six integral layers',len(m.get('data',[]))==29*21*6 and all(type(v) is int and v>=0 for v in m['data']))
if not all(c['status']=='PASS' for c in checks):
    print(json.dumps(checks,indent=2));sys.exit(1)
w,h=29,21
def tile(x,y,layer):return m['data'][(layer*h+y)*w+x]
check('sample fixture tileset only',m.get('tilesetId')==4)
check('empty display name',m.get('displayName')=='')
check('no encounters or autoplay',m.get('encounterList')==[] and m.get('autoplayBgm') is False and m.get('autoplayBgs') is False)
check('no parallax or loop',m.get('scrollType')==0 and m.get('parallaxName')=='' and not m.get('parallaxLoopX') and not m.get('parallaxLoopY'))
check('zero regions',all(tile(x,y,5)==0 for y in range(h) for x in range(w)))
check('valid shadow bits',all(0<=tile(x,y,4)<=15 for y in range(h) for x in range(w)))
anchors=[('EV_Story_PrologueOpening',14,10),('EV_Story_PrologueOmen',14,10),('EV_Visual_FracturedRing',14,6),('EV_FX_DustTremor',14,12),('EV_Camera_Chamber',14,10),('EV_Camera_Ring',14,8)]
events=m.get('events',[])
check('exactly six events plus null zero',len(events)==7 and events[0] is None)
for i,(name,x,y) in enumerate(anchors,1):
    e=events[i] if len(events)>i else {}
    check(f'anchor {i} identity and location',(e.get('id'),e.get('name'),e.get('x'),e.get('y'))==(i,name,x,y))
    pages=e.get('pages',[])
    ok=len(pages)==1
    if ok:
        p=pages[0];im=p.get('image',{});co=p.get('conditions',{})
        ok=(p.get('trigger')==0 and p.get('priorityType')==0 and p.get('through') is True and p.get('moveType')==0 and p.get('moveRoute',{}).get('list')==[{'code':0,'parameters':[]}] and im.get('tileId')==0 and im.get('characterName')=='' and p.get('list')==[{'code':0,'indent':0,'parameters':[]}] and all(co.get(k) is False for k in ['actorValid','itemValid','selfSwitchValid','switch1Valid','switch2Valid','variableValid']))
    check(f'anchor {i} inert unconditional blank page',ok)
used=sorted({tile(x,y,l) for l in range(4) for y in range(h) for x in range(w)})
check('tile flags exist',all(0<=t<len(flags) for t in used))
check('ring reservation has wall backing and no upper graphics',all(flags[tile(x,y,0)]&15==15 and all(tile(x,y,l)==0 for l in (1,2,3)) for y in range(4,8) for x in range(12,17)))
manifest=json.loads(map_path.with_name('Tile_Dependency_Manifest.json').read_text())
entries=manifest['tiles']
check('manifest tile coverage and flags',set(e['tile_id'] for e in entries)==set(used)-{0} and all(e['flag_decimal']==flags[e['tile_id']] and e['passage_bits']==flags[e['tile_id']]&15 and e['count']==m['data'][:w*h*4].count(e['tile_id']) for e in entries))
check('manifest sample provenance and isolated dependency',manifest['sample_archive_sha256']==hashlib.sha256(archive.read_bytes()).hexdigest() and manifest['review_fixture_tileset_id']==4 and manifest['production_tileset_id'] is None)

# Mirrors the supplied MZ Game_Map.checkPassage, layeredTiles order 3,2,1,0.
# Stubs have no tile graphics, so tileEventsXy contributes nothing.
def passage(x,y,bit):
    for l in (3,2,1,0):
        flag=flags[tile(x,y,l)]
        if flag&0x10:continue
        if flag&bit==0:return True
        if flag&bit==bit:return False
    return False
outer=[(x,y) for y in range(h) for x in range(w) if not (5<=x<=23 and 4<=y<=17)]
leaks=[(x,y) for x,y in outer if any(passage(x,y,b) for b in (1,2,4,8))]
check('outer buffer blocks all four directions',not leaks,{'tested_cells':len(outer),'leaks':leaks})
check('no ladder counter damage flags',not any(flags[t]&0x1a0 for t in used))
seen={(14,10)};q=collections.deque(seen)
forbidden=[]
while q:
    x,y=q.popleft()
    for dx,dy,b,reverse in [(0,1,1,8),(-1,0,2,4),(1,0,4,2),(0,-1,8,1)]:
        a,c=x+dx,y+dy
        if 0<=a<w and 0<=c<h and passage(x,y,b) and passage(a,c,reverse) and (a,c) not in seen:
            seen.add((a,c));q.append((a,c))
check('floor cannot escape sealed chamber',not any(p in seen for p in outer),{'reachable_from_14_10':len(seen)})
# Detect disconnected walkable areas, without imposing player-pathing as a gameplay goal.
walkable={(x,y) for y in range(h) for x in range(w) if any(passage(x,y,b) for b in (1,2,4,8))}
check('one connected walkable chamber',walkable==seen,{'walkable_cells':len(walkable),'disconnected':sorted(walkable-seen)})
for name,cx,cy in [('default',14,10),('alternate',14,8)]:
    bounds=(cx-8,cy-6,cx+8,cy+6)
    a,b,c,d=bounds
    check(f'{name} camera within map and full ring rectangle visible',a>=0 and b>=0 and c<w and d<h and a<=12<=16<=c and b<=4<=7<=d,{'tile_bounds_inclusive':bounds})
result={'map_sha256':hashlib.sha256(map_path.read_bytes()).hexdigest(),'sample_archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'checks':checks,'tile_flags':{str(t):flags[t] for t in used},'mz_editor_open':'NOT RUN','scope':'Independent static JSON, exact anchors, tile-flag collision and camera bounds; visual/canon review recorded separately.'}
print(json.dumps(result,indent=2))
sys.exit(1 if any(c['status']=='FAIL' for c in checks) else 0)
