import unittest
import runner

class Test(unittest.TestCase):
    def test_1(self):
        score1, score2 = runner.run_and_evaluate('T01')
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)

    def test_2(self):
        score1, score2 = runner.run_and_evaluate('T02')
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)

    def test_3(self):
        score1, score2 = runner.run_and_evaluate('T03')
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)

    def test_4(self):
        score1, score2 = runner.run_and_evaluate('T04')
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)

    def test_5(self):
        score1, score2 = runner.run_and_evaluate('T05')
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)

    def test_6(self):
        score1, score2 = runner.run_and_evaluate('T06')
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)

    def test_7(self):
        score1, score2 = runner.run_and_evaluate('T07')
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)

    def test_8(self):
        score1, score2 = runner.run_and_evaluate('T08')
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)

    def test_9(self):
        score1, score2 = runner.run_and_evaluate('T09')
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)

    def test_10(self):
        score1, score2 = runner.run_and_evaluate('T10')
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)