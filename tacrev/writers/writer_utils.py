from typing import List, Tuple, Dict, Any

import pandas as pd

from tacrev.readers.tacred import Document
from tacrev.readers.evaluation_results import EvaluationResult


def _highlight_arguments(tokens: List[str],
                         head: Tuple[int, int],
                         tail: Tuple[int, int]) -> List[str]:
    first_arg_start, first_arg_end = head if head[0] < tail[0] else tail
    second_arg_start, second_arg_end = tail if head[0] < tail[0] else head

    head_color = "rgba(255, 0, 0, 0.5)"
    tail_color = "rgba(0, 255, 0, 0.5)"

    first_arg_color = head_color if head[0] < tail[0] else tail_color
    second_arg_color = tail_color if head[0] < tail[0] else head_color

    tokens[second_arg_start] = f'<span style="background-color:{second_arg_color};">' + tokens[second_arg_start]
    tokens[second_arg_end] = tokens[second_arg_end] + '</span>'

    tokens[first_arg_start] = f'<span style="background-color:{first_arg_color};">' + tokens[first_arg_start]
    tokens[first_arg_end] = tokens[first_arg_end] + '</span>'

    return tokens


def _mark_arguments(tokens: List[str],
                    head: Tuple[int, int],
                    tail: Tuple[int, int]) -> List[str]:
    first_arg_start, first_arg_end = head if head[0] < tail[0] else tail
    second_arg_start, second_arg_end = tail if head[0] < tail[0] else head

    first_arg_type = "HEAD" if head[0] < tail[0] else "TAIL"
    second_arg_type = "TAIL" if head[0] < tail[0] else "HEAD"

    tokens[second_arg_start] = f"<{second_arg_type}>" + tokens[second_arg_start]
    tokens[second_arg_end] = tokens[second_arg_end] + f"</{second_arg_type}>"

    tokens[first_arg_start] = f"<{first_arg_type}>" + tokens[first_arg_start]
    tokens[first_arg_end] = tokens[first_arg_end] + f"</{first_arg_type}>"

    return tokens


def documents_as_dataframe(documents: List[Document],
                           highlight_arguments: bool = False,
                           mark_arguments: bool = False) -> pd.DataFrame:

    highlight = (lambda x: x)
    if highlight_arguments:
        highlight = _highlight_arguments
    if mark_arguments:
        highlight = _mark_arguments

    rows = []
    for doc in documents:
        tokens = [token.text for token in doc.tokens]
        head_tokens = doc.tags[0].tokens
        tail_tokens = doc.tags[1].tokens

        head = head_tokens[0].i, head_tokens[-1].i
        tail = tail_tokens[0].i, tail_tokens[-1].i

        rows.append({
                "id": doc.id,
                "text": " ".join(highlight(tokens, head, tail)),
                "true_label_reannotated": doc.relations[0].label,
                "head_span": head,
                "tail_span": tail,
                "num_tokens": len(tokens),
                # "tags": doc.tags,
                # "ner": doc.ner,
                # "pos": doc.pos
        })

    dataframe = pd.DataFrame(rows)
    dataframe = dataframe.set_index("id")

    return dataframe


def results_as_dataframe(results: List[EvaluationResult]) -> pd.DataFrame:
    def as_dict(result: EvaluationResult) -> Dict[str, Any]:
        dct = result._asdict()
        dct.update({
                "pred_label": result.pred_labels.most_common(1)[0][0],
                "num_predicted": len(result.pred_labels)
        })
        return dct

    dataframe = pd.DataFrame([as_dict(result) for result in results])
    dataframe = dataframe.set_index("id")
    return dataframe
