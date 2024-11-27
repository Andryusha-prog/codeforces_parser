from deep_translator import GoogleTranslator


def translate_func(problems_list: list[dict]):
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
    translated_words['graphs'] = 'графы'
    translated_words['strings'] = 'строки'
    translated_words['brute force'] = 'перебор'
    translated_words['greedy'] = 'жадные алгоритмы'

    return translated_words

def data_for_printing(insert_list: list[set]):
    result_list = []
    for data in insert_list:
        temp_list = []
        for text in data:
            temp_list.append(text)
        result_list.append(f'контест: {temp_list[0]} номер: {temp_list[1]} название: {temp_list[2]}'
                           f' рейтинг: {temp_list[3]} кол-во решений: {temp_list[4]} \n'
                           f'ссылка: https://codeforces.com/problemset/problem/{temp_list[0]}/{temp_list[1]} \n')

    return result_list
