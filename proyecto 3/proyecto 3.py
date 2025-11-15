import yaml

class TuringMachine:
    def __init__(self, states, input_alphabet, tape_alphabet,
                 initial_state, accept_states, transitions):
        self.states = states
        self.input_alphabet = input_alphabet
        self.tape_alphabet = tape_alphabet
        self.initial_state = initial_state
        self.accept_states = accept_states
        self.transitions = transitions

    def simulate(self, input_string):
        # cinta inicial
        tape = list(input_string) + ["B"] * 50  # relleno con blancos
        head = 0
        current_state = self.initial_state
        steps = []

        while True:
            # guardar descripción instantánea
            steps.append(f"({current_state}, {''.join(tape)}, head={head})")

            symbol = tape[head]

            # buscar transición válida
            transition = None
            for t in self.transitions:
                if t["state"] == current_state and symbol in t["read"]:
                    transition = t
                    break

            if transition is None:
                break  # no hay transición válida → detener

            # aplicar transición
            write_symbol = transition["write"][transition["read"].index(symbol)]
            tape[head] = write_symbol
            move = transition["move"]
            current_state = transition["next"]

            if move == "R":
                head += 1
            elif move == "L":
                head -= 1

            # condición de aceptación
            if current_state in self.accept_states:
                steps.append(f"({current_state}, {''.join(tape)}, head={head})")
                return steps, True

        return steps, False


def load_mt_from_yaml(file_path):
    with open(file_path, "r") as f:
        data = yaml.safe_load(f)

    mt_data = data["mt"]
    return TuringMachine(
        states=mt_data["states"],
        input_alphabet=mt_data["input_alphabet"],
        tape_alphabet=mt_data["tape_alphabet"],
        initial_state=mt_data["initial_state"],
        accept_states=mt_data["accept_states"],
        transitions=mt_data["transitions"]
    ), mt_data["inputs"]


if __name__ == "__main__":
    # lista de archivos YAML que quieres correr
    yaml_files = ["mt_reconocedora.yaml", "mt_alteradora.yaml"]

    for yaml_file in yaml_files:
        print("\n" + "="*50)
        print(f"Ejecutando Máquina de Turing desde: {yaml_file}")
        print("="*50)

        tm, inputs = load_mt_from_yaml(yaml_file)

        for inp in inputs:
            print(f"\nSimulación para input: {inp}")
            steps, accepted = tm.simulate(inp)
            for s in steps:
                print(s)
            print("Resultado:", "ACEPTADO ✅" if accepted else "RECHAZADO ❌")

