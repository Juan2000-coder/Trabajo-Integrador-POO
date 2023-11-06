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

public class GUIClass {
    private Process externalProcess;
    private static final String EXE_PATH = "D:\\tareas pancho\\UnCuyo\\Programacion Orientada a Objetos\\Trabajo-Integrador-POO-main\\CLIENTE\\build\\Cliente.exe";//cambiar para que sea una ruta relativa

    public void runExternalProgram(String ip, String port, javax.swing.JTextArea outputTextArea) {
        try {
            ProcessBuilder processBuilder = new ProcessBuilder(EXE_PATH, ip, port);
            processBuilder.redirectErrorStream(true);
            externalProcess = processBuilder.start();

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
                        if (line.contains("Error in XmlRpcClient::doConnect: Could not connect to server (error 0).")) {
                            mostrarErrorPopup(1);
                        }else if (line.contains("ERROR: POINT IS OUTSIDE OF WORKSPACE")){
                            mostrarErrorPopup(2);
                        }
                    }
                }
            };

            outputReader.execute();

            int exitCode = externalProcess.waitFor();
            appendToOutput(outputTextArea, "External program exited with code: " + exitCode);

        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
            appendToOutput(outputTextArea, "Error: " + e.getMessage());
        }
    }

    public void sendCommands(String command, javax.swing.JTextArea outputTextArea) {
        try {
            if (externalProcess != null) {
                OutputStream outputStream = externalProcess.getOutputStream();
                outputStream.write(command.getBytes());
                outputStream.flush();
            }
        } catch (IOException e) {
            e.printStackTrace();
            appendToOutput(outputTextArea, "Error: " + e.getMessage());
        }
    }

    public void closeProgram() {
        if (externalProcess != null) {
            externalProcess.destroy();
        }
    }

    private void appendToOutput(javax.swing.JTextArea outputTextArea, String text) {
        javax.swing.SwingUtilities.invokeLater(() -> {
            outputTextArea.append(text + "\n");
        });
    }

    public void showOutput(List<String> output, javax.swing.JTextArea outputTextArea) {
        for (String line : output) {
            appendToOutput(outputTextArea, line);
        }
    }
    private void mostrarErrorPopup(int tipo) {
        switch (tipo){
            case 1:
                sonido("D:\\tareas pancho\\UnCuyo\\Programacion Orientada a Objetos\\Trabajo-Integrador-POO-main\\CLIENTE\\audio\\Spongebob-Disappointed-Sound-Effect.wav");
                JOptionPane.showMessageDialog(null, "Error: No hay conexion con el servidor", "Error", JOptionPane.ERROR_MESSAGE);
                
                break;
            case 2:
                JOptionPane.showMessageDialog(null, "Error: Punto fuera de limites", "Error", JOptionPane.ERROR_MESSAGE);
                break;
        }
    
}
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
