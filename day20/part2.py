import os
import sys
from part1 import *


def simulate_once(button):
    broadcaster = button.outputs[0]
    signal_queue = [(False, button, broadcaster)]
    while signal_queue:
        signal, node_from, node_to = signal_queue[0]
        signal_queue = signal_queue[1:]

        if node_to.name == "rx" and not signal:
            return True


        propagate = node_to.receive_signal(node_from, signal)
        if propagate:
            for output in node_to.outputs:
                signal_queue.append((node_to.state, node_to, output))
    return False


if __name__ == "__main__":
    inf = sys.argv[1]
    with open(inf, "r") as inf:
        button = parse_input(inf)

    runs = 0
    while True:
        runs += 1
        print(runs)
        if simulate_once(button):
            break

    print(runs)
