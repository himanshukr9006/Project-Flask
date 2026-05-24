# ─────────────────────────────────────
# IMPORTS
# Flask    → web framework
# request  → read incoming data
# jsonify  → send JSON response
# pymongo  → connect to MongoDB
# ─────────────────────────────────────
from flask import Flask, request, jsonify
from pymongo import MongoClient

# ─────────────────────────────────────
# APP SETUP
# ─────────────────────────────────────
app = Flask(__name__)

# ─────────────────────────────────────
# MONGODB CONNECTION
# ─────────────────────────────────────
client     = MongoClient("mongodb://localhost:27017/")
db         = client["todo_db"]
collection = db["todos"]

# ─────────────────────────────────────
# ROUTE: POST /submittodoitem
# PURPOSE: accept and save todo item
# RECEIVES: itemName, itemDescription
# RETURNS:  201 Created + saved item
# ─────────────────────────────────────
@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():

    # STEP 1 — check JSON was sent
    if not request.is_json:
        return jsonify({
            "error": "Request must be JSON"
        }), 400

    # STEP 2 — read incoming data
    data            = request.json
    item_name       = data.get("itemName")
    item_description = data.get("itemDescription")

    # STEP 3 — validate required fields
    if not item_name:
        return jsonify({
            "error": "itemName is required"
        }), 400

    if not item_description:
        return jsonify({
            "error": "itemDescription is required"
        }), 400

    # STEP 4 — save to MongoDB
    todo_item = {
        "itemName"       : item_name,
        "itemDescription": item_description,
    }
    result = collection.insert_one(todo_item)

    # STEP 5 — return success
    return jsonify({
        "message": "Todo item saved successfully",
        "id"     : str(result.inserted_id),
    }), 201


# ─────────────────────────────────────
# RUN APP
# ─────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)