import javax.swing.*;
import java.awt.*;

public class House extends JPanel {

    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        setBackground(Color.white);

        // === Grass ===
        g.setColor(Color.GREEN);
        g.fillRect(0, 250, 400, 50);
        g.setColor(Color.BLACK);
        g.drawRect(0, 250, 400, 50);

        // === House body (heliotrope rectangle) ===
        g.setColor(new Color(223, 115, 255)); // Heliotrope
        g.fillRect(120, 150, 160, 100);
        g.setColor(Color.BLACK);
        g.drawRect(120, 150, 160, 100);

        // === Chimney (draw first so roof overlaps it) ===
        g.setColor(new Color(139, 69, 19)); // Brown
        g.fillRect(230, 90, 20, 40);
        g.setColor(Color.BLACK);
        g.drawRect(230, 90, 20, 40);

        // === Roof (brown triangle, drawn after chimney) ===
        g.setColor(new Color(139, 69, 19));
        int[] roofX = {120, 200, 280};
        int[] roofY = {150, 80, 150};
        g.fillPolygon(roofX, roofY, 3);
        g.setColor(Color.BLACK);
        g.drawPolygon(roofX, roofY, 3);

        // === Door (burgundy rectangle, toward right side) ===
        g.setColor(new Color(128, 0, 32)); // Burgundy
        g.fillRect(220, 190, 40, 60);
        g.setColor(Color.BLACK);
        g.drawRect(220, 190, 40, 60);

        // === Window (sky blue square with + cross) ===
        int wx = 140, wy = 170, wsize = 40;
        g.setColor(new Color(135, 206, 235)); // Sky blue
        g.fillRect(wx, wy, wsize, wsize);
        g.setColor(Color.BLACK);
        g.drawRect(wx, wy, wsize, wsize);
        // Draw + cross
        g.drawLine(wx + wsize / 2, wy, wx + wsize / 2, wy + wsize); // vertical
        g.drawLine(wx, wy + wsize / 2, wx + wsize, wy + wsize / 2); // horizontal

        // === Sun (yellow circle) ===
        g.setColor(Color.YELLOW);
        g.fillOval(300, 50, 50, 50);
        g.setColor(Color.BLACK);
        g.drawOval(300, 50, 50, 50);
    }

    public static void main(String[] args) {
        JFrame frame = new JFrame("House");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(400, 350);
        frame.add(new House());
        frame.setVisible(true); v
    }
}
