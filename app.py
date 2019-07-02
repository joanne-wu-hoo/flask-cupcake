from flask import Flask, jsonify, request, render_template, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake
from forms import CupcakeForm
from sqlalchemy import or_




app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

# debug = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcake-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


connect_db(app)
db.create_all()

@app.route("/", methods=["GET", "POST"])
def show_cupcakes_and_cupcake_form():
    """Show existing cupcakes and handle add-cupcake form:
    - if form not filled out or invalid: show form
    - if valid: add cupcake to SQLA and redirect to same page
    """

    form = CupcakeForm()

    if form.validate_on_submit():
        flavor = form.flavor.data
        size = form.size.data
        rating = form.rating.data
        image = form.image.data

        new_cupcake = Cupcake(
            flavor=flavor,
            size=size,
            rating=rating,
            image=image,
        )
        db.session.add(new_cupcake)
        db.session.commit()

        flash(f"{flavor} cupcake added to cupcakes!", "success")
        return redirect("/")

    else:
        return render_template("index.html", form=form)


@app.route('/cupcakes')
def return_cupcakes():
    """ Query for cupcakes. Rturn a list of dictionaries """

    cupcakes = Cupcake.query.all()

    serialized_cupcakes = [ 
        cupcake.serialize()
        for cupcake in cupcakes
    ]

    return jsonify(response=serialized_cupcakes)


@app.route('/cupcakes', methods=['POST'])
def add_cupcake():
    """ Insert cupcake in cupcake database """
    data = request.json

    cupcake = Cupcake(
        flavor=data['flavor'],
        size=data['size'],
        rating=data['rating'],
        image=data.get('image')
    )

    db.session.add(cupcake)
    db.session.commit()

    serialized_cupcake = cupcake.serialize()

    return jsonify(response=serialized_cupcake)


@app.route("/cupcakes/<cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """ Update cupcake. Return a dictionary with updated values and ID  """
    # Get entry in cupcakes datatable
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    # Get values from request
    data = request.json
    # Update values
    cupcake.flavor = data['flavor']
    cupcake.size = data['size']
    cupcake.rating = data['rating']
    cupcake.image = data['image']
    db.session.commit()

    serialized_updated_cupcake_info = cupcake.serialize()

    return jsonify(response=serialized_updated_cupcake_info)


@app.route("/cupcakes/<cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """ Delete cupcake, return confirmation message """
    # Cupcake.query.filter(Cupcake.id == cupcake_id).delete()
    # db.session.commit()

    cupcake = Cupcake.query.get(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()

    confirmation_message = dict(
        message="Deleted"
    )

    return jsonify(response=confirmation_message)


@app.route('/search')
def search_cupcakes():
    """ Given search term return a list of matching cupcake dictionaries """
    import pdb; pdb.set_trace()
    search_term = request.args['search-term']

    filtered_cupcakes = Cupcake.query.filter(
        or_(
            Cupcake.flavor.like("%" + search_term + "%"),
            Cupcake.size.like("%" + search_term + "%"))).all()

    serialized_filtered_cupcakes = [
        cupcake.serialize()
        for cupcake in filtered_cupcakes
    ]

    return jsonify(response=serialized_filtered_cupcakes)
