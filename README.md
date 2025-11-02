# 🏥 Healthcare Analysis Assistant

An AI-powered medical research assistant that helps healthcare professionals, researchers, and students analyze medical literature using Retrieval-Augmented Generation (RAG) technology.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.31.0-FF4B4B.svg)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/langchain-0.1.9-green.svg)](https://python.langchain.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ⚕️ Medical Disclaimer

**THIS TOOL IS FOR EDUCATIONAL AND RESEARCH PURPOSES ONLY.** It should not be used for medical diagnosis, treatment decisions, or as a substitute for professional medical advice. Always consult qualified healthcare providers for medical concerns.

---

## 🌟 Features

- **🔍 Intelligent Medical Research**: Analyze medical literature from trusted sources (PubMed, WHO, CDC, NIH)
- **📊 RAG Technology**: Uses Retrieval-Augmented Generation for accurate, context-aware responses
- **⭐ Source Credibility**: Automatic rating of medical sources (peer-reviewed, government authorities)
- **🎯 Query Classification**: Automatically categorizes questions (treatment, diagnosis, research, etc.)
- **🛡️ Safety First**: Built-in safeguards against providing diagnoses or prescriptions
- **💬 User-Friendly**: Clean, intuitive Streamlit interface
- **📚 Multiple Sources**: Process multiple medical URLs simultaneously

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Groq API Key (free at [console.groq.com](https://console.groq.com))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/healthcare-analysis-assistant.git
cd healthcare-analysis-assistant
```

2. **Create virtual environment**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Mac/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
```

5. **Run the application**
```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

---

## 📖 Usage

### Step 1: Load Medical Resources

1. Open the sidebar
2. Enter URLs from trusted medical sources:
   - WHO: `https://www.who.int/news-room/fact-sheets/detail/diabetes`
   - CDC: `https://www.cdc.gov/heartdisease/facts.htm`
   - NIH: `https://www.nhlbi.nih.gov/health/high-blood-pressure`
3. Click "Process URLs"
4. Wait for processing to complete

### Step 2: Ask Questions

Type your medical research question in the input box. Examples:

- "What are the diagnostic criteria for Type 2 diabetes?"
- "What are evidence-based treatments for hypertension?"
- "What are the risk factors for cardiovascular disease?"
- "Summarize recent research on asthma management"

### Step 3: Review Results

- Read the AI-generated analysis
- Check the source citations
- View credibility ratings for each source

---

## 🏗️ Project Structure

```
healthcare-analysis-assistant/
│
├── main.py                      # Streamlit UI (frontend)
├── rag.py                      # RAG logic and LLM integration
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create this)
├── README.md                   # This file
├── LICENSE                     # MIT License
│
└── resources/                  # Auto-generated
    └── vectorstore/           # Vector database storage
```

---

## 🛠️ Technology Stack

- **Frontend**: [Streamlit](https://streamlit.io/) - Interactive web interface
- **LLM**: [Groq](https://groq.com/) with Llama 3.3 70B - Fast inference
- **Framework**: [LangChain](https://python.langchain.com/) - RAG orchestration
- **Embeddings**: [HuggingFace Sentence Transformers](https://huggingface.co/sentence-transformers) - Text embeddings
- **Vector Store**: [ChromaDB](https://www.trychroma.com/) - Vector database
- **Document Processing**: [Unstructured](https://unstructured.io/) - URL content extraction

---

## ⚙️ Configuration

### Adjustable Parameters (in `rag.py`)

```python
CHUNK_SIZE = 800              # Text chunk size for processing
CHUNK_OVERLAP = 100           # Overlap between chunks
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
TEMPERATURE = 0.2             # LLM temperature (lower = more factual)
MAX_TOKENS = 1200             # Maximum response length
```

### Retrieval Settings

```python
search_type = "mmr"           # Maximum Marginal Relevance
k = 5                         # Number of documents to retrieve
fetch_k = 15                  # Initial fetch before MMR
lambda_mult = 0.7             # Diversity vs relevance balance
```

---

## 🎯 Key Features Explained

### 1. **Query Classification**
Automatically detects query type and adjusts response:
- Treatment queries
- Diagnosis queries
- Side effects queries
- Prevention queries
- Research queries
- General queries

### 2. **Source Credibility Assessment**
Rates sources based on domain:
- ⭐⭐⭐ Peer-Reviewed (PubMed, Cochrane)
- ⭐⭐⭐ Government Health Authority (NIH, WHO, CDC)
- ⭐⭐ Trusted Medical Institution (Mayo Clinic, Cleveland Clinic)
- ℹ️ Medical Resource (other sources)

### 3. **Safety Features**
- Never provides diagnoses
- Never prescribes medications or dosages
- Always includes medical disclaimers
- Encourages professional consultation
- Low temperature (0.2) for factual accuracy

### 4. **RAG Pipeline**
1. User asks question
2. Question is embedded using sentence transformers
3. Similar medical documents retrieved from vector store
4. Retrieved context passed to LLM
5. LLM generates evidence-based response
6. Sources cited with credibility ratings

---

## 📚 Supported Medical Sources

### Recommended Sources

| Source | URL Pattern | Credibility |
|--------|------------|-------------|
| PubMed Central | pubmed.ncbi.nlm.nih.gov | ⭐⭐⭐ |
| WHO | who.int | ⭐⭐⭐ |
| CDC | cdc.gov | ⭐⭐⭐ |
| NIH | nih.gov | ⭐⭐⭐ |
| Mayo Clinic | mayoclinic.org | ⭐⭐ |
| Cleveland Clinic | clevelandclinic.org | ⭐⭐ |
| Cochrane Reviews | cochrane.org | ⭐⭐⭐ |

---

## 🔧 Troubleshooting

### Common Issues

**"GROQ_API_KEY not set"**
- Create `.env` file with your API key
- Ensure `.env` is in project root directory

**"Module not found"**
- Activate virtual environment
- Run `pip install -r requirements.txt`

**Processing URLs fails**
- Check internet connection
- Verify URLs are publicly accessible (not paywalled)
- Try simpler article URLs

**Slow performance**
- First run downloads models (normal)
- Start with 1-2 URLs instead of 3
- Choose shorter articles initially

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add docstrings to functions
- Test with multiple medical sources
- Ensure medical disclaimers remain prominent
- Maintain safety features (no diagnosis/prescription)

---

## 📝 Future Enhancements

- [ ] PDF document support for research papers
- [ ] Multi-language support
- [ ] Chat history and conversation memory
- [ ] Export analysis to PDF/Word
- [ ] Advanced filtering by publication date
- [ ] Integration with medical databases (PubMed API)
- [ ] Support for medical images analysis
- [ ] Batch processing of multiple queries
- [ ] Custom medical ontology integration

---

## 🔒 Privacy & Security

- ✅ Runs locally on your machine
- ✅ No patient data collection
- ✅ Only processes publicly available information
- ✅ No data sent to third parties (except Groq API for LLM)
- ⚠️ Never input personal health information (PHI)
- ⚠️ Not HIPAA compliant - do not use with patient data

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Groq](https://groq.com/) for fast LLM inference
- [LangChain](https://python.langchain.com/) for RAG framework
- [Streamlit](https://streamlit.io/) for the amazing web framework
- [HuggingFace](https://huggingface.co/) for embedding models
- Medical institutions (WHO, CDC, NIH) for open access resources

---

## 📧 Contact

**Project Maintainer**: Your Name
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

**Project Link**: [https://github.com/yourusername/healthcare-analysis-assistant](https://github.com/yourusername/healthcare-analysis-assistant)

---

## ⚖️ Ethical Use Statement

This tool is designed to:
- ✅ Support medical education and research
- ✅ Help healthcare professionals review literature
- ✅ Assist students in understanding medical concepts
- ✅ Provide quick access to medical information

This tool should NOT be used to:
- ❌ Diagnose medical conditions
- ❌ Prescribe medications or treatments
- ❌ Replace professional medical consultation
- ❌ Make clinical decisions
- ❌ Process personal health information

**Always consult qualified healthcare providers for medical advice.**

---

## 📊 System Requirements

### Minimum Requirements
- **CPU**: Dual-core processor
- **RAM**: 4 GB
- **Storage**: 2 GB free space
- **Internet**: Stable connection for API calls

### Recommended Requirements
- **CPU**: Quad-core processor or better
- **RAM**: 8 GB or more
- **Storage**: 5 GB free space (for model caching)
- **Internet**: Broadband connection

---

## 🌍 Supported Languages

Currently supports English medical content. Future versions may include:
- Spanish
- French
- German
- Mandarin Chinese
- Hindi

---

<div align="center">

**Made with ❤️ for healthcare research and education**

⭐ Star this repository if you find it helpful!

</div>