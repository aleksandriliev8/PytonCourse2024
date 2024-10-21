class Person:

    def __init__(self, name="", age=0):
        self.name = name
        self.age = age

    def __repr__(self):
        return ""
    
    def __str__(self):
        return f"{self.name} ({self.age})"
    
    def __gt__(self, other):
        if isinstance(other, Person):
            return self.age > other.age
        return NotImplemented
    
class FamilyTree:
    
    def __init__(self, root = Person()):
        self.root = root
        self.children = []

    def __str__(self, level=0):
        indent = "    " * level
        result = f"{indent}> {self.root.name} ({self.root.age})\n"

        for child in self.children:
            result += child.__str__(level + 1)

        return result
    
    def add_child_tree(self, other):
        if isinstance(other, FamilyTree):
            self.children.append(other)

    def count_descendants(self):
        count = len(self.children)

        for child in self.children:
            if isinstance(child, FamilyTree):
                count += child.count_descendants()
                
        return count

# tests

# Create dummies of class Person
john = Person("John", 50)
emily = Person("Emily", 30)
jake = Person("Jake", 18)
dan = Person("Dan", 3)
fiona = Person("Fiona", 7)

# Create family trees for each person
john_familiy_tree = FamilyTree(john)
emily_familiy_tree = FamilyTree(emily)
jake_familiy_tree = FamilyTree(jake)
dan_familiy_tree = FamilyTree(dan)
fiona_familiy_tree = FamilyTree(fiona)

# ---- Testing add_child_tree functionality ----

# Add children to John
john_familiy_tree.add_child_tree(jake_familiy_tree)
john_familiy_tree.add_child_tree(emily_familiy_tree)

# Add children to Emily
emily_familiy_tree.add_child_tree(dan_familiy_tree)
emily_familiy_tree.add_child_tree(fiona_familiy_tree)

assert john_familiy_tree.children[1] == emily_familiy_tree
assert john_familiy_tree.children[0] == jake_familiy_tree
assert emily_familiy_tree.children[0] == dan_familiy_tree
assert emily_familiy_tree.children[1] == fiona_familiy_tree

# ---- Testing __init__ functionality ----

assert john.name == "John"
assert john.age == 50


assert jake.name == "Jake"
assert jake.age == 18


assert john_familiy_tree.root == john
assert len(john_familiy_tree.children) == 2

assert jake_familiy_tree.root == jake
assert len(jake_familiy_tree.children) == 0

assert emily_familiy_tree.root == emily
assert dan_familiy_tree.root == dan
assert fiona_familiy_tree.root == fiona


# ---- Testing __str__functionality ----
expected_repr = "> John (50)\n    > Jake (18)\n    > Emily (30)\n        > Dan (3)\n        > Fiona (7)\n"
assert str(john_familiy_tree) == expected_repr

# # ---- Testing __gt__functionality ---- 
assert john > emily
assert john > jake
assert emily > jake
assert jake > dan

# # ---- Testing __gt__functionality ---- 
assert john_familiy_tree.count_descendants() == 4
assert jake_familiy_tree.count_descendants() == 0
assert emily_familiy_tree.count_descendants() == 2