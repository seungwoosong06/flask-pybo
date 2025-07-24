import time
from datetime import datetime
from pybo import create_app, db
from pybo.models import Distance
import random  # 테스트용 랜덤값

app = create_app()

with app.app_context():
    while True:
        dist = random.uniform(50, 300)  # 실제 센서값 넣으세요
        data = Distance(distance=dist)
        db.session.add(data)
        db.session.commit()
        print(f"Saved distance: {dist:.2f} cm at {datetime.now()}")
        time.sleep(2)
