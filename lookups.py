from config import db
from models import Category, Difficulty, RouteType
from models import category_schema, difficulty_schema, route_type_schema
from flask import abort

# ==========================
# CATEGORY CRUD
# ==========================
def get_categories():
    """GET /categories"""
    data = Category.query.all()
    return category_schema.dump(data)

def create_category(category_body):
    """POST /categories"""
    name = category_body.get("Category_Name")
    new_cat = Category(Category_Name=name)
    db.session.add(new_cat)
    db.session.commit()
    return category_schema.dump(new_cat), 201

def read_one_category(id):
    """GET /categories/{id}"""
    cat = Category.query.get(id)
    if cat: return category_schema.dump(cat)
    else: abort(404, f"Category {id} not found")

def update_category(id, category_body):
    """PUT /categories/{id}"""
    cat = Category.query.get(id)
    if cat:
        cat.Category_Name = category_body.get("Category_Name")
        db.session.commit()
        return category_schema.dump(cat)
    else: abort(404, f"Category {id} not found")

def delete_category(id):
    """DELETE /categories/{id}"""
    cat = Category.query.get(id)
    if cat:
        db.session.delete(cat)
        db.session.commit()
        return {"message": f"Category {id} deleted"}, 204
    else: abort(404, f"Category {id} not found")

# ==========================
# DIFFICULTY CRUD
# ==========================
def get_difficulties():
    """GET /difficulties"""
    data = Difficulty.query.all()
    return difficulty_schema.dump(data)

def create_difficulty(body):
    """POST /difficulties"""
    new_diff = Difficulty(Difficulty_Name=body.get("Difficulty_Name"))
    db.session.add(new_diff)
    db.session.commit()
    return difficulty_schema.dump(new_diff), 201

def read_one_difficulty(id):
    """GET /difficulties/{id}"""
    diff = Difficulty.query.get(id)
    if diff: return difficulty_schema.dump(diff)
    else: abort(404, f"Difficulty {id} not found")

def update_difficulty(id, body):
    """PUT /difficulties/{id}"""
    diff = Difficulty.query.get(id)
    if diff:
        diff.Difficulty_Name = body.get("Difficulty_Name")
        db.session.commit()
        return difficulty_schema.dump(diff)
    else: abort(404, f"Difficulty {id} not found")

def delete_difficulty(id):
    """DELETE /difficulties/{id}"""
    diff = Difficulty.query.get(id)
    if diff:
        db.session.delete(diff)
        db.session.commit()
        return {"message": f"Difficulty {id} deleted"}, 204
    else: abort(404, f"Difficulty {id} not found")

# ==========================
# ROUTE TYPE CRUD
# ==========================
def get_route_types():
    """GET /route-types"""
    data = RouteType.query.all()
    return route_type_schema.dump(data)

def create_route_type(body):
    """POST /route-types"""
    new_rt = RouteType(Route_Type=body.get("Route_Type"))
    db.session.add(new_rt)
    db.session.commit()
    return route_type_schema.dump(new_rt), 201

def read_one_route_type(id):
    """GET /route-types/{id}"""
    rt = RouteType.query.get(id)
    if rt: return route_type_schema.dump(rt)
    else: abort(404, f"Route Type {id} not found")

def update_route_type(id, body):
    """PUT /route-types/{id}"""
    rt = RouteType.query.get(id)
    if rt:
        rt.Route_Type = body.get("Route_Type")
        db.session.commit()
        return route_type_schema.dump(rt)
    else: abort(404, f"Route Type {id} not found")

def delete_route_type(id):
    """DELETE /route-types/{id}"""
    rt = RouteType.query.get(id)
    if rt:
        db.session.delete(rt)
        db.session.commit()
        return {"message": f"Route Type {id} deleted"}, 204
    else: abort(404, f"Route Type {id} not found")