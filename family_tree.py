from typing import Self

from graphviz import Digraph


class Person:
    def __init__(self, name: str, relation: str) -> None:
        self.name = name
        self.relation = relation
        self.father: Self | None = None
        self.mother: Self | None = None
        self.siblings: list[Self] = []
        self.children: list[Self] = []

    def add_parents(self, father: Self | None, mother: Self | None) -> None:
        self.father = father
        self.mother = mother
        if father:
            father.children.append(self)
        if mother:
            mother.children.append(self)

    def add_sibling(self, sibling: Self):
        self.siblings.append(sibling)
        sibling.siblings.append(self)


def build_ancestors(person: Person, gen: int, max_gen: int, side: str = ""):
    if gen > max_gen:
        return
    father = Person(
        f"{side}{ordinal(gen)} Great-Grandfather",
        f"{side}{ordinal(gen)} Great-Grandfather",
    )
    mother = Person(
        f"{side}{ordinal(gen)} Great-Grandmother",
        f"{side}{ordinal(gen)} Great-Grandmother",
    )
    person.add_parents(father, mother)

    # Add uncle/aunt as sibling
    if gen < max_gen:
        uncle = Person(
            f"{side}{ordinal(gen)} Great-Uncle", f"{side}{ordinal(gen)} Great-Uncle"
        )
        father.add_sibling(uncle)
        aunt = Person(
            f"{side}{ordinal(gen)} Great-Aunt", f"{side}{ordinal(gen)} Great-Aunt"
        )
        mother.add_sibling(aunt)

    build_ancestors(father, gen + 1, max_gen, side)
    build_ancestors(mother, gen + 1, max_gen, side)


def ordinal(n: int) -> str:
    return {1: "1st", 2: "2nd", 3: "3rd"}.get(n, f"{n}th")


def build_graph(person: Person, dot: Digraph | None = None) -> Digraph:
    if dot is None:
        dot = Digraph(comment="Family Tree")
    if person is None:
        return dot

    dot.node(person.name, f"{person.name}\n({person.relation})")

    if person.father:
        dot.node(
            person.father.name, f"{person.father.name}\n({person.father.relation})"
        )
        dot.edge(person.father.name, person.name)
        build_graph(person.father, dot)

    if person.mother:
        dot.node(
            person.mother.name, f"{person.mother.name}\n({person.mother.relation})"
        )
        dot.edge(person.mother.name, person.name)
        build_graph(person.mother, dot)

    for sib in person.siblings:
        dot.node(sib.name, f"{sib.name}\n({sib.relation})")
        dot.edge(sib.father.name if sib.father else sib.mother.name, sib.name)

    return dot


# Build tree
you = Person("You", "Self")
build_ancestors(you, 1, 6, side="Paternal ")
build_ancestors(you, 1, 6, side="Maternal ")

# Add a cousin for demo
second_cousin = Person(
    "Paternal 2nd Cousin Twice Removed", "Paternal 2nd Cousin Twice Removed"
)
if you.father and you.father.siblings:
    second_cousin.add_parents(you.father.siblings[0], None)

fourth_cousin = Person("Fourth Cousin", "Fourth Cousin")
fourth_cousins_daughter = Person("Rebecca Amy McDermott", "Fourth Cousin's Daughter")
fourth_cousins_daughter.add_parents(fourth_cousin, fourth_cousin)

# Build and render graph
dot = build_graph(you)
dot.render("family_tree_graphviz", view=True)
