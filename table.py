
# a 3D tic tac toe table

# list comprehension
import numpy as np

def generate_tables_combinations(table_3d):
    table1, table2, table3 = table_3d
    T_table1, T_table2, T_table3 = np.transpose(table1), np.transpose(table2), np.transpose(table3)
    return [
        table1,
        table2,
        table3,
        [table1[0], table2[0], table3[0]],
        [table1[1], table2[1], table3[1]],
        [table1[2], table2[2], table3[2]],
        [table1[0], table2[1], table3[2]],
        np.transpose([T_table1[0], T_table2[0], T_table3[0]]).tolist(),
        np.transpose([T_table1[1], T_table2[1], T_table3[1]]).tolist(),
        np.transpose([T_table1[2], T_table2[2], T_table3[2]]).tolist(),
        np.transpose([T_table1[0], T_table2[1], T_table3[2]]).tolist(),
    ]
def get_empty_table():
    return [[[0 for _ in range(3)] for _ in range(3)] for _ in range(3)]
class Table:
    def __init__(self):
        self.table = get_empty_table()  # 0 = empty, 1 = player 1, 2 = player 2
        self.turn = 1  # 1 or 2
        self.score = [0, 0]  # [player 1, player 2]
        self.round = 0

    def validate_position(self):
        def check_win(table):
            for row in table:
                if row.count(row[0]) == 3 and row[0] != 0:
                    return True

            for col in range(3):
                if all(table[row][col] == table[0][col] and table[0][col] != 0 for row in range(3)):
                    return True

            if all(table[i][i] == table[0][0] and table[0][0] != 0 for i in range(3)):
                return True

            if all(table[i][2 - i] == table[0][2] and table[0][2] != 0 for i in range(3)):
                return True

            return False

        # Check for win
        possible_combinations = generate_tables_combinations(self.table)
        for face in possible_combinations:
            if check_win(face):
                return 'win'

        # Check for draw
        if all(self.table[z][x][y] != 0 for z in range(3) for x in range(3) for y in range(3)):
            return 'draw'

        return 'continue'

    def validate_move(self, x, y, z):
        try:
            return self.table[z][x][y] == 0
        except:
            return False

    def update_table(self, x, y, z):
        move_validation = self.validate_move(x, y, z)
        if not move_validation:
            return False
        self.table[z][x][y] = self.turn
        position_validation = self.validate_position()
        self.pass_turn()
        return position_validation

    def reset_table(self, increase_round):
        self.table = get_empty_table()
        if increase_round:
            self.round += 1
        self.turn = self.round % 2 + 1

    def reset_score(self):
        self.score = [0, 0]

    def update_score(self, winner):
        if winner == 1:
            self.score[0] += 1
        elif winner == 2:
            self.score[1] += 1

    def pass_turn(self):
        if self.turn == 1:
            self.turn = 2
            return
        self.turn = 1

