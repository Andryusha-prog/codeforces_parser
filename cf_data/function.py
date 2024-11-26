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