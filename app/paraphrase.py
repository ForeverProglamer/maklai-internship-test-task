from functools import partial
from itertools import islice, permutations
from typing import Callable, Iterable, TypeVar

from nltk import Tree

NP = 'NP'
CC = 'CC'

COMMA = ','

_ParaphrasingStrategy = Callable[[Tree], Iterable[Tree]]


class DeserializationError(Exception):
    """Inappropriate serialized tree given."""


def paraphrase_sentence(
    serialized_tree: str,
    strategy: _ParaphrasingStrategy | None = None
) -> Iterable[Tree]:
    """High-level interface for sentence paraphrasing."""
    tree = _deserialize_tree(serialized_tree)
    if strategy is None:
        return np_permutation_paraphrasing(tree)
    return strategy(tree)


def np_permutation_paraphrasing(tree: Tree) -> Iterable[Tree]:
    """Default paraphrasing implementation that uses NP permutation."""
    for subtree in _find_all_np_subtrees(tree):
        nps = [
            (idx, value) for idx, value in enumerate(subtree) 
            if _has_np_label(value)
        ]
        np_idxs = [i for i, _ in nps]
        np_permutations = _generate_subtree_permutations(nps)

        for permutation in np_permutations:
            yield _apply_permutation(tree, subtree, permutation, np_idxs)


def _deserialize_tree(serialized_tree: str) -> Tree:
    try:
        return Tree.fromstring(serialized_tree)
    except ValueError:
        raise DeserializationError()


def _find_all_np_subtrees(tree: Tree) -> Iterable[Tree]:
    def predicate(tree: Tree) -> bool:
        return _has_np_label(tree) and _is_separated_by_tags_or_cc(tree)

    return tree.subtrees(predicate)


def _is_separated_by_tags_or_cc(tree: Tree) -> bool:
    children_labels = [child.label() for child in tree]
    return COMMA in children_labels or CC in children_labels


def _has_label(tree: Tree, label: str) -> bool:
    return tree.label() == label


_has_np_label = partial(_has_label, label=NP)


def _generate_subtree_permutations(
    nps: list[tuple[int, Tree]]
) -> Iterable[Tree]:
    return _skip(permutations([value for _, value in nps]), 1)


def _apply_permutation(
    tree: Tree,
    subtree: Tree,
    permutation: tuple[Tree],
    permutation_indexes: list[int]
) -> Tree:
    tree_copy = tree.copy(deep=True)
    target_subtree = _find_subtree(tree_copy, subtree)
    permutation_iterator = iter(permutation)
    for idx in permutation_indexes:
        target_subtree[idx] = next(permutation_iterator)
    return tree_copy


def _find_subtree(tree: Tree, subtree: Tree) -> Tree:
    return next(tree.subtrees(lambda t: t == subtree))


_T = TypeVar('_T')


def _skip(iterable: Iterable[_T], n: int) -> Iterable[_T]:
    return islice(iterable, n, None)
