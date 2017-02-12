#Chess AI for the bcp95 project
#I used minimax and alpha-beta algorithm to predict the next move

inf = 1000*1000

class chess:
    #chess object
    #captal letters are for white pieces and small letters for black pieces
    # p = pawn, r = rook, b = bishop, q = queen, k = king, n = knight

    def set_pos(self, value):
        tmp = value.split('/')
        for i in range(8):
            self.board.append(list(tmp[i]))
        self.out[0] = list(tmp[8])
        self.out[1] = list(tmp[9])

    def __init__(self, value="rnbqkbnr/pppppppp/......../......../......../......../PPPPPPPP/RNBQKBNR//"):
        self.board = []
        self.out =[[], []]
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
                    moves = [(0, 1), (1, 0), (-1, 0), (0, -1)]
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
    
                #bishop moves
                if(self.board[i][j].lower() == 'b'):
                    moves = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
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

                #queen moves
                if(self.board[i][j].lower() == 'q'):
                    moves = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
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
             
                #knight moves
                if(self.board[i][j].lower() == 'n'):
                    moves = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
                    for d in moves:
                        x, y = i + d[0], j + d[1]
                        if(x < 0 or x >=8 or y < 0 or y >= 8):
                            continue
                        if(self.board[x][y] == '.'):
                            yield (i, j, x, y, 0)
                        elif(chess.is_opponent(self.board[i][j], self.board[x][y])):
                            yield (i, j, x, y, 1)

                #pawn moves
                if(self.board[i][j].lower() == 'p'):
                    d = 1
                    if(color == 1): d = -1
                    moves = [(d, 0), (d, 1), (d, -1), (2 * d, 0)]
                    for mv in moves:
                        x, y = i + mv[0], j + mv[1]
                        if(x < 0 or x >=8 or y < 0 or y >= 8):
                            continue
                        if(mv[1] == 0):
                            if(mv[0] == d):
                                if(self.board[x][y] == ".") :
                                    yield (i, j, x, y, 0)
                            else:
                                if(((color == 0 and i == 1) or (color == 1 and i == 6)) and self.board[i+d][j] == "." and self.board[x][y] == '.'):
                                    yield (i, j, x, y, 0)
                        elif(self.board[x][y] != '.' and chess.is_opponent(self.board[i][j], self.board[x][y])):
                            yield (i, j, x, y, 1)

                #king moves
                if(self.board[i][j].lower() == 'k'):
                    moves = [(0, 1), (0, -1), (1, 1), (1, 0), (1, -1), (-1, 1), (-1, 0), (-1, -1)]
                    for d in moves:
                        x, y = i + d[0], j + d[1]
                        if(x < 0 or x >=8 or y < 0 or y >= 8):
                            continue
                        if(self.board[x][y] == '.'):
                            yield (i, j, x, y, 0)
                        elif(chess.is_opponent(self.board[i][j], self.board[x][y])):
                            yield (i, j, x, y, 1)

    def next_possible_moves(self, color):
        for mv in self.next_move_gen(color):
            self.move(mv)
            if(self.king_is_under_attack(color)):
                self.undo_move(mv)
                continue
            x, y = mv[2], mv[3]
            if((color == 0 and self.board[x][y] == "K") or (color == 1 and self.board[x][y] == "k")):
                self.undo_move(mv)
                continue
            self.undo_move(mv)
            yield mv
    
    def king_is_under_attack(self, color):
        opp = 1 - color
        kx, ky = 0, 0
        for i in range(8):
            for j in range(8):
                if((self.board[i][j] == 'k' and color == 0) or (self.board[i][j] == 'K' and color == 1)):
                    kx, ky = i, j
        for mv in list(self.next_move_gen(opp)):
            if(mv[2] == kx and mv[3] == ky):
                return True
        return False

                        
    def move(self, mv):
        x0, y0 = mv[0], mv[1]
        x1, y1 = mv[2], mv[3]
        mod = (self.board[x1][y1] != '.')
        if(mod):
            if(self.board[x1][y1].islower()):
                self.out[0].append(self.board[x1][y1])
            else:
                self.out[1].append(self.board[x1][y1])
        self.board[x1][y1] = self.board[x0][y0]
        self.board[x0][y0] = "."

    def undo_move(self, mv):
        x0, y0 = mv[0], mv[1]
        x1, y1 = mv[2], mv[3]
        if(mv[4]):
            if('a'<self.board[x1][y1]<'z'): dead = self.out[1].pop()
            else: dead = self.out[0].pop() 
        else:
            dead = "."
        self.board[x0][y0] = self.board[x1][y1]
        self.board[x1][y1] = dead

    def heuristic_value(self, color):
        return [len(list(self.next_move_gen(color))) - len(list(self.next_move_gen(1-color))), None]

        val = {"p": 1, "b": 3.5, "r": 5.25, "n": 3.5, "q":9.75, "k":0, ".":0}
        ret = 0
        for i in range(8):
            for j in range(8):
                if(self.board[i][j].islower()):
                    ret += val[self.board[i][j]]
                else:
                    ret -= val[self.board[i][j].lower()]
        if(color):
            ret = -ret
        return [ret, None]

    def pr_table(self, tab = 0):
        print("-----------------")
        for i in range(8):
            print('\t'*tab, ''.join(self.board[i]))
        print("-----------------")

    def user_move(self, mv):
        src = mv.split()[0]
        dest = mv.split()[1]
        x0, y0 = 8 - int(src[1]), ord(src[0]) - ord("A")
        x1, y1 = 8 - int(dest[1]), ord(dest[0]) - ord("A")
        self.move((x0, y0, x1, y1))

def alpha_beta_pruning(node, depth, a = -inf, b = inf, player = 1, maxim = 1):
    if(depth == 0):
        return node.heuristic_value(player)
    #print(len(list(node.next_possible_moves(player))))
    if(maxim):
        v = [-inf, None]
        for mv in node.next_possible_moves(player):
            # child = chess(str(node))
            # child.move(mv)
            node.move(mv)
            tmp = alpha_beta_pruning(node, depth-1, a, b, player, 0)
            node.undo_move(mv)
            
            if(tmp[0] >= v[0]):
                v[0], v[1] = tmp[0], mv
            a = max(a, v[0])
            if(a >= b):
                break
        return v
    else:
        v = [inf, None]
        for mv in node.next_possible_moves(1 - player):
            # child = chess(str(node))
            # child.move(mv)
            node.move(mv)
            tmp = alpha_beta_pruning(node, depth-1, a, b, player, 1)
            node.undo_move(mv)
            
            if(tmp[0] <= v[0]):
                v[0], v[1] = tmp[0], mv
            b = min(b, v[0])
            if(a >= b):
                break
        return v


def main():
    tmp=chess()
    tmp.pr_table()
    while(1):
        mv = input()
        tmp.user_move(mv)
        tmp.pr_table()

        ai_mv = alpha_beta_pruning(tmp, 4, -inf, inf, 0, 1)[1]
        print(ai_mv)
        tmp.move(ai_mv)
        tmp.pr_table()    

        

if __name__=="__main__": main()