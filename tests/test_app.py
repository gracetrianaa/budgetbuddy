import unittest
from app.app import app

class BudgetAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.reset_global_state()

    def reset_global_state(self):
        global total_income, total_expense
        total_income = 0
        total_expense = 0

    def test_add_income(self):
        response = self.app.post('/add_income', json={'amount': 500})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Income added', response.data)

    def test_add_expense(self):
        response = self.app.post('/add_expense', json={'amount': 200})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Expense added', response.data)

    def test_summary(self):
        # self.app.post('/add_income', json={'amount': 500})
        # self.app.post('/add_expense', json={'amount': 200})
        response = self.app.get('/summary')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['total_income'], 500)
        self.assertEqual(data['total_expense'], 200)
        self.assertEqual(data['balance'], 300)

if __name__ == '__main__':
    unittest.main()
