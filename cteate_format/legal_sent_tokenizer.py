import re
from nltk.tokenize.punkt import PunktSentenceTokenizer
from utils import flatten_list, slice_string_by_indices

tokenizer = PunktSentenceTokenizer()


def merge_multiple_tokens(sentence, delimiter=' '):
    """
    Объединяет группу токенов формата (text, (start, end)) в один токен (text, (start, end)),
    где start - начало первого токена, а end - конец последнего.
    :param sentence: list of tokens
    :param delimiter: pattern for join function
    :return:
    """
    start = sentence[0][1][0]
    end = sentence[-1][1][1]
    text = delimiter.join([text for text, spans in sentence])
    return (text, (start, end))


def get_full_text_spans(nltk_spans, spans):
    """

    :param nltk_spans:
    :param spans:
    :return:
    """
    full_text_spans = []
    number_slice_start, _ = spans
    for span in nltk_spans:
        start, end = span
        end = end + number_slice_start
        start = start + number_slice_start
        full_text_spans.append((start, end))
    return full_text_spans


def align_spans(number_slices):
    """
    Выравнивает спаны
    :param number_slices: list
    :return: list
    """
    spans = []
    for number_text, number_spans in number_slices:
        # этот кусок разделяем обычным токенизатором нлтк
        nltk_sentences = tokenizer.tokenize(number_text)
        # достаем спаны этих предложений, проблема в том, что начинаются с нуля для каждого слайса
        nltk_spans = list(tokenizer.span_tokenize(number_text, realign_boundaries=True))
        full_text_spans = get_full_text_spans(nltk_spans, number_spans)
        nltk_tokens = list(zip(nltk_sentences, full_text_spans))
        spans.append(nltk_tokens)
    return spans


def merge_tokens_by_pattern(spans, merge_pattern, delimiter=''):
    sentences = []
    sentence = []
    for sent_with_spans in spans:
        last_text, last_spans = sent_with_spans[-1]
        if merge_pattern.search(last_text):
            s = merge_multiple_tokens(sent_with_spans)
            sentence.append(s)
        else:
            sent_with_spans = merge_multiple_tokens(sent_with_spans)
            sentence.append(sent_with_spans)
            if len(sentence) > 1:
                sentence = [merge_multiple_tokens(sentence, delimiter)]
            sentences.append(sentence)
            sentence = []
    return sentences


def slice_by_numbers(text, split_pattern):
    """
    Борется с частой ошибкой в распознанных текстах, когда номер пункта "приклеивается" к предыдущему тексту,
    из-за чего токенизатор не видит границы нового предложения.
    :param text: str
    :return: list of strings
    """
    indices = [i.span()[0]+1 for i in re.finditer(split_pattern, text)]
    indices.insert(0, 0)
    parts = slice_string_by_indices(indices, text)
    assert len(text) == len(''.join(parts))
    number_tokens = []
    previous = 0
    for i in list(zip(parts, indices)):
        text, start = i
        assert previous == start
        number_tokens.append((text, (start, start+len(text))))
        previous = start + len(text)
    return number_tokens


class LegalSentenceTokenizer:
    def __init__(self):
        self.text = ''
        self.tokens = []
        self.spans = []

    def _slices_from_text(self, text):
        # паттерн для номеров пункта
        #number_pattern = re.compile("[А-яа-яё:;|,.\s]\d{1,3}[.,]")
        # нарезаем текст по номерам пункта
        #number_slices = slice_by_numbers(text, split_pattern=number_pattern)
        # после этого нарезаем текст с помощью нлтк-токенизатора
        new_spans = align_spans(number_slices)
        # паттерн для склеивания текста обратно, если там сокращение "ст.4.4 УК"
        contraction_pattern = re.compile("(?:^|\s)((([а-я]|\d{1,3})[.,]){1,6}|ст.)$")
        # паттерн для склеивания текста, если это "пункт 4.4"
        punkt_pattern = re.compile("пункт(|а|у|ом|е|ы|ов|ам|ах|ами|)$")
        # склеиваем по сокращениям
        sentences = merge_tokens_by_pattern(new_spans, contraction_pattern)
        # склеиваем по слову "пункт"
        sentences = merge_tokens_by_pattern(sentences, punkt_pattern, delimiter=' ')
        sentences = flatten_list(sentences)
        tokens, spans = list(zip(*sentences)) #TODO то же самое нарезается в tokenize, подумать, как туда пересохранить
        # список спанов
        return spans

    def tokenize(self, text):
        return list(self.sentences_from_text(text))

    def span_tokenize(self, text):
        slices = self._slices_from_text(text)
        for sl in slices:
            yield sl

    def sentences_from_text(self, text):
        return [text[s:e] for s, e in self.span_tokenize(text)]




