from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnight, AKnave),  # A is either a knight or a knave
    Implication(AKnight, Not(AKnave)),  # If A is a knight, then A is not a knave
    Implication(AKnave, Not(AKnight))  # If A is a knave, then A is not a knight
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnight, AKnave),  # A is either a knight or a knave
    Or(BKnight, BKnave),  # B is either a knight or a knave
    Implication(AKnight, And(AKnave, BKnave)),  # If A is a knight, then A and B are both knaves
    Implication(AKnave, Or(BKnight, Not(BKnave)))  # If A is a knave, then B is a knight or B is not a knave
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnight, AKnave),  # A is either a knight or a knave
    Or(BKnight, BKnave),  # B is either a knight or a knave
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),  # If A is a knight, then A and B are both knights or both knaves
    Implication(AKnave, Or(And(AKnight, BKnave), And(AKnave, BKnight))),  # If A is a knave, then A and B are of different kinds
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),  # If B is a knight, then A and B are of different kinds
    Implication(BKnave, Or(And(AKnight, BKnight), And(AKnave, BKnave)))  # If B is a knave, then A and B are both knights or both knaves
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B then says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(AKnight, AKnave),  # A is either a knight or a knave
    Or(BKnight, BKnave),  # B is either a knight or a knave
    Or(CKnight, CKnave),  # C is either a knight or a knave
    Implication(AKnight, Or(AKnight, AKnave)),  # If A is a knight, then A says either "I am a knight." or "I am a knave."
    Implication(AKnave, Not(Or(AKnight, AKnave))),  # If A is a knave, then A cannot say either "I am a knight." or "I am a knave."
    Implication(BKnight, Implication(AKnight, AKnave)),  # If B is a knight, then if A is a knight, then A is a knave
    Implication(BKnave, Not(Implication(AKnight, AKnave))),  # If B is a knave, then A did not say "I am a knave."
    Implication(BKnight, CKnave),  # If B is a knight, then C is a knave
    Implication(BKnave, CKnight),  # If B is a knave, then C is a knight
    Implication(CKnight, AKnight),  # If C is a knight, then A is a knight
    Implication(CKnave, AKnave)  # If C is a knave, then A is a knave
)

def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")

if __name__ == "__main__":
    main()
