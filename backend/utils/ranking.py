"""Utilities for ranking resumes based on similarity to a job description."""

from __future__ import annotations

from typing import Dict, List, Optional, TYPE_CHECKING

import math

if TYPE_CHECKING:  # pragma: no cover - for type hints only
    from openai import OpenAI

EMBEDDING_MODEL = "text-embedding-3-small"


def _get_embedding(client: "OpenAI", text: str | None) -> List[float] | None:
    """Return the embedding for ``text`` or ``None`` if the text is empty."""
    if not text:
        return None
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return response.data[0].embedding


def rank_resumes_by_similarity(
    resumes: List[Dict[str, str]],
    job_description: str,
    top_n: int = 5,
    client: Optional["OpenAI"] = None,
) -> List[Dict[str, object]]:
    """Rank resumes by similarity to the job description.

    Parameters
    ----------
    resumes:
        List of dictionaries, each containing ``filename`` and ``text`` keys.
    job_description:
        Plain text describing the job requirements.
    top_n:
        The maximum number of resumes to return. Defaults to 5.

    Returns
    -------
    list of dict
        Each dictionary contains the original resume fields plus a ``score`` key
        representing the cosine similarity to the job description. The list is
        sorted in descending order of similarity.
    """
    if not job_description:
        return []

    if client is None:
        from openai import OpenAI

        client = OpenAI()
    jd_embedding = _get_embedding(client, job_description)
    if jd_embedding is None:
        return []
    jd_vector = jd_embedding

    ranked: List[Dict[str, object]] = []
    jd_norm = math.sqrt(sum(x * x for x in jd_vector))
    for resume in resumes:
        embedding = _get_embedding(client, resume.get("text"))
        if embedding is None:
            score = 0.0
        else:
            vector = embedding
            denom = jd_norm * math.sqrt(sum(x * x for x in vector))
            score = float(
                sum(a * b for a, b in zip(jd_vector, vector)) / denom
            ) if denom else 0.0
        ranked.append({**resume, "score": score})

    ranked.sort(key=lambda x: x["score"], reverse=True)
    return ranked[:top_n]
