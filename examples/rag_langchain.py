"""Load YouTube transcripts into LangChain documents, one per paragraph, with timestamp links.

pip install transcriptyt langchain-core
"""

from langchain_core.documents import Document
from transcriptyt import TranscriptYT

client = TranscriptYT()


def load_youtube(video: str) -> list[Document]:
    data = client.get_transcript(video, paragraphs=True)
    return [
        Document(
            page_content=seg["text"],
            metadata={
                "video_id": data["videoId"],
                "title": data["title"],
                "start": seg["start"],
                "source": f"https://www.youtube.com/watch?v={data['videoId']}&t={int(seg['start'])}s",
            },
        )
        for seg in data["segments"]
    ]


if __name__ == "__main__":
    docs = load_youtube("https://youtu.be/dQw4w9WgXcQ")
    print(len(docs), docs[0].metadata["source"])
    # vector_store.add_documents(docs)
