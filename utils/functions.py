def serialize_document(document: dict) -> dict:
    if document and "_id" in document:
        document["id"] = str(document["_id"])
        del document["_id"]
    return document