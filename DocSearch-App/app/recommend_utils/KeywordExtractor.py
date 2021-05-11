from rake_nltk import Metric, Rake


class KeywordExtractor:
    def __init__(self):
        self.extractedKeywords = []

    def rakealgo(self, abstract):
        r = Rake(min_length=1, max_length=2)
        r.extract_keywords_from_text(abstract)
        result = r.get_ranked_phrases()
        topResult = result[:10]
        self.extractedKeywords.append(topResult)
        return self.extractedKeywords