package com.mycompany.guicliente;

import javax.swing.*;
import javax.swing.SwingWorker;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.util.List;
import javax.sound.sampled.*;
import java.io.File;

/**
 * Esta clase gestiona la interacción con un programa externo a través de procesos, proporcionando
 * funcionalidad para ejecutar, enviar comandos y cerrar el programa.
 */
public class GUIClass {
    private Process externalProcess;
    private static String EXE_PATH;
    private boolean logFlag = false;
    /**
     * Ejecuta un programa externo con los parámetros proporcionados y redirige su salida estándar.
     *
     * @param ip              Dirección IP para la conexión.
     * @param port            Puerto para la conexión.
     * @param outputTextArea  JTextArea donde se mostrará la salida del programa.
     */
    public void runExternalProgram(String ip, String port, javax.swing.JTextArea outputTextArea) {
        try {
            // Obtiene la ruta de la aplicación externa y configura ProcessBuilder.
            String basePath = new File("").getAbsolutePath();
            System.out.println(basePath);
            //EXE_PATH = basePath.replace("GUI", "\\CONSOLA\\build\\Cliente.exe");
            EXE_PATH = basePath + "\\CLIENTE\\CONSOLA\\build\\Cliente.exe";
            System.out.println(EXE_PATH);
            ProcessBuilder processBuilder = new ProcessBuilder(EXE_PATH, ip, port);
            processBuilder.redirectErrorStream(true);
            externalProcess = processBuilder.start();

            // Configura un SwingWorker para leer y mostrar la salida del proceso.
            //SwingWorker es una clase en Swing que proporciona una forma de realizar tareas en segundo plano de manera concurrente con el hilo de 
            //la interfaz de usuario (UI). 
            SwingWorker<Void, String> outputReader = new SwingWorker<Void, String>() {
                @Override
                protected Void doInBackground() throws Exception {
                    BufferedReader reader = new BufferedReader(new InputStreamReader(externalProcess.getInputStream()));
                    String line;
                    while ((line = reader.readLine()) != null) {
                        publish(line);
                    }
                    return null;
                }

                @Override
                protected void process(List<String> chunks) {
                    for (String line : chunks) {
                        appendToOutput(outputTextArea, line);
                        // Muestra mensajes de error emergentes según el contenido de la salida.
                        if(logFlag == false){
                            if (line.contains("Error in XmlRpcClient::doConnect: Could not connect to server (error 0).")) {
                                mostrarErrorPopup(1);
                            } else if (line.contains("POINT IS OUTSIDE OF WORKSPACE")) {
                                mostrarErrorPopup(2);
                            } else if (line.contains("Error in XmlRpcClient::writeRequest: write error (error 10053).")) {
                                mostrarErrorPopup(3);
                            }else if(line.contains("Conexión exitosa con el robot.")){
                                //sonido(basePath + "\\audio\\USB-CONNECTING-SOUND-EFFECT.wav");
                                sonido(basePath + "\\CLIENTE\\GUI\\audio\\USB-CONNECTING-SOUND-EFFECT.wav");
                            }else if(line.contains("Conexión cerrada.")){
                                //sonido(basePath + "\\audio\\Sonido-de-Robot-Apagándose-Efecto-de-Sonido.wav");
                                sonido(basePath + "\\CLIENTE\\GUI\\audio\\Sonido-de-Robot-Apagándose-Efecto-de-Sonido.wav");
                            }
                        }
                    }
                    logFlag = false;
                }
            };

            outputReader.execute();

            int exitCode = externalProcess.waitFor();
            appendToOutput(outputTextArea, "El programa externo ha finalizado con código: " + exitCode);

        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
            appendToOutput(outputTextArea, "Error: " + e.getMessage());
        }
    }

    /**
     * Envía comandos al programa externo a través de su entrada estándar.
     *
     * @param command         Comando a enviar.
     * @param outputTextArea  JTextArea donde se mostrará la salida del programa.
     */
    public void sendCommands(String command, javax.swing.JTextArea outputTextArea) {
        try {
            if (command.contains("log")){
                    logFlag = true;
                    System.out.println(logFlag);
             }
            if (externalProcess != null) {

                OutputStream outputStream = externalProcess.getOutputStream();
                System.out.println(command);
                outputStream.write(command.getBytes());
                outputStream.flush();
            }
        } catch (IOException e) {
            e.printStackTrace();
            appendToOutput(outputTextArea, "Error: " + e.getMessage());
        }
    }

    /**
     * Cierra el programa externo si está en ejecución.
     */
    public void closeProgram() {
        if (externalProcess != null) {
            externalProcess.destroy();
        }
    }

    /**
     * Agrega texto al JTextArea de salida de manera segura en el hilo de interfaz gráfica.
     *
     * @param outputTextArea  JTextArea donde se mostrará el texto.
     * @param text            Texto para agregar.
     */
    private void appendToOutput(javax.swing.JTextArea outputTextArea, String text) {
        javax.swing.SwingUtilities.invokeLater(() -> {
            outputTextArea.append(text + "\n");
        });
    }

    /**
     * Muestra un mensaje emergente de error junto con un efecto de sonido.
     *
     * @param tipo  Tipo de error (1, 2 o 3).
     */
    private void mostrarErrorPopup(int tipo) {
        String audioBasePath = new File("").getAbsolutePath();
        String audioPath = audioBasePath.replace("GUI", "GUI\\audio");
        switch (tipo) {
            case 1:
                sonido(audioPath + "\\Spongebob-Disappointed-Sound-Effect.wav");
                JOptionPane.showMessageDialog(null, "Error: No hay conexión con el servidor", "Error", JOptionPane.ERROR_MESSAGE);
                break;
            case 2:
                sonido(audioPath + "\\Spongebob-Disappointed-Sound-Effect.wav");
                JOptionPane.showMessageDialog(null, "Error: Punto fuera de límites", "Error", JOptionPane.ERROR_MESSAGE);
                break;
            case 3:
                JOptionPane.showMessageDialog(null, "Error inesperado. Intente reiniciar la conexión con el robot", "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    /**
     * Reproduce un archivo de sonido.
     *
     * @param soundFileName Ruta del archivo de sonido a reproducir.
     */
    public static void sonido(String soundFileName) {
        try {
            File soundFile = new File(soundFileName);
            AudioInputStream audioInputStream = AudioSystem.getAudioInputStream(soundFile);
            Clip clip = AudioSystem.getClip();
            clip.open(audioInputStream);
            clip.start();
        } catch (UnsupportedAudioFileException | LineUnavailableException | IOException e) {
            e.printStackTrace();
        }
    }
}
