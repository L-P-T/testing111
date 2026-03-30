import javax.swing.*;
import java.awt.*;

public class ChrismasTree extends JPanel {
    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        setBackground(Color.white);

        // === Tree (3 stacked green triangles, no outline) ===
        g.setColor(Color.GREEN);
        g.fillPolygon(new int[]{150, 100, 200}, new int[]{20, 120, 120}, 3);   // Top
        g.fillPolygon(new int[]{150, 90, 210}, new int[]{60, 160, 160}, 3);   // Middle
        g.fillPolygon(new int[]{150, 80, 220}, new int[]{100, 200, 200}, 3);  // Bottom

        // === Tree trunk ===
        g.setColor(new Color(139, 69, 19)); // Brown
        g.fillRect(135, 200, 30, 50);

        // === Ornaments (colored squares with black outline) ===
        g.setColor(Color.RED);
        g.fillRect(145, 40, 15, 15);
        g.setColor(Color.BLACK);
        g.drawRect(145, 40, 15, 15);

        g.setColor(Color.BLUE);
        g.fillRect(120, 100, 15, 15);
        g.setColor(Color.BLACK);
        g.drawRect(120, 100, 15, 15);

        g.setColor(Color.YELLOW);
        g.fillRect(170, 140, 15, 15);
        g.setColor(Color.BLACK);
        g.drawRect(170, 140, 15, 15);

        g.setColor(new Color(128, 0, 128)); // Purple
        g.fillRect(140, 170, 15, 15);
        g.setColor(Color.BLACK);
        g.drawRect(140, 170, 15, 15);

        g.setColor(new Color(0, 128, 0)); // Green
        g.fillRect(160, 110, 15, 15);
        g.setColor(Color.BLACK);
        g.drawRect(160, 110, 15, 15);
    }

    public static void main(String[] args) {
        JFrame frame = new JFrame("ChrismasTree");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(400, 300);
        frame.add(new ChrismasTree());
        frame.setVisible(true);
    }
}