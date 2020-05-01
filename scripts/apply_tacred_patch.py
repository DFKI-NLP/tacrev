import sys
import argparse
import json
import logging
from collections import Counter

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def read_tacred(path):
    with open(path, "r") as in_f:
        return json.load(in_f)


def read_patch(path):
    with open(path, "r") as in_f:
        data = json.load(in_f)
    
    patch = {}
    for example in data:
        patch[example.pop("id")] = example
    return patch


def write_tacred(path, dataset):
    with open(path, "w") as out_f:
        json.dump(dataset, out_f)


def main():
    parser = argparse.ArgumentParser(description="Patch TACRED dataset file with improved gold standard.")

    parser.add_argument("--dataset-file", type=str, required=True, help="")
    parser.add_argument("--patch-file", type=str, required=True, help="")
    parser.add_argument("--output-file", type=str, required=True, help="")

    args = parser.parse_args()

    dataset = read_tacred(args.dataset_file)
    patch = read_patch(args.patch_file)

    unique_rels = set([example["relation"] for example in dataset])
    cnt_rels = Counter([example["relation"] for example in dataset])
    logger.info("Number of examples in TACRED dataset: %d" % len(dataset))
    logger.info("Number of unique relations in TACRED dataset: %d", len(unique_rels))
    logger.info("Relation counts in TACRED dataset: %s" % cnt_rels.most_common())

    assert patch.keys() <= set([e["id"] for e in dataset])

    num_replaced = 0
    for example in dataset:
        id_orig = example["id"]
        relation_orig = example["relation"]

        if id_orig in patch:
            patch_example = patch[id_orig]
            example.update(patch_example)

            if relation_orig != example["relation"]:
                num_replaced += 1

    unique_rels_augmented = set([example["relation"] for example in dataset])
    cnt_augmented = Counter([example["relation"] for example in dataset])
    rels_difference = unique_rels ^ unique_rels_augmented
    logger.info("Number of overwritten ground truth relations: %d" % num_replaced)
    logger.info("Number of unique relations in patched dataset: %d" % len(unique_rels_augmented))
    logger.info("Relation counts in patched dataset: %s" % cnt_augmented.most_common())
    logger.info("!!! Relations not in patched dataset: %s" % rels_difference)

    write_tacred(args.output_file, dataset)

    reread_patched_dataset = read_tacred(args.output_file)

    unique_rels_reread = set([example["relation"] for example in reread_patched_dataset])
    logger.info("Number of examples in re-read dataset: %d" % len(reread_patched_dataset))
    logger.info("Number of unique relations in re-read dataset: %d", len(unique_rels_reread))

    assert len(reread_patched_dataset) == len(dataset)
    assert unique_rels_augmented == unique_rels_reread


if __name__ == "__main__":
    main()
