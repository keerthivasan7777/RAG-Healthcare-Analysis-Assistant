from uuid import uuid4
from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os

load_dotenv()

# Constants - Optimized for healthcare content
CHUNK_SIZE = 800  # Smaller chunks for precise medical information
CHUNK_OVERLAP = 100  # Overlap to maintain context in medical content
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # Fast and effective
VECTORSTORE_DIR = Path(__file__).parent / "resources/vectorstore"
COLLECTION_NAME = "healthcare_analysis"

llm = None
vector_store = None


def initialize_components():
    """Initialize LLM and vector store components"""
    global llm, vector_store
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        raise RuntimeError(
            "GROQ_API_KEY not set. Add it to a .env file or set the environment variable."
        )

    if llm is None:
        llm = ChatGroq(
            api_key=groq_key,
            model="llama-3.3-70b-versatile",
            temperature=0.2,  # Low temperature for medical accuracy and consistency
            max_tokens=1200   # More space for detailed medical explanations
        )

    if vector_store is None:
        VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)

        ef = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"trust_remote_code": True},
        )

        vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=ef,
            persist_directory=str(VECTORSTORE_DIR),
        )


def process_urls(urls):
    """
    Process medical resource URLs and store documents in vector database.
    Yields status messages for Streamlit display.
    
    :param urls: List of medical resource URLs to process
    :yield: Status messages
    """
    yield "🔧 Initializing healthcare analysis components..."
    initialize_components()

    if vector_store is None:
        raise RuntimeError("vector_store was not initialized")

    yield "🗑️ Clearing existing medical data..."
    if hasattr(vector_store, "reset_collection"):
        vector_store.reset_collection()

    yield "📥 Loading medical resources from URLs..."
    loader = UnstructuredURLLoader(urls=urls)
    data = loader.load()

    yield "✂️ Splitting medical content into analyzable chunks..."
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ". ", " "],
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    docs = text_splitter.split_documents(data)

    yield f"💾 Adding {len(docs)} medical documents to knowledge base..."
    uuids = [str(uuid4()) for _ in range(len(docs))]
    vector_store.add_documents(docs, ids=uuids)

    yield "✅ Medical resources processed successfully!"


def format_docs(docs):
    """Format retrieved documents into a single context string"""
    return "\n\n".join([doc.page_content for doc in docs])


def classify_query_type(query):
    """
    Classify the type of medical query to provide context-appropriate responses.
    Returns a query category.
    """
    query_lower = query.lower()
    
    if any(word in query_lower for word in ['treat', 'treatment', 'therapy', 'medication', 'drug']):
        return "treatment"
    elif any(word in query_lower for word in ['diagnose', 'diagnosis', 'symptoms', 'signs', 'criteria']):
        return "diagnosis"
    elif any(word in query_lower for word in ['side effect', 'adverse', 'complication', 'risk']):
        return "side_effects"
    elif any(word in query_lower for word in ['prevent', 'prevention', 'avoid', 'reduce risk']):
        return "prevention"
    elif any(word in query_lower for word in ['research', 'study', 'evidence', 'findings']):
        return "research"
    else:
        return "general"


def generate_answer(query):
    """
    Generate a professional, evidence-based answer for healthcare queries.
    
    :param query: User's medical question
    :return: Tuple of (answer, sources)
    """
    initialize_components()
    
    # Classify query type
    query_type = classify_query_type(query)
    
    # Retrieve relevant documents with higher k for medical queries
    retriever = vector_store.as_retriever(
        search_type="mmr",  # Maximum Marginal Relevance for diverse results
        search_kwargs={
            "k": 5,  # Retrieve more documents for comprehensive medical answers
            "fetch_k": 15,
            "lambda_mult": 0.7
        }
    )
    retrieved_docs = retriever.invoke(query)
    
    # Create a professional medical analysis prompt
    prompt = ChatPromptTemplate.from_template("""You are a knowledgeable healthcare analysis assistant helping medical professionals, researchers, and informed individuals understand medical information.

CRITICAL SAFETY GUIDELINES:
1. **Accuracy First**: Only provide information directly supported by the provided context
2. **Never Diagnose**: Do not diagnose conditions or tell users they have a specific disease
3. **Never Prescribe**: Do not prescribe medications, dosages, or specific treatment plans
4. **Always Defer**: Encourage consultation with qualified healthcare professionals for medical decisions
5. **Acknowledge Limitations**: If information is insufficient, clearly state this

RESPONSE STRUCTURE:
1. **Direct Answer**: Start with a clear, evidence-based answer
2. **Detailed Explanation**: Provide medical context using accessible language
3. **Key Points**: Highlight important information (symptoms, risk factors, etc.)
4. **Evidence Base**: Reference the type of source (guideline, research, etc.)
5. **Professional Consultation**: Always remind about seeking professional medical advice

TONE & STYLE:
- Professional yet approachable
- Clear and precise medical terminology with explanations
- Evidence-focused and objective
- Empathetic and supportive
- Use simple language when explaining complex concepts

SAFETY RULES - CRITICAL:
- If asked about specific symptoms → Suggest consulting a healthcare provider
- If asked about medication dosing → Refer to prescribing physician or pharmacist
- If asked to diagnose → Explain that diagnosis requires professional clinical evaluation
- For emergency situations → Advise immediate medical attention

Query Type: {query_type}

Context from Medical Resources:
{context}

Question: {question}

Professional Analysis:

[Provide your evidence-based response here]

---

⚕️ **Important Medical Disclaimer**: This information is for educational purposes only and should not replace professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers for medical decisions, especially regarding medications, treatments, or health concerns.

""")
    
    # Create RAG chain
    rag_chain = (
        {
            "context": lambda x: format_docs(retrieved_docs),
            "question": RunnablePassthrough(),
            "query_type": lambda x: query_type
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    # Generate answer
    answer = rag_chain.invoke(query)
    
    # Extract and format sources with credibility indicators
    sources = []
    for doc in retrieved_docs:
        source_url = doc.metadata.get('source', 'Medical Resource')
        credibility = assess_source_credibility(source_url)
        sources.append(f"{source_url} {credibility}")
    
    sources_text = "\n".join(sources)
    
    return answer, sources_text


def assess_source_credibility(source_url):
    """
    Assess the credibility of medical sources based on domain.
    Returns a credibility indicator string.
    """
    trusted_domains = {
        "pubmed": "⭐⭐⭐ Peer-Reviewed",
        "nih.gov": "⭐⭐⭐ Government Health Authority",
        "who.int": "⭐⭐⭐ International Health Authority",
        "cdc.gov": "⭐⭐⭐ Government Health Authority",
        "mayoclinic.org": "⭐⭐ Trusted Medical Institution",
        "clevelandclinic.org": "⭐⭐ Trusted Medical Institution",
        "cochrane.org": "⭐⭐⭐ Systematic Reviews",
        "uptodate.com": "⭐⭐ Clinical Decision Support",
    }
    
    for domain, rating in trusted_domains.items():
        if domain in source_url.lower():
            return rating
    
    return "ℹ️ Medical Resource"










