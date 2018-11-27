# coding=utf-8
from __future__ import unicode_literals, print_function
from itertools import groupby

import attr
import lingpy
from pycldf.sources import Source

from clldutils.path import Path
from clldutils.misc import slug
from pylexibank.dataset import Metadata, Concept
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.util import pb, getEvoBibAsBibtex


@attr.s
class BDConcept(Concept):
    Portuguese_Gloss = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = 'chaconarawakan'
    concept_class = BDConcept

    def cmd_download(self, **kw):
        pass

    def cmd_install(self, **kw):

        # sources are poorly annotated, so we need to correct manually
        src = {
            "H&R92": "huber_vocabulario_1991",
            "Klumpp95": "",
            "H&R 1992": "huber_vocabulario_1991",
            "None": "",
            "Melendez 2011": "melendez_lozano_diccionario_2011",
            "Epps": "",
            "Schauer2005": "",
            "Allin 1979": "allin_vocabulario_1979",
            "Aikhenvald": "",
            "dp91": "",
            "Aikhenvald 2012": "aikhenvald_dicionario_2012",
            "Aikenvald2001": "aihenvald_dicionario_2001",
            "Oliveira 93": "cunha_de_oliveira_uma_1993",
            "Ramirez2001": "ramirez_dicionario_2001",
            "Ramirez 2001": "ramirez_dicionario_2001",
            "Schauer 2005": "schauer_diccionario_2005",
            "Aikhenvald 2001": "aikhenvald_dicionario_2001"
            }
        

        wl = lingpy.Wordlist(self.raw.posix('arawakan_swadesh_100_edictor.tsv'))
        with self.cldf as ds:
            ds.add_sources(*self.raw.read_bib())
            for l in self.languages:
                ds.add_language(
                    ID=slug(l['Name']),
                    Name=l['Name'],
                    Glottocode=l['Glottocode']
                    )
            for c in self.concepts:
                ds.add_concept(
                    ID=slug(c['ENGLISH']),
                    Name=c['ENGLISH'],
                    Concepticon_ID=c['CONCEPTICON_ID'],
                    Portuguese_Gloss=c['PORTUGUESE']
                    )

            for k in pb(wl, desc='wl-to-cldf'):
                if wl[k, 'value']:
                    for row in ds.add_lexemes(
                        Language_ID=slug(wl[k, 'doculect']),
                        Parameter_ID=slug(wl[k, 'concept']),
                        Value=wl[k, 'value'],
                        Form=wl[k, 'form'],
                        Segments=wl[k, 'segments'],
                        Source=src.get(wl[k, 'source'], '')):
                        
                        cid = slug(wl[k, 'concept'] + '-' + '{0}'.format(wl[k,
                            'cogid']))
                        ds.add_cognate(
                            lexeme=row,
                            Cognateset_ID=cid,
                            Source=['Chacon2017'],
                            Alignment=wl[k, 'alignment'],
                            Alignment_Source='Chacon2017'
                            )
