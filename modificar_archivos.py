import sys

def modificarArchivos():
    decision = input(
        "Que queres modificar:\n1. favourite_leagues.txt\n2. not_interested_leagues.txt\nELECCION: "
    )
    switch_case(decision)


def switch_case(decision):
    match decision:
        case "1":
            with open("favourite_leagues.txt", "a") as file:
                new_league = input("Que liga deseas agregar: ")
                file.write(f', "{new_league}"')
                sys.exit("Se ha modificado el archivo correctamente")

        case "2":
            with open("not_interested_leagues.txt", "a") as file:
                new_league = input("Que liga deseas agregar: ")
                file.write(f', "{new_league}"')
                sys.exit("Se ha modificado el archivo correctamente")
