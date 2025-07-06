#!/usr/bin/env python3

from database import init_db, SessionLocal
from models.user import User

def test_database():
    try:
        print("正在初始化数据库...")
        init_db()
        print("数据库初始化成功！")
        
        # 测试创建用户
        db = SessionLocal()
        try:
            test_user = User(
                username="test_user",
                password="test_password",
                role="user"
            )
            db.add(test_user)
            db.commit()
            print("用户创建成功！")
            
            # 查询用户
            user = db.query(User).filter(User.username == "test_user").first()
            if user:
                print(f"查询成功！用户ID: {user.id}, 用户名: {user.username}")
            else:
                print("查询失败！")
                
        finally:
            db.close()
            
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_database()