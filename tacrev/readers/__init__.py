from collections import namedtuple


Document = namedtuple("Document", ["id", "tokens", "relations", "tags", "ner", "pos"])
Token = namedtuple("Token", ["text", "sent", "i", "idx"])
Relation = namedtuple("Relation", ["head", "tail", "label"])
Tag = namedtuple("Tag", ["tokens", "label", "attr"])
