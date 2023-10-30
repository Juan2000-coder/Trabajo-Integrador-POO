#include <iostream>
#include <stdlib.h>
#include <fstream>
#include <algorithm>
#include <cctype> // Include for std::isdigit
#include <iomanip> 
#include <map>
#include <string>
#include <cstdlib> // Para la función 'system'

#include <future> // Para la función 'async' y 'future' en el metodo timeOut.
#include <chrono>

using namespace std;

//#include "json.hpp"
#include "XmlRpc.h"

using namespace XmlRpc;

//METODO PARA LLAMAR AL SERVIDOR CON TIMEOUT

bool llamarAlServidorConTimeout(XmlRpcClient& c, const char* metodo, const XmlRpcValue& args, XmlRpcValue& result, int timeout) {
    std::future<bool> future = std::async(std::launch::async, [&] {
        return c.execute(metodo, args, result);
    });

    // Esperar hasta que se complete la llamada o hasta que se agote el tiempo.
    std::future_status status = future.wait_for(std::chrono::seconds(timeout));

    if (status == std::future_status::timeout) {
        // La llamada ha superado el tiempo límite, por lo que la cancelamos.
        // Nota: XmlRpc no proporciona una forma directa de cancelar la llamada, por lo que puedes intentar manejarlo de manera personalizada si es necesario.
        return false;  // Timeout
    }

    // La llamada se completó dentro del tiempo límite.
    return future.get();
}


//METODO CLS PARA LIMPIAR CONSOLA. 
void cls() {
    #ifdef _WIN32
    // Código para Windows
    std::system("cls");
    #else
    // Código para sistemas tipo Unix/Linux (incluyendo macOS)
    std::system("clear");
    #endif
}

//METODO DE AYUDA
void mostrarAyuda(int comando) {
    switch (comando) {
        case 1:
            cout << "Comando: reporteGeneral\nDescripción: Genera un reporte general del robot.\n";
            break;
        case 2:
            cout << "Comando: obtenerLogServidor\nDescripción: Obtiene el registro de actividad del servidor.\n";
            break;
        case 3:
            cout << "Comando: seleccionarModo\nDescripción: Selecciona el modo de operación (auto o manual) del robot.\n";
            break;
        case 4:
            cout << "Comando: conectarRobot\nDescripción: Conecta el robot al servidor.\n";
            break;
        case 5:
            cout << "Comando: desconectarRobot\nDescripción: Desconecta el robot del servidor.\n";
            break;
        
        case 6:
            cout << "Comando: activarMotores\nDescripción: Activa los motores del robot.\n";
            break;
        
        case 7:
            cout << "Comando: desactivarMotores\nDescripción: Desactiva los motores del robot.\n";
            break;
        
        case 8:
            cout << "Comando: home\nDescripción: Mueve el robot a la posición home.\n";
            break;
        
        case 9:
            cout << "Comando: movLineal\nDescripción: Mueve el robot en línea recta.\n";
            break;
        
        case 10:
            cout << "Comando: activarPinza\nDescripción: Activa la pinza del robot.\n";
            break;

        case 11:
            cout << "Comando: desactivarPinza\nDescripción: Desactiva la pinza del robot.\n";
            break;
        
        case 12:
            cout << "Comando: grabar\nDescripción: Graba una secuencia de movimientos.\n";
            break;
        
        case 13:
            cout << "Comando: cargar\nDescripción: Carga una secuencia de movimientos.\n";
            break;
        
        case 14:
            cout << "Comando: posicionActual\nDescripción: Obtiene la posición actual del robot.\n";
            break;
        
        case 15:
            cout << "Comando: desconectarServidor\nDescripción: Desconecta el servidor.\n";
            break;
    
        case 16:
            cout << "Comando: listarArchivosDeTrabajo\nDescripción: Lista los archivos de trabajo disponibles.\n";
            break;

        case 17:
            cout << "Comando: ayuda\nDescripción: Muestra la lista de comandos disponibles.\n";
            break;

        case 18:
            cout << "Comando: cls\nDescripción: Limpia la consola.\n";
            break;
        
        case 19:
            cout << "Comando: salir\nDescripción: Cierra el programa.\n";
            break;

        default:
            cout << "Comando no reconocido. Use 'ayuda' para ver la lista de comandos disponibles.\n";
            break;
        }
    }


// Función que se ejecutará al recibir la señal SIGINT (Ctrl + C).
    void signalHandler(int signum) {
        std::cout << "\n Interrupcion por teclado recibida. \n Desconectando del servidor..." << std::endl;
        exit(0);
    }



int main(int argc, char* argv[]) {
    
    //VERIFICACION POR SI NO SE INGRESO CORRECTAMENTE LOS PARAMETROS DEL SERVIDOR PARA CONECTARSE
    if (argc != 3) {
    std::cerr << "Uso: hola_Client IP_HOST N_PORT\n";
    return -1;
    }
    
    int port = atoi(argv[2]);

    XmlRpcClient c(argv[1], port);
    XmlRpcValue oneArg, noArgs, result, args;

    // Registra la función signalHandler para la señal SIGINT.
    signal(SIGINT, signalHandler);


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
    comandoANumero["ayuda"] = 17;   // Agregamos el comando "ayuda" a la lista de comandos.
    comandoANumero["cls"] = 18;     // Agregamos el comando "cls" a la lista de comandos.
    comandoANumero["salir"] = 19;   // Agregamos el comando "salir" a la lista de comandos.
    comandoANumero["enviarComando"] = 20;  // Agregamos el comando "enviarComando" a la lista de comandos.

    
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
     
    int timeout = 15; // Tiempo límite en segundos para la llamada al servidor.

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

                if (llamarAlServidorConTimeout(c, "activarMotores", noArgs, result, timeout)) {
                    std::cout << "Llamada exitosa. Resultado: " << result << std::endl;
                } else {
                    std::cout << "Timeout: la llamada al servidor ha superado el tiempo límite." << std::endl;
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

            case 15: // desconectarServidor
                if (c.execute("desconectarServidor", noArgs, result)) {
                    cout << "Desconectando del servidor...\n";    
                    cout << "Desconectado del servidor.\n";
                    cout << "Saliendo del programa...\n";
                    exit(0);
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
            
            case 17: // Ayuda
                    cout << "Lista de comandos disponibles:" << endl;
                    for (const auto &cmd : comandoANumero) {
                        if (cmd.first != "ayuda") {  // Excluir el comando "ayuda" de la lista de comandos.
                            cout << cmd.first << endl;
                        }
                    }
                    cout << "Ingrese el comando del cual desea obtener informacion'.\n";
                    cin >> input2;
                    it = comandoANumero.find(input2);                        
                    if (it != comandoANumero.end()) {
                        
                        int value = it->second; //accede al valor asociado a la clave
                        mostrarAyuda(value);
                        }
                        else{
                        cout << "Error en la llamada a 'ayuda [Comando]'\n\n";
                        }
                    
                    break;
            

            case 18:    // cls
                    cls();
                    
                break;
            
            case 19:    //salir
                cout << "Saliendo del programa...\n";
                flagCliente = false;
                break;

            case 20:   //enviarComando
                cin.ignore(); // Ignora el salto de línea pendiente en el búfer.
                getline(cin, input); // Lee toda la línea como una cadena.
                

                // Luego, puedes procesar la cadena según tus necesidades.
                // Por ejemplo, si necesitas enviarla como argumento, puedes hacerlo como lo estabas haciendo.

                oneArg[0] = input;

                if (c.execute("enviarComando", oneArg, result)) {
                    cout << result << "\n\n";
                } else {
                    cout << "Error en la llamada a 'enviarComando'\n\n";
                }
                break;
                           

            default:
                std::cout << "Opción no válida" << std::endl;
        }
    }
    else {
        std::cout << "Opción no encontrada" << std::endl;
    }
    }
    
    return 0;
}