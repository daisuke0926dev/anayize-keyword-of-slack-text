from array import array
import pke
import separatingWords


def getKeywordAndImportance():
    extractor = pke.unsupervised.MultipartiteRank()
    # for return
    word_and_importance = {}

    separated_words_massage_array = separatingWords.separete()
    for separated_words_massage in separated_words_massage_array:
        extractor.load_document(input=separated_words_massage, language='ja', normalization=None)
        extractor.candidate_selection(pos={'NOUN', 'PROPN', 'ADJ', 'NUM'})
        extractor.candidate_weighting(threshold=0.74, method='average', alpha=1.1)
        temp = extractor.get_n_best(3)
        if(len(temp) > 0):
            for hash in temp:
                word, importance = hash
                if(word in word_and_importance):
                    word_and_importance[word] = word_and_importance[word] + importance
                else:
                    word_and_importance[word] = importance
    return word_and_importance