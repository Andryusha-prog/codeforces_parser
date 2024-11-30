import settings
from cf_data.cf_api import APIClient
from cf_data.function import translate_func
from db_data.db_manager import ManagerDB
from tg_bot.tg_bot_func import bot


if __name__ == "__main__":

    tag_words = set()
    result = []

    problems_list = APIClient.get()["problems"]
    statistics_list = APIClient.get()["problemStatistics"]

    problems_list.reverse()
    statistics_list.reverse()

    translated_words = translate_func(problems_list)

    start_db = ManagerDB(
        db_user=settings.DB_USER,
        db_password=settings.DB_PASSWORD,
        db_name=settings.DB_NAME,
        db_host=settings.DB_HOST,
        db_port=settings.DB_PORT,
    )

    start_db.insert_tag_words(translated_words)

    start_db.delete_table()
    start_db.create_tables()

    start_db.insert_problems(problems_list, translated_words)
    start_db.insert_statistics(statistics_list)

    bot.infinity_polling()
