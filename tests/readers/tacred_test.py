import os

from tests import FIXTURES_ROOT

from tacrev.readers.tacred import load_tacred


def test_load_tacred():
    tacred_path = os.path.join(FIXTURES_ROOT, "test_data.json")

    documents = load_tacred(tacred_path)
    assert len(documents) == 3

    document = documents[0]
    print(document)
    assert len(document.tokens) == 26
    assert len(document.relations) == 1
    assert len(document.tags) == 4

    token = document.tokens[1]
    assert token.text == "the"
    assert token.sent == 1
    assert token.i == 1
    assert token.idx == 3

    tag_head = document.tags[0]
    assert len(tag_head.tokens) == 2
    assert [t.text for t in tag_head.tokens] == ["Douglas", "Flint"]
    assert [t.i for t in tag_head.tokens] == [8, 9]

    tag_tail = document.tags[1]
    assert len(tag_tail.tokens) == 1
    assert [t.text for t in tag_tail.tokens] == ["chairman"]
    assert [t.i for t in tag_tail.tokens] == [12]

    relation = document.relations[0]
    assert relation.head.i == 8
    assert relation.tail.i == 12
