from langchain_core.documents import Document
from app.db.pinecone_client import index,vector_store

def store_emails(data):
    user_id = data.userId
    docs = []

    for email in data.emails:
        result = index.fetch(ids=[email.id],namespace=user_id)

        if result.vectors:
            continue
        docs.append(
            Document(
                page_content=f"""
                Subject : {email.subject}
                Body : {email.body}
                """,
                metadata={
                    "gmail_id" : email.id
                }
            )
        )

        if docs :
            vector_store.add_documents(
                docs,
                ids=[doc.metadata['gmail_id'] for doc in docs],
                namespace=user_id
            )

        return {"embedded" : len(docs)}