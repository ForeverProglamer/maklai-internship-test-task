import json

import pytest
from nltk import Tree

from app.paraphrase import paraphrase_sentence

TEST_TREE = '(S (NP (NP (DT The) (JJ charming) (NNP Gothic) (NNP Quarter) ) (, ,) (CC or) (NP (NNP Barri) (NNP Gòtic) ) ) (, ,) (VP (VBZ has) (NP (NP (JJ narrow) (JJ medieval) (NNS streets) ) (VP (VBN filled) (PP (IN with) (NP (NP (JJ trendy) (NNS bars) ) (, ,) (NP (NNS clubs) ) (CC and) (NP (JJ Catalan) (NNS restaurants) ) ) ) ) ) ) )'
RESULT_FILE = 'expected-result-example.json'


@pytest.fixture
def expected_results() -> list[Tree]:
    with open(RESULT_FILE, 'r') as f:
        data = json.load(f)
        return [
            Tree.fromstring(paraphrase['tree']) 
            for paraphrase in data['paraphrases']
        ]


def test_paraphrase_sentence(expected_results: list[Tree]) -> None:
    paraphrases = list(paraphrase_sentence(TEST_TREE))
    for tree in expected_results:
        assert tree in paraphrases
