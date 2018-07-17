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
    Portugues_Gloss = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    concept_class = BDConcept

    def cmd_download(self, **kw):
        #self.raw.write('sources.bib', getEvoBibAsBibtex('Cihui', **kw))
        pass

    def cmd_install(self, **kw):
        wl = lingpy.Wordlist(self.raw.posix('arawakan_swadesh_100_edictor.tsv'))

        with self.cldf as ds:
            ds.add_sources(*self.raw.read_bib())
            for k in pb(wl, desc='wl-to-cldf'):
                if wl[k, 'value']:
                    ds.add_language(
                        ID=wl[k, 'doculect'],
                        Name=wl[k, 'doculect'],
                        Glottocode='')
                    ds.add_concept(
                        ID=slug(wl[k, 'concept']),
                        Name=wl[k, 'concept'],
                        Concepticon_ID='',
                        Portuguese_Gloss=wl[k, 'concept_spanish'])
                    for row in ds.add_lexemes(
                        Language_ID=wl[k, 'doculect'],
                        Parameter_ID=slug(wl[k, 'concept']),
                        Value=wl[k, 'value'],
                        Form=wl[k, 'form'],
                        Segments=wl[k, 'segments'],
                        Source=''):
                        cid = wl[k, 'concept'] + '-' + '{0}'.format(wl[k,
                            'cogid'])
                        ds.add_cognate(
                            lexeme=row,
                            Cognateset_ID=cid,
                            Source=['Chacon2017'],
                            Alignment_Source='')
