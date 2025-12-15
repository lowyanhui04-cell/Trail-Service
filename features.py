from flask import abort
from config import db
from models import Feature, TrailFeature, features_schema, feature_schema, Trail, trail_feature_schema
from auth import token_required
import jwt
from flask import current_app, request

# Helper to check Admin role manually inside the function
def is_admin():
    token = request.headers['Authorization'].split(" ")[1]
    data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
    return data['Role'] == 'Admin'

def read_all():
    """GET /features"""
    features = Feature.query.all()
    return features_schema.dump(features)

@token_required
def create_feature(current_user_id, body):
    """POST /features"""
    if not is_admin(): abort(403, "Permission Denied: Admins only.")
    
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

@token_required
def update_feature(current_user_id, id, body):
    """PUT /features/{id}"""
    if not is_admin(): abort(403, "Permission Denied: Admins only.")

    feat = Feature.query.get(id)
    if feat:
        feat.Feature_Name = body.get("Feature_Name")
        feat.Feature_Description = body.get("Feature_Description")
        db.session.commit()
        return feature_schema.dump(feat)
    else: abort(404, f"Feature {id} not found")

@token_required
def delete_feature(current_user_id, id):
    """DELETE /features/{id}"""
    if not is_admin(): abort(403, "Permission Denied: Admins only.")

    feat = Feature.query.get(id)
    if feat:
        db.session.delete(feat)
        db.session.commit()
        return {"message": f"Feature {id} deleted"}, 204
    else: abort(404, f"Feature {id} not found")

@token_required
def add_feature_to_trail(current_user_id, trail_id, feature_id):
    """POST /trails/{trail_id}/features/{feature_id}"""
    if not is_admin(): abort(403, "Permission Denied: Admins only.")

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