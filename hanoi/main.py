import sys, time, argparse
print = sys.stdout.write

class Tower:
    def __init__(self, n=0):
        self.floors = [i for i in reversed(range(1, n+1))]
    
    def stack(self, floor):
        if len(self.floors) > 0:
            assert floor < self.floors[-1], "Tower must be shaped pyramid, {}".format(self.floors)
        self.floors.append(floor)

    def pop(self):
        return self.floors.pop() if len(self.floors) else None

    def get_height(self):
        return len(self.floors)


class Towers:
    def __init__(self, towers, delay=0.5):
        self.towers = towers
        self.delay = delay
        self.step = 0
        self.max_height = max([f for t in towers for f in t.floors])

    def solve(self, n=0, verbose=False):
        # defalut of n is max_height
        if not n:
            n = self.max_height
        self.max_step = 2 ** n - 1
        if verbose:
            towers.display()
            time.sleep(1)
        self.move_floors(self.towers[0], self.towers[2], self.towers[1], n, verbose=verbose)

    def move_floors(self, dep, des, tmp, n, verbose=False):
        if n == 0:
            return

        if verbose:
            self.move_floors(dep, tmp, des, n-1, verbose)
            self.step += 1
            des.stack(dep.pop())
            self.display()
            self.move_floors(tmp, des, dep, n-1, verbose)
        else:
            self.move_floors(dep, tmp, des, n-1)
            des.stack(dep.pop())
            self.move_floors(tmp, des, dep, n-1)
        return    

    def display(self):
        print("\033[0;0H")
        print("\033[2J")

        for i in reversed(range(self.max_height)):
            for t in self.towers:
                print("\t")
                if len(t.floors) > i:
                    print("{}\t".format(t.floors[i]))
                else:
                    print("|\t")
            print("\n")

        print("\t-\t\t-\t\t-\n\tstep: {} / {}".format(self.step, self.max_step))
        time.sleep(self.delay)

if __name__ == "__main__":
    parser= argparse.ArgumentParser()

    parser.add_argument("n", type=int, help="Number of all discs")
    parser.add_argument("m", type=int, help="Number of discs to be moved")
    parser.add_argument("-d", "--delay", type=float, default=0.5, help="Seconds per frame")
    parser.add_argument("-f", "--force", action="store_true", help="Excecute huge steps")
    parser.add_argument("-v", "--verbose", action="store_true", help="Display towers moving discs")

    args = parser.parse_args()
    N = args.n
    M = args.m
    D = args.delay
    force = args.force
    verbose = args.verbose
    takes = (2**M - 1) * D
    
    # assert N >= M, f"M must be under N. N: {N}, M:{M} are given."
    if N < M:
       print(f"M must be under N. N: {N}, M:{M} are given.")
       exit()

    # assert takes < 30, f"This process takes {takes / 60} mins. Please execute with flag, '-f'"
    if  takes > 30:
       print(f"This process takes {takes / 60} mins. Please execute with flag, '-f'")
       exit()

    towers = Towers([Tower(N) if i == 0 else Tower() for i in range(3)], D)
    towers.solve(M, verbose=verbose)
