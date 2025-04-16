def get_machine(node: ParseTreeNode, cfg: CFG):

    if node.symbol in cfg.T:
        # Make terminal machine here
        # return terminal_machine

    machines = []

    for child in node.children:
        machines.append(child.get_machine())

    node.combine_machines(machines)


def parse_tree_to_nfa(tree: ParseTree):
