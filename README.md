# AI Document Processing Pipeline

End-to-end document processing pipeline using DocLing, BERT models and FAISS for intelligent document analysis and querying.

## Project Structure
```
.
├── README.md
├── config/
│   ├── settings.yaml
│   └── pipeline-resources.yaml
├── src/
│   ├── backend/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── settings/
│   │       └── settings_manager.py
│   ├── docprocessing/
│   │   ├── extractor.py
│   │   ├── preprocessor.py
│   │   └── vectorizer.py
│   └── chatbot/
│       ├── bot.py
│       └── query_engine.py
├── k8s/
│   ├── deployments/
│   │   ├── backend.yaml
│   │   └── chatbot.yaml
│   └── storage/
│       └── document-pvc.yaml
└── pipelines/
    ├── tasks/
    │   ├── git-clone.yaml
    │   ├── extract-content.yaml
    │   ├── preprocess.yaml
    │   ├── vectorize.yaml
    │   └── deploy.yaml
    └── pipeline.yaml
```

## Prerequisites
- OpenShift 4.x cluster
- Tekton Pipelines installed
- FAISS vector database
- NFS storage for documents

## Configuration
Edit `config/settings.yaml` to configure:
- Document source paths
- Processing options
- Model parameters
- Chatbot settings

## Components
1. Document Storage: NFS/local storage for raw documents
2. Backend API: Flask service for settings management
3. Processing Pipeline: DocLing extraction and preprocessing
4. Vector Store: FAISS with Sentence-BERT embeddings
5. Chatbot: DistilBERT-based QA system

## Deployment
```bash
# Create pipeline resources
oc apply -f config/pipeline-resources.yaml

# Deploy pipeline
oc apply -f pipelines/pipeline.yaml

# Start pipeline
tkn pipeline start doc-processing-pipeline
```
