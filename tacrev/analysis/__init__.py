from typing import List, Tuple, Optional

import pandas as pd


def true_pred_labels_from_dataframe(dataframe: pd.DataFrame,
                                    ignore_label: str,
                                    true_label_col: str = "true_label",
                                    model_name: Optional[str] = None) -> Tuple[List[str],
                                                                               List[str],
                                                                               List[str]]:
    true_labels = dataframe[true_label_col].values
    if model_name:
        pred_labels = dataframe["model_pred"].apply(lambda p: p[model_name])
    else:
        pred_labels = dataframe["pred_label"]

    unique_labels = set()
    unique_labels.update(true_labels)
    unique_labels.update(pred_labels)

    if ignore_label:
        unique_labels.remove(ignore_label)
    unique_labels = list(unique_labels)

    return true_labels, pred_labels, unique_labels


def add_annotation_labels_to_df(dataframe, path: str, from_column: str, new_column: str, n_rows: int):
    df_annotations = pd.read_excel(path, usecols=["id", from_column], index_col=0, nrows=n_rows)
    df_with_annotations = dataframe.merge(df_annotations, left_index=True, right_on="id", how="left").rename(columns={from_column: new_column})
    df_with_annotations[new_column].fillna(df_with_annotations["true_label"], inplace=True)

    return df_with_annotations
