#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os,datetime
from django.utils.timezone import now

# Directory prüfen und an PYTHONPATH anhängen
if os.path.isfile('bbs/settings.py'):
    sys.path.append(os.getcwd())
else:
    sys.exit('Error: not in the root directory of the django project.');

# Environment setzen und Models importieren
os.environ['DJANGO_SETTINGS_MODULE'] = 'bbs.settings'
from projects.models import Bezirk,Ort,Veroeffentlichung
from news.models import Abonnent,Mail

# gegenwärtige Zeit finden
yesterday = now() - datetime.timedelta(days=1)

# neue Veröffentlichungen finden
veroeffentlichungen = Veroeffentlichung.objects.filter(created__range=[yesterday, now()]).all()

news = {}
for abonnent in Abonnent.objects.all():
    
    # die Veroeffentlichungen fuer den Abonenten sammeln
    n = []
    for bezirk in abonnent.bezirke.all():
        for veroeffentlichung in veroeffentlichungen:
            if bezirk in veroeffentlichung.ort.bezirke.all():
                n.append(veroeffentlichung)

    # Doubletten ausfiltern
    n = list(set(n))

    # an zu verschickende News anhängen
    news[abonnent.email] = n

i = 0
for email in news:
    # Mail abschicken
    if news[email]:
        i+=1
        Mail().newsletter(email,news[email])

print i,"Mails gesendet."
