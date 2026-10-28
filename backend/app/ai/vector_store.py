import faiss
import numpy as np


def create_index(vectors):

    vectors = np.asarray(
        vectors,
        dtype="float32"
    )

    dimension = vectors.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(vectors)

    return index


def search(
    index,
    query_vectors,
    k=3
):

    query_vectors = np.asarray(
        query_vectors,
        dtype="float32"
    )

    distances, indices = index.search(
        query_vectors,
        k
    )

    return indices