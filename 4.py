import tkinter as tk
from random import choice
import json


def load_words():

    with open('words.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def choose_random_word(words):

    return choice(list(words.items()))


class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()


        self.title("Поле Чудес")


        self.words = load_words()
        self.word, self.question = choose_random_word(self.words)
        self.hidden_word = ['_' for _ in range(len(self.word))]
        self.guesses = []
        self.score = 0
        self.best_score = None
        self.load_best_score()


        self.create_widgets()

    def create_widgets(self):


        self.label_question = tk.Label(self, text=self.question, font=("Arial", 16))
        self.label_question.pack(pady=10)


        self.label_hidden_word = tk.Label(self, text=" ".join(self.hidden_word), font=("Arial", 24))
        self.label_hidden_word.pack(pady=10)


        self.entry_guess = tk.Entry(self, width=1, font=("Arial", 24))
        self.entry_guess.pack(side=tk.LEFT, padx=(20, 10))

        self.entry_guess.bind('<Return>', lambda event: self.check_letter())


        self.button_submit = tk.Button(self, text="Проверить", command=self.check_letter)
        self.button_submit.pack(side=tk.LEFT)


        self.label_status = tk.Label(self, text="", fg="red", font=("Arial", 14))
        self.label_status.pack(pady=10)


        self.label_score = tk.Label(self, text=f"Текущие очки: {self.score}", font=("Arial", 14))
        self.label_score.pack(pady=10)


        self.label_best_score = tk.Label(self, text=f"Лучший результат: {self.best_score or '-'}", font=("Arial", 14))
        self.label_best_score.pack(pady=10)


        self.button_new_round = tk.Button(self, text="Следующий раунд", state=tk.DISABLED, command=self.start_new_round)
        self.button_new_round.pack(pady=10)

    def start_new_round(self):

        self.word, self.question = choose_random_word(self.words)
        self.hidden_word = ['_' for _ in range(len(self.word))]
        self.guesses.clear()
        self.label_question.config(text=self.question)
        self.label_hidden_word.config(text=" ".join(self.hidden_word))
        self.label_status.config(text="")  # Очищаем статусную строку
        self.button_submit.config(state=tk.NORMAL)
        self.button_new_round.config(state=tk.DISABLED)

    def check_letter(self):
        """Обрабатываем ввод буквы игроком."""
        guess = self.entry_guess.get().strip().upper()
        if len(guess) != 1 or not guess.isalpha():
            self.label_status.config(text="Ошибка! Нужно ввести одну букву.", fg="red")
            return

        if guess in self.guesses:
            self.label_status.config(text="Вы уже пробовали эту букву.", fg="orange")
            return

        found = False
        for i, char in enumerate(self.word):
            if char.upper() == guess:
                self.hidden_word[i] = char
                found = True
                self.score += 10

        if found:
            self.label_status.config(text="Правильно!", fg="green")
        else:
            self.label_status.config(text="Неправильно!", fg="gray")

        self.update_labels()
        self.guesses.append(guess)

        if '_' not in self.hidden_word:
            self.end_game()

    def update_labels(self):

        self.label_hidden_word.config(text=" ".join(self.hidden_word))
        self.label_score.config(text=f"Текущие очки: {self.score}")

    def end_game(self):

        message = f"Победа! Вы отгадали слово '{self.word}'. Ваш счёт: {self.score}\n"
        if self.best_score is None or self.score > self.best_score:
            self.save_best_score(self.score)
            message += "Новый рекорд!\n"


        self.label_status.config(text=message + "Нажмите \"Следующий раунд\", чтобы продолжить игру.", fg="blue")
        self.button_submit.config(state=tk.DISABLED)
        self.button_new_round.config(state=tk.NORMAL)

    def save_best_score(self, score):

        try:
            with open('best_scores.txt', 'w') as file:
                file.write(str(score))
        except Exception as e:
            print(e)

    def load_best_score(self):

        try:
            with open('best_scores.txt', 'r') as file:
                self.best_score = int(file.read())
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    app = GameApp()
    app.mainloop()