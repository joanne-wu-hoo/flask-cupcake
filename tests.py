from app import app
from models import db, connect_db, Cupcake
import unittest

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes-app-test'
db.create_all()


class AppTestCase(unittest.TestCase):

    def setUp(self):
        """Set up test client and make new cupcake."""

        Cupcake.query.delete()

        self.client = app.test_client()

        self.cupcake = Cupcake(
            flavor='testing', size='small', rating=10)
        db.session.add(self.cupcake)
        db.session.commit()

    def test_get_cupcakes(self):
        """ Test read functionality """

        response = self.client.get('/cupcakes')
        response_data = response.json['response']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_data,
            [dict(
                id=self.cupcake.id,
                flavor='testing',
                size='small',
                rating=10,
                image='https://tinyurl.com/truffle-cupcake'
            )]
        )

    def test_add_cupcake(self):
        """ Test create functionality """

        response = self.client.post('/cupcakes', json={
            "flavor": "chocolate",
            "size": "mini",
            "rating": 5
        })
        response_data = response.json['response']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_data,
            dict(
                id=response_data['id'],
                flavor='chocolate',
                size='mini',
                rating=5.0,
                image='https://tinyurl.com/truffle-cupcake'
            )
        )
        self.assertEqual(Cupcake.query.count(), 2)

    def test_edit_cupcake(self):
        """ Test update functionality """

        response = self.client.patch(f'/cupcakes/{self.cupcake.id}', json={
            "flavor": "chocolate",
            "size": "mini",
            "rating": 5,
            "image": "https://tinyurl.com/truffle-cupcake"
        })
        response_data = response.json['response']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_data,
            dict(
                id=self.cupcake.id,
                flavor='chocolate',
                size='mini',
                rating=5.0,
                image='https://tinyurl.com/truffle-cupcake'
            )
        )

    def test_delete_cupcake(self):
        """ Test delete functionality """

        response = self.client.delete(f'/cupcakes/{self.cupcake.id}')
        response_data = response.json['response']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Cupcake.query.count(), 0)
        self.assertEqual(response_data, {"message": "Deleted"})
