from models import db, Cupcake

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
Cupcake.query.delete()

# Add cupcakes
cupcake1 = Cupcake(
        flavor='chocolate',
        size='mini',
        rating=5.0,
    )

cupcake2 = Cupcake(
        flavor='vanilla',
        size='mini',
        rating=4.0,
    )

cupcake3 = Cupcake(
        flavor='strawberry',
        size='mini',
        rating=2.0,
    )

db.session.add(cupcake1)
db.session.add(cupcake2)
db.session.add(cupcake3)

db.session.commit()
