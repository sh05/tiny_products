import random

def get_shuffle_list(n):
    tmp = list(range(n))
    random.shuffle(tmp)
    return [set([tmp.pop(), tmp.pop()]) for _ in range(int(n/2))]

def fortune_flower(n, verbose=False):
    # 上下共にランダムに結び目を作ってしまう
    top_edges = get_shuffle_list(n)
    bottom_edges = get_shuffle_list(n)
    failure_flag = False
    
    # popで取り出してしまうので今のうちに表示
    if verbose:
        print("上側の結び目", top_edges)
        print("下側の結び目", bottom_edges)
    
    # pop: 通過したら取り出す
    start_pair = top_edges.pop()
    start_edge = start_pair.pop()
    tied = start_pair.pop()
    
    # 結果確認用に経路情報を保持
    path = []
    path.append(start_edge)
    path.append(tied)
    
    while top_edges:
        # 下の結び目を伝う
        # 下側で該当する結び目を探す
        current_pair = [be for be in bottom_edges if tied in be].pop()
        # setなので差集合演算をしてから取り出している
        tmp = current_pair - {tied}
        tied = tmp.pop()
        # 結果確認用に経路
        path.append(tied)
        # 通過したら取り出す
        bottom_edges.remove(current_pair)
        
        # 輪ができているかのチェックは下を伝った後だけでよい
        if tied == start_edge:
            failure_flag = True
            break
        
        # 上の結び目を伝う
        # 上側で該当する結び目を探す
        current_pair = [te for te in top_edges if tied in te].pop()
        # setなので差集合演算をしてから取り出している
        tmp = current_pair - {tied}
        tied = tmp.pop()
        # 結果確認用に経路
        path.append(tied)
        # 通過したら取り出す
        top_edges.remove(current_pair)
    
    
    if verbose:
        if failure_flag:
            print("失敗: ", "経路（輪っか）", path, "\n")
        else:
            print("成功: ", "経路（輪っか）", path, "\n")
    
    return failure_flag


# 短冊の本数
n = 10
# 試行回数
sample = 50000
print("1回試しに実行")
# 詳細を表示 False or True
verbose = True
# 実行
fortune_flower(n, verbose)

print("{}回実行して割合を算出".format(sample))
# 詳細を表示 False or True
verbose = False
# 実行
results = [fortune_flower(n, verbose) for _ in range(sample)]
print("失敗", results.count(True))
print("成功", results.count(False))
print("成功確率", results.count(False) / sample * 100, "%")
