#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    users = User.query.filter(User.user_hash == None).all()
    for user in users:
        user.user_hash = user.generate_user_hash()
        db.session.add(user)
    db.session.commit()
    print(f'✅ {len(users)} usuários atualizados com hash')
