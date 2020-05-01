from collections import defaultdict

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn

from strong_tacred.definitions import RELATION_DEFS


def plot_model_confusion_matrix(dataframe: pd.DataFrame,
                                ignore_label: str = "no_relation",
                                figsize=(25, 25),
                                fontsize=10,
                                title=None):
    def sort_by_arg_type(label):
        relation_def = RELATION_DEFS.get(label)
        if relation_def is None:
            return label, label

        (type_head, _), (type_tail, _) = relation_def

        return type_head, type_tail

    unique_labels = set(dataframe["true_label"].values)
    if ignore_label:
        unique_labels.remove(ignore_label)
    unique_labels = list(sorted(unique_labels, key=sort_by_arg_type))

    prediction_count = defaultdict(lambda: defaultdict(int))
    for _, row in dataframe.iterrows():
        true_label = row["true_label"]
        pred_labels = row["pred_labels"]

        for pred_label, count in pred_labels.most_common():
            prediction_count[true_label][pred_label] += count

    cm = []
    for label_actual in unique_labels:
        cm_row = []
        for label_pred in unique_labels:
            count = prediction_count[label_actual][label_pred]
            cm_row.append(count)
        cm.append(cm_row)

    df_cm = pd.DataFrame(cm, unique_labels, unique_labels)

    plt.figure(figsize=figsize, dpi=150)
    sn.set(font_scale=1.4)  #for label size
    sn.heatmap(df_cm, annot=True, fmt="", robust=True, cbar=False, annot_kws={"size": fontsize})
