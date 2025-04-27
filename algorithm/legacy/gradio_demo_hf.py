import gradio as gr
from gradio_pdf import PDF
from llama_index.core import (
    StorageContext,
    load_index_from_storage,
)
from llama_parse import LlamaParse

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

from llama_index.llms.replicate import Replicate


llm = Replicate(
    model="meta/llama-2-70b-chat:2796ee9483c3fd7aa2e171d38f4ca12251a30609463dcfd4cd76703f22e96cdf",
    is_chat_model=True,
    additional_kwargs={"max_new_tokens": 512}
)

Settings.llm = llm

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

PERSIST_DIR = "./storage"
parser = LlamaParse(api_key="",result_type="markdown")


def user_query(query, cv):
    input_cv = parser.load_data(cv)

    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context,llm=llm)

    query_engine = index.as_query_engine(similarity_top_k=2,llm=llm)
    # response = query_engine.query(
    #     f"""
    #     You are a brilliant career adviser. Answer a question of job seekers with given information.\n
    #     If their CV information is given, use that information as well to answer the question.\n
    #     When you respond, please make sure to answer step by step and also show the reference information that you used to answer. \n
    #     If you are not sure about the answer, return NA.\n
    #     You need to show the source nodes that you are using to answer the question at the end of your response.\n
    #     CV: {input_cv[0]}\n
    #     Question: {query}"""
    # )
    response = query_engine.query(
        f"""
            You are a career adviser. Answer a question of job seekers with given information.\n
            If their CV information is given, use that information as well to answer the question.\n
            Make sure to answer step by step and also show the reference information such as job ID at the end. \n
            If you are not sure about the answer, return NA.\n
            CV: {input_cv}\n
            Question: {query}"""
    )
    return response


def main(query: str, cv):
    response = user_query(query, cv)
    return response.response


if __name__ == "__main__":
    demo = gr.Interface(main, inputs=[gr.Textbox(label="Query"), PDF(label="CV")], outputs=gr.Textbox())
    demo.launch()