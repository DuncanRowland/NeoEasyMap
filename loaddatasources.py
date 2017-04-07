import json
import urllib.request
import os.path

#Create and cache a lookup table for the old style data source ids
def allUidForGuid():
   filename='guid-to-uid.json'
   guid_to_uid={}

   if os.path.exists(filename):
      with open(filename,'r') as f:
         guid_to_uid=json.load(f)
   else:
      req = 'http://records-ws.nbnatlas.org/occurrences/search?q=*:*&facets=data_resource_uid&flimit=1999&pageSize=0'
      rsp=urllib.request.urlopen(req).readall().decode('utf-8')
      obj1=json.loads(rsp)
      for i in obj1['facetResults'][0]['fieldResult']:
         druid = i['fq'].split(':')[1].strip('\"')
         req = 'https://registry.nbnatlas.org/ws/dataResource/'+druid
         try:
            rsp=urllib.request.urlopen(req).readall().decode('utf-8')
            obj2 = json.loads(rsp)
            guid_to_uid[obj2['guid']]=obj2['uid']
         except:
            pass
      with open(filename,'w') as f:
         json.dump(guid_to_uid,f)

   return guid_to_uid

def sciNameForTVK(tvk):
   req = 'https://species-ws.nbnatlas.org/species/'+tvk
   rsp=urllib.request.urlopen(req).readall().decode('utf-8')
   obj=json.loads(rsp)
   try:
      nameString=obj['taxonConcept']['nameString']
   except:
      nameString='No taxonConcept/nameString for tvk:'+tvk
   return nameString

def comNameForTVK(tvk):
   req = 'https://species-ws.nbnatlas.org/species/'+tvk
   rsp=urllib.request.urlopen(req).readall().decode('utf-8')
   obj=json.loads(rsp)
   try:
      nameString=obj['commonNames'][0]['nameString']
   except:
      nameString=sciNameForTVK(tvk)+' (no common names)'
   return nameString

def datasourceListForDRUIDSandTVK(druids,tvk):
   req = 'http://records-ws.nbnatlas.org/occurrences/search?q=*:*&fq=lsid:'+tvk+'&facets=data_resource_uid&flimit=1999&pageSize=0'
   rsp=urllib.request.urlopen(req).readall().decode('utf-8')
   obj=json.loads(rsp)
   result=[]
   for i in obj['facetResults'][0]['fieldResult']:
      druid = i['fq'].split(':')[1].strip('\"')
      if len(druids)==0 or druid in druids:
         result.append(i['label'])
   return result
