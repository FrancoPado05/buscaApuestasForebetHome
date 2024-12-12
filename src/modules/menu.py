import busca_forebet
import goles_forebet
import modificar_archivos
import gol_HT

def main():
    
    menu = input(
        '1. GOLES\n2.GANADOR DE PARTIDO\n3.GOL HT\n4.ADD\nELECCION: '
        )

    match menu:
        case '1':
            dia = input('Today, Tomorrow o Otro: ')
            goles_forebet.buscarPartidosDeGoles(dia)
        case '2':
            dia = input('Today o Tomorrow: ')
            busca_forebet.buscarPartidosDeGanador(dia)
            
        case '3':
            dia = input('Today o Tomorrow: ')
            gol_HT.buscarPartidosGolHT(dia)

        case '4':
            modificar_archivos.modificarArchivos()

if __name__ == '__main__':
    main()