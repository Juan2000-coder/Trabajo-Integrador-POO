#include <iostream>
#include <stdlib.h>
#include <fstream>
#include <algorithm>
#include <cctype> // Include for std::isdigit
#include <iomanip> 
#include <map>
#include <string>
#include <cstdlib> // Para la función 'system'
#include <future>   // Para la función 'async' y 'future' en el metodo timeOut.
#include <chrono>   // Para la función 'wait_for' en el metodo timeOut.


using namespace std;

//#include "json.hpp"
#include "XmlRpc.h" 

using namespace XmlRpc;

//METODO PARA SOLICITAR Y VERIFICAR EL ID DE UN CLIENTE

std::string generarIDUsuario(const std::string& nombre) {
    // Genera el ID a partir del nombre, eliminando espacios y reemplazando por guiones bajos.
    std::string id = nombre;
    std::replace(id.begin(), id.end(), ' ', '_'); // Reemplaza los espacios por guiones bajos
    std::transform(id.begin(), id.end(), id.begin(), ::tolower); // Convierte a minúsculas
    return id;
}


//METODO PARA LLAMAR AL SERVIDOR CON TIMEOUT

bool llamarAlServidorConTimeout(XmlRpcClient& c, const char* metodo, const XmlRpcValue& args, XmlRpcValue& result, int timeout, const std::string& id) {
    XmlRpcValue argsConId;
    argsConId[0] = id;

    // Establece el ID de usuario como primer argumento.
    if (args.valid()){
        for (int i = 0; i < args.size(); i++) {
            argsConId[1 + i] = args[i];
        }
    }

    std::future<bool> future = std::async(std::launch::async, [&] {
        return c.execute(metodo, argsConId, result);
    });

    // Espera hasta que se complete la llamada o hasta que se agote el tiempo.
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
            cout << "Comando: reporte\nDescripción: genera un reporte general del robot.\n";
            break;
        case 2:
            cout << "Comando: log\nDescripción: obtiene el registro de actividad del servidor.\n";
            break;
        case 3:
            cout << "Comando: modo\nDescripción: selecciona el modo (a) coordenadas absolutas o (r) relativas.\n";
            break;
        case 4:
            cout << "Comando: robot\nDescripción: conecta (on) o desconecta(off) el robot.\n";
            break;
        case 5:
            cout << "Comando: motores\nDescripción: activa(on) o desactiva(off) los motores del robot.\n";
            break;
        case 6:
            cout << "Comando: home\nDescripción: mueve el robot a la posición home.\n";
            break;
        case 7:
            cout << "Comando: movlineal\nDescripción: movimiento lineal del efecto final.\n";
            break;
        case 8:
            cout << "Comando: efector\nDescripción: activa(on) o desactiva(off) el efector final del robot.\n";
            break;
        case 9:
            cout << "Comando: grabar\nDescripción: graba una secuencia de movimientos en un archivo de trabajo.\n";
            break;
        case 10:
            cout << "Comando: cargar\nDescripción: carga una secuencia de movimientos de un archivo de trabajo.\n";
            break;
        case 11:
            cout << "Comando: estado\nDescripción: obtiene el estado actual del robot (posicion y modo).\n";
            break;
        case 12:
            cout << "Comando: listar\nDescripción: lista los archivos de trabajo disponibles en el servidor.\n";
            break;
        case 13:
            cout << "Comando: ayuda\nDescripción: Muestra la lista de comandos disponibles.\n";
            break;
        case 14:
            cout << "Comando: cls\nDescripción: limpia la consola.\n";
            break;
        case 15:
            cout << "Comando: salir\nDescripción: cierra el programa.\n";
            break;
        case 16:
            cout << "Comando: ejecutar\nDescripción: ejecuta un comando en código G.\n";
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

    std::string nombre;
    std::string id;
    std::string mensaje ="Ingrese su nombre <Apellido Nombre>";
    std::cout << mensaje << std::endl;
    std::getline(cin, nombre); // Lee toda la línea, incluyendo espacios en blanco.

    id = generarIDUsuario(nombre);

    std::cout << "Su ID de usuario es: " << id << std::endl;
    std::cout << "Bienvenido " << nombre << '\n'<< std::endl;



    int port = atoi(argv[2]);

    XmlRpcClient c(argv[1], port);
    XmlRpcValue oneArg, noArgs, result, args;

    // Registra la función signalHandler para la señal SIGINT.
    signal(SIGINT, signalHandler);


    //MAPA
    std::map<std::string, int> comandoANumero;
    // Llena el mapa con las correspondencias entre strings y valores. Esto es similar a un diccionario en python.
    comandoANumero["reporte"] = 1;
    comandoANumero["log"] = 2;
    comandoANumero["modo"] = 3;
    comandoANumero["robot"] = 4;
    comandoANumero["motores"] = 5;
    comandoANumero["home"] = 6;
    comandoANumero["movlineal"] = 7;
    comandoANumero["efector"] = 8;
    comandoANumero["grabar"] = 9;
    comandoANumero["cargar"] = 10;
    comandoANumero["estado"] = 11;
    comandoANumero["listar"] = 12;
    comandoANumero["ayuda"] = 13;   // Agregamos el comando "ayuda" a la lista de comandos.
    comandoANumero["cls"] = 14;     // Agregamos el comando "cls" a la lista de comandos.
    comandoANumero["salir"] = 15;   // Agregamos el comando "salir" a la lista de comandos.
    comandoANumero["ejecutar"] = 16;  // Agregamos el comando "enviarComando" a la lista de comandos.

    
    bool flagCliente = true;
    string input;
    string input1, input2, input3, input4;

  

    while (flagCliente) {
    cin >> input;
    
    auto it = comandoANumero.find(input); //Aquí, it es un iterador que apunta a la ubicación de input en el std::map stringToValue. La función find busca la clave input 
                                          //en el mapa. Si input se encuentra en el mapa, it apuntará a esa ubicación, y it != stringToValue.end() será verdadero, 
                                          //lo que significa que la clave se encontró. Si input no se encuentra en el mapa, it será igual a stringToValue.end(), y la 
                                          //condición será falsa, lo que indica que la clave no se encontró.
    
    

    int timeout = 60; // Tiempo límite en segundos para la llamada al servidor.
    if (it != comandoANumero.end()) { 
        int value = it->second; //accede al valor asociado a la clave
       
        
        switch (value) {
            case 1: //reporte

                if (llamarAlServidorConTimeout(c, "reporte", noArgs, result, timeout, id)) {
                    cout << result << "\n\n";
                } else {
                    cout << "Error en la llamada a 'reporte'\n\n";
                }
                break;

            case 2: //log

                if (llamarAlServidorConTimeout(c, "log", noArgs, result, timeout, id)) {
                    cout << result << "\n\n";
                } else {
                    cout << "Error en la llamada a 'log'\n\n";
                }
                break;

            case 3: //modo
                cin >> input;
                oneArg[0] = input;
                if (llamarAlServidorConTimeout(c, "modo", oneArg, result, timeout, id)) {
                    cout << result << "\n\n";
                } else {
                    cout << "Error en la llamada a 'modo'\n\n";
                }
                break;
            case 4: //robot
                cin >> input;
                oneArg[0] = input;
                if (llamarAlServidorConTimeout(c, "robot", oneArg, result, timeout, id)) {
                    cout << result << "\n\n";
                } else {
                    cout << "Error en la llamada a 'robot'\n\n";
                }
                break;
            case 5: //motores
                cin >> input;
                oneArg[0] = input;
                if (llamarAlServidorConTimeout(c, "motores", oneArg, result, timeout, id)) {
                    std::cout<< result << std::endl;
                } else {
                    std::cout << "Error en la llamada a 'motores'\n\n" << std::endl;
                }
                break;
            case 6: //home
                if (llamarAlServidorConTimeout(c, "home", noArgs, result, timeout, id)) {
                    cout << result << "\n\n";
                } else {
                    cout << "Error en la llamada a 'home'\n\n";
                }
                break;

            case 7: //movlineal
                
                cin >> input1 >> input2 >> input3;
                args[0]=input1;
                args[1]=input2;
                args[2]=input3;
                if (cin.peek() != '\n') {
                    cin >> input4;
                    args[3]=input4;
                }

                if (llamarAlServidorConTimeout(c, "movlineal", args, result, timeout, id)) {
                    cout << result << "\n\n";
                } else {
                    cout << "Error en la llamada a 'movlineal'\n\n";
                }
                break;

            case 8: //efector
                cin >> input;
                oneArg[0] = input;
                if (llamarAlServidorConTimeout(c, "efector", oneArg, result, timeout, id)) {
                    cout << result << "\n\n";
                } else {
                    cout << "Error en la llamada a 'efector'\n\n";
                }
                break;

            case 9: //grabar
                if (cin.peek() != '\n') {
                    cin >> input1;
                    oneArg[0]=input1;
                }
                if (llamarAlServidorConTimeout(c, "grabar", oneArg, result, timeout, id)) {
                    cout << result << "\n\n";
                } else {
                    cout << "Error en la llamada a 'grabar'\n\n";
                }
                break;

            case 10: //cargar
                cin >> input;
                oneArg[0] = input;
                if (llamarAlServidorConTimeout(c, "cargar", oneArg, result, timeout, id)) {
                    cout << result << "\n\n";
                } else {
                    cout << "Error en la llamada a 'cargar'\n\n";
                }
                break;

            case 11: //estado

                if (llamarAlServidorConTimeout(c, "estado", noArgs, result, timeout, id)) {
                    cout << result << "\n\n";
                } else {
                    cout << "Error en la llamada a 'estado'\n\n";
                }
                break;

            case 12: //listar

                if (llamarAlServidorConTimeout(c, "listar", noArgs, result, timeout, id)) {
                    cout << result << "\n\n";
                } else {
                    cout << "Error en la llamada a 'listar'\n\n";
                }
                break;
            
            case 13: // Ayuda
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
            

            case 14:    // cls
                    cls();
                    
                break;
            
            case 15:    //salir
                cout << "Saliendo del programa...\n";
                flagCliente = false;
                break;

            case 16:   //ejecutar
                cin.ignore(); // Ignora el salto de línea pendiente en el búfer.
                getline(cin, input); // Lee toda la línea como una cadena.
                

                // Luego, puedes procesar la cadena según tus necesidades.
                // Por ejemplo, si necesitas enviarla como argumento, puedes hacerlo como lo estabas haciendo.

                oneArg[0] = input;

                if (llamarAlServidorConTimeout(c, "ejecutar", oneArg, result, timeout, id)) {
                    cout << result << "\n\n";
                } else {
                    cout << "Error en la llamada a 'ejecutar'\n\n";
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