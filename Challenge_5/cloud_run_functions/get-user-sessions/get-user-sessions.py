import functions_framework
from flask import jsonify, Request
from google.cloud import firestore
from datetime import datetime, timezone, timedelta

db = firestore.Client(project="qwiklabs-gcp-03-f951e059a60d")

@functions_framework.http
def user_chat_handler(request: Request):
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({"error": "Missing required query parameter: user_id"}), 400

    user_collection = db.collection(user_id)
    docs = list(user_collection.stream())

    if not docs:
        user_collection.document("placeholder").set({"created": True})
        return jsonify([]), 200

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(minutes=15)

    recent_chats = []

    for doc in docs:
        try:
            doc_time = datetime.fromisoformat(doc.id)
        except ValueError:
            continue  # skip invalid timestamp document IDs

        if doc_time < cutoff:
            doc.reference.delete()
            continue

        data = doc.to_dict()
        chat_name = data.get("chat_name")

        if chat_name:
            recent_chats.append({
                "chat_name": chat_name,
                "timestamp": doc.id
            })

    return jsonify(recent_chats), 200
