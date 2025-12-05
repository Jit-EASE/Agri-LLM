# core/retrieval.py
import textwrap

from .nlu import stable_score  # used indirectly via signals, but ok to import here if needed


def retrieve_chunks(prepared: dict) -> dict:
    base = textwrap.fill(prepared["normalized"], width=80)
    chunks = [
        {
            "id": "C1",
            "heading": "Macro & Market Context",
            "path": "Ireland › Sector › Markets",
            "preview": base[:240] + "...",
        },
        {
            "id": "C2",
            "heading": "Behaviour & Adoption",
            "path": "Ireland › Farm Systems › Behaviour",
            "preview": base[60:300] + "...",
        },
        {
            "id": "C3",
            "heading": "Policy & Instruments",
            "path": "EU › CAP › National Implementation",
            "preview": base[120:360] + "...",
        },
    ]
    return {"chunks": chunks}


def rag_retrieve(prepared: dict) -> dict:
    """
    Real vectorstore RAG retriever using FAISS + sentence transformers.
    Falls back to mocked retrieval if index not present.
    """
    try:
        from langchain_community.vectorstores import FAISS
        from langchain.embeddings import HuggingFaceEmbeddings

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        db = FAISS.load_local("vectorstore_index", embeddings)

        results = db.similarity_search(prepared["normalized"], k=3)

        chunks = []
        for i, r in enumerate(results):
            chunks.append(
                {
                    "id": f"R{i+1}",
                    "heading": r.metadata.get("title", "Evidence"),
                    "path": r.metadata.get("source", "Unknown"),
                    "preview": r.page_content[:300] + "...",
                }
            )
        return {"chunks": chunks}

    except Exception:
        return retrieve_chunks(prepared)
