import os

from tests import FIXTURES_ROOT

from tacrev.readers.tacred import load_tacred
from tacrev.readers.evaluation_results import load_evaluation_results


def test_load_tacred_results():
    tacred_path = os.path.join(FIXTURES_ROOT, "test_data.json")
    results_path = os.path.join(FIXTURES_ROOT, "results")

    documents = load_tacred(tacred_path)
    eval_results = load_evaluation_results(results_path, documents)

    eval_result_1 = eval_results[0]
    assert eval_result_1.id == "e7798fb926b9403cfcd2"
    assert eval_result_1.true_label == "per:title"
    assert len(eval_result_1.pred_labels) == 1
    assert eval_result_1.pred_labels.most_common() == [("per:title", 2)]
    assert eval_result_1.num_correct == 2

    eval_result_2 = eval_results[2]
    assert eval_result_2.id == "e7798ae9c0adbcdc81e7"
    assert eval_result_2.true_label == "per:city_of_death"
    assert len(eval_result_2.pred_labels) == 2
    assert (set(eval_result_2.pred_labels.most_common())
            == set([("no_relation", 1), ("per:city_of_death", 1)]))
    assert eval_result_2.num_correct == 1
