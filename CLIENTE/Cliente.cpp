#include <iostream>
#include <stdlib.h>
#include <fstream>
#include <algorithm>
#include <cctype> // Include for std::isdigit
#include <iomanip> 
#include <map>
#include <string>
using namespace std;

//#include "json.hpp"
#include "XmlRpc.h"

using namespace XmlRpc;




int main(int argc, char* argv[]) {
    
    //VERIFICACION POR SI NO SE INGRESO CORRECTAMENTE LOS PARAMETROS DEL SERVIDOR PARA CONECTARSE
    if (argc != 3) {
    std::cerr << "Uso: hola_Client IP_HOST N_PORT\n";
    return -1;
    }
    
    int port = atoi(argv[2]);

    XmlRpcClient c(argv[1], port);
    XmlRpcValue oneArg, result;




    //MAPA
    std::map<std::string, int> comandoANumero;
    // Llena el mapa con las correspondencias entre strings y valores. Esto es similar a un diccionario en python.
    comandoANumero["reporteGeneral"] = 1;
    comandoANumero["obtenerLogServidor"] = 2;
    comandoANumero["seleccionarModo"] = 3;
    comandoANumero["conectarRobot"] = 4;
    comandoANumero["desconectarRobot"] = 5;
    comandoANumero["activarMotor"] = 6;
    comandoANumero["desactivarMotor"] = 7;
    comandoANumero["home"] = 8;
    comandoANumero["movLineal"] = 9;
    comandoANumero["activarPinza"] = 10;
    comandoANumero["desactivarPinza"] = 11;
    comandoANumero["grabar"] = 12;
    comandoANumero["cargar"] = 13;
    comandoANumero["levantarServidor"] = 14;
    comandoANumero["desconectarServidor"] = 15;
    comandoANumero["listarArchivosDeTrabajo"] = 16;    





    string input;
    cout << "Ingrese una opción: ";
    cin >> input;

    auto it = comandoANumero.find(input); //Aquí, it es un iterador que apunta a la ubicación de input en el std::map stringToValue. La función find busca la clave input 
                                          //en el mapa. Si input se encuentra en el mapa, it apuntará a esa ubicación, y it != stringToValue.end() será verdadero, 
                                          //lo que significa que la clave se encontró. Si input no se encuentra en el mapa, it será igual a stringToValue.end(), y la 
                                          //condición será falsa, lo que indica que la clave no se encontró.

    if (it != comandoANumero.end()) { 
        int value = it->second; //accede al valor asociado a la clave
        switch (value) {
            case 1: //reporteGeneral
                oneArg[0] = "reporteGeneral";

                if (c.execute("Generar", oneArg, result)) { //ESTO POSIBLEMENTE ESTA MAL. HAY QUE VER COMO HACER PARA LLAMAR AL METODO DEL SERVIDOR PERO EN PYTHON.
                    cout << result << "\n\n";
                } else {
                    cout << "Error en la llamada a 'Generar'\n\n";
                };
                break;
            case 2: //obtenerLogServidor
                std::cout << "Opción 2 seleccionada" << std::endl; //de aca para abajo esta sin modificar de lo que me dio chatgpt
                break;
            case 3: //seleccionarModo
                std::cout << "Opción 3 seleccionada" << std::endl;
                break;
            default:
                std::cout << "Opción no válida" << std::endl;
        }
    } else {
        std::cout << "Opción no encontrada" << std::endl;
    }

    return 0;
}