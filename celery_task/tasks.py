from sqlalchemy import text

import settings
from celery_task.celery import app
from cf_data.cf_api import APIClient
from cf_data.function import translate_func
from db_data.db_manager import ManagerDB
from db_data.models import ProblemsTable


@app.task
def update_data():
    """
    Функция обновления данных о задачах с сайта codeforces.
      Вызывается каждый час, проверяет количество задач на сайте и
      добавляет только недостающие.
      Перед началом работы проводится проверка на сществоавание БД задач.
    :return:
    """

    problems_list = APIClient.get()["problems"]
    statistics_list = APIClient.get()["problemStatistics"]

    cnt_problems = len(problems_list)
    cnt_statistics = len(statistics_list)

    dat = ManagerDB(
        db_user=settings.DB_USER,
        db_password=settings.DB_PASSWORD,
        db_name=settings.DB_NAME,
        db_host=settings.DB_HOST,
        db_port=settings.DB_PORT,
    )  # получение данных о созданной БД
    with dat.session as session:

        smtm = """SELECT EXISTS (
            SELECT 1 FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'problems'
            ) AS table_exists;"""
        result = session.execute(text(smtm))
        if not result.first()[0]:
            dat.create_tables()

        cnt_tab = session.query(ProblemsTable).count()
        # проверка количества задача на текущий момент с сайта и сколько
        # сохранено в БД (если на сайе больше, чем сохранено в БД, то
        # находим разность между количеством и добавляем в таблицу
        # недостабщие данные с ГОЛОВЫ СПИСКА задач с сайта)
        # translated_words =
        # translate_func(problems_list[:cnt_problems - cnt_tab])

        if cnt_problems > cnt_tab:
            translated_words = translate_func(
                problems_list[: cnt_problems - cnt_tab]
            )
            problems_reverse = problems_list[: cnt_problems - cnt_tab]
            statistics_reverse = statistics_list[: cnt_statistics - cnt_tab]
            problems_reverse.reverse()
            statistics_reverse.reverse()
            dat.insert_problems(problems_reverse, translated_words)
            dat.insert_statistics(statistics_reverse)
