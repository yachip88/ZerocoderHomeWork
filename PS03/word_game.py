import requests
from bs4 import BeautifulSoup
from googletrans import Translator

translator = Translator()

def get_english_words():
    url = "https://randomword.com/"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        english_words = soup.find("div", id="random_word").text.strip()
        word_definition = soup.find("div", id="random_word_definition").text.strip()
        return {
            "english_words": english_words,
            "word_definition": word_definition
        }
    except Exception:
        print("Произошла ошибка")
        return None

def word_game():
    print("Добро пожаловать в игру")
    while True:
        word_dict = get_english_words()
        if not word_dict:
            break
        word = translator.translate(word_dict.get("english_words"), dest="ru").text
        word_definition = translator.translate(word_dict.get("word_definition"), dest="ru").text
        print(f"Значение слова - {word_definition}")
        user = input("Что это за слово? ")
        if user == word:
            print("Все верно!")
        else:
            print(f"Ответ неверный, было загадано это слово - {word}")
        play_again = input("Хотите сыграть еще раз? y/n")
        if play_again != "y":
            print("Спасибо за игру!")
            break

if __name__ == "__main__":
    word_game()
