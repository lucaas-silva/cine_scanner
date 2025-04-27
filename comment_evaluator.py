from patterns import POSITIVE, NEGATIVE
import re


class CommentEvaluator:
    positive_patterns = POSITIVE
    negative_patterns = NEGATIVE

    def detect_negation(self, comment, match_start_index):
        negations = ['não', 'nem', 'nunca', 'jamais']
        window = comment[max(0, match_start_index - 10):match_start_index].lower()

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
            for match in re.finditer(pattern, comment_lower):
                if self.detect_negation(comment, match.start()):
                    negative_count += 1
                else:
                    positive_count += 1

        for pattern in self.negative_patterns:
            for match in re.finditer(pattern, comment_lower):
                if self.detect_negation(comment, match.start()):
                    positive_count += 1
                else:
                    negative_count += 1

        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
