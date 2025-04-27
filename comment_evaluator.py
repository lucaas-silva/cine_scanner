import re

class CommentEvaluator:
    positive_patterns = [
        r'\bmaravilhoso\b', r'\bincrível\b', r'\bgostei\b', r'\bamazing\b', r'\bperfeito\b',
        r'\bexcelente\b', r'\bsensacional\b', r'\bemocionante\b'
    ]
    negative_patterns = [
        r'\bhorrível\b', r'\bpéssimo\b', r'\bodiei\b', r'\bterrível\b', r'\bdecepcionante\b',
        r'\bchato\b', r'\bfraco\b', r'\bruim\b'
    ]

    def detect_negation(self, comment, match_start_index):
        window = comment[max(0, match_start_index - 10):match_start_index].lower()
        return 'não' or 'nao' or 'nem' in window

    def evaluate_comment(self, comment):
        positive_count = 0
        negative_count = 0
        comment_lower = comment.lower()

        for pattern in self.positive_patterns:
            for match in re.finditer(pattern, comment_lower):
                if self.detect_negation(comment_lower, match.start()):
                    negative_count += 1
                else:
                    positive_count += 1

        for pattern in self.negative_patterns:
            for match in re.finditer(pattern, comment_lower):
                if self.detect_negation(comment_lower, match.start()):
                    positive_count += 1
                else:
                    negative_count += 1

        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
