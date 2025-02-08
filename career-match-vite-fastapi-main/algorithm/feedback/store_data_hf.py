import logging
import sys
import os.path
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
)

from transformers import pipeline

# 设置Hugging Face API密钥
HUGGING_FACE_API_KEY = os.getenv("HUGGING_FACE_API_KEY")

# 配置日志
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

PERSIST_DIR = "./storage"
def flatten_embeddings(embeddings):
    return [item for sublist in embeddings for item in sublist]

class HuggingFaceAPIEmbedding:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        # 使用 Hugging Face Inference API 进行嵌入生成
        self.embedding_pipeline = pipeline(
            'feature-extraction',
            model=model_name,
            use_auth_token=HUGGING_FACE_API_KEY
        )



    def get_embedding(self, text: str):
        embeddings = self.embedding_pipeline(text, truncation=True)
        logging.debug(f"Embedding shape: {len(embeddings[0][0])}")
        return flatten_embeddings(embeddings[0])

    def get_text_embedding_batch(self, texts, **kwargs):
        embeddings = self.embedding_pipeline(texts, truncation=True)
        flattened_embeddings = [flatten_embeddings(embedding[0]) for embedding in embeddings]
        logging.debug(f"Batch embedding shape: {len(flattened_embeddings[0])}")
        return flattened_embeddings



def create_vector_storage():
    # 检查存储目录是否存在
    if not os.path.exists(PERSIST_DIR):
        # 加载文档并创建索引
        documents = SimpleDirectoryReader("data/").load_data()
        embedding_model = HuggingFaceAPIEmbedding()
        index = VectorStoreIndex.from_documents(documents, embed_model=embedding_model)
        # 保存索引以便后续使用
        index.storage_context.persist(persist_dir=PERSIST_DIR)
    else:
        logging.error(f"{PERSIST_DIR} already exists")

if __name__ == "__main__":
    create_vector_storage()