import collections

class TrieNode:
    def __init__(self):
        self.children = collections.defaultdict(TrieNode)
        self.is_end = False
        self.indice = None

class Trie:
    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.root = TrieNode()

    def insert(self, word: str, indice) -> None:
        """
        Inserts a word into the trie.
        """
        current = self.root
        for letter in word:
            current = current.children[letter]
        current.is_end = True
        current.indice = indice

    def search(self, word: str) -> int or list or None:
        """
        Returns indice if word is in the trie, returns none otherwise.
        """
        current = self.root
        for letter in word:
            current = current.children.get(letter)
            if current is None:
                return None
        return current.indice

    def startswith(self, prefix: str) -> bool:
        """
        Returns if there is any word in the trie that starts with the given prefix.
        """
        current = self.root

        for letter in prefix:
            current = current.children.get(letter)
            if not current:
                return False

        return True

    def allthatstartswith(self, prefix: str, listt):
        current = self.root

        for letter in prefix:
            current = current.children.get(letter)
            if not current:
                return  # Prefixo não encontrado

        stack = [current]
        while stack:
            node = stack.pop()
            if node.is_end:
                listt.append(node.indice)  # Adiciona o índice se for um fim de palavra
            for child in node.children.values():
                stack.append(child)  # Adiciona os filhos na pilha
