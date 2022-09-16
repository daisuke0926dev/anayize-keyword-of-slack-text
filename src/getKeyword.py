import pke
import separatingWords

extractor = pke.unsupervised.MultipartiteRank()

separated_words_massage_array = separatingWords.separete()
for separated_words_massage in separated_words_massage_array:
    extractor.load_document(input=separated_words_massage, language='ja', normalization=None)
    extractor.candidate_selection(pos={'NOUN', 'PROPN', 'ADJ', 'NUM'})
    extractor.candidate_weighting(threshold=0.74, method='average', alpha=1.1)
    print(extractor.get_n_best(3))