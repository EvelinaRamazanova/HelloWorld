import json
import re
from utils import write_multiple_lines
from nltk import PunktSentenceTokenizer
from pathlib import Path
from legal_sent_tokenizer import merge_multiple_tokens


def group_tokens_by_pattern(tokens, pattern, negative_pattern):
    paragraphs = []
    for item, span in tokens:
        if not paragraphs:
            # создание списка с предложениями из параграфа
            paragraphs.append([(item, span)])
        else:
            if re.match(pattern, item) and not re.match(negative_pattern, item):
                paragraphs.append([(item, span)])
            else:
                paragraphs[-1].append((item, span))
    return paragraphs


class TextAnnotator:
    """
    Базовый класс для автоматической разметки текста,
    размечает файл со списком страниц документа
    в формате {"text" : "текст документа"}
    """
    def __init__(self, file_path, annotation_path):
        self.file_path = file_path
        self.annotation_path = annotation_path
        self.doc = ''
        self.page = {}
        self.get_labels = TextAnnotator.get_labels

    def get_labels(self):
        return self.page

    def annotate_page(self):
        self.page["labels"] = []
        self.page["meta"] = {}
        self.page["annotation_approver"] = 'null'
        self.page = self.get_labels(self)
        return self.page

    def annotate_doc(self, doc):
        # постранично
        annotated_doc = []
        for page in doc.readlines():
            self.page = json.loads(page)
            self.page = TextAnnotator.annotate_page(self)
            js_data = json.dumps(self.page, ensure_ascii=False)
            annotated_doc.append(js_data)
        return annotated_doc

    def annotate_file(self):
        with open(self.file_path, 'r') as doc:
            annotated_doc = TextAnnotator.annotate_doc(self, doc)
        with open(self.annotation_path, 'w+') as out_file:
            write_multiple_lines(out_file, annotated_doc)


class ParagraphAnnotator(TextAnnotator):
    """Класс для разметки текста договора по пунктам,
    get_labels находит спаны для каждого пункта на странице,
    добавляет в "labels" список найденных спанов
    с тегом 'punkt'
    """
    def __init__(self, file_path, annotation_path):
        super().__init__(file_path, annotation_path)
        self.get_labels = ParagraphAnnotator.get_labels
        self.number_spans = None
        self.start_positions = None
        self.paragraph_spans = None

    def get_number_spans(self):
        return [_.span() for _ in re.finditer(r'\n\d{1,2}[.,\d]+', self.page['text'])]

    def get_paragraph_start_positions(self):
        paragraph_start_positions = []
        for number_span in self.number_spans:
            paragraph_start_positions.append(number_span[0] + 1)
        # разметить последний пункт (до конца страницы)
        paragraph_start_positions.insert(len(paragraph_start_positions) + 1, len(self.page['text']))
        return paragraph_start_positions

    def add_label_names(self, label_name="podpunkt"):
        return [[s1, s2, label_name] for s1, s2 in self.paragraph_spans]

    def get_paragraph_spans(self):
        return [_ for _ in zip(self.start_positions, self.start_positions[1:])]

    def get_labels(self):
        self.number_spans = ParagraphAnnotator.get_number_spans(self)
        if self.number_spans:
            self.start_positions = ParagraphAnnotator.get_paragraph_start_positions(self)
            self.paragraph_spans = ParagraphAnnotator.get_paragraph_spans(self)
            self.page["labels"] = ParagraphAnnotator.add_label_names(self)
        return self.page


class SentenceBasedAnnotator():
    def __init__(self):
        self.text = None
        self.spans = None
        self.paragraphs = None
        self.sent_tokenizer = PunktSentenceTokenizer()

    def load_text(self, text):
        self.text = text

    def get_paragraphs(self):
        """Group list of sentences to paragraphs"""
        sentences = self.sent_tokenizer.tokenize(self.text)
        spans = self.sent_tokenizer.span_tokenize(self.text)
        sentences = zip(sentences, spans)
        paragraph_number_pattern = re.compile('^(\d{1,2}|З|Б|!)([.,]|\s)((\d{1,3}|З|Б|\!)[.,]|\s|[А-я])')
        date_pattern = re.compile('^\d{1,2}([.,])(\d{1}|10|11|12|0\d{1})[.,](1|2)\d')
        # TODO group tokens by pattern and merge tokens by pattern попробовать скомбинировать
        paragraphs = group_tokens_by_pattern(sentences, paragraph_number_pattern, date_pattern)
        paragraphs = [merge_multiple_tokens(item) for item in paragraphs]
        self.paragraphs = paragraphs
        self.tokens, self.spans = list(zip(*(paragraphs)))
        return paragraphs


source_dir = Path('/Users/Evelina/Desktop/medsi_storage/Документы для разметчика')
out_dir = source_dir / 'annotated'
if out_dir.exists() == False:
    out_dir.mkdir()
for file_path in source_dir.glob('*.json'):
    print(file_path)
    new_path = out_dir / file_path.name
    annotator = ParagraphAnnotator(file_path, new_path)
    annotator.annotate_file()
