/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */

package com.mycompany.guicliente;
import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.awt.Image;
import org.bytedeco.opencv.opencv_core.Mat;
import org.bytedeco.opencv.opencv_videoio.*;
import org.bytedeco.javacv.Java2DFrameUtils;

public class VideoStreamingGUI extends JFrame {
    private final VideoCapture videoCapture;
    private final VideoPanel videoPanel;
    
    public VideoStreamingGUI(String streamUrl) {
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(640, 480);

        videoPanel = new VideoPanel();
        add(videoPanel);

        videoCapture = new VideoCapture(streamUrl); // Replace with the correct IP and port of the streaming server.


    }
    public void startVideoStream() {
        System.out.println(videoCapture.isOpened());
        if (videoCapture.isOpened()) {
            new Thread(this::showVideo).start();
        }
    }
    
    private Image matToImage(Mat mat) {
        BufferedImage bufImage = Java2DFrameUtils.toBufferedImage(mat);
        return bufImage;
    }
    
private void showVideo() {
    Mat frame = new Mat();
    while (true) {
        if (videoCapture.read(frame)) {
            System.out.println("Frame dimensions: " + frame.cols() + "x" + frame.rows());
            Image image = matToImage(frame);
            videoPanel.updateImage(image);
        } else {
            System.err.println("Video capture read failed.");
        }
    }
}

}


class VideoPanel extends JPanel {
    private Image image;

    public void updateImage(Image image) {
        this.image = image;
        repaint();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        if (image != null) {
            g.drawImage(image, 0, 0, getWidth(), getHeight(), this);
        }
    }
}
