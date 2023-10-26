//NOTA: ESTO POR AHORA FUNCIONA SOLO EN LINUX

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
    XmlRpcValue oneArg, noArgs, result, args;




    //MAPA
    std::map<std::string, int> comandoANumero;
    // Llena el mapa con las correspondencias entre strings y valores. Esto es similar a un diccionario en python.
    comandoANumero["reporteGeneral"] = 1;
    comandoANumero["obtenerLogServidor"] = 2;
    comandoANumero["seleccionarModo"] = 3;
    comandoANumero["conectarRobot"] = 4;
    comandoANumero["desconectarRobot"] = 5;
    comandoANumero["activarMotores"] = 6;
    comandoANumero["desactivarMotores"] = 7;
    comandoANumero["home"] = 8;
    comandoANumero["movLineal"] = 9;
    comandoANumero["activarPinza"] = 10;
    comandoANumero["desactivarPinza"] = 11;
    comandoANumero["grabar"] = 12;
    comandoANumero["cargar"] = 13;
    comandoANumero["posicionActual"] = 14;
    comandoANumero["desconectarServidor"] = 15;
    comandoANumero["listarArchivosDeTrabajo"] = 16;    




    
    bool flagCliente = true;
    string input;
    string input1, input2, input3, input4;
    while (flagCliente) {
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

                if (c.execute("reporteGeneral", noArgs, result)) { //ESTO ESTA BIEN... FUNCIONA!
                    cout << result << "\n\n";
                } else {
                    cout << "Error en la llamada a 'reporteGeneral'\n\n";
                }
                break;

            case 2: //obtenerLogServidor

                if (c.execute("obtenerLogServidor", noArgs, result)) { 
                    cout << result << "\n\n";
                } else {
                    cout << "Error en la llamada a 'obtenerLogServidor'\n\n";
                }
                break;

            case 3: //seleccionarModo
                cin >> input;
                oneArg[0] = input;
                if (c.execute("seleccionarModo", oneArg, result)) {
                    cout << result << "\n\n";
                } else {
                    cout << "Error en la llamada a 'seleccionarModo'\n\n";
                }
                break;
            case 4: //conectarRobot
        
                if (c.execute("conectarRobot", noArgs, result)) {
                    cout << result << "\n\n";
                } else {
                    cout << "Error en la llamada a 'conectarRobot'\n\n";
                }
                break;


            case 5: //desconectarRobot
  
                if (c.execute("desconectarRobot", noArgs, result)) {
                    cout << result << "\n\n";
                } else {
                    cout << "Error en la llamada a 'desconectarRobot'\n\n";
                }
                break;

            
            case 6: //activarMotor

                if (c.execute("activarMotores", noArgs, result)) {
                    cout << result << "\n\n";
                } else {
                    cout << "Error en la llamada a 'activarMotores'\n\n";
                }
                break;

            case 7: //desactivarMotores

                if (c.execute("desactivarMotores", noArgs, result)) {
                    cout << result << "\n\n";
                } else {
                    cout << "Error en la llamada a 'desactivarMotores'\n\n";
                }
                break;

            case 8: //home

                if (c.execute("home", noArgs, result)) {
                    cout << result << "\n\n";
                } else {
                    cout << "Error en la llamada a 'home'\n\n";
                }
                break;

            case 9: //movLineal
                
                cin >> input1 >> input2 >> input3;
                args[0]=input1;
                args[1]=input2;
                args[2]=input3;
                if (cin.peek() != '\n') {
                    cin >> input4;
                    args[3]=input4;
                }

                if (c.execute("movLineal", args, result)) {
                    cout << result << "\n\n";
                } else {
                    cout << "Error en la llamada a 'movLineal'\n\n";
                }
                break;

            case 10: //activarPinza

                if (c.execute("activarPinza", noArgs, result)) {
                    cout << result << "\n\n";
                } else {
                    cout << "Error en la llamada a 'activarPinza'\n\n";
                }
                break;

            case 11: //desactivarPinza

                if (c.execute("desactivarPinza", noArgs, result)) {
                    cout << result << "\n\n";
                } else {
                    cout << "Error en la llamada a 'desactivarPinza'\n\n";
                }
                break;

            case 12: //grabar
                if (cin.peek() != '\n') {
                    cin >> input1;
                    oneArg[0]=input1;
                }
                if (c.execute("grabar", oneArg, result)) {
                    cout << result << "\n\n";
                } else {
                    cout << "Error en la llamada a 'grabar'\n\n";
                }
                break;

            case 13: //cargar

                if (c.execute("cargar", noArgs, result)) {
                    cout << result << "\n\n";
                } else {
                    cout << "Error en la llamada a 'cargar'\n\n";
                }
                break;

            case 14: //posicionActual
                if (c.execute("posicionActual", noArgs, result)) {
                    cout << result << "\n\n";
                } else {
                    cout << "Error en la llamada a 'posicionActual'\n\n";
                }
                break;
            case 15: //desconectarServidor

                if (c.execute("desconectarServidor", noArgs, result)) {
                    cout << result << "\n\n";
                } else {
                    cout << "Error en la llamada a 'desconectarServidor'\n\n";
                }
                break;

            case 16: //listarArchivosDeTrabajo

                if (c.execute("listarArchivosDeTrabajo", noArgs, result)) {
                    cout << result << "\n\n";
                } else {
                    cout << "Error en la llamada a 'listarArchivosDeTrabajo'\n\n";
                }
                break;
          

            default:
                std::cout << "Opción no válida" << std::endl;
        }
    } else {
        std::cout << "Opción no encontrada" << std::endl;
    }
    }
    return 0;
}