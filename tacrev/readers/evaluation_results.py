from typing import List

import os
import json
from collections import defaultdict, namedtuple, Counter

from tacrev.readers import Document


EvaluationResult = namedtuple("EvaluationResult",
                              ["id", "true_label", "pred_labels", "num_correct", "model_pred"])


def load_evaluation_results(path: str,
                            documents: List[Document]) -> List[EvaluationResult]:
    true_labels = defaultdict(str)
    pred_labels = defaultdict(lambda: defaultdict(int))
    model_preds = defaultdict(lambda: defaultdict(int))
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            result_path = os.path.join(dirpath, filename)
            model_name = os.path.splitext(filename)[0]
            if filename.endswith(".jsonl"):
                with open(result_path, "r") as result_f:
                    clf_results = [json.loads(line.strip()) for line in result_f]
                    for result in clf_results:
                        model_preds[result["id"]][model_name] = result["label_pred"]
                        pred_labels[result["id"]][result["label_pred"]] += 1
                        true_labels[result["id"]] = result["label_true"]
            elif filename.endswith(".txt"):
                with open(result_path, "r") as result_f:
                    labels_pred = [line.strip() for line in result_f]
                    for doc, label_pred in zip(documents, labels_pred):
                        model_preds[doc.id][model_name] = label_pred
                        pred_labels[doc.id][label_pred] += 1
                        true_labels[doc.id] = doc.relations[0].label

    eval_results = []
    for doc_id, true_label in true_labels.items():
        pred_counts = pred_labels[doc_id]
        model_pred = model_preds[doc_id]
        eval_results.append(EvaluationResult(id=doc_id,
                                             true_label=true_label,
                                             pred_labels=Counter(pred_counts),
                                             num_correct=pred_counts[true_label],
                                             model_pred=model_pred))

    return eval_results
