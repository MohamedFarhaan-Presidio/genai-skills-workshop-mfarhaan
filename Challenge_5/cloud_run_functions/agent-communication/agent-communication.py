from google.cloud import bigquery
from flask import jsonify, Request
from vertexai.preview.language_models import ChatModel
from vertexai.preview.generative_models import GenerativeModel
import functions_framework
import vertexai
import pandas as pd

project_id="qwiklabs-gcp-03-f951e059a60d"
dataset_id="ads_dataset"
embedding_model_name="ads_embedding_model"
embedded_dataset_table_name="ads_vector_dataset"
bigquery_location="us"
vertexai_location="us-central1"
bq_client = None
chatmodel_location="global"
chatmodel_name="gemini-2.0-flash-001"

def get_bq_client():
    global bq_client
    if bq_client is None:
        bq_client = bigquery.Client(project=project_id, location=bigquery_location)
    return bq_client

@functions_framework.http
def agent_communication(request: Request):
    user_id = request.args.get("user_id")
    chat_name = request.args.get("chat_name")
    data = request.get_json(silent=True)
    if not user_id:
        return jsonify({"error": "Missing required query parameter: user_id"}), 400
    if not chat_name:
        return jsonify({"error": "Missing required query parameter: chat_name"}), 400
    if not data:
        return jsonify({"error": "Missing required request body: data"}), 400
    query = data.get("query")
    if not query:
        return jsonify({"error": "Missing query in request body"}), 400
    context = query_embdded_table(query)
    print("retrieved context from rag, initing Vertex ai")
    vertexai.init(project=project_id, location=vertexai_location)
    chat_model = GenerativeModel(chatmodel_name)
    prompt = f"""
      Answer to the question based on the context. Do not answer on your own.

      Context:
        {context}

      Question: {query}
    :\n\n{context}\n\nUser: {query}"""
    results = chat_model.generate_content(prompt)
    print("Answer retrieved from LLM")
    return jsonify({"system": results.text}), 200


def query_embdded_table(query, top_k = 3):
    bq = get_bq_client()
    query = f"""
      SELECT query.query, r.base.question, r.base.answer, r.distance
      FROM VECTOR_SEARCH(
        TABLE `{dataset_id}.{embedded_dataset_table_name}`,
        'vector_embedding',
        (
          SELECT
            ml_generate_embedding_result AS vector_embedding,
            '{query}' AS query
          FROM ML.GENERATE_EMBEDDING(
            MODEL `{dataset_id}.{embedding_model_name}`,
            (SELECT '{query}' AS content)
          )
        ),
        top_k => {top_k},
        options => '{{"fraction_lists_to_search": 1.0}}'
      ) AS r
    """
    results = bq.query(query).to_dataframe()
    return "\n\n".join([f"Q: {row['question']}\nA: {row['answer']}" for _, row in results.iterrows()])