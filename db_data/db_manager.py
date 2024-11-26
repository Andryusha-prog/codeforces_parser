from sqlalchemy.orm import Session

from db_data.db_init import StartDB
from db_data.models import ProblemsTable, StatisticsTable


class ManagerDB(StartDB):

    def insert_problems(self, problems_list: list[dict], tag_words: dict):
        set_of_words = set()
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


# def update_table(problems_list: list[dict], session: Session):
    def update_table(self):
        pass


    def select_problem_rating(self):
        pass
