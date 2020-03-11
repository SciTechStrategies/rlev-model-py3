import os
import pickle

import click
import numpy as np
import sklearn.linear_model.logistic  # noqa required for loading pickled model

DATA_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'data',
)
PUNCT = '()-:;\'",.{}[]?'


@click.command()
@click.argument('infile', type=click.File('rt'))
@click.option('--delimiter', default='\t')
@click.option('--min-features', type=int, default=2)
@click.option('--max-features', type=int)
def cli(infile, delimiter, min_features, max_features):
    """SciTechStrategies Research Level Model."""
    probs = yield_probs(
        fp=infile,
        delimiter=delimiter,
        min_features=min_features,
        max_features=max_features,
    )
    for row in probs:
        print(*row, sep=delimiter)


def yield_rows(fp, delimiter):
    for line in fp:
        yield line.strip().split(delimiter)


def yield_probs(fp, delimiter='\t', min_features=2, max_features=None):
    """Yield research level probabilities for a sequence of text.

    Args:
        fp: A file pointer to a CSV file with columns ID, title, abstract.
        delimiter: The character used to delimit the columns.
        min_features: The minimum number of word features.
        max_features: The maximum number of word features.

    Yields:
        A sequence of [ID, *prob] lists.
    """
    title_features = unpickle('title-features')
    abstr_features = unpickle('abstract-features')
    n_features = len(title_features) + len(abstr_features)
    model = unpickle('model')

    rows = yield_rows(fp, delimiter=delimiter)
    for iden, title, abstr in rows:
        features = np.zeros(n_features)
        features_found = 0
        for word in get_words(title):
            if word in title_features:
                feature_id = title_features[word]
                features[feature_id] = 1
                features_found += 1
        for word in get_words(abstr):
            if word in abstr_features:
                feature_id = abstr_features[word]
                features[feature_id] = 1
                features_found += 1

        if min_features and features_found < min_features:
            continue
        if max_features and features_found > max_features:
            continue

        features = np.array([features])
        yield [iden] + list(model.predict_proba(features)[0])


def unpickle(name):
    """Unpickle a pickled object.

    Args:
        name (str): The name of the pickled object.

    Returns:
        The unpickled object.
    """
    pkl_file = os.path.join(DATA_DIR, "{0}.pkl".format(name))
    with open(pkl_file, 'rb') as fp:
        return pickle.load(fp)


def get_words(text, punct=PUNCT):
    """Get set of words in text.

    Args:
        text (str): The text.

    Returns:
        set: set of words in text, lowercased, punctuation removed.
    """
    text = text.lower()
    for p in PUNCT:
        text = text.replace(p, ' ')
    return set([w for w in text.split(' ') if w])

if __name__ == '__main__':
    cli()
