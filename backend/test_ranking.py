import pytest

from utils.ranking import rank_resumes_by_similarity


class DummyEmbeddingResponse:
    def __init__(self, vector):
        self.data = [type("Data", (), {"embedding": vector})]


class DummyClient:
    def __init__(self):
        self.embeddings = self

    def create(self, model, input):  # pragma: no cover - simple stub
        mapping = {
            "JD": [1.0, 0.0],
            "Resume A": [0.5, 0.5],
            "Resume B": [0.0, 1.0],
            "": [0.0, 0.0],
        }
        return DummyEmbeddingResponse(mapping.get(input, [0.0, 0.0]))


def test_rank_resumes_by_similarity():
    client = DummyClient()
    resumes = [
        {"filename": "A", "text": "Resume A"},
        {"filename": "B", "text": "Resume B"},
        {"filename": "Empty", "text": ""},
    ]

    ranked = rank_resumes_by_similarity(resumes, "JD", top_n=2, client=client)

    assert len(ranked) == 2
    assert ranked[0]["filename"] == "A"
    assert ranked[0]["similarity"] >= ranked[1]["similarity"]


def test_rank_resumes_by_similarity_empty_jd():
    client = DummyClient()
    resumes = [{"filename": "A", "text": "Resume A"}]
    ranked = rank_resumes_by_similarity(resumes, "", client=client)
    assert ranked == []
