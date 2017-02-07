#Chess AI for the bcp95 project
#I used minimax and alpha-beta algorithm to predict the next move

inf = 1000*1000

class chess:
    #chess object
    #captal letters are for white pieces and small letters for black pieces
    # p = pawn, r = rook, b = bishop, q = queen, k = king, n = knight

    board = []
    out =[[], []]

    def set_pos(self, value):
        tmp = value.split('/')
        for i in range(8):
            self.board.append(list(tmp[i]))
        self.out[0] = list(tmp[8])
        self.out[1] = list(tmp[9])

    def __init__(self, value="rnbqkbrn/pppppppp/......../......../......../......../PPPPPPPP/RNBQKBRN//"):
        chess.set_pos(self, value)

    def __str__(self):
        return '/'.join([''.join([self.board[i][j] for j in range(8)]) for i in range(8)] + [''.join([c for c in self.out[0]]), ''.join([c for c in self.out[1]])])

    def is_opponent(p1, p2):
        return p1.islower() != p2.islower()

    def next_move_gen(self, color):
        for i in range(8):
            for j in range(8):
                if(self.board[i][j] == "." or (color == 0 and "A" <= self.board[i][j] <= "Z") or (color == 1 and "a" <= self.board[i][j] <= "z")):
                    continue

                # rook moves
                if(self.board[i][j].lower() == 'r'):
                    moves = [(0,1), (1,0), (-1, 0), (0, -1)]
                    for d in moves:
                        x, y = i + d[0], j + d[1]
                        while(0 <= x < 8 and 0 <= y < 8):
                            if(self.board[x][y] == "."):
                                yield (i, j, x, y, 0)
                            elif(chess.is_opponent(self.board[i][j], self.board[x][y])):
                                yield (i, j, x, y, 1)
                                break
                            else:
                                break
                            x, y = x + d[0], y + d[1]
    def move(self, mv):
        x0, y0 = mv[0], mv[1]
        x1, y1 = mv[2], mv[3]
        mod = mv[4]
        if(mod):
            if(self.board[x1][y1].islower()):
                self.out[0].append(self.board[x1][y1])
            else:
                self.out[1].append(self.board[x1][y1])
        self.board[x1][y1] = self.board[x0][y0]
        self.board[x0][y0] = "."

    def heuristic_value(self):
        val = {"p": 1, "b": 3, "r": 2, "n": 2, "q":5, "k":0, ".":0}
        ret = 0
        for i in range(8):
            for j in range(8):
                if(self.board[i][j].islower()):
                    ret += val[self.board[i][j]]
                else:
                    ret -= val[self.board[i][j].lower()]
        return ([ret, None])

    def pr_table(self):
        print("-----------------")
        for i in range(8):
            print(''.join(self.board[i]))
        print("------------------")

def alpha_beta_pruning(node, depth, a = -inf, b = inf, player = 1):
    if(depth == 0):
        return node.heuristic_value()
    if(player):
        v = [-inf, None]
        for mv in list(node.next_move_gen(player)):
            child = chess(str(node))
            child.move(mv)
            tmp = alpha_beta_pruning(child, depth-1, a, b, 1 - player)
            if(tmp[0] > v[0]):
                v[0], v[1] = tmp[0], mv
            a = max(a, v[0])
            if(a >= b):
                break
        return v
    else:
        v = [inf, None]
        for mv in list(node.next_move_gen(player)):
            child = chess(str(node))
            child.move(mv)
            tmp = alpha_beta_pruning(child, depth-1, a, b, 1 - player)
            if(tmp[0] < v[0]):
                v[0], v[1] = tmp[0], mv
            b = min(a, v[0])
            if(a >= b):
                break
        return v

tmp = chess("rnbqkbrn/pprpprpp/......../......../......../......../PPRPPPRP/RNBQKBRN//")
tmp.pr_table()

for i in range(4):
    t = alpha_beta_pruning(tmp, 4, -inf, inf, 1 - i%2)
    tmp.move(t[1])
    tmp.pr_table()
