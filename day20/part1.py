import sys
from collections import defaultdict


class Node(object):
    s_low_count = 0
    s_high_count = 0

    def __init__(self, name):
        self.name = name
        self.outputs = []
        self.inputs = {}
        self.state = False

    def connect_output(self, node):
        self.outputs.append(node)

    def connect_input(self, node):
        self.inputs[node] = False

    def receive_signal(self, node_from, high):
        self.inputs[node_from] = high
        print(f"{node_from.name} -{'high' if high else 'low'}-> {self.name}")
        if high:
            Node.s_high_count += 1
        else:
            Node.s_low_count += 1
        return False


class FF(Node):
    def __init__(self, name):
        super().__init__(name)

    def receive_signal(self, node_from, high):
        super().receive_signal(node_from, high)
        if not high:
            self.state = not self.state
            return True
        return False


class Button(Node):
    def __init__(self, name):
        super().__init__(name)


class Broadcast(Node):
    def __init__(self, name):
        super().__init__(name)

    def receive_signal(self, node_from, high):
        super().receive_signal(node_from, high)
        self.state = high
        return True


class Conjunction(Node):
    def __init__(self, name):
        super().__init__(name)

    def receive_signal(self, node_from, high):
        super().receive_signal(node_from, high)
        self.state = not all(v for _, v in self.inputs.items())
        return True


def parse_input(inf):
    root = Button("button")
    connections = defaultdict(list)
    connections["button"] = ["broadcaster"]
    nodes = {"button": root}

    for line in inf:
        connect_from, connect_to = [x.strip() for x in line.split("->")]
        connect_to = [x.strip() for x in connect_to.split(",")]

        if connect_from == "broadcaster":
            node_type = Broadcast
            node_name = connect_from
        elif connect_from[0] == "%":
            node_type = FF
            node_name = connect_from[1:]
        elif connect_from[0] == "&":
            node_type = Conjunction
            node_name = connect_from[1:]
        else:
            node_type = Node
            node_name = connect_from

        node = node_type(node_name)
        nodes[node_name] = node
        connections[node_name] += connect_to

    for connect_from, connect_to in connections.items():
        from_node = nodes[connect_from]
        for to in connect_to:
            to_node = nodes.get(to, Node(to))
            from_node.connect_output(to_node)
            to_node.connect_input(from_node)

    return root


def simulate_once(button):
    broadcaster = button.outputs[0]
    signal_queue = [(False, button, broadcaster)]
    while signal_queue:
        signal, node_from, node_to = signal_queue[0]
        signal_queue = signal_queue[1:]

        propagate = node_to.receive_signal(node_from, signal)
        if propagate:
            for output in node_to.outputs:
                signal_queue.append((node_to.state, node_to, output))


if __name__ == "__main__":
    inf = sys.argv[1]
    with open(inf, "r") as inf:
        button = parse_input(inf)

    for i in range(1):
        simulate_once(button)

    print(Node.s_high_count)
    print(Node.s_low_count)
