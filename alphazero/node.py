# coding: utf-8
from math import sqrt
from typing import Tuple, Iterable, Dict


class Node:
    """ 蒙特卡洛树节点 """

    def __init__(self, prior_prob: float, c_puct: float = 5, parent=None):
        """
        Parameters
        ----------
        prior_prob: float
            节点的先验概率 `P(s, a)`

        c_puct: float
            探索常数

        parent: Node
            父级节点
        """
        self.c_puct = c_puct
        self.parent = parent
        self.P = prior_prob
        self.Q = 0
        self.U = 0
        self.N = 0
        self.score = 0
        self.children = {}  # type:Dict[int, Node]

    def select(self) -> tuple:
        """ 返回 `score` 最大的子节点，同时返回该节点对应的 action

        Returns
        -------
        action: int
            动作

        child: Node
            子节点
        """
        return max(self.children.items(), key=lambda item: item[1].score)

    def expand(self, action_probs: Iterable[Tuple[int, float]]):
        """ 拓展节点

        Parameters
        ----------
        action_probs: Iterable
            每个元素都为 `(action, prior_prob)` 元组，根据这个元组创建子节点，
            `action_probs` 的长度为当前棋盘的可用落点的总数
        """
        for action, prior_prob in action_probs:
            self.children[action] = Node(prior_prob, self.c_puct, self)

    def __update(self, value: float):
        """ 更新节点的访问次数 `N(s, a)`、节点的累计平均奖赏 `Q(s, a)` 、节点的 `U(s, a)` 和评分 `Score`

        Parameters
        ----------
        value: float
            用来更新节点内部数据
        """
        self.Q = (self.N * self.Q + value)/(self.N + 1)
        self.N += 1
        self.U = self.c_puct*self.P * sqrt(self.parent.N)/(1 + self.N)
        self.score = self.U + self.Q

    def backup(self, value: float):
        """ 反向传播 """
        if self.parent:
            # 每一层节点代表的玩家不同，所以需要将 value 取反
            self.parent.backup(-value)
            self.__update(value)

    def is_leaf_node(self):
        """ 是否为叶节点 """
        return len(self.children) == 0