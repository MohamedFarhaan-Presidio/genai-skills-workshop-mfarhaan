import functions_framework
from flask import jsonify, Request
from google.cloud import firestore
from datetime import datetime, timezone

db = firestore.Client()

@functions_framework.http
def get_session(request: Request):
    user_id = request.args.get("user_id")
    chat_name = request.args.get("chat_name")

    if not user_id:
        return jsonify({"error": "Missing required query parameter: user_id"}), 400
    if not chat_name:
        return jsonify({"error": "Missing required query parameter: chat_name"}), 400

    user_collection = db.collection(user_id)
    docs = list(user_collection.stream())

    # If user_id collection doesn't exist (i.e., no documents), throw 404
    if not docs:
        return jsonify({"error": f"User ID '{user_id}' not found"}), 404

    # Search for existing chat_name
    for doc in docs:
        data = doc.to_dict()
        if data.get("chat_name") == chat_name:
            return jsonify(data.get("chat_history", [])), 200

    # Not found: Create new document with current timestamp
    timestamp_id = datetime.now(timezone.utc).isoformat()
    user_collection.document(timestamp_id).set({
        "chat_name": chat_name,
        "chat_history": []
    })

    return jsonify([]), 200
