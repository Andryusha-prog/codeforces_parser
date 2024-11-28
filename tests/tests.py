import unittest

import testing.postgresql
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

import settings
from cf_data.function import translate_func
from db_data.db_manager import ManagerDB
from db_data.models import ProblemsTable, StatisticsTable


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.db = ManagerDB(db_user=settings.DB_USER, db_password=settings.DB_PASSWORD, db_name=settings.DB_NAME)
        self.db.create_tables()
        self.problems = [
            {
                "contestId": 20,
                "index": "I",
                "name": "Схема",
                "type": "PROGRAMMING",
                "rating": 2300,
                "tags": [
                    'graphs',
                    'math'
                ]
            }
        ]
        self.problems_2 = [
            {
                "contestId": 21,
                "index": "I",
                "name": "Схема_2",
                "type": "PROGRAMMING",
                "rating": 700,
                "tags": [
                    'graphs',
                    'math'
                ]
            }
        ]
        self.statistics = [
            {
                "contestId": 2041,
                "index": "I",
                "solvedCount": 308
            }
        ]

        self.translated_words = {'graphs': 'графы', 'math': 'математика'}

    def tearDown(self):
        self.db.delete_table()

    def test_create_tables(self):
        with self.db.session as session:
            smtm = '''SELECT EXISTS (
                        SELECT 1 FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        AND table_name = 'problems'
                        ) AS table_exists;'''
            result = session.execute(text(smtm))
        is_exists_problems = result.first()[0]

        self.assertTrue(is_exists_problems)

    def test_insert_problems(self):
        self.db.insert_problems(self.problems, self.translated_words)
        with self.db.session as session:
            cnt = session.query(ProblemsTable).count()
        self.assertEqual(cnt, 1)

    def test_insert_statistics(self):
        self.db.insert_statistics(self.statistics)
        with self.db.session as session:
            cnt = session.query(StatisticsTable).count()
        self.assertEqual(cnt, 1)

    def test_insert_tag_words(self):
        self.db.insert_tag_words(self.translated_words)
        self.assertEqual(len(self.translated_words), 2)

    def test_get_count_data(self):
        self.db.insert_problems(self.problems, self.translated_words)
        self.assertEqual(self.db.get_count_data(), 1)

    def test_select_problem_rating(self):
        self.db.insert_problems(self.problems, self.translated_words)
        self.db.insert_problems(self.problems_2, self.translated_words)
        min_max_problem = self.db.select_problem_rating()

        self.assertEqual(min_max_problem['min'], 700)
        self.assertEqual(min_max_problem['max'], 2300)

    def test_result_select(self):
        self.db.insert_problems(self.problems, self.translated_words)
        self.db.insert_problems(self.problems_2, self.translated_words)

        result = self.db.result_select({'tag': 'математика', 'level': 700})
        self.assertEqual(result, [(21, 'I', 'Схема_2', 700, None)])

    # def test_translate_func(self):
    #     result = translate_func(self.problems)
    #     self.assertEqual(result, {'graphs': 'графы', 'math': 'математика'})

    def test_delete_tables(self):
        self.db.delete_table()
        with self.db.session as session:
            smtm = '''SELECT EXISTS (
                        SELECT 1 FROM information_schema.tables
                        WHERE table_schema = 'public'
                        AND table_name = 'problems'
                        ) AS table_exists;'''
            result = session.execute(text(smtm))
        is_exists_problems = result.first()[0]

        self.assertFalse(is_exists_problems)

