<<<<<<< HEAD
from flask import abort
from sqlalchemy import text
from config import db
# Combine all imports into one clean line
from models import (
    Trail, trail_schema, trails_schema, trails_public_schema,
    TrailPoint, trail_point_schema, trail_points_schema
)
from auth import token_required

# ==========================================
# PART 1: TRAIL CRUD OPERATIONS
# ==========================================

def read_all():
    """
    GET /trails
    Returns a LIMITED view of all trails (names, locations, etc.)
    Uses trails_public_schema to hide sensitive IDs/details.
    """
    trails = Trail.query.all()
    return trails_public_schema.dump(trails)

def read_one(trail_id):
    """
    GET /trails/{trail_id}
    Returns the FULL detailed view of a specific trail.
    Uses trail_schema to show everything.
    """
    trail = Trail.query.filter(Trail.Trail_ID == trail_id).one_or_none()
    
    if trail is not None:
        return trail_schema.dump(trail)
    else:
        abort(404, f"Trail {trail_id} not found")

@token_required 
def create(current_user_id, trail):  # <--- Secure version uses Token ID
    """
    POST /trails
    Now protected by Token!
    """
    try:
        sql = text("""
            DECLARE @NewID INT;
            EXEC CW2.sp_InsertTrail 
                @Trail_Name = :name,
                @Trail_Description = :desc,
                @Location = :loc,
                @Distance = :dist,
                @Elevation_Gain = :gain,
                @Estimate_Time = :time,
                @Trail_Info = :info,
                @Category_ID = :cat,
                @Difficulty_ID = :diff,
                @Route_ID = :route,
                @User_ID = :user,  -- We inject the ID from the token here
                @New_Trail_ID = @NewID OUTPUT;
            SELECT @NewID;
        """)
        
        result = db.session.execute(sql, {
            'name': trail.get("Trail_Name"),
            'desc': trail.get("Trail_Description"),
            'loc': trail.get("Location"),
            'dist': trail.get("Distance"),
            'gain': trail.get("Elevation_Gain"),
            'time': trail.get("Estimate_Time"),
            'info': trail.get("Trail_Info"),
            'cat': trail.get("Category_ID"),
            'diff': trail.get("Difficulty_ID"),
            'route': trail.get("Route_ID"),
            
            # SECURITY UPGRADE: Use the ID from the token, ignore the JSON body
            'user': current_user_id 
        })
        db.session.commit()
        return {'message': 'Trail created successfully'}, 201

    except Exception as e:
        db.session.rollback()
        abort(500, f"Error creating trail: {str(e)}")

def update(trail_id, trail):
    """
    PUT /trails/{trail_id}
    Updates a trail using the Stored Procedure 'CW2.sp_UpdateTrail'.
    """
    existing_trail = Trail.query.filter(Trail.Trail_ID == trail_id).one_or_none()

    if existing_trail:
        try:
            sql = text("""
                EXEC CW2.sp_UpdateTrail 
                    @Trail_ID = :id,
                    @Trail_Name = :name,
                    @Location = :loc,
                    @Distance = :dist
            """)
            
            db.session.execute(sql, {
                'id': trail_id,
                'name': trail.get("Trail_Name"),
                'loc': trail.get("Location"),
                'dist': trail.get("Distance")
            })
            db.session.commit()
            return {'message': f'Trail {trail_id} updated successfully'}, 200
        except Exception as e:
            db.session.rollback()
            abort(500, f"Error updating trail: {str(e)}")
    else:
        abort(404, f"Trail {trail_id} not found")

def delete(trail_id):
    """
    DELETE /trails/{trail_id}
    Deletes a trail using the Stored Procedure 'CW2.sp_DeleteTrail'.
    """
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
# PART 2: SUB-RESOURCE OPERATIONS (POINTS)
# ==========================================

def get_points(trail_id):
    """
    GET /trails/{trail_id}/points
    Returns all points for a specific trail.
    """
    # Verify trail exists first
    if Trail.query.filter(Trail.Trail_ID == trail_id).count() == 0:
        abort(404, f"Trail {trail_id} not found")
        
    points = TrailPoint.query.filter(TrailPoint.Trail_ID == trail_id).all()
    return trail_points_schema.dump(points)

def add_point(trail_id, point):
    """
    POST /trails/{trail_id}/points
    Adds a new point to a trail.
    """
    # Verify trail exists first
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


# ==========================================
# PART 3: POINT CRUD (Individual Points)
# ==========================================

def read_one_point(point_id):
    """GET /points/{point_id}"""
    point = TrailPoint.query.get(point_id)
    if point: return trail_point_schema.dump(point)
    else: abort(404, f"Point {point_id} not found")

def update_point(point_id, body):
    """PUT /points/{point_id}"""
    point = TrailPoint.query.get(point_id)
    if point:
        point.Point_of_Interest = body.get("Point_of_Interest")
        point.Location_Point = body.get("Location_Point")
        point.Longitude = body.get("Longitude")
        point.Latitude = body.get("Latitude")
        db.session.commit()
        return trail_point_schema.dump(point)
    else: abort(404, f"Point {point_id} not found")

def delete_point(point_id):
    """DELETE /points/{point_id}"""
    point = TrailPoint.query.get(point_id)
    if point:
        db.session.delete(point)
        db.session.commit()
        return {"message": f"Point {point_id} deleted"}, 204
=======
from flask import abort
from sqlalchemy import text
from config import db
# Combine all imports into one clean line
from models import (
    Trail, trail_schema, trails_schema, trails_public_schema,
    TrailPoint, trail_point_schema, trail_points_schema
)

# ==========================================
# PART 1: TRAIL CRUD OPERATIONS
# ==========================================

def read_all():
    """
    GET /trails
    Returns a LIMITED view of all trails (names, locations, etc.)
    Uses trails_public_schema to hide sensitive IDs/details.
    """
    trails = Trail.query.all()
    return trails_public_schema.dump(trails)

def read_one(trail_id):
    """
    GET /trails/{trail_id}
    Returns the FULL detailed view of a specific trail.
    Uses trail_schema to show everything.
    """
    trail = Trail.query.filter(Trail.Trail_ID == trail_id).one_or_none()
    
    if trail is not None:
        return trail_schema.dump(trail)
    else:
        abort(404, f"Trail {trail_id} not found")

def create(trail):
    """
    POST /trails
    Creates a new trail using the Stored Procedure 'CW2.sp_InsertTrail'.
    """
    try:
        sql = text("""
            DECLARE @NewID INT;
            EXEC CW2.sp_InsertTrail 
                @Trail_Name = :name,
                @Trail_Description = :desc,
                @Location = :loc,
                @Distance = :dist,
                @Elevation_Gain = :gain,
                @Estimate_Time = :time,
                @Trail_Info = :info,
                @Category_ID = :cat,
                @Difficulty_ID = :diff,
                @Route_ID = :route,
                @User_ID = :user,
                @New_Trail_ID = @NewID OUTPUT;
            SELECT @NewID;
        """)
        
        result = db.session.execute(sql, {
            'name': trail.get("Trail_Name"),
            'desc': trail.get("Trail_Description"),
            'loc': trail.get("Location"),
            'dist': trail.get("Distance"),
            'gain': trail.get("Elevation_Gain"),
            'time': trail.get("Estimate_Time"),
            'info': trail.get("Trail_Info"),
            'cat': trail.get("Category_ID"),
            'diff': trail.get("Difficulty_ID"),
            'route': trail.get("Route_ID"),
            'user': trail.get("User_ID")
        })
        db.session.commit()
        return {'message': 'Trail created successfully'}, 201

    except Exception as e:
        db.session.rollback()
        abort(500, f"Error creating trail: {str(e)}")

def update(trail_id, trail):
    """
    PUT /trails/{trail_id}
    Updates a trail using the Stored Procedure 'CW2.sp_UpdateTrail'.
    """
    existing_trail = Trail.query.filter(Trail.Trail_ID == trail_id).one_or_none()

    if existing_trail:
        try:
            sql = text("""
                EXEC CW2.sp_UpdateTrail 
                    @Trail_ID = :id,
                    @Trail_Name = :name,
                    @Location = :loc,
                    @Distance = :dist
            """)
            
            db.session.execute(sql, {
                'id': trail_id,
                'name': trail.get("Trail_Name"),
                'loc': trail.get("Location"),
                'dist': trail.get("Distance")
            })
            db.session.commit()
            return {'message': f'Trail {trail_id} updated successfully'}, 200
        except Exception as e:
            db.session.rollback()
            abort(500, f"Error updating trail: {str(e)}")
    else:
        abort(404, f"Trail {trail_id} not found")

def delete(trail_id):
    """
    DELETE /trails/{trail_id}
    Deletes a trail using the Stored Procedure 'CW2.sp_DeleteTrail'.
    """
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
# PART 2: SUB-RESOURCE OPERATIONS (POINTS)
# ==========================================

def get_points(trail_id):
    """
    GET /trails/{trail_id}/points
    Returns all points for a specific trail.
    """
    # Verify trail exists first
    if Trail.query.filter(Trail.Trail_ID == trail_id).count() == 0:
        abort(404, f"Trail {trail_id} not found")
        
    points = TrailPoint.query.filter(TrailPoint.Trail_ID == trail_id).all()
    return trail_points_schema.dump(points)

def add_point(trail_id, point):
    """
    POST /trails/{trail_id}/points
    Adds a new point to a trail.
    """
    # Verify trail exists first
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


# ==========================================
# PART 3: POINT CRUD (Individual Points)
# ==========================================

def read_one_point(point_id):
    """GET /points/{point_id}"""
    point = TrailPoint.query.get(point_id)
    if point: return trail_point_schema.dump(point)
    else: abort(404, f"Point {point_id} not found")

def update_point(point_id, body):
    """PUT /points/{point_id}"""
    point = TrailPoint.query.get(point_id)
    if point:
        point.Point_of_Interest = body.get("Point_of_Interest")
        point.Location_Point = body.get("Location_Point")
        point.Longitude = body.get("Longitude")
        point.Latitude = body.get("Latitude")
        db.session.commit()
        return trail_point_schema.dump(point)
    else: abort(404, f"Point {point_id} not found")

def delete_point(point_id):
    """DELETE /points/{point_id}"""
    point = TrailPoint.query.get(point_id)
    if point:
        db.session.delete(point)
        db.session.commit()
        return {"message": f"Point {point_id} deleted"}, 204
>>>>>>> e2889fc1841252d7c44d92ac0068773bc7bfc1eb
    else: abort(404, f"Point {point_id} not found")