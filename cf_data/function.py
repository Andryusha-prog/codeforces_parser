from deep_translator import GoogleTranslator


def translate_func(problems_list: list[dict]) -> dict[str, str]:
    """
    Функция для перевода тем задач с английского на русский язык (занимает продолжительное время)
    :param problems_list: список задач codeforces.com
    :return: словарь вида {слово на английском: перевод на русском}
    """
    tag_words = set()
    result = []
    translated_words = {}

    for word in problems_list:
        [tag_words.add(tag) for tag in word['tags']]

    for word in tag_words:
        result.append(word)

    translated = GoogleTranslator(source='en', target='ru').translate_batch(result)
    for i in range(len(translated)):
        translated_words[result[i]] = translated[i]
    if 'graphs' in tag_words:
        translated_words['graphs'] = 'графы'
    if 'strings' in tag_words:
        translated_words['strings'] = 'строки'
    if 'brute force' in tag_words:
        translated_words['brute force'] = 'перебор'
    if 'greedy' in tag_words:
        translated_words['greedy'] = 'жадные алгоритмы'

    return translated_words

def data_for_printing(insert_list: list[set]) -> list[str]:
    """
    Функция преобразует входной список множеств данных о задачах в список строк для вывода пользователю через ТГ бота
    :param insert_list: список множеств из результирующего запроса, содержащий как информацию о задачах, так и количество решений
    :return: список строк для представления информации пользователю
    """
    result_list = []
    for data in insert_list:
        temp_list = []
        for text in data:
            temp_list.append(text)
        result_list.append(f'контест: {temp_list[0]} номер: {temp_list[1]} название: {temp_list[2]}'
                           f' рейтинг: {temp_list[3]} кол-во решений: {temp_list[4]} \n'
                           f'ссылка: https://codeforces.com/problemset/problem/{temp_list[0]}/{temp_list[1]} \n')

    return result_list
