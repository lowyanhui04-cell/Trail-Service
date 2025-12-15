from flask import abort
from config import db
from models import Feature, TrailFeature, features_schema, feature_schema, Trail, trail_feature_schema

# ==========================
# FEATURE CRUD
# ==========================
def read_all():
    """GET /features"""
    features = Feature.query.all()
    return features_schema.dump(features)

def create_feature(body):
    """POST /features"""
    new_feat = Feature(
        Feature_Name=body.get("Feature_Name"),
        Feature_Description=body.get("Feature_Description")
    )
    db.session.add(new_feat)
    db.session.commit()
    return feature_schema.dump(new_feat), 201

def read_one_feature(id):
    """GET /features/{id}"""
    feat = Feature.query.get(id)
    if feat: return feature_schema.dump(feat)
    else: abort(404, f"Feature {id} not found")

def update_feature(id, body):
    """PUT /features/{id}"""
    feat = Feature.query.get(id)
    if feat:
        feat.Feature_Name = body.get("Feature_Name")
        feat.Feature_Description = body.get("Feature_Description")
        db.session.commit()
        return feature_schema.dump(feat)
    else: abort(404, f"Feature {id} not found")

def delete_feature(id):
    """DELETE /features/{id}"""
    feat = Feature.query.get(id)
    if feat:
        db.session.delete(feat)
        db.session.commit()
        return {"message": f"Feature {id} deleted"}, 204
    else: abort(404, f"Feature {id} not found")

# ==========================
# LINKING LOGIC (Already existed)
# ==========================
def add_feature_to_trail(trail_id, feature_id):
    """POST /trails/{trail_id}/features/{feature_id}"""
    if Trail.query.filter(Trail.Trail_ID == trail_id).count() == 0:
        abort(404, f"Trail {trail_id} not found")
    if Feature.query.filter(Feature.Feature_ID == feature_id).count() == 0:
        abort(404, f"Feature {feature_id} not found")

    try:
        new_link = TrailFeature(Trail_ID=trail_id, Feature_ID=feature_id)
        db.session.add(new_link)
        db.session.commit()
        return {"message": "Feature linked successfully"}, 201
    except Exception as e:
        db.session.rollback()
        return {"message": f"Could not link feature: {str(e)}"}, 400