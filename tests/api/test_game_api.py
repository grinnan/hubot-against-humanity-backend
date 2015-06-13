from tests.hahtest import HahTest
from hah.models.game import Game
from tests.factory_boy.game_factory import GameFactory
import json

class GameApiTest(HahTest):
    def test_create_game(self):
        Game.query.delete()

        rv = self.auth_post('/game', data={'channel':'#slackagainsthumanity'})
        self.assert_200(rv)
        rv_data = json.loads(rv.data.decode('utf-8'))

        self.assertIn('id', rv_data)
        self.assertEqual(0, rv_data['turn'])
        self.assertEqual('#slackagainsthumanity', rv_data['channel'])

        game = Game.query.get(rv_data['id'])
        self.assertIsNotNone(game)

    def test_create_game_already_exist(self):
        game = GameFactory()
        self.api_client.game = game

        rv = self.auth_post('/game')
        self.assertStatus(rv, 422)

    def test_get_game(self):
        game = GameFactory()
        self.api_client.game = game

        rv = self.auth_get('/game')
        rv_data = json.loads(rv.data.decode('utf-8'))

        self.assertIn('id', rv_data)
        self.assertEqual(0, rv_data['turn'])
