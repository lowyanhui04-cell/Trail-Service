from config import db, ma

class Category(db.Model):
    __tablename__ = "CATEGORY"
    __table_args__ = {"schema": "CW2"}
    Category_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Category_Name = db.Column(db.String(255), nullable=False)

class Difficulty(db.Model):
    __tablename__ = "DIFFICULTY"
    __table_args__ = {"schema": "CW2"}
    Difficulty_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Difficulty_Name = db.Column(db.String(255), nullable=False)

class RouteType(db.Model):
    __tablename__ = "ROUTE_TYPE"
    __table_args__ = {"schema": "CW2"}
    Route_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Route_Type = db.Column(db.String(255), nullable=False)

class Feature(db.Model):
    __tablename__ = "FEATURE"
    __table_args__ = {"schema": "CW2"}
    Feature_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Feature_Name = db.Column(db.String(255), nullable=False, unique=True)
    Feature_Description = db.Column(db.String)

class Trail(db.Model):
    __tablename__ = "TRAIL"
    __table_args__ = {"schema": "CW2"}

    Trail_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Trail_Name = db.Column(db.String(255), nullable=False)
    Trail_Description = db.Column(db.String) 
    Location = db.Column(db.String(255), nullable=False)
    Distance = db.Column(db.Numeric(10, 2), nullable=False)
    Elevation_Gain = db.Column(db.Integer)
    Estimate_Time = db.Column(db.Integer)
    Trail_Info = db.Column(db.String)
    Category_ID = db.Column(db.Integer, nullable=False)
    Difficulty_ID = db.Column(db.Integer, nullable=False)
    Route_ID = db.Column(db.Integer, nullable=False)
    User_ID = db.Column(db.Integer, nullable=False)

class TrailPoint(db.Model):
    __tablename__ = "TRAIL_POINT"
    __table_args__ = {"schema": "CW2"}

    Point_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Trail_ID = db.Column(db.Integer, db.ForeignKey("CW2.TRAIL.Trail_ID"), nullable=False)
    Point_of_Interest = db.Column(db.String(255))
    Location_Point = db.Column(db.String(255))
    Longitude = db.Column(db.Numeric(9, 6), nullable=False)
    Latitude = db.Column(db.Numeric(8, 6), nullable=False)

class TrailFeature(db.Model):
    __tablename__ = "TRAIL_FEATURE"
    __table_args__ = {"schema": "CW2"}

    Trail_ID = db.Column(db.Integer, db.ForeignKey("CW2.TRAIL.Trail_ID"), primary_key=True)
    Feature_ID = db.Column(db.Integer, db.ForeignKey("CW2.FEATURE.Feature_ID"), primary_key=True)

class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True
        sqla_session = db.session

class DifficultySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Difficulty
        load_instance = True
        sqla_session = db.session

class RouteTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RouteType
        load_instance = True
        sqla_session = db.session

class FeatureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Feature
        load_instance = True
        sqla_session = db.session

class TrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        load_instance = True
        sqla_session = db.session

class TrailPublicSchema(ma.SQLAlchemyAutoSchema):
    """Limited view for public/unauthenticated users"""
    class Meta:
        model = Trail
        load_instance = True
        sqla_session = db.session
        exclude = ('User_ID', 'Trail_Info', 'Trail_Description')

class TrailPointSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrailPoint
        load_instance = True
        sqla_session = db.session
        include_fk = True

class TrailFeatureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrailFeature
        load_instance = True
        sqla_session = db.session

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)

difficulty_schema = DifficultySchema()
difficulties_schema = DifficultySchema(many=True)

route_type_schema = RouteTypeSchema()
route_types_schema = RouteTypeSchema(many=True)

feature_schema = FeatureSchema()
features_schema = FeatureSchema(many=True)

trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)
trail_public_schema = TrailPublicSchema()
trails_public_schema = TrailPublicSchema(many=True)

trail_point_schema = TrailPointSchema()
trail_points_schema = TrailPointSchema(many=True)
trail_feature_schema = TrailFeatureSchema()