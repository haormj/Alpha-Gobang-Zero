# coding:utf-8

from app.common.windoweffect import WindowEffect
from PyQt5.QtCore import QEasingCurve, QEvent, QPropertyAnimation, QRect, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QApplication, QMenu


class ChessBoardMenu(QMenu):
    """ 棋盘右击菜单 """

    def __init__(self, parent):
        super().__init__('', parent)
        self.windowEffect = WindowEffect()
        self.animation = QPropertyAnimation(self, b'geometry')
        # 创建动作
        self.restartGameAct = QAction(
            QIcon(r'app\resource\images\chess_board_interface\重新开始.png'), '重新开始', self)
        self.settingAct = QAction(
            QIcon(r'app\resource\images\chess_board_interface\设置.png'), '设置', self)
        self.action_list = [self.restartGameAct, self.settingAct]
        self.addActions(self.action_list)
        self.__initWidget()

    def __initWidget(self):
        """ 初始化小部件 """
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.OutQuad)
        self.setWindowFlags(self.windowFlags() | Qt.NoDropShadowWindowHint)
        self.windowEffect.addShadowEffect(self.winId())
        self.__setQss()

    def event(self, e: QEvent):
        if e.type() == QEvent.WinIdChange:
            self.windowEffect.addShadowEffect(self.winId())
        return QMenu.event(self, e)

    def exec_(self, pos):
        width = 176
        actionNum = len(self.action_list)
        # 每个item的高度为38px，10为上下的内边距和
        height = actionNum * 38 + 10
        # 设置动画
        self.animation.setStartValue(
            QRect(pos.x(), pos.y(), 1, height))
        self.animation.setEndValue(
            QRect(pos.x(), pos.y(), width, height))
        self.setStyle(QApplication.style())
        # 开始动画
        self.animation.start()
        super().exec_(pos)

    def __setQss(self):
        """ 设置层叠样式 """
        with open(r'app\resource\qss\menu.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())