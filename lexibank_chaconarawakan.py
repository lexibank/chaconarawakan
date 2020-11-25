import attr
import lingpy
from clldutils.misc import slug
from clldutils.path import Path
from pylexibank import Concept
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.util import progressbar


@attr.s
class CustomConcept(Concept):
    Portuguese_Gloss = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "chaconarawakan"
    concept_class = CustomConcept

    def cmd_makecldf(self, args):
        # sources are poorly annotated, so we need to correct manually
        src = {
            "H&R92": "huber_vocabulario_1992",
            "H&R 1992": "huber_vocabulario_1992",
            "Melendez 2011": "melendez_lozano_diccionario_2011",
            "Allin 1979": "allin_vocabulario_1979",
            "Aikhenvald 2012": "aikhenvald_dicionario_2012",
            "Aikenvald2001": "aihenvald_dicionario_2001",
            "Oliveira 93": "cunha_de_oliveira_uma_1993",
            "Ramirez2001": "ramirez_dicionario_2001",
            "Ramirez 2001": "ramirez_dicionario_2001",
            "Schauer 2005": "schauer_diccionario_2005",
            "Aikhenvald 2001": "aikhenvald_dicionario_2001",
        }

        # add source
        args.writer.add_sources()

        # add languages
        languages = args.writer.add_languages(lookup_factory="Name")

        # add concepts
        concepts = args.writer.add_concepts(
            id_factory=lambda c: "%s_%s" % (c.id.split("-")[-1], slug(c.english)),
            lookup_factory="Name",
        )

        # read raw wordlist add lexemes
        wl_file = self.raw_dir / "arawakan_swadesh_100_edictor.tsv"
        wl = lingpy.Wordlist(wl_file.as_posix())

        for idx in progressbar(wl, desc="makecldf"):
            if wl[idx, "value"]:
                if wl[idx, 'segments'][0] == '_':
                    wl[idx, 'segments'] = wl[idx, 'segments'][1:]
                lex = args.writer.add_form_with_segments(
                    Language_ID=languages[wl[idx, "doculect"]],
                    Parameter_ID=concepts[wl[idx, "concept"]],
                    Value=wl[idx, "value"],
                    Form=wl[idx, "form"],
                    Segments=wl[idx, "segments"],
                    Source=src.get(wl[idx, "source"], "Chacon2017"),
                )

                # add cognate
                args.writer.add_cognate(
                    lexeme=lex, Cognateset_ID=wl[idx, "cogid"], Source=["Chacon2017"]
                )
