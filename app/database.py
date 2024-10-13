from sqlalchemy import text

def insert_crack_coordinates(x_start, y_start, x_end, y_end, session):
    query = text("""
        INSERT INTO crackcoordinates (x_start, y_start, x_end, y_end)
        VALUES (:x_start, :y_start, :x_end, :y_end) RETURNING id
    """)
    
    result = session.execute(query, {
        'x_start': x_start,
        'y_start': y_start,
        'x_end': x_end,
        'y_end': y_end
    })
    
    return result.fetchone()[0]

def insert_crack_summary(image_id, crack_count, session):
    query = text("""
        INSERT INTO cracksummary (image_id, crack_count)
        VALUES (:image_id, :crack_count)
    """)
    
    session.execute(query, {
        'image_id': image_id,
        'crack_count': crack_count
    })
