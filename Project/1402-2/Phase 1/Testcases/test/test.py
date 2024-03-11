import unittest
import subprocess
import evaluator
import logging


class Test(unittest.TestCase):
    def test_1(self):
        score1, score2, score3 = evaluator.calc_test_score('T01')
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)
        self.assertEqual(score3, 0)

    def test_2(self):
        score1, score2, score3 = evaluator.calc_test_score('T02')
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)
        self.assertEqual(score3, 0)

    def test_3(self):
        score1, score2, score3 = evaluator.calc_test_score('T03')
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)
        self.assertEqual(score3, 0)

    def test_4(self):
        score1, score2, score3 = evaluator.calc_test_score('T04')
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)
        self.assertEqual(score3, 0)

    def test_5(self):
        score1, score2, score3 = evaluator.calc_test_score('T05')
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)
        self.assertEqual(score3, 0)

    def test_6(self):
        score1, score2, score3 = evaluator.calc_test_score('T06')
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)
        self.assertEqual(score3, 0)

    def test_7(self):
        score1, score2, score3 = evaluator.calc_test_score('T07')
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)
        self.assertEqual(score3, 0)

    def test_8(self):
        score1, score2, score3 = evaluator.calc_test_score('T08')
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)
        self.assertEqual(score3, 0)

    def test_9(self):
        score1, score2, score3 = evaluator.calc_test_score('T09')
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)
        self.assertEqual(score3, 0)

    def test_10(self):
        score1, score2, score3 = evaluator.calc_test_score('T10')
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)
        self.assertEqual(score3, 0)
        
    def test_11(self):
        score1, score2, score3 = evaluator.calc_test_score('T11')
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)
        self.assertEqual(score3, 0)
        
    def test_12(self):
        score1, score2, score3 = evaluator.calc_test_score('T12')
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)
        self.assertEqual(score3, 0)
        
    def test_13(self):
        score1, score2, score3 = evaluator.calc_test_score('T13')
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)
        self.assertEqual(score3, 0)
        
    def test_14(self):
        score1, score2, score3 = evaluator.calc_test_score('T14')
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)
        self.assertEqual(score3, 0)
        
    def test_15(self):
        score1, score2, score3 = evaluator.calc_test_score('T15')
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)
        self.assertEqual(score3, 0)
