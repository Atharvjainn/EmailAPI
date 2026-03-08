from langchain_core.documents import Document
from app.db.pinecone_client import index,vector_store
from langchain_groq import ChatGroq
from app.models.schemas import DeadlineList, prompt_template
from app.db.pinecone_client import vector_store,retriever
from app.lib.utils import calculate_urgency

#Embeddings model is with pinecone_client
llm = ChatGroq(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    temperature=0
)
structured_llm = llm.with_structured_output(DeadlineList)

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

        # return {"embedded" : len(docs)}
        list = llm_work()
        return list

def llm_work():
    relevant_docs = retriever.invoke(
        "Find emails that mention deadlines, due dates, payments, submissions, exams, interviews."
    )
    context = ""
    for doc in relevant_docs:
        context += f"\nSubject: {doc.metadata['subject']}\n"
        context += doc.page_content
        context += "\n\n---\n\n"
    prompt = prompt_template(context)
    response = structured_llm.invoke(prompt)
    for item in response.deadlines:
        item.urgency = calculate_urgency(item)
    items_list = [item.model_dump() for item in response.deadlines]
    return items_list