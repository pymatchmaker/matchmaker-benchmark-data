"""Export every performed visit from a synthetic alignment NPZ.

The source contains repeated performance-note IDs. Match each alignment entry
to the next occurrence of that ID, preserving the alignment's occurrence order.
A dictionary mapping an ID to a single onset would discard earlier visits.
"""
from collections import Counter, defaultdict, deque
from pathlib import Path
import argparse
import numpy as np

def export(source, output):
 data=np.load(source,allow_pickle=True)
 score={str(n['id']):n for n in data['score_note_array']}
 notes=defaultdict(deque)
 for n in data['performance_note_array']: notes[str(n['id'])].append(n)
 matches=[a for a in data['alignment'] if a.get('label')=='match']
 assert Counter(a['performance_id'] for a in matches)==Counter({k:len(v) for k,v in notes.items()})
 pairs=[]
 for a in matches:
  n=notes[a['performance_id']].popleft();s=score[a['score_id']]
  assert n['pitch']==s['pitch']
  pairs.append((float(n['onset_sec']),float(s['onset_beat'])))
 assert not any(notes.values())
 pairs=np.array(pairs);pairs=pairs[np.argsort(pairs[:,0],kind='stable')]
 pairs=pairs[np.r_[True,np.diff(pairs[:,1])!=0]]
 np.savetxt(output,pairs,fmt='%.12g',delimiter='\t',header='perf_sec\tscore_beat',comments='')
 return pairs
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('output',type=Path);a=p.parse_args();g=export(a.source,a.output);print(f'{len(g)} annotated positions exported')
