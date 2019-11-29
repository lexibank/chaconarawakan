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
            "Aikhenvald 2001": "aikhenvald_dicionario_2001",
        }

        # add source
        args.writer.add_sources()

        # add languages
        languages = args.writer.add_languages(lookup_factory="Name")

        # add concepts
        concepts = args.writer.add_concepts(
            id_factory=lambda c: "%s_%s"
            % (c.id.split("-")[-1], slug(c.english)),
            lookup_factory="Name",
        )

        # Hard-coded fixes to segment errors in raw source
        segments = {
            "?": "ʔ",
            "'": "ʔ",
            "')": "ʔ",
            "'a": "ʔ a",
            "'e": "ʔ e",
            "'i": "ʔ i",
            "'í": "ʔ í/i",
            "'o": "ʔ o",
            "'u": "ʔ u",
            "(h": "h",
            ")h": "h",
            "∫": "ʃ",
            "á:": "á:/aː",
            "á": "á/a",
            "à": "à/a",
            "ch": "ʃ",
            "čh": "tʃʰ",
            "é:": "é:/eː",
            "é": "é/e",
            "è": "è/e",
            "ê": "ê/e",
            "éː": "éː/eː",
            "éh": "é/e h",
            "hn": "ʰn",
            "hɲ": "ʰɲ",
            "hr": "hɾ",
            "hɾ": "h ɾ",
            "hw": "h w",
            "í:": "í:/iː",
            "í": "í/i",
            "í́": "í/i",
            "ì": "ì/i",
            "Ih": "ɪ h",
            "íí": "íí/iː",
            "J": "ʒ",
            "ǰ": "ʒ",
            "jβ": "j β",
            "kh": "kʰ",
            "lh": "ʎ",
            "ll": "lː",
            "mh": "mʰ",
            "nh": "ɲ",
            "ñh": "ɲ",
            "ó": "ó/o",
            "ô": "ô/o",
            "ph": "pʰ",
            "rh": "rʰ",
            "ɻh": "ɻ h",
            "š": "ʃ",
            "th": "tʰ",
            "tsh": "tsʰ",
            "tʃh": "tʃʰ",
            "ú:": "ú:/uː",
            "ú": "ú/u",
            "ù": "ù/u",
            "úú": "ú:/uː",
            "wh": "w h",
            "ʔh": "ʔ h",
            "ʔʒ": "ʔ ʒ",
        }

        # read raw wordlist add lexemes
        wl_file = self.raw_dir / "arawakan_swadesh_100_edictor.tsv"
        wl = lingpy.Wordlist(wl_file.as_posix())

        for idx in progressbar(wl, desc="makecldf"):
            if wl[idx, "value"]:
                lex = args.writer.add_form_with_segments(
                    Language_ID=languages[wl[idx, "doculect"]],
                    Parameter_ID=concepts[wl[idx, "concept"]],
                    Value=wl[idx, "value"],
                    Form=wl[idx, "form"],
                    Segments=" ".join(
                        [
                            segments.get(x, x)
                            for x in wl[idx, "segments"]
                            if x not in ["(", ")", "[", "]"]
                        ]
                    ).split(),
                    Source=src.get(wl[idx, "source"], ""),
                )

                # add cognate
                args.writer.add_cognate(
                    lexeme=lex,
                    Cognateset_ID=wl[idx, "cogid"],
                    Source=["Chacon2017"],
                )
