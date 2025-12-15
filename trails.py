from flask import abort, request, current_app
from sqlalchemy import text
from config import db
from models import (
    Trail, trail_schema, trails_schema, trails_public_schema,
    TrailPoint, trail_point_schema, trail_points_schema
)
from auth import token_required
import jwt

# Helper to check Admin role
def is_admin():
    token = request.headers['Authorization'].split(" ")[1]
    data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
    return data['Role'] == 'Admin'

# ==========================================
# PART 1: TRAIL CRUD OPERATIONS
# ==========================================

def read_all():
    """GET /trails (Public)"""
    trails = Trail.query.all()
    return trails_public_schema.dump(trails)

def read_one(trail_id):
    """GET /trails/{trail_id} (Public)"""
    trail = Trail.query.filter(Trail.Trail_ID == trail_id).one_or_none()
    if trail is not None:
        return trail_schema.dump(trail)
    else:
        abort(404, f"Trail {trail_id} not found")

@token_required 
def create(current_user_id, trail):
    """POST /trails (Admin Only)"""
    if not is_admin(): abort(403, "Permission Denied: Admins only.")

    try:
        sql = text("""
            DECLARE @NewID INT;
            EXEC CW2.sp_InsertTrail 
                @Trail_Name = :name, @Trail_Description = :desc, @Location = :loc,
                @Distance = :dist, @Elevation_Gain = :gain, @Estimate_Time = :time,
                @Trail_Info = :info, @Category_ID = :cat, @Difficulty_ID = :diff,
                @Route_ID = :route, @User_ID = :user, @New_Trail_ID = @NewID OUTPUT;
            SELECT @NewID;
        """)
        
        result = db.session.execute(sql, {
            'name': trail.get("Trail_Name"), 'desc': trail.get("Trail_Description"),
            'loc': trail.get("Location"), 'dist': trail.get("Distance"),
            'gain': trail.get("Elevation_Gain"), 'time': trail.get("Estimate_Time"),
            'info': trail.get("Trail_Info"), 'cat': trail.get("Category_ID"),
            'diff': trail.get("Difficulty_ID"), 'route': trail.get("Route_ID"),
            'user': current_user_id 
        })
        db.session.commit()
        return {'message': 'Trail created successfully'}, 201
    except Exception as e:
        db.session.rollback()
        abort(500, f"Error creating trail: {str(e)}")

@token_required
def update(current_user_id, trail_id, trail):
    """PUT /trails/{trail_id} (Admin Only)"""
    if not is_admin(): abort(403, "Permission Denied: Admins only.")

    existing_trail = Trail.query.filter(Trail.Trail_ID == trail_id).one_or_none()
    if existing_trail:
        try:
            sql = text("""
                EXEC CW2.sp_UpdateTrail 
                    @Trail_ID = :id, @Trail_Name = :name, @Location = :loc, @Distance = :dist
            """)
            db.session.execute(sql, {
                'id': trail_id, 'name': trail.get("Trail_Name"),
                'loc': trail.get("Location"), 'dist': trail.get("Distance")
            })
            db.session.commit()
            return {'message': f'Trail {trail_id} updated successfully'}, 200
        except Exception as e:
            db.session.rollback()
            abort(500, f"Error updating trail: {str(e)}")
    else:
        abort(404, f"Trail {trail_id} not found")

@token_required
def delete(current_user_id, trail_id):
    """DELETE /trails/{trail_id} (Admin Only)"""
    if not is_admin(): abort(403, "Permission Denied: Admins only.")

    existing_trail = Trail.query.filter(Trail.Trail_ID == trail_id).one_or_none()
    if existing_trail:
        try:
            sql = text("EXEC CW2.sp_DeleteTrail @Trail_ID = :id")
            db.session.execute(sql, {'id': trail_id})
            db.session.commit()
            return {'message': f'Trail {trail_id} successfully deleted'}, 204
        except Exception as e:
            db.session.rollback()
            abort(500, f"Error deleting trail: {str(e)}")
    else:
        abort(404, f"Trail {trail_id} not found")

# ==========================================
# PART 2: POINTS (Admin Only for Edit/Delete)
# ==========================================

def get_points(trail_id):
    """GET /trails/{trail_id}/points (Public)"""
    if Trail.query.filter(Trail.Trail_ID == trail_id).count() == 0:
        abort(404, f"Trail {trail_id} not found")
    points = TrailPoint.query.filter(TrailPoint.Trail_ID == trail_id).all()
    return trail_points_schema.dump(points)

@token_required
def add_point(current_user_id, trail_id, point):
    """POST /trails/{trail_id}/points (Admin Only)"""
    if not is_admin(): abort(403, "Permission Denied: Admins only.")

    if Trail.query.filter(Trail.Trail_ID == trail_id).count() == 0:
        abort(404, f"Trail {trail_id} not found")
    try:
        new_point = TrailPoint(
            Trail_ID=trail_id,
            Point_of_Interest=point.get("Point_of_Interest"),
            Location_Point=point.get("Location_Point"),
            Longitude=point.get("Longitude"),
            Latitude=point.get("Latitude")
        )
        db.session.add(new_point)
        db.session.commit()
        return trail_point_schema.dump(new_point), 201
    except Exception as e:
        db.session.rollback()
        abort(500, f"Error adding point: {str(e)}")

def read_one_point(point_id):
    """GET /points/{point_id} (Public)"""
    point = TrailPoint.query.get(point_id)
    if point: return trail_point_schema.dump(point)
    else: abort(404, f"Point {point_id} not found")

@token_required
def update_point(current_user_id, point_id, body):
    """PUT /points/{point_id} (Admin Only)"""
    if not is_admin(): abort(403, "Permission Denied: Admins only.")

    point = TrailPoint.query.get(point_id)
    if point:
        point.Point_of_Interest = body.get("Point_of_Interest")
        point.Location_Point = body.get("Location_Point")
        point.Longitude = body.get("Longitude")
        point.Latitude = body.get("Latitude")
        db.session.commit()
        return trail_point_schema.dump(point)
    else: abort(404, f"Point {point_id} not found")

@token_required
def delete_point(current_user_id, point_id):
    """DELETE /points/{point_id} (Admin Only)"""
    if not is_admin(): abort(403, "Permission Denied: Admins only.")

    point = TrailPoint.query.get(point_id)
    if point:
        db.session.delete(point)
        db.session.commit()
        return {"message": f"Point {point_id} deleted"}, 204
    else: abort(404, f"Point {point_id} not found")