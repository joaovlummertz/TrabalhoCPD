# Searching a key on a B-tree in Python
class NodeData:
    def __init__(self, data, indice):
        self.data = data
        self.indice = indice

# Create a node
class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.child = []

    def display(self, list_t):
        i =0
        while i < len(self.child) or i < len(self.keys):
            if i < len(self.child):
                self.child[i].display(list_t)
            if i < len(self.keys):
                list_t.append(self.keys[i].indice)
            i += 1
        if self.leaf:
            for c in self.child:
                list_t.append(c.indice)

# Tree
class BTree:
    def __init__(self, t):
        self.root = BTreeNode(True)
        self.t = t

    # Insert a key
    def insert(self, data, indice):
        root = self.root
        k = NodeData(data, indice)
        if len(root.keys) == (2 * self.t) - 1:
            temp = BTreeNode()
            self.root = temp
            temp.child.insert(0, root)
            self.split_child(temp, 0)
            self.insert_non_full(temp, k)
        else:
            self.insert_non_full(root, k)

    # Insert non full
    def insert_non_full(self, x, k):
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append((None, None))
            while i >= 0 and k.data < x.keys[i].data:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = k
        else:
            while i >= 0 and k.data < x.keys[i].data:
                i -= 1
            i += 1
            if len(x.child[i].keys) == (2 * self.t) - 1:
                self.split_child(x, i)
                if k.data > x.keys[i].data:
                    i += 1
            self.insert_non_full(x.child[i], k)

    # Split the child
    def split_child(self, x, i):
        t = self.t
        y = x.child[i]
        z = BTreeNode(y.leaf)
        x.child.insert(i + 1, z)
        x.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t: (2 * t) - 1]
        y.keys = y.keys[0: t - 1]
        if not y.leaf:
            z.child = y.child[t: 2 * t]
            y.child = y.child[0: t]

    # Returns sorted list
    def display(self, list_t):
            self.root.display(list_t)
