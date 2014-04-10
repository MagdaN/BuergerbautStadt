#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json,sys,os

# Directory prüfen und an PYTHONPATH anhängen
if os.path.isfile('bbs/settings.py'):
    sys.path.append(os.getcwd())
else:
    sys.exit('Error: not in the root directory of the django project.');

# Environment setzen und Models importieren
os.environ['DJANGO_SETTINGS_MODULE'] = 'bbs.settings'
from projects.models import Bezirk,Ort,Veroeffentlichung, Verfahrensschritt, Behoerde

try:
    veroeffentlichungen_file = sys.argv[1]
    orte_data = sys.argv[2]
except IndexError:
    sys.exit('Usage: bin/insert-bbs.py VEROEFFENLICHUNGENFILE ORTEFILE')

veroeffentlichungen_data = json.load(veroeffentlichungen_file)
orte_data = json.load(open(orte_file))

orte_dict = {}
for ort in orte_data:
    fields = ort['fields']
    orte_dict[ort['pk']] = fields['bezeichner']

for v in veroeffentlichung_data:
    fields = v['fields']
    
    ort_pk                      = fields['ort']
    verfahrensschritt_data      = fields['verfahrensschritt']
    beginn_data                 = fields['beginn']
    ende_data                   = fields['ende']
    behoerde_data               = fields['behoerde']

    updated_data                = fields['updated']
    zeiten_data                 = fields['zeiten']    
    created_data                = fields['created']    
    auslegungsstelle_data       = fields['auslegungsstelle']
    beschreibung_data           = fields['beschreibung']    
    link_data                   = fields['link']    
        
    ort_bezeichner = orte_dict[ort_pk].replace(" ","")
    verfahrensschritt = Verfahrensschritt.objects.get(pk=verfahrensschritt_data)
    behoerde = Behoerde.objects.get(pk=behoerde_data)

    try:
        ort = Ort.objects.get(bezeichner=ort_bezeichner)        
        v = Veroeffentlichung.objects.create(ort=ort, verfahrensschritt=verfahrensschritt, beginn=beginn_data, ende=ende_data, behoerde=behoerde, updated = updated_data, zeiten = zeiten_data, created = created_data, auslegungsstelle = auslegungsstelle_data, beschreibung = beschreibung_data, link = link_data)       
    except:
        print 'Error: could not find: ' + str(orte_dict[fields['ort']].replace(" ",""))