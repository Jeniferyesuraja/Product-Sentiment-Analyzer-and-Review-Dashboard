"""MongoDB persistence with a useful in-memory fallback for local demos."""

from collections import Counter
from datetime import datetime
from uuid import uuid4

try:
    from pymongo import MongoClient
    from bson import ObjectId
except ImportError:
    MongoClient = None
    ObjectId = None


class Database:
    def __init__(self):
        self.client = None
        self.products = []
        self.reviews = []
        self.history = []
        self.favorites = []

    def connect(self, uri, name):
        if uri and MongoClient:
            self.client = MongoClient(uri, serverSelectionTimeoutMS=1500)
            self.client.admin.command("ping")
            self.db = self.client[name]

    def save_product(self, name, source):
        document = {"_id": str(uuid4()), "name": name, "source": source, "created_at": datetime.utcnow().isoformat()}
        if self.client:
            self.db.products.update_one({"name": name}, {"$set": {key: value for key, value in document.items() if key != "_id"}}, upsert=True)
        else:
            self.products = [item for item in self.products if item["name"].lower() != name.lower()]
            self.products.append(document)
        return document

    def save_reviews(self, reviews):
        for review in reviews:
            review.setdefault("_id", str(uuid4()))
        if self.client:
            self.db.reviews.insert_many(reviews)
        else:
            self.reviews.extend(reviews)

    def list_products(self):
        products = list(self.db.products.find({})) if self.client else self.products
        for product in products:
            if self.client:
                product["_id"] = str(product["_id"])
        for product in products:
            items = self.list_reviews(product["name"])
            ratings = [float(item.get("rating", 0)) for item in items]
            product["review_count"] = len(items)
            product["rating"] = round(sum(ratings) / len(ratings), 2) if ratings else 0
            product["sentiment"] = Counter(item.get("sentiment", "Neutral") for item in items).most_common(1)[0][0] if items else "Neutral"
        return products

    def list_reviews(self, product=None):
        if self.client:
            query = {"product": product} if product else {}
            items = list(self.db.reviews.find(query))
            for item in items:
                item["_id"] = str(item["_id"])
            return items
        return [item for item in self.reviews if not product or item["product"].lower() == product.lower()]

    def delete_review(self, review_id):
        if self.client:
            result = self.db.reviews.delete_one({"_id": ObjectId(review_id)}) if ObjectId and ObjectId.is_valid(review_id) else None
            return bool(result and result.deleted_count > 0)
        before = len(self.reviews)
        self.reviews = [item for item in self.reviews if item.get("_id") != review_id]
        return len(self.reviews) < before

    def list_history(self):
        if self.client:
            return list(self.db.analysis_history.find({}, {"_id": 0}).sort("created_at", -1))
        return sorted(self.history, key=lambda item: item["created_at"], reverse=True)

    def save_history(self, item):
        item.setdefault("_id", str(uuid4()))
        item.setdefault("created_at", datetime.utcnow().isoformat())
        if self.client:
            self.db.analysis_history.insert_one(item)
        else:
            self.history.append(item)
        return item

    def delete_history(self, history_id):
        if self.client:
            result = self.db.analysis_history.delete_one({"_id": history_id})
            return result.deleted_count > 0
        before = len(self.history)
        self.history = [item for item in self.history if item.get("_id") != history_id]
        return len(self.history) < before

    def list_favorites(self):
        if self.client:
            return list(self.db.favorites.find({}, {"_id": 0}))
        return self.favorites

    def toggle_favorite(self, product):
        existing = next((item for item in self.list_favorites() if item["name"].lower() == product["name"].lower()), None)
        if existing:
            if self.client:
                self.db.favorites.delete_one({"name": existing["name"]})
            else:
                self.favorites.remove(existing)
            return False
        product = {"_id": str(uuid4()), **product, "created_at": datetime.utcnow().isoformat()}
        if self.client:
            self.db.favorites.insert_one(product)
        else:
            self.favorites.append(product)
        return True

    def overview(self):
        reviews = self.list_reviews()
        products = self.list_products()
        counts = Counter(item.get("sentiment", "Neutral") for item in reviews)
        ratings = [float(item.get("rating", 0)) for item in reviews]
        return {
            "total_products": len(products),
            "total_reviews": len(reviews),
            "positive": counts["Positive"],
            "negative": counts["Negative"],
            "neutral": counts["Neutral"],
            "average_rating": round(sum(ratings) / len(ratings), 2) if ratings else 0,
        }

    def word_frequency(self, product):
        words = Counter()
        for review in self.list_reviews(product):
            words.update(word for word in review["text"].split() if len(word) > 3)
        return [{"word": word, "count": count} for word, count in words.most_common(10)]


database = Database()


def init_database(config):
    try:
        database.connect(config["MONGODB_URI"], config["MONGODB_DATABASE"])
    except Exception:
        database.client = None
