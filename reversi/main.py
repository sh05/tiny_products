from typing import List, Tuple, Optional
import sys

STONE_LIST: List[str] = [s for s in "●○▲△□■◆◇"]
ROW_IDS: List[str] = [str(i) for i in range(1, 27)]
COL_NAMES: List[str] = [chr(i) for i in range(65, 91)]
V_BAR: str = "｜"
H_BAR: str = "一"
DIRECTIONS =  [
        [-1,  -1], [ 0,  -1], [ 1,  -1],
        [-1,   0], [ 0,   0], [ 1,   0],
        [-1,   1], [ 0,   1], [ 1,   1],
        ]
ColIdx = int
RowIdx = int
X = ColIdx
Y = RowIdx
Coord = Tuple[X, Y]

class Stage:

    def __init__(self, row: int =8, col: int =8, p_num: int =2):
        self.r_len: int = row
        self.c_len: int = col
        # 初期配置
        self.stones: List[str] = [["  " for c in range(self.c_len)] for r in range(self.r_len)]
        r_start: int = int(self.r_len / 2 - p_num / 2) 
        c_start: int = int(self.c_len / 2 - p_num / 2) 
        for i in range(p_num):
            for j in range(p_num):
                k = i + j
                if k >= p_num:
                    k -= p_num
                target: Coord = [c_start + j, r_start + i]
                self.set_stone_by_coord(STONE_LIST[k], target)

        # 表示用
        self.R_NAME_WIDTH: int = len(str(self.r_len))
        if self.R_NAME_WIDTH % 2 != 0:
            self.R_NAME_WIDTH += 1
        self.HEADER: str = " " * self.R_NAME_WIDTH + V_BAR \
                + V_BAR.join([COL_NAMES[c].rjust(2) for c in range(self.c_len)]) \
                + V_BAR
        self.H_LINE: str = H_BAR * 2 * (self.c_len + 1)

    def get_stone_by_coord(self, idx: Coord):
        return self.stones[idx[1]][idx[0]]

    def set_stone_by_coord(self, stone: str, idx: Coord):
        self.stones[idx[1]][idx[0]] = stone

    def set_stones_by_coord(self, stone: str, idx: Coord):
        can_put_directions: List[Coord] = self.look_around(idx, stone)
        dir_dis_list: List[Tuple[int, int, int]] = self.look_ahead(idx, can_put_directions, stone)
        for dir_dis in dir_dis_list:
            target: Coord = idx
            for i in range(dir_dis[2]):
                travel = [i * dd for dd in dir_dis]
                target = add_2d_vectors(idx, travel[:2])
                self.set_stone_by_coord(stone, target)

    def look_around(self, idx: Coord, stone: str):
        can_put_directions: List[Coord] = []
        for d in DIRECTIONS:
            if d == [0, 0]:
                continue
            target: Coord = add_2d_vectors(idx, d)
            if self.is_on(target):
                if self.get_stone_by_coord(target) not in ["  ", stone]:
                    can_put_directions.append(d)
        return can_put_directions
        
    def look_ahead(self, idx: Coord, can_put_directions: List[Coord], stone: str):
        dir_dis_list: List[Tuple[int, int, int]] = []
        for dire in can_put_directions:
            distance: int = 1
            target: Coord = idx
            while (True):
                target = add_2d_vectors(target, dire)
                if not self.is_on(target):
                    break
                elif self.get_stone_by_coord(target) == "  ":
                    break
                elif self.get_stone_by_coord(target) == stone:
                    dir_dis_list.append([*dire, distance])
                    break
                distance += 1
        return dir_dis_list

    def is_on(self, idx: Coord):
        if idx[0] in range(self.c_len) and idx[1] in range(self.r_len):
            return True
        else:
            return False

    def search(self, query: str):
        idxes: List[Coord] = []
        for i in range(self.r_len):
            for j, s in enumerate(self.stones[i]):
                if s == query:
                    idxes.append((j, i))
        return idxes
            
    def get_can_put(self, stone: str):
        blanks: List[Coord] = self.search("  ")
        can_put_blanks: List[Coord] = []
        for b in blanks:
            directions: List[Coord] = self.look_around(b, stone)
            if directions:
                if self.look_ahead(b, directions, stone):
                    can_put_blanks.append(b)
        return can_put_blanks

    def draw(self):
        sys.stdout.write("\033[0;0H\033[2J")
        sys.stdout.write(self.HEADER + "\n")
        sys.stdout.write(self.H_LINE + "\n")
        for i, stones in zip(range(self.r_len), self.stones):
            sys.stdout.write(ROW_IDS[i].rjust(self.R_NAME_WIDTH) + V_BAR)
            sys.stdout.write(V_BAR.join([s for s in stones]) + V_BAR + "\n")
            sys.stdout.write(self.H_LINE + "\n")

class Player:
    _id: int = 0
    stone: str = ""
    score: int = 0
    name: str = ""

    def __init__(self, _id: int, name: str):
        self._id = _id
        self.stone = STONE_LIST[_id]
        self.name = name

    def show(self):
        emphasize("Player {}".format(self._id))
        print(self.name)
        print(self.score)

def emphasize(text: str):
    print("\n--- {} ---\n".format(text))

def add_2d_vectors(vec1: Coord, vec2: Coord):
    return [ vec1[0]+vec2[0], vec1[1]+vec2[1] ]

def initialize_game(player_num: int =0, row: int =0, col: int =0):
    emphasize("START")
    players: List[Player] = []
    while (row % 2 != 0 or 0 >= row  or row >= 27):
        row = int(input("How many rows? Please input an even number under 26! #"))

    while (col % 2 != 0 or 0 >= col  or col >= 27):
        col = int(input("How many colmuns? Please input an even number under 26!  #"))

    while (player_num % 2 != 0
            or 0 >= player_num
            or player_num >= len(STONE_LIST)
            or player_num >= row
            or player_num >= col
            ):
        player_num = int(input("How many players?\
            \nPlease input an even number and under {} or number of columns and number of rows! #"\
                    .format(len(STONE_LIST))))

    stage: Stage = Stage(row, col, player_num)
    for i in range(player_num):
        ans: str = "no"
        while (ans == "no"):
            name: str = input("Player{0} please input your name![default: Player{0}] #".format(COL_NAMES[i]))
            if name == "":
                name = "Player{}".format(COL_NAMES[i])
            ans = input("Player{} name is {}. OK? [yes]/no  #".format(i, name))

        players.append(Player(i, name))
        emphasize("Player{} {} your stone is {}".format(players[i]._id, players[i].name, players[i].stone))

    return stage, players


def get_input_to_put(stage, player, valid_places):
    print("Player{} {}\'s turn! Your stone is {}".format(player._id, player.name, player.stone))
    while (True):
        raw = input("Input index! (ex. A6):" )
        idx = apply_input_format(raw, stage)
        print(idx, valid_places)
        if stage.is_on(idx):
            if idx in valid_places:
                break
            else:
                print("You Cannot put there")
        else:
            print("Follow a pattern")

    return idx
def apply_input_format(raw_in, stage):
    row = 0
    col = 0
    if len(str(raw_in)) != 2:
        return (col, row)
    for char in raw_in:
        if char in ROW_IDS:
            row = char
        if char in COL_NAMES:
            col = char
    if row == 0 or col == 0:
        return (col, row)

    return (COL_NAMES.index(col), ROW_IDS.index(row))

def is_finished(stage, players):
    # 全マス埋まった
    if stage.search("  ") == []:
        return True

    no_valid_places = 0
    for player in players:
        if stage.search(player.stone) == []:
            no_valid_places += 1
    if no_valid_places == len(players):
        return True

    return False


def finish_game(stage, players):
    emphasize("FINISH")
    winid = 0
    winname = ""
    winscore = -1
    for player in players:
        player.score = len(stage.search(player.stone))
        print("player{} {}\' score is {}!".format(player._id, player.name, player.score))
        if player.score > winscore:
            winid = player._id
            winname = player.name
            winscore = player.score

    emphasize("The winner is player{} {}! score {}pts".format(winid, winname, winscore))

def main():
    stage, players = initialize_game()
    while(True):
        for player in players:
            stage.draw()
            valid_places = stage.get_can_put(player.stone)
            if valid_places:

            # auto 
                import time, random
                time.sleep(0.1)
                selected = random.choices(valid_places)
                stage.set_stones_by_coord(player.stone, selected.pop())
                print()
            
            # manual
                """
                print(
                        "You can put on " +
                        ", ".join( [ROW_IDS[vp[1]] + COL_NAMES[vp[0]] for vp in valid_places] ) +
                        "."
                )
                place = get_input_to_put(stage, player, valid_places)
                stage.set_stones_by_coord(player.stone, place)

            else:
                print("player{} {} cannot put the stone...".format(player._id, player.name))
                tmp = input("Press any key")
                """

        if is_finished(stage, players):
            stage.draw()
            break
    finish_game(stage, players)

if __name__ == "__main__":
    main()
