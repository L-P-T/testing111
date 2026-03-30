import javax.swing.*;
import java.awt.*;

public class NightCity extends JPanel 
{

    @Override
    public void paintComponent(Graphics g) 
    {
        super.paintComponent(g);
        setBackground(new Color(10, 10, 60)); // Dark blue night sky

        // === Crescent Moon ===
        g.setColor(new Color(245, 245, 220)); // Pale moon color
        g.fillOval(50, 50, 60, 60);           // Full moon base
        g.setColor(new Color(10, 10, 60));    // Sky overlap for crescent
        g.fillOval(65, 50, 60, 60);
        g.setColor(Color.BLACK);
        g.drawOval(50, 50, 60, 60);

        // === Stars ===
        g.setColor(Color.WHITE);
        g.fillOval(150, 40, 5, 5);
        g.fillOval(200, 80, 5, 5);
        g.fillOval(300, 60, 5, 5);
        g.fillOval(350, 30, 5, 5);
        g.fillOval(250, 50, 5, 5);
        g.fillOval(100, 90, 5, 5);

        // === Buildings ===
        g.setColor(new Color(70, 70, 120));
        g.fillRect(100, 150, 80, 150);
        g.setColor(Color.BLACK);
        g.drawRect(100, 150, 80, 150);

        g.setColor(new Color(90, 90, 150));
        g.fillRect(200, 120, 100, 180);
        g.setColor(Color.BLACK);
        g.drawRect(200, 120, 100, 180);

        // Windows
        g.setColor(Color.YELLOW);
        for (int y = 160; y < 280; y += 30) 
        {
            g.fillRect(110, y, 15, 15);
            g.fillRect(140, y, 15, 15);
        }
        for (int y = 130; y < 280; y += 30) 
        {
            g.fillRect(210, y, 15, 15);
            g.fillRect(240, y, 15, 15);
            g.fillRect(270, y, 15, 15);
        }

        // === Road ===
        g.setColor(Color.DARK_GRAY);
        g.fillRect(0, 300, 400, 50);
        g.setColor(Color.BLACK);
        g.drawRect(0, 300, 400, 50);

        g.setColor(Color.WHITE);
        g.fillRect(50, 320, 40, 5);
        g.fillRect(150, 320, 40, 5);
        g.fillRect(250, 320, 40, 5);
        g.fillRect(350, 320, 40, 5);

        // === Car ===
        g.setColor(Color.RED);
        g.fillRect(60, 280, 80, 20);
        g.setColor(Color.BLACK);
        g.drawRect(60, 280, 80, 20);

        g.setColor(Color.BLACK);
        g.fillOval(70, 300, 20, 20);
        g.fillOval(110, 300, 20, 20);

        g.setColor(Color.CYAN);
        g.fillRect(65, 282, 30, 15);
        g.fillRect(95, 282, 40, 15);
        g.setColor(Color.BLACK);
        g.drawLine(95, 282, 95, 297);

        // === Street Lamps 
        int postWidth = 6;
        int postHeight = 30;
        int postTopY = 300 - postHeight;  // sits on road top
        int headSize = 20;

        for (int postX : new int[]{200, 320}) 
        {
            
            // Post
            g.setColor(Color.GRAY);
            g.fillRect(postX, postTopY, postWidth, postHeight);
            g.setColor(Color.BLACK);
            g.drawRect(postX, postTopY, postWidth, postHeight);

            // Head centered above post
            int headX = postX + (postWidth - headSize) / 2;
            int headY = postTopY - headSize;

            g.setColor(new Color(255, 255, 180)); // soft yellow glow
            g.fillOval(headX, headY, headSize, headSize);
            g.setColor(Color.BLACK);
            g.drawOval(headX, headY, headSize, headSize);
        }
    }

    public static void main(String[] args) {
        JFrame frame = new JFrame("Night City View");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(420, 400);
        frame.add(new NightCity());
        frame.setVisible(true);
    }
}