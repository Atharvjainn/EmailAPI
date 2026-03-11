from langchain_core.documents import Document
from app.db.pinecone_client import index,get_vector_store,get_retriever
from langchain_groq import ChatGroq
from langchain_pinecone import PineconeVectorStore
from app.models.schemas import DeadlineList, prompt_template
from app.lib.utils import calculate_urgency
from app.db.mongoDB_client import results_collection
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    temperature=0
)
structured_llm = llm.with_structured_output(DeadlineList)



def store_emails(data):
    user_id = data.userId
    vector_store = get_vector_store(user_id)
    all_ids = [email.id for email in data.emails]
    existing = index.fetch(ids=all_ids,namespace=user_id)
    existing_ids = set(existing.vectors.keys())
    docs = []

    if set(all_ids) == existing_ids:
        cached = results_collection.find_one({
            "userId" : user_id
        })
        if cached : 
            return sorted(cached['results'],key=lambda x : x['urgency'],reverse=True)

    for email in data.emails:
       if email.id not in existing_ids: 
        docs.append(
            Document(
                page_content=f"Subject: {email.subject}\nBody: {email.body}",
                metadata={
                    "gmail_id": email.id,
                    "subject": email.subject  # ✅ store subject in metadata
                }
            )
        )

    # ✅ moved outside the loop — store all at once, then call LLM once
    if docs:
        vector_store.add_documents(
            docs,
            ids=[doc.metadata['gmail_id'] for doc in docs],
            namespace=user_id
        )

    results = llm_work(user_id)  # ✅ pass user_id for namespace
    results_collection.update_one(
        {"userId" : user_id},
        {"$set" : {"userId" : user_id, "results" : results}},
        upsert=True
    )

    return sorted(results, key=lambda x: x['urgency'], reverse=True)

def llm_work(user_id: str):
    # ✅ use a namespace-scoped retriever
    retriever = get_retriever(user_id,k=10)
    relevant_docs = retriever.invoke(
    """
    due by, deadline, submit before, payment due, 
    expires on, last date, interview on, meeting scheduled,
    exam on, appointment, please respond by, reminder
    """
    )
    context = ""
    for doc in relevant_docs:
        context += f"gmail_id: {doc.metadata['gmail_id']}\n"
        context += doc.page_content  # ✅ subject is already inside page_content
        context += "\n\n---\n\n"

    if not context.strip():
        return []  # ✅ guard: nothing relevant found

    prompt = prompt_template(context)
    response = structured_llm.invoke(prompt)
    results = []

    

    for item in response.deadlines:
        item.urgency = calculate_urgency(item)
        doc = item.model_dump()

        if isinstance(doc.get("deadline"), (str)) is False and doc.get("deadline"):
            doc["deadline"] = doc["deadline"].isoformat()

        results.append(doc)

    return results




