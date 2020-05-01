from typing import List

import json
from itertools import accumulate, groupby

from tacrev.readers import Document, Relation, Tag, Token


def load_tacred(path: str) -> List[Document]:
    with open(path, "r") as input_f:
        dataset = json.load(input_f)

        documents = []
        for example in dataset:
            raw_tokens = example["token"]
            id_ = example["id"]
            relation = example["relation"]
            head_start, head_end = example["subj_start"], example["subj_end"]
            tail_start, tail_end = example["obj_start"], example["obj_end"]
            head_tag = example["subj_type"]
            tail_tag = example["obj_type"]
            ner_tags = example["stanford_ner"]
            pos_tags = example["stanford_pos"]

            raw_token_offsets = [0] + list(accumulate([len(token)+1
                                                       for token in raw_tokens]))

            tokens = []
            for token_idx, token_text in enumerate(raw_tokens):
                tokens.append(Token(text=token_text,
                                    sent=1,
                                    i=token_idx,
                                    idx=raw_token_offsets[token_idx]))

            relations = [Relation(head=tokens[head_start],
                                  tail=tokens[tail_start],
                                  label=relation)]

            tags = []
            tags.append(Tag(tokens=[tokens[i] for i in range(head_start, head_end+1)],
                            label=head_tag, attr={"type": "arg", "arg_type": "head"}))
            tags.append(Tag(tokens=[tokens[i] for i in range(tail_start, tail_end+1)],
                            label=tail_tag, attr={"type": "arg", "arg_type": "tail"}))

            start_idx = 0
            tag_spans = []
            for ner_tag, group in groupby(ner_tags):
                if ner_tag == "O":
                    start_idx += len(list(group))
                    continue

                end_idx = start_idx + len(list(group))
                tag_spans.append((ner_tag, (start_idx, end_idx)))

                start_idx = end_idx

            for ner_tag, (tag_start, tag_end) in tag_spans:
                tags.append(Tag(tokens=[tokens[i] for i in range(tag_start, tag_end)],
                                label=ner_tag, attr={"type": "ner"}))

            documents.append(Document(id=id_,
                                      tokens=tokens,
                                      ner=ner_tags,
                                      pos=pos_tags,
                                      relations=relations,
                                      tags=tags))

    return documents
