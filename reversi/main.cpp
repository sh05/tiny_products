// stone_list = ['●', '○', '▲', '△', '□', '■', '◆', '◇']
// row_ids = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26']
// col_names = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'v', 'z' ]
//
//
// class Stage:
//     """
//     8x8以外用に配列で生成するように書きかえる
//     """
//     stones = []
//     r_len = 0
//     c_len = 0
//     # stones = [
//     #     ['  ','  ','  ','  ','  ','  ','  ','  '],
//     #     ['  ','  ','  ','  ','  ','  ','  ','  '],
//     #     ['  ','  ','  ','  ','  ','  ','  ','  '],
//     #     ['  ','  ','  ','  ','  ','  ','  ','  '],
//     #     ['  ','  ','  ','  ','  ','  ','  ','  '],
//     #     ['  ','  ','  ','  ','  ','  ','  ','  '],
//     #     ['  ','  ','  ','  ','  ','  ','  ','  '],
//     #     ['  ','  ','  ','  ','  ','  ','  ','  '],
//     # ]
//
//     def __init__(self, row=8, col=8, p_num=2):
//         self.r_len = row
//         self.c_len = col
//         for r in range(row):
//             self.stones.append([])
//             for c in range(col):
//                 self.stones[r].append('  ')
//         """
//         プレイヤー数に応じるなら書きかえる
//         self.stones[3][3] = '●'
//         self.stones[3][4] = '○'
//         self.stones[4][3] = '○'
//         self.stones[4][4] = '●'
//         """
//         r_start = int(row / 2 - p_num / 2) 
//         c_start = int(col / 2 - p_num / 2) 
//
//         for i in range(p_num):
//             for j in range(p_num):
//                 k = i + j
//                 if k >= p_num:
//                     k -= p_num
//                 self.stones[r_start + i][c_start + j] = stone_list[k]
//
//     def paint(self):
//         width = len(str(self.r_len))
//         if width % 2 != 0:
//             width += 1
//         print('  ｜', end='')
//         for c in range(self.c_len):
//             print(' {}｜'.format(col_names[c]), end='')
//         print()
//         for c in range(self.c_len + 1):
//             print('一一', end='')
//         print()
//         for i, stones in zip(range(self.r_len), self.stones):
//             print(row_ids[i].rjust(width), end='')
//             print('｜', end='')
//
//             for s in stones:
//                 print('{}｜'.format(s), end='')
//             print()
//             for c in range(self.c_len + 1):
//                 if c == 0:
//                     for i in range(int(width / 2)):
//                         print('一', end='')
//                 else:
//                     print('一一', end='')
//             print()
//
//     def put_stone(self, stone, idx):
//         self.stones[idx[0]][idx[1]] = stone
//         directions = self.look_around(idx, stone)
//         dir_dis_list = self.measure(idx, directions, stone)
//         for dir_dis in dir_dis_list:
//             for i in range(dir_dis[2]):
//                 vec = [i * x for x in dir_dis]
//                 self.stones[idx[0] + vec[0]][idx[1] + vec[1]] = stone
//
//     def search(self, query):
//         idxes = []
//         for i in range(self.r_len):
//             js = [k for k, x in enumerate(self.stones[i]) if x == query]
//             for j in js:
//                 idxes.append([i, j])
//         return idxes
//         
//     def look_around(self, idx, stone):
//         directions = []
//         for i in range(-1, 2):
//             if not self.is_on(row=i+idx[0]):
//                 continue
//             for j in range(-1, 2):
//                 if not self.is_on(col=j+idx[1]):
//                     continue
//                 if i == 0 and j == 0:
//                     continue
//                 if self.stones[idx[0] + i][idx[1] + j] != '  ' and self.stones[idx[0] + i][idx[1] + j] != stone:
//                     directions.append([i, j])
//         return directions
//
//     def measure(self, idx, directions, stone):
//         rem_list = []
//         for dire in directions:
//             distance = 1
//             while (True):
//                 vec = [d * distance for d in dire]
//                 if not self.is_on(row=idx[0]+vec[0], col=idx[1]+vec[1]):
//                     dire.append(0)
//                     break
//                 elif self.stones[idx[0] + vec[0]][idx[1] + vec[1]] == '  ':
//                     dire.append(0)
//                     break
//                 elif self.stones[idx[0] + vec[0]][idx[1] + vec[1]] == stone:
//                     dire.append(distance)
//                     break
//                 distance += 1
//         return [d for d in directions if d[2] != 0]
//             
//     def filter_places(self, stone):
//         places = []
//         idxes = self.search('  ')
//         for idx in idxes:
//             directions = self.look_around(idx, stone)
//             if directions:
//                 if self.measure(idx, directions, stone):
//                     places.append(idx)
//         return places
//
//     def is_on(self, row=None, col=None):
//         if row is not None and col is not None:
//             if row in range(self.r_len) and col in range(self.c_len):
//                 return True
//             else:
//                 return False
//         elif row is not None:
//             if row in range(self.r_len):
//                 return True
//             else:
//                 return False
//         elif col is not None:
//             if col in range(self.c_len):
//                 return True
//             else:
//                 return False
//
//
// class Player:
//     _id = 0
//     stone = ''
//     score = 0
//     name = ''
//
//     def __init__(self, _id, name):
//         self._id = _id + 1
//         self.stone = stone_list[_id]
//         self.name = name
//
//
//
// def emphaseze(text):
//     print('\n--- {} ---\n'.format(text))
//
//
// # def initialize_game(player_num=2, row=8, col=8):
// def initialize_game(player_num=8, row=16, col=16):
//     emphaseze('START')
//     players = []
//     while (True):
//         row = int(input('How many rows dou you want  #?'))
//         if row % 2 == 0 and row < 27:
//             break
//         print('Must be a even number and under 26!')
//
//     while (True):
//         col = int(input('How many colmuns dou you want  #?'))
//         if col % 2 == 0 and col < 27:
//             break
//         print('Must be even a number and under 26!')
//
//     while (True):
//         player_num = int(input('How many players  #'))
//         if player_num % 2 != 0 or player_num > len(stone_list):
//             print('Must be even a number and under {}!'.format(len(stone_list)))
//         elif player_num > row or player_num > col:
//             print('Sorry must be under column number and row number')
//         else:
//             break
//
//     stage = Stage(row, col, player_num)
//     for i in range(player_num):
//         while (True):
//             name = input('Player{} please input your name!  #'.format(i))
//             break
//             """
//             ans = input('Player{} name is {}. OK? [yes/no]  #'.format(i, name))
//             if ans == 'yes':
//                 break
//             """
//         players.append(Player(i, name))
//         emphaseze('Player{} {} your stone is {}'.format(players[i]._id, players[i].name, players[i].stone))
//
//     return stage, players
//
//
// def get_input(stage, player, valid_places):
//     print('Player{} {}\'s turn! Your stone is {}'.format(player._id, player.name, player.stone))
//     while (True):
//         idx = input('Input index! (ex. a6):' )
//         row, col = apply_input_format(idx, stage)
//         if stage.is_on(row=row, col=col):
//             if [row, col] in valid_places:
//                 break
//             else:
//                 print('You Cannot put there')
//         else:
//             print('Follow a pattern')
//
//     return [row, col]
//
// def apply_input_format(idx, stage):
//     row = 0
//     col = 0
//     if len(str(idx)) != 2:
//         return row, col
//     for char in idx:
//         if char in row_ids:
//             row = char
//         if char in col_names:
//             col = char
//     if row == 0 or col == 0:
//         return row, col
//
//     return row_ids.index(row), col_names.index(col)
//
// def is_finished(stage, players):
//     # 全マス埋まった
//     if stage.search('  ') == []:
//         return True
//
//     # 誰も置けない
//     no_valid_places = 0
//     for player in players:
//         if stage.filter_places(player.stone) == []:
//             no_valid_places += 1
//     if no_valid_places == len(players):
//         return True
//
//     return False
//
//
// def finish_game(stage, players):
//     emphaseze('FINISH')
//     winid = 0
//     winname = ''
//     winscore = -1
//     for player in players:
//         player.score = len(stage.search(player.stone))
//         print('player{} {}\' score is {}!'.format(player._id, player.name, player.score))
//         if player.score > winscore:
//             winid = player._id
//             winname = player.name
//             winscore = player.score
//
//     emphaseze('The winner is player{} {}! score {}pts'.format(winid, winname, winscore))
//
// def main():
//     stage, players = initialize_game()
//     while(True):
//         for player in players:
//             stage.paint()
//             valid_places = stage.filter_places(player.stone)
//             if valid_places:
//                 """
//                 # manual
//                 print('You can put on', end=' ')
//                 for valid_place in valid_places:
//                     print('{}{}'.format(row_ids[valid_place[0]], col_names[valid_place[1]]), end=' ')
//                 print('.')
//                 place = get_input(stage, player, valid_places)
//                 stage.put_stone(player.stone, place)
//                 """
//
//                 """
//                 # automation 
//                 """
//                 import time, random
//                 time.sleep(0.1)
//                 stage.put_stone(player.stone, valid_places[random.randrange(len(valid_places))])
//                 print()
//             # else:
//                 # print('player{} {} cannot put the stone...'.format(player._id, player.name))
//                 # tmp = input('Press any key')
//         if is_finished(stage, players):
//             stage.paint()
//             break
//     finish_game(stage, players)
//
// if __name__ == '__main__':
//     main()
