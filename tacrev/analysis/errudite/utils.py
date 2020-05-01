from typing import List, Dict

import pandas as pd
import numpy as np
from sklearn.metrics import classification_report

from errudite.builts import Group
from errudite.targets.instance import Instance
from errudite.targets.interfaces import InstanceKey
from errudite.build_blocks.prim_funcs import prediction as get_prediction
from errudite.targets.label import PredefinedLabel


def strip_end(text, suffix):
    if not text.endswith(suffix):
        return text
    return text[:len(text)-len(suffix)]


def set_predictions_from_df(instances, dataframe: pd.DataFrame):
    for instance in instances:
        instance_in_df = dataframe.loc[instance.qid]
        predictions = []
        for model_name, prediction in instance_in_df["model_pred"].items():
            for suffix in ["_dev", "_test"]:
                model_name = strip_end(model_name, suffix)

            pred_label = PredefinedLabel(model=model_name,
                                         qid=instance.qid,
                                         text=prediction,
                                         vid=max([instance.text.vid, instance.groundtruth.vid]))
            pred_label.compute_perform(groundtruths=instance.groundtruth)
            predictions.append(pred_label)

        # set the predictions
        instance.set_entries(predictions=predictions)


def classification_report_from_instances(instances: List[Instance],
                                         model: str,
                                         ignore_label: str = None,
                                         output_dict: bool = False):
    true_labels = []
    pred_labels = []
    for instance in instances:
        true_labels.append(instance.get_entry("groundtruth").label)
        pred_labels.append(get_prediction(model, instance.get_entry("predictions")).label)

    unique_labels = set(true_labels + pred_labels)

    if ignore_label is not None and ignore_label in unique_labels:
        unique_labels.remove(ignore_label)
    
    return classification_report(true_labels,
                                 pred_labels,
                                 labels=list(sorted(unique_labels)),
                                 output_dict=output_dict,
                                 digits=4)


def classification_report_from_group(group,
                                     model: str,
                                     ignore_label: str = None,
                                     output_dict: bool = False,
                                     instance_hash: Dict[InstanceKey, Instance] = None,
                                     instance_hash_rewritten: Dict[InstanceKey, Instance] = None):

    instance_hash = instance_hash or Instance.instance_hash
    instance_hash_rewritten = instance_hash_rewritten or Instance.instance_hash_rewritten

    def get_instance_by_key(key: InstanceKey) -> Instance:
        if not key:
            return None
        if key.vid == 0 and key in instance_hash:
            return instance_hash[key]
        if key.vid != 0 and key in instance_hash_rewritten:
            return instance_hash_rewritten[key]
        return None

    instances = [get_instance_by_key(key) for key in group.get_instance_list()]

    return classification_report_from_instances(instances,
                                                model,
                                                ignore_label,
                                                output_dict)


def usefulness_score(group, model):
    stats = Group.eval_stats(group.get_instance_list(), model=model)["stats"]
    return stats["local_error_rate"] / np.abs(stats["coverage"] - 0.5)


def group_info(group_name, models):
    for model in models:
        group = Group.get(group_name)
        print("Model: ", model)
        print(Group.eval_stats(group.get_instance_list(), model=model))
        print("Usefulness: ", usefulness_score(group, model))
