#!/usr/bin/env python3
"""Reproduce the isolated candidate; requires Pillow and the supplied sample ZIP.
Usage: python build_candidate.py /path/to/02-SampleGenerated.zip
No stock assets are extracted into the repository.
"""
import sys,json,zipfile,hashlib,io,math,re
from pathlib import Path
from PIL import Image,ImageDraw
OUT=Path(__file__).resolve().parent
z=zipfile.ZipFile(sys.argv[1]); root='SampleGenerated/'
flags=json.loads(z.read(root+'data/Tilesets.json'))[4]['flags']
W,H,T=29,21,48
cells=[1536]*(W*H)+[0]*(W*H*5)
# Three-tile structural sides; north four-tile wall face, sealed south foreground.
wall=set()
for y in range(4,18):
 for x in range(5,24):
  if y<=7 or y>=16 or x<=7 or x>=21:wall.add((x,y))
  else:cells[y*W+x]=1559
for x,y in wall:
 shape=(1 if (x-1,y) not in wall else 0)+(2 if (x,y-1) not in wall else 0)+(4 if (x+1,y) not in wall else 0)+(8 if (x,y+1) not in wall else 0)
 cells[y*W+x]=7856+shape
anchors=[('EV_Story_PrologueOpening',14,10),('EV_Story_PrologueOmen',14,10),('EV_Visual_FracturedRing',14,6),('EV_FX_DustTremor',14,12),('EV_Camera_Chamber',14,10),('EV_Camera_Ring',14,8)]
events=[None]
for i,(name,x,y) in enumerate(anchors,1):
 page=dict(conditions=dict(actorId=1,actorValid=False,itemId=1,itemValid=False,selfSwitchCh='A',selfSwitchValid=False,switch1Id=1,switch1Valid=False,switch2Id=1,switch2Valid=False,variableId=1,variableValid=False,variableValue=0),directionFix=False,image=dict(characterIndex=0,characterName='',direction=2,pattern=1,tileId=0),list=[dict(code=0,indent=0,parameters=[])],moveFrequency=3,moveRoute=dict(list=[dict(code=0,parameters=[])],repeat=True,skippable=False,wait=False),moveSpeed=3,moveType=0,priorityType=0,stepAnime=False,through=True,trigger=0,walkAnime=True)
 events.append(dict(id=i,name=name,note='',pages=[page],x=x,y=y))
m=dict(autoplayBgm=False,autoplayBgs=False,battleback1Name='',battleback2Name='',bgm=dict(name='',pan=0,pitch=100,volume=90),bgs=dict(name='',pan=0,pitch=100,volume=90),disableDashing=False,displayName='',encounterList=[],encounterStep=30,height=H,note='',parallaxLoopX=False,parallaxLoopY=False,parallaxName='',parallaxShow=False,parallaxSx=0,parallaxSy=0,scrollType=0,specifyBattleback=False,tilesetId=4,width=W,data=cells,events=events)
(OUT/'Map001.json').write_text(json.dumps(m,ensure_ascii=False,separators=(',',':'))+'\n')
# Exact quarter-tile composition for selected A4 wall tiles, following sample engine table.
js=z.read(root+'js/rmmz_core.js').decode('utf-8-sig')
table=json.loads(re.search(r'Tilemap.WALL_AUTOTILE_TABLE = (\[.*?\]);',js,re.S).group(1))
sheets={k:Image.open(io.BytesIO(z.read(root+'img/tilesets/Dungeon_'+k+'.png'))).convert('RGBA') for k in ['A4','A5']}
def tile(n):
 result=Image.new('RGBA',(48,48))
 if 1536<=n<1664:
  k=n-1536; sx=(k%8)*48;sy=(k//8)*48
  return sheets['A5'].crop((sx,sy,sx+48,sy+48))
 kind=(n-2048)//48;shape=(n-2048)%48;tx=kind%8;ty=kind//8
 bx=tx*2;by=math.floor((ty-10)*2.5+(0.5 if ty%2 else 0))
 for i,(qx,qy) in enumerate(table[shape]):
  sx=(bx*2+qx)*24;sy=(by*2+qy)*24
  result.paste(sheets['A4'].crop((sx,sy,sx+24,sy+24)),((i%2)*24,(i//2)*24))
 return result
canvas=Image.new('RGB',(W*T,H*T),'black')
for y in range(H):
 for x in range(W):canvas.paste(tile(cells[y*W+x]),(x*T,y*T))
canvas.save(OUT/'Map001_Tile_Composite.png')
for label,cy in [('Default',10),('Alternate',8)]:
 crop=canvas.crop((6*T,(cy-6)*T,23*T,(cy+7)*T));crop.save(OUT/f'Camera_{label}_816x624.png')
# Review-only geometry diagrams; no image here is a runtime ring asset or lighting implementation.
review=Image.new('RGB',(1020,640),(18,21,27));d=ImageDraw.Draw(review)
d.text((20,14),'MAP-001 | RING FOOTPRINT REVIEW ONLY - NOT RUNTIME ART OR EFFECTS',fill='white')
d.text((20,36),'North wall x12..16 / y4..7. All states use the same geometry; black division stays open.',fill='#aebccc')
for k,(label,col,extent) in enumerate([('Dormant','#454d53',0),('Pulse (one-frame mock-up)','#b5d0d6',348),('Opening residual','#6c858d',22),('Closing propagated','#9aafb9',220)]):
 ox=20+(k%2)*500;oy=75+(k//2)*275
 d.text((ox,oy),label,fill='white')
 patch=canvas.crop((12*T,4*T,17*T,8*T));review.paste(patch,(ox,oy+24))
 box=(ox+34,oy+35,ox+206,oy+202)
 d.arc(box,276,624,fill='#394046',width=8)
 if extent:d.arc(box,276,276+extent,fill=col,width=4)
 d.rectangle((ox,oy+24,ox+239,oy+215),outline='#778594')
 d.text((ox+254,oy+55),'5 x 4 tile reserve',fill='#b6c2ce')
 d.text((ox+254,oy+77),'No symbols / no doorway',fill='#b6c2ce')
 d.text((ox+254,oy+99),'Deliberate top division',fill='#b6c2ce')
review.save(OUT/'Ring_State_Footprint_REVIEW_ONLY.png')
manifest=dict(sample_archive_sha256=hashlib.sha256(Path(sys.argv[1]).read_bytes()).hexdigest(),review_fixture_tileset_id=4,production_tileset_id=None,tiles=[],empty_layer_value=dict(tile_id=0,flag=flags[0],meaning='star/skip; never used as collision foundation'),camera_frames=[dict(center=[14,10],bounds_inclusive=[6,4,22,16]),dict(center=[14,8],bounds_inclusive=[6,2,22,14])],ring_rectangle_inclusive=[12,4,16,7],runtime_ring_asset=False)
for n in sorted(set(cells)-{0}):
 manifest['tiles'].append(dict(tile_id=n,sheet='Dungeon_A5.png' if n<2048 else 'Dungeon_A4.png',flag_decimal=flags[n],flag_hex=hex(flags[n]),passage_bits=flags[n]&15,ladder=bool(flags[n]&32),bush=bool(flags[n]&64),counter=bool(flags[n]&128),damage_floor=bool(flags[n]&256),terrain_tag=flags[n]>>12,purpose='solid black outer buffer' if n==1536 else 'fitted-stone floor placeholder' if n==1559 else 'sealed dark stone wall placeholder',count=cells.count(n)))
(OUT/'Tile_Dependency_Manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Built map and five PNGs; no MZ editor-open claim.')
