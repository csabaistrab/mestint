from collections import namedtuple



State = namedtuple("State", ["disk", "char"])
Student = namedtuple('Student', ['name', 'age', 'DOB'])
S = Student('Nandini', '19', '2541997')

class Problem:
    """A formális problémát leíró absztrakt osztálya.
    Az __init__, goal_test és path_cost metódusok adott esetben felülírhatók.
    A létrehozzott alosztály példányai, megoldhatók a különféle keresési funkciókkal."""

    def __init__(self, initial, goal=None):
        """Konstruktor. Szükség esetén további tulajdonságokkal bővíthető"""
        # kezdő állapot
        self.initial = initial

        # cél állapot
        self.goal = goal

    def actions(self, state):
        """Az adott állapotban végrehajtható műveletek visszaadásár szolgáló metódus.
        Az eredmény általában egy lista, de ha sok művelet van, akkor célszerű lehet
        iterátor alkalmazás a teljes lista vissza adása helyett."""
        raise NotImplementedError

    def result(self, state, action):
        """Azt az állapotot adja vissza, amely az adott művelet adott állapotban
        történő végrehajtásából adódik.A cselekvésnek a self.actions(state) egyikének kell lennie."""
        raise NotImplementedError

    def goal_test(self, state):
        """Igaz értékkel tér vissza, ha az adott állapot egy cél állapot.
        Az alapértelmezett metódus összehasonlítja az állapotot a self.goal-al,
        vagy ellenőrzi a self.goal állapotát, ha az egy lista, a konstruktorban megadottak szerint.
        A módszer felülírása szükséges lehet, ha nem elegendő egyetlen self.goal összehasonlítása."""
        if isinstance(self.goal, list):
            for s in self.goal:
                if s==state:
                    return True

            return False
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Egy olyan megoldási útvonal költségét adja vissza.
        Ha a probléma olyan, hogy az elérési út nem számít, ez a függvény csak az állapot2-t nézi.
        Ha az elérési út számít, figyelembe veszi a c-t, esetleg az állapot1-et és az akciót.
        Az alapértelmezetten a költség 1 az elérési út minden lépéséért."""
        return c + 1

    def value(self, state):
        """Optimalizálási problémák esetén minden állapotnak van értéke.
        A hegymászó és más hasonló algoritmusok megpróbálják maximalizálni ezt az értéket."""
        raise NotImplementedError
class Hanoi(Problem):
    def __init__(self, n):
        # n darab korongunk van
        self.size = n

        # "1" * n : Kezdő állapot. Hány darab korng van az 1-es rúdon
        # "3" * n : Cél állapot. Hány darab korong van a 2-es rúdon
        super().__init__("1" * n, "3" * n)

    def actions(self, state):
        """Operátorok definiálása"""
        acts = []

        # Nézzük meg az egyes rúdak állapotát
        f1 = state.find("1")
        f2 = state.find("2")
        f3 = state.find("3")

        # Ha az 1. rúd nem üres és tartalma kisebb mint ami
        # a 2. rúdon van vagy a 2. rúd üres akkor
        # 1. rúdról átrakhatunk a második rúdra
        if -1 < f1 and (f1 < f2 or f2 == -1):
            acts.append(State(f1, "2"))

        if -1 < f1 and (f1 < f3 or f3 == -1):
            acts.append(State(f1, "3"))

        if -1 < f2 and (f2 < f1 or f1 == -1):
            acts.append(State(f2, "1"))

        if -1 < f2 and (f2 < f3 or f3 == -1):
            acts.append(State(f2, "3"))

        if -1 < f3 and (f3 < f1 or f1 == -1):
            acts.append(State(f3, "1"))

        if -1 < f3 and (f3 < f2 or f2 == -1):
            acts.append(State(f3, "2"))

        return acts

    def result(self, state, action):
        """Operátorok hatásának definiálása"""

        # diks = korong, char = rúd
        disk, char = action

        # Előtte és utánna lévő korongok helyeinek összefűzése
        return state[0:disk] + char + state[disk + 1:]
def heuristic_calc_empty_jar(State):
    if State==(3,3,3) or State == (4,1,0):
        return 0
    c=0
    for i in State:
        if i == 0:
            c+=1
        else:
            i == 1
    return c+1

def main():
    h = Hanoi(3)

    print(h.size, h.initial, h.goal)
    print("Index is :", S[1])



if __name__ == '__main__':
    main()