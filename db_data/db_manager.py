import random

from celery.bin.result import result
from sqlalchemy import select, func, and_, text
from sqlalchemy.orm import Session

from db_data.db_init import StartDB
from db_data.models import ProblemsTable, StatisticsTable


class ManagerDB(StartDB):
    tags_words = []

    def insert_problems(self, problems_list: list[dict], tag_words: dict):
        with self.session as session:
            prepare_data_problems = []

            for problems in problems_list:
                tags = [tag_words[tag] for tag in problems['tags']]
                # print(tags)

                pr_rat = 1 if 'rating' in problems.keys() else 0
                prepare_data_problems.append(ProblemsTable(
                    contestId=problems['contestId'],
                    index=problems['index'],
                    name=problems['name'],
                    rating=problems['rating'] if pr_rat == 1 else None,
                    # tags=', '.join(problems['tags'])
                    tags=', '.join(tags)
                )
                )
                # [set_of_words.add(word) for word in problems['tags']]
            session.add_all(prepare_data_problems)
            session.commit()

        # return [word for word in set_of_words]

    def insert_statistics(self, statistics_list: list[dict]):

        prepare_data_statistics = []

        with self.session as session:
            for statistics in statistics_list:
                prepare_data_statistics.append(StatisticsTable(
                    contestId=statistics['contestId'],
                    index=statistics['index'],
                    solvedCount=statistics['solvedCount'],
                )
                )
        session.add_all(prepare_data_statistics)
        session.commit()

    def insert_tag_words(self, translate_words: dict[str, str]):
        for values in translate_words.values():
            if values not in self.tags_words:
                self.tags_words.append(values)

    def get_count_data(self):
        with self.session as session:
            count_data = session.query(ProblemsTable).count()

        return count_data

    def select_problem_rating(self) -> dict[str, int]:
        min_max_rate = {}
        with self.session as session:
            min_max_rate['min'] = session.query(func.min(ProblemsTable.rating)).scalar()
            min_max_rate['max'] = session.query(func.max(ProblemsTable.rating)).scalar()

        return min_max_rate

    def result_select(self, input_data: dict[str, int]) -> list:
        result_list = []
        result_list_contest = []
        # вернет все задачи у которых сложность = lvl по одной выбранной теме
        with self.session as session:
            # list_data = session.query(ProblemsTable).join(StatisticsTable, and_(ProblemsTable.contestId == StatisticsTable.contestId,
            #                                                         ProblemsTable.index == StatisticsTable.index,
            #                                                         ProblemsTable.tags.like(f"'%{input_data['tag']}%'"),
            #                                                         ProblemsTable.rating == int(input_data['level'])),
            #                                   isouter=True).all()
            str_select = f'''SELECT pr."contestId", pr.index, pr.name, pr.rating, st."solvedCount"
                FROM problems as pr 
                LEFT JOIN statistics as st
                on pr."contestId" = st."contestId" and pr.index = st.index
	            WHERE pr.rating = {int(input_data['level'])}
	            and pr.tags like \'%{input_data['tag']}%\''''
            list_data = session.execute(text(str_select)).all()

        if len(list_data) == 0:
            return []
        else:
            count_task = 10 if len(list_data) >= 10 else len(list_data)
            while len(result_list) < count_task:
                elem = random.choice(list_data)
                if elem.contestId not in result_list_contest:
                    result_list.append(elem)
                    result_list_contest.append(elem.contestId)

        # return result_list
        return result_list
