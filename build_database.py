<<<<<<< HEAD
from sqlalchemy import text
from config import app, db


# ==========================================
# PART 1: DATA DEFINITIONS
# ==========================================

# 1.1 Lookup Data (The missing piece that caused your error)
# We wrap these in T-SQL "IF NOT EXISTS" checks so you can run this script multiple times safely.
SQL_LOOKUP_DATA = [
    """
    -- Insert Users if they don't exist
    IF NOT EXISTS (SELECT * FROM CW2.[USER] WHERE Username = 'Grace')
    BEGIN
        INSERT INTO CW2.[USER] (Username, Email, Password_Hash, Role) VALUES 
        ('Grace', 'grace@plymouth.ac.uk', 'ISAD123!', 'Admin'), 
        ('Tim Berners-Lee', 'tim@plymouth.ac.uk', 'COMP2001!', 'User'), 
        ('Ada Lovelace', 'ada@plymouth.ac.uk', 'insecurePassword', 'User');
    END
    """,
    """
    -- Insert Categories
    IF NOT EXISTS (SELECT * FROM CW2.CATEGORY WHERE Category_Name = 'Coastal')
    BEGIN
        INSERT INTO CW2.CATEGORY (Category_Name) VALUES ('Coastal'), ('Forest'), ('Mountain');
    END
    """,
    """
    -- Insert Difficulties
    IF NOT EXISTS (SELECT * FROM CW2.DIFFICULTY WHERE Difficulty_Name = 'Easy')
    BEGIN
        INSERT INTO CW2.DIFFICULTY (Difficulty_Name) VALUES ('Easy'), ('Medium'), ('Hard');
    END
    """,
    """
    -- Insert Route Types
    IF NOT EXISTS (SELECT * FROM CW2.ROUTE_TYPE WHERE Route_Type = 'Loop')
    BEGIN
        INSERT INTO CW2.ROUTE_TYPE (Route_Type) VALUES ('Loop'), ('Point to Point'), ('Out & Back');
    END
    """
]

SQL_FEATURES_DATA = [
    """
    -- Insert Features
    IF NOT EXISTS (SELECT * FROM CW2.FEATURE WHERE Feature_Name = 'Views')
    BEGIN
        INSERT INTO CW2.FEATURE (Feature_Name, Feature_Description) VALUES 
        ('Views', 'Panoramic scenery and designated lookout points.'),
        ('Waterfall', 'A natural waterfall is present.'),
        ('Rail trails', 'Converted railway track for easy walking and cycling.');
    END
    """
]

# 1.2 Trail Data (Your existing data)
TRAILS_DATA = [
    {
        "name": "Plymbridge Circular",
        "desc": "A beautiful walk through the woods.",
        "loc": "Plymbridge Woods",
        "dist": 5.00,
        "gain": 120,
        "time": 90,
        "info": "Car can park in the public carpark.",
        "cat": 2,  # Forest (ID 2 will exist now)
        "diff": 1, # Easy
        "route": 1, # Loop
        "user": 1   # Grace
    },
    {
        "name": "Old Rag Mountain Loop",
        "desc": "Challenging hike with great views.",
        "loc": "Shenandoah National Park",
        "dist": 14.8,
        "gain": 795,
        "time": 240,
        "info": "Blue blazes marked with handwritten numbers.",
        "cat": 3, # Mountain
        "diff": 3, # Hard
        "route": 1,
        "user": 2 # Tim
    }
]

SQL_TRAIL_POINTS_DATA = [
    """
    -- Insert Trail Points for Trail ID 1
    -- We check if 'Start Point' exists for Trail 1 to avoid duplicates
    IF NOT EXISTS (SELECT * FROM CW2.TRAIL_POINT WHERE Trail_ID = 1 AND Point_of_Interest = 'Start Point')
    BEGIN
        INSERT INTO CW2.TRAIL_POINT (Trail_ID, Point_of_Interest, Location_Point, Longitude, Latitude) VALUES
        (1, 'Start Point', 'Car Park', -4.093450, 50.407620),
        (1, 'Bridge View', 'Old Bridge', -4.091200, 50.409800);
    END
    """
]


# ==========================================
# PART 2: EXECUTION FUNCTIONS
# ==========================================

def seed_lookups():
    """Inserts Users, Categories, Difficulties, and Route_Types."""
    print("1. Seeding Lookup Tables...")
    try:
        for sql_command in SQL_LOOKUP_DATA:
            db.session.execute(text(sql_command))
        db.session.commit()
        print("   -> Success: Lookup tables populated.")
    except Exception as e:
        db.session.rollback()
        print(f"   -> Error seeding lookups: {e}")


def seed_features():
    """Inserts features."""
    print("2. Seeding Features...")
    try:
        for sql_command in SQL_FEATURES_DATA:
            db.session.execute(text(sql_command))
        db.session.commit()
        print("   -> Success: Features populated.")
    except Exception as e:
        db.session.rollback()
        print(f"   -> Error seeding features: {e}")


def seed_trails():
    """Inserts the Trails using Stored Procedure."""
    print("3. Seeding Trails...")
    
    for trail in TRAILS_DATA:
        try:
            # Check if trail already exists to avoid duplicates (Optional safety check)
            # This assumes Trail_Name is unique. If not, you can remove this check.
            check_sql = text("SELECT COUNT(*) FROM CW2.TRAIL WHERE Trail_Name = :name")
            result = db.session.execute(check_sql, {"name": trail['name']}).scalar()
            
            if result == 0:
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
                """)
                db.session.execute(sql, trail)
                db.session.commit()
                print(f"   -> Added: {trail['name']}")
            else:
                print(f"   -> Skipped: {trail['name']} (Already exists)")
            
        except Exception as e:
            db.session.rollback()
            print(f"   -> Failed to add {trail['name']}: {e}")


def seed_trail_points():
    """Inserts Trail_Points."""
    print("4. Seeding Trail_Points...")
    try:
        for sql_command in SQL_TRAIL_POINTS_DATA:
            db.session.execute(text(sql_command))
        db.session.commit()
        print("   -> Success: Trail_Points populated.")
    except Exception as e:
        db.session.rollback()
        print(f"   -> Error seeding trail_points: {e}")

# ==========================================
# PART 3: MAIN ENTRY POINT
# ==========================================

if __name__ == "__main__":
    # We must use app.app_context() because we are using 'db' outside of a web request
    with app.app_context():
        print("--- Starting Database Build ---")
        seed_lookups() # Step 1: Fixes your Foreign Key Error
        seed_features()
        seed_trails()  # Step 2: Adds your trails
        seed_trail_points()
=======
from sqlalchemy import text
from config import app, db


# ==========================================
# PART 1: DATA DEFINITIONS
# ==========================================

# 1.1 Lookup Data (The missing piece that caused your error)
# We wrap these in T-SQL "IF NOT EXISTS" checks so you can run this script multiple times safely.
SQL_LOOKUP_DATA = [
    """
    -- Insert Users if they don't exist
    IF NOT EXISTS (SELECT * FROM CW2.[USER] WHERE Username = 'Grace')
    BEGIN
        INSERT INTO CW2.[USER] (Username, Email, Password_Hash, Role) VALUES 
        ('Grace', 'grace@plymouth.ac.uk', 'ISAD123!', 'Admin'), 
        ('Tim Berners-Lee', 'tim@plymouth.ac.uk', 'COMP2001!', 'User'), 
        ('Ada Lovelace', 'ada@plymouth.ac.uk', 'insecurePassword', 'User');
    END
    """,
    """
    -- Insert Categories
    IF NOT EXISTS (SELECT * FROM CW2.CATEGORY WHERE Category_Name = 'Coastal')
    BEGIN
        INSERT INTO CW2.CATEGORY (Category_Name) VALUES ('Coastal'), ('Forest'), ('Mountain');
    END
    """,
    """
    -- Insert Difficulties
    IF NOT EXISTS (SELECT * FROM CW2.DIFFICULTY WHERE Difficulty_Name = 'Easy')
    BEGIN
        INSERT INTO CW2.DIFFICULTY (Difficulty_Name) VALUES ('Easy'), ('Medium'), ('Hard');
    END
    """,
    """
    -- Insert Route Types
    IF NOT EXISTS (SELECT * FROM CW2.ROUTE_TYPE WHERE Route_Type = 'Loop')
    BEGIN
        INSERT INTO CW2.ROUTE_TYPE (Route_Type) VALUES ('Loop'), ('Point to Point'), ('Out & Back');
    END
    """
]

SQL_FEATURES_DATA = [
    """
    -- Insert Features
    IF NOT EXISTS (SELECT * FROM CW2.FEATURE WHERE Feature_Name = 'Views')
    BEGIN
        INSERT INTO CW2.FEATURE (Feature_Name, Feature_Description) VALUES 
        ('Views', 'Panoramic scenery and designated lookout points.'),
        ('Waterfall', 'A natural waterfall is present.'),
        ('Rail trails', 'Converted railway track for easy walking and cycling.');
    END
    """
]

# 1.2 Trail Data (Your existing data)
TRAILS_DATA = [
    {
        "name": "Plymbridge Circular",
        "desc": "A beautiful walk through the woods.",
        "loc": "Plymbridge Woods",
        "dist": 5.00,
        "gain": 120,
        "time": 90,
        "info": "Car can park in the public carpark.",
        "cat": 2,  # Forest (ID 2 will exist now)
        "diff": 1, # Easy
        "route": 1, # Loop
        "user": 1   # Grace
    },
    {
        "name": "Old Rag Mountain Loop",
        "desc": "Challenging hike with great views.",
        "loc": "Shenandoah National Park",
        "dist": 14.8,
        "gain": 795,
        "time": 240,
        "info": "Blue blazes marked with handwritten numbers.",
        "cat": 3, # Mountain
        "diff": 3, # Hard
        "route": 1,
        "user": 2 # Tim
    }
]

SQL_TRAIL_POINTS_DATA = [
    """
    -- Insert Trail Points for Trail ID 1
    -- We check if 'Start Point' exists for Trail 1 to avoid duplicates
    IF NOT EXISTS (SELECT * FROM CW2.TRAIL_POINT WHERE Trail_ID = 1 AND Point_of_Interest = 'Start Point')
    BEGIN
        INSERT INTO CW2.TRAIL_POINT (Trail_ID, Point_of_Interest, Location_Point, Longitude, Latitude) VALUES
        (1, 'Start Point', 'Car Park', -4.093450, 50.407620),
        (1, 'Bridge View', 'Old Bridge', -4.091200, 50.409800);
    END
    """
]


# ==========================================
# PART 2: EXECUTION FUNCTIONS
# ==========================================

def seed_lookups():
    """Inserts Users, Categories, Difficulties, and Route_Types."""
    print("1. Seeding Lookup Tables...")
    try:
        for sql_command in SQL_LOOKUP_DATA:
            db.session.execute(text(sql_command))
        db.session.commit()
        print("   -> Success: Lookup tables populated.")
    except Exception as e:
        db.session.rollback()
        print(f"   -> Error seeding lookups: {e}")


def seed_features():
    """Inserts features."""
    print("2. Seeding Features...")
    try:
        for sql_command in SQL_FEATURES_DATA:
            db.session.execute(text(sql_command))
        db.session.commit()
        print("   -> Success: Features populated.")
    except Exception as e:
        db.session.rollback()
        print(f"   -> Error seeding features: {e}")


def seed_trails():
    """Inserts the Trails using Stored Procedure."""
    print("3. Seeding Trails...")
    
    for trail in TRAILS_DATA:
        try:
            # Check if trail already exists to avoid duplicates (Optional safety check)
            # This assumes Trail_Name is unique. If not, you can remove this check.
            check_sql = text("SELECT COUNT(*) FROM CW2.TRAIL WHERE Trail_Name = :name")
            result = db.session.execute(check_sql, {"name": trail['name']}).scalar()
            
            if result == 0:
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
                """)
                db.session.execute(sql, trail)
                db.session.commit()
                print(f"   -> Added: {trail['name']}")
            else:
                print(f"   -> Skipped: {trail['name']} (Already exists)")
            
        except Exception as e:
            db.session.rollback()
            print(f"   -> Failed to add {trail['name']}: {e}")


def seed_trail_points():
    """Inserts Trail_Points."""
    print("4. Seeding Trail_Points...")
    try:
        for sql_command in SQL_TRAIL_POINTS_DATA:
            db.session.execute(text(sql_command))
        db.session.commit()
        print("   -> Success: Trail_Points populated.")
    except Exception as e:
        db.session.rollback()
        print(f"   -> Error seeding trail_points: {e}")

# ==========================================
# PART 3: MAIN ENTRY POINT
# ==========================================

if __name__ == "__main__":
    # We must use app.app_context() because we are using 'db' outside of a web request
    with app.app_context():
        print("--- Starting Database Build ---")
        seed_lookups() # Step 1: Fixes your Foreign Key Error
        seed_features()
        seed_trails()  # Step 2: Adds your trails
        seed_trail_points()
>>>>>>> e2889fc1841252d7c44d92ac0068773bc7bfc1eb
        print("--- Database Build Complete ---")