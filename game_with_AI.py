# Write your code here
import random
import sqlite3


class GameLogic:
    def __init__(self):
        self.user = ''
        self.conn = sqlite3.connect('rockpaperscissors.s3db')
        self.cur = self.conn.cursor()
        self.user_score = 0

    def start_game(self):
        """Starts game by asking for User's name and searching the rating.txt file for it."""
        self.user = input('Enter your name: ')
        print(f'Hello, {self.user}')
        self.cur.execute('''SELECT score FROM scorecard WHERE (user = ?)''',
                         [self.user])
        query = self.cur.fetchone()
        if query:
            self.user_score = query[0]
        else:
            pass
        print(f'Starting Score: {self.user_score}')

    def random_comp_guess(self):
        """Generates random Computer guess
        and returns either 'rock', 'paper' or 'scissors'.
        """
        computer_random = random.randint(0, 2)
        if computer_random == 0:
            guess = 'rock'
        elif computer_random == 1:
            guess = 'paper'
        elif computer_random == 2:
            guess = 'scissors'
        return guess

    def decision(self, user_guess, comp_guess):
        """Decides if the user: wins, losses, or draws"""
        # Scoring:
        win = 100
        draw = 50
        lose = 0
        if user_guess == comp_guess:
            return f'There is a draw ({user_guess})', draw
        elif ((user_guess == 'rock') and (comp_guess == 'scissors')) \
                or ((user_guess == 'paper') and (comp_guess == 'rock')) \
                or ((user_guess == 'scissors') and (comp_guess == 'paper')):
            return f'Well done. The computer chose {comp_guess} and failed', win
        else:
            return f'Sorry, but the computer chose {comp_guess}', lose

    def save_score(self):
        """save score in database."""
        self.cur.execute('''SELECT score FROM scorecard WHERE (user = ?)''',
                         [self.user])
        query = self.cur.fetchone()
        if query:
            self.cur.execute("UPDATE scorecard SET score = ? WHERE user = ?",
                             [self.user_score, self.user])
        else:
            self.cur.execute("INSERT INTO scorecard(user, score) VALUES (?,?)", [self.user, self.user_score])
        self.conn.commit()

    def see_scores(self):
        """Prints records in table"""
        self.cur.execute('''SELECT score, user FROM scorecard ORDER BY SCORE DESC''')
        query = self.cur.fetchall()
        for i in query:
            print(i[0], i[1])

    def end(self):
        """Ends game by closing connection"""
        self.conn.close()


game = GameLogic()
game.start_game()
while True:
    game_prompt = '''rock, paper, scissors, !rating, !exit: '''
    user_input = input(game_prompt)
    if user_input == '!exit':
        game.save_score()
        game.end()
        print('Bye!')
        break
    elif (user_input == 'rock') \
            or (user_input == 'paper') \
            or (user_input == 'scissors'):
        computer_input = game.random_comp_guess()
        [decision_string, points] = game.decision(user_input, computer_input)
        print(decision_string)
        game.user_score += points
    elif user_input == '!rating':
        print(f'Your rating: {game.user_score}')
        game.see_scores()
    else:
        print('Invalid input')


