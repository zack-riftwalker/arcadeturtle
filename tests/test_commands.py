from collections import deque

from arcadeturtle._commands import InstantCmd, MoveCmd, RotateCmd


def test_fifo_order_preserved():
    q = deque()
    q.append(MoveCmd(0, (0, 0), (100, 0), True, (0, 0, 0), 1, 3))
    q.append(RotateCmd(0, 0, 90, 90, 3))
    q.append(InstantCmd(0, lambda: None))
    assert isinstance(q.popleft(), MoveCmd)
    assert isinstance(q.popleft(), RotateCmd)
    assert isinstance(q.popleft(), InstantCmd)


def test_instant_cmd_runs_callable():
    hits = []
    cmd = InstantCmd(0, lambda: hits.append(1))
    cmd.fn()
    assert hits == [1]
