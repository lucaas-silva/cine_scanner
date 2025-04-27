import re

class CommentEvaluator:
    positive_patterns = [
        r'\bmaravilhoso\b', r'\bmaravilhosa\b', r'\bmaravilhosos\b', r'\bmaravilhosas\b',
        r'\bincrível\b', r'\bincríveis\b',
        r'\bgostei\b', r'\bamazing\b', r'\bperfeito\b', r'\bperfeita\b', r'\bperfeitos\b', r'\bperfeitas\b',
        r'\bexcelente\b', r'\bexcelentes\b',
        r'\bsensacional\b', r'\bsensacionais\b',
        r'\bemocionante\b', r'\bemocionantes\b',
        r'\bespetacular\b', r'\bespetaculares\b',
        r'\bfenomenal\b', r'\bfenomenais\b',
        r'\bfantástico\b', r'\bfantástica\b', r'\bfantásticos\b', r'\bfantásticas\b',
        r'\bdivertido\b', r'\bdivertida\b', r'\bdivertidos\b', r'\bdivertidas\b',
        r'\bengraçado\b', r'\bengraçada\b', r'\bengraçados\b', r'\bengraçadas\b',
        r'\bimpactante\b', r'\bimpactantes\b',
        r'\bprofundo\b', r'\bprofunda\b', r'\bprofundos\b', r'\bprofundas\b',
        r'\bapaixonante\b', r'\bapaixonantes\b',
        r'\bmemorável\b', r'\bmemoráveis\b',
        r'\bimpressionante\b', r'\bimpressionantes\b',
        r'\binteressante\b', r'\binteressantes\b',
        r'\bmagnífico\b', r'\bmagnífica\b', r'\bmagníficos\b', r'\bmagníficas\b',
        r'\bviciante\b', r'\bviciantes\b',
        r'\búnico\b', r'\búnica\b', r'\búnicos\b', r'\búnicas\b',
        r'\brefrescante\b', r'\brefrescantes\b',
        r'\bmarcante\b', r'\bmarcantes\b',
        r'\bdeslumbrante\b', r'\bdeslumbrantes\b',
        r'\barrebatador\b', r'\barrebatadora\b', r'\barrebatadores\b', r'\barrebatadoras\b',
        r'\bpositivo\b', r'\bpositiva\b', r'\bpositivos\b', r'\bpositivas\b',
        r'\bdivino\b', r'\bdivina\b', r'\bdivinos\b', r'\bdivinas\b',
        r'\bradiante\b', r'\bradiantes\b',
        r'\bgenuíno\b', r'\bgenuína\b', r'\bgenuínos\b', r'\bgenuínas\b',
        r'\bcativante\b', r'\bcativantes\b',
        r'\bemocional\b', r'\bemocionais\b',
        r'\bextraordinário\b', r'\bextraordinária\b', r'\bextraordinários\b', r'\bextraordinárias\b',
        r'\bprimoroso\b', r'\bprimorosa\b', r'\bprimorosos\b', r'\bprimorosas\b',
        r'\bbom\b', r'\bboa\b', r'\bbons\b', r'\bboas\b'
    ]
    negative_patterns = [
        r'\bhorrível\b', r'\bhorríveis\b',
        r'\bpéssimo\b', r'\bpéssima\b', r'\bpéssimos\b', r'\bpéssimas\b',
        r'\bodiei\b', r'\bodeio\b',
        r'\bterrível\b', r'\bterríveis\b',
        r'\bdecepcionante\b', r'\bdecepcionantes\b',
        r'\bchato\b', r'\bchata\b', r'\bchatos\b', r'\bchatas\b',
        r'\bfraco\b', r'\bfraca\b', r'\bfracos\b', r'\bfracas\b',
        r'\bruim\b', r'\bruins\b',
        r'\bmorno\b', r'\bmorna\b', r'\bmornos\b', r'\bmornas\b',
        r'\barrastado\b', r'\barrastada\b', r'\barrastados\b', r'\barrastadas\b',
        r'\bprevisível\b', r'\bprevisíveis\b',
        r'\bsonolento\b', r'\bsonolenta\b', r'\bsonolentos\b', r'\bsonolentas\b',
        r'\bconfuso\b', r'\bconfusa\b', r'\bconfusos\b', r'\bconfusas\b',
        r'\bcansativo\b', r'\bcansativa\b', r'\bcansativos\b', r'\bcansativas\b',
        r'\bmedíocre\b', r'\bmedíocres\b',
        r'\bforçado\b', r'\bforçada\b', r'\bforçados\b', r'\bforçadas\b',
        r'\bdesinteressante\b', r'\bdesinteressantes\b',
        r'\bdesgastado\b', r'\bdesgastada\b', r'\bdesgastados\b', r'\bdesgastadas\b',
        r'\bsuperficial\b', r'\bsuperficiais\b',
        r'\binconsistente\b', r'\binconsistentes\b',
        r'\bsem\s+graça\b', r'\bsem\s+graças\b',
        r'\bsaturado\b', r'\bsaturada\b', r'\bsaturados\b', r'\bsaturadas\b',
        r'\brepetitivo\b', r'\brepetitiva\b', r'\brepetitivos\b', r'\brepetitivas\b',
        r'\bproblemático\b', r'\bproblemática\b', r'\bproblemáticos\b', r'\bproblemáticas\b',
        r'\bfrustrante\b', r'\bfrustrantes\b',
        r'\binsosso\b', r'\binsossa\b', r'\binsossos\b', r'\binsossas\b',
        r'\bobscuro\b', r'\bobscura\b', r'\bobscuros\b', r'\bobscuras\b',
        r'\bdesnecessário\b', r'\bdesnecessária\b', r'\bdesnecessários\b', r'\bdesnecessárias\b',
        r'\bpretensioso\b', r'\bpretensiosa\b', r'\bpretensiosos\b', r'\bpretensiosas\b',
        r'\bdesleixado\b', r'\bdesleixada\b', r'\bdesleixados\b', r'\bdesleixadas\b',
        r'\bcaricato\b', r'\bcaricata\b', r'\bcaricatos\b', r'\bcaricatas\b',
        r'\bmalfeito\b', r'\bmalfeita\b', r'\bmalfeitos\b', r'\bmalfeitas\b',
        r'\banticlimático\b', r'\banticlimática\b', r'\banticlimáticos\b', r'\banticlimáticas\b',
        r'\btruncado\b', r'\btruncada\b', r'\btruncados\b', r'\btruncadas\b',
        r'\bdecepção\b', r'bpior'
]

    def detect_negation(self, comment, match_start_index):
        """
        Detects whether a negation occurs before a match in the comment.
        A negation is typically a word like 'não', 'nem', 'nunca', 'jamais'.
        """
        negations = ['não', 'nem', 'nunca', 'jamais']
        # Check the window of text before the match (up to 10 characters before)
        window = comment[max(0, match_start_index - 10):match_start_index].lower()
        
        # Check if any negation word is present in the window
        for neg in negations:
            if neg in window:
                return True
        return False

    def evaluate_comment(self, comment, is_fragment=False):
        comment = comment.strip()
        
        if not is_fragment and len(comment) > 50:  
            fragments = re.split(r'[.,;!?]', comment)
            results = {'positive': 0, 'negative': 0, 'neutral': 0}

            for fragment in fragments:
                fragment = fragment.strip()
                if fragment:
                    result = self.evaluate_comment(fragment, is_fragment=True)
                    results[result] += 1

            if results['positive'] > results['negative']:
                return 'positive'
            elif results['negative'] > results['positive']:
                return 'negative'
            else:
                return 'neutral'

        positive_count = 0
        negative_count = 0
        comment_lower = comment.lower()

        for pattern in self.positive_patterns:
            positive_count += len(re.findall(pattern, comment_lower))

        for pattern in self.negative_patterns:
            negative_count += len(re.findall(pattern, comment_lower))

        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
