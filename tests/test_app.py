import unittest
from app.app import app, reset_global_state, mysql

class BudgetAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.reset_global_state()

    def reset_global_state(self):
        with app.app_context():
            reset_global_state()

    def test_add_income(self):
        response = self.app.post('/add_income', json={'amount': 500})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Income added', response.data)

    def test_add_expense(self):
        response = self.app.post('/add_expense', json={'amount': 200})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Expense added', response.data)

    def test_summary(self):
        with app.app_context():
            self.app.post('/add_income', json={'amount': 500})
            self.app.post('/add_expense', json={'amount': 200})

        response = self.app.get('/daily_summaries')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1) 
        summary = data[0]
        self.assertEqual(summary['total_income'], 500.0)
        self.assertEqual(summary['total_expense'], 200.0)
        self.assertEqual(summary['balance'], 300.0)

    def tearDown(self):
        # Clean up the database after each test
        with app.app_context():
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM transactions")
            mysql.connection.commit()
            cur.close()

if __name__ == '__main__':
    unittest.main()
