from flask import Blueprint, request, jsonify
import sqlite3, datetime

bp = Blueprint('sensor', __name__, url_prefix='/sensor')

# 센서에서 값 받기
@bp.route('', methods=['POST'])
def receive_sensor_data():
    distance = request.form.get('distance')
    if not distance:
        return "NO DATA", 400

    conn = sqlite3.connect('ultrasonic_data.db')
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO distance_data (timestamp, distance_cm) VALUES (?, ?)",
        (datetime.datetime.now().isoformat(), float(distance))
    )
    conn.commit()
    conn.close()
    return "OK", 200

# 최근 10개 값 보기 (웹에서 확인용)
@bp.route('/recent', methods=['GET'])
def recent_data():
    conn = sqlite3.connect('ultrasonic_data.db')
    cur = conn.cursor()
    cur.execute("SELECT timestamp, distance_cm FROM distance_data ORDER BY id DESC LIMIT 10")
    rows = cur.fetchall()
    conn.close()
    # 간단히 JSON으로 반환 (원하면 HTML로 바꿔줄 수 있음)
    return jsonify([{"timestamp": ts, "distance_cm": dist} for ts, dist in rows])
