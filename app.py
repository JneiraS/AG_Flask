#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pg_app import initialize_database_in_threads
from pg_app.member_app.routes import render_votes_results

initialize_database_in_threads()
print(render_votes_results(2, 8))

dict_ = [{'id_livre': 2, 'nombre_de_votes': 10, 'title': 'Paris Musée du XXIe siècle'},
         {'id_livre': 4, 'nombre_de_votes': 10, 'title': 'Houris'},
         {'id_livre': 1, 'nombre_de_votes': 7, 'title': 'Tout le bruit du Guéliz'},
         {'id_livre': 5, 'nombre_de_votes': 6, 'title': 'Jacaranda'},
         {'id_livre': 3, 'nombre_de_votes': 4, 'title': "Madelaine avant l'aube"},
         {'id_livre': 6, 'nombre_de_votes': 4, 'title': 'Archipels'},
         {'id_livre': 7, 'nombre_de_votes': 3, 'title': 'La désinvolture est une bien belle chose'},
         {'id_livre': 8, 'nombre_de_votes': 2, 'title': 'Jour de ressac'}]

list_ids = [d['id_livre'] for d in dict_]
print(list_ids)
