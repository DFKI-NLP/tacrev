from typing import List

import csv
from collections import defaultdict

from tacrev.readers.tacred import Document


def doc_to_webanno_v3(doc: Document) -> List[List[str]]:
    header = [
            ["#FORMAT=WebAnno TSV 3.2"],
            ["#T_SP=webanno.custom.NamedEntityTACRED|value"],
            ["#T_RL=webanno.custom.RelationTACRED|value|BT_webanno.custom.NamedEntityTACRED"],
            [],
            []
    ]

    token_ids = [f"{token.sent}-{token.i+1}" for token in doc.tokens]
    token_spans = [f"{token.idx}-{token.idx+len(token.text)}" for token in doc.tokens]
    token_texts = [token.text for token in doc.tokens]

    token_types = len(doc.tokens) * ["_"]
    for tag_id, tag in enumerate(doc.tags, start=1):
        for token in tag.tokens:
            token_types[token.i] = f"{tag.label}[{tag_id}]"

    relations_grouped = defaultdict(list)
    for relation in doc.relations:
        relations_grouped[relation.tail].append((relation))

    relation_tags = len(doc.tokens) * ["_"]
    relation_heads = len(doc.tokens) * ["_"]
    for tail, relations in relations_grouped.items():
        r_tags = []
        r_heads = []
        for relation_id, relation in enumerate(relations, start=1):
            head = relation.head
            r_tags.append(f"{relation.label}[{relation_id}]")
            r_heads.append(f"{head.sent}-{head.i+1}")

        relation_tags[tail.i] = "|".join(r_tags)
        relation_heads[tail.i] = "|".join(r_heads)

    rows = list(header)
    rows.append(["#Text=" + " ".join(token_texts)])

    rows += list(zip(token_ids, token_spans, token_texts,
                     token_types, relation_tags, relation_heads))

    return rows


def save_as_tsv(rows: List[List[str]], path: str) -> None:
    with open(path, "w") as tsv_file:
        writer = csv.writer(tsv_file, delimiter='\t',
                            quotechar=None, quoting=csv.QUOTE_NONE)
        for row in rows:
            writer.writerow(row)
