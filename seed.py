from models import User, db
from app import app

with app.app_context():
    db.drop_all()
    db.create_all()
    User.query.delete()

# Add users
Regina = User(first_name='Regina', 
              last_name='George', 
              image_url='https://www.collegefashion.net/wp-content/uploads/2019/02/screen-shot-2019-01-01-at-114050-am.png' )

Cady = User(first_name='Cady', 
            last_name='Heron', 
            image_url= 'https://pbs.twimg.com/profile_images/1392858015829737474/xjSoA6_O_400x400.jpg')

Gretchen = User(first_name='Gretchen', 
                last_name='Weiners', 
                image_url='https://miro.medium.com/max/1400/0*o2-o5DEdv1IWm2Qw.jpg')

Karen = User(first_name='Karen', 
             last_name='Smith', 
             image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQLtEeLadxHXNDHB2yTQuJ-WEpNsxHmWYB4aA&usqp=CAU')

Janis = User(first_name='Janis', 
             last_name='Ian', 
             image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBz5VqgFzwt7oC53vDnAw-Ugy32-67nUl84A&usqp=CAU')

Aaron = User(first_name='Aron', 
             last_name='Samuels', 
             image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRzYhMCCUdh4AVIbKlfy1ySCMnmTaRxDepTsQ&usqp=CAU')

John = User(first_name='John', last_name='Doe')

# Add new objects to session, so they'll persist
with app.app_context():
    db.session.add(Regina)
    db.session.add(Cady)
    db.session.add(Gretchen)
    db.session.add(Karen)
    db.session.add(Janis)
    db.session.add(Aaron)
    db.session.add(John)


# Commit--otherwise, this never gets saved!
    db.session.commit()
