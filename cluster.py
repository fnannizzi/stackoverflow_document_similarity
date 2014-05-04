#! /usr/bin/env python
import sys
import math
import operator
import nltk
from Queue import PriorityQueue

class Doc:
  def __lt__(self, other):
    return self.reach_dist < other.reach_dist

stopwords = []
with open('stopwords.txt') as f:
  for line in f:
    stopwords.append(line)
stopwords = set(stopwords)

def doc_stats(doc):
  stats = {}
  tokens = nltk.word_tokenize(doc.lower())
  unique = set(tokens) - stopwords
  for t in unique:
    stats[t] = tokens.count(t)
  return stats
  
def cosine_simularity(a, b):
  common_features = set(a.keys()) & set(b.keys())
  dot_prod = sum([a[x] * b[x] for x in common_features])
  sum1 = sum([a[x]**2 for x in a.keys()])
  sum2 = sum([b[x]**2 for x in b.keys()])
  denominator = math.sqrt(sum1) * math.sqrt(sum2)

  if not denominator:
    return 1.0
  else:
    return 1.0 - (float(dot_prod) / denominator)

def core_dist(p, db, eps, min_pts):
  region_points = []
  for doc in db:
    doc.score = cosine_simularity(p.freq, doc.freq)
    if doc.score <= eps:
      region_points.append(doc) 
  if len(region_points) >= min_pts:
    region_points.sort(key=operator.attrgetter('score'))
    return region_points[min_pts-1].score
  else:
    return None

def reachability_dist(p, o, db, eps, min_pts):
  region_points = []
  for doc in db:
    doc.score = cosine_simularity(p.freq, doc.freq)
    if doc.score <= eps:
      region_points.append(doc) 
  if len(region_points) >= min_pts:
    return max(cosine_simularity(o.freq, p.freq), p.core_dist)
  else:
    return None

def output_doc(d):
  if d.core_dist:
    if d.reach_dist:
      print '        MEMBER %.3f %s\n %s' % (d.reach_dist, d.title, d.body)
    else:
      print '-----'
      print 'CLUSTER START %s\n %s' % (d.title, d.body)
  else:
    print ' ~~ NOISE ~~ %s\n %s' % (d.title, d.body)
    

def update(db, neighbors, p, seeds, eps, min_pts):
  for doc in neighbors:
    if not doc.visited:
      rdist = reachability_dist(p, doc, db, eps, min_pts)
      if not doc.reach_dist:
        doc.reach_dist = rdist
        seeds.put(doc)
      elif rdist < doc.reach_dist:
        doc.reach_dist = rdist

def optics(db, eps, min_pts):
  for doc in db:
    doc.core_dist = core_dist(doc, db, eps, min_pts)
  for doc in db:
    if not doc.visited:
      neighbors = region_query(db, doc, eps)
      doc.visited = True
      output_doc(doc)
      if doc.core_dist:
        seeds = PriorityQueue()
        update(db, neighbors, doc, seeds, eps, min_pts)
        while not seeds.empty():
          q = seeds.get()
          neighbors_q = region_query(db, q, eps)
          q.visited = True
          output_doc(q)
          if q.core_dist:
            update(db, neighbors, q, seeds, eps, min_pts)

def region_query(docs, pt, eps):
  eps_region = []
  for doc in docs:
    if pt.doc_id != doc.doc_id:
      if cosine_simularity(pt.freq, doc.freq) <= eps:
        eps_region.append(doc) 
  return eps_region

raw_data = []
with open(str(sys.argv[1])) as f:
  raw_data = f.read().splitlines()

docs = []
for i in range(0,len(raw_data),3):
  doc = Doc()
  doc.doc_id = i / 3
  doc.title = raw_data[i]
  doc.tags = raw_data[i+1].split()
  doc.body = raw_data[i+2]
  doc.freq = doc_stats(doc.title + ' ' + doc.body)
  doc.reach_dist = None
  doc.core_dist = None
  doc.visited = False
  docs.append(doc)

optics(docs, float(sys.argv[2]), int(sys.argv[3]))
