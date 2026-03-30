import javax.swing.*;
import java.awt.*;

public class ZigzagSquares extends JPanel
{

public void paintComponent(Graphics g)
{

super.paintComponent(g);

int size = 40; // square size
int startX = 100;
int startY = 50;

// Coordinates for 5 squares touching corners
int[ ] x = {startX, startX + size, startX + 2*size, startX + size, startX};
int[ ] y = {startY, startY + size, startY + 2*size, startY + 3*size, startY + 4*size};

for (int i = 0; i < 5; i++)
{

g.drawRect(x[i], y[i], size, size);

// Diagonal \
g.drawLine(x[i], y[i], x[i] + size, y[i] + size);

// Diagonal /
g.drawLine(x[i] + size, y[i], x[i], y[i] + size);

}
}

public static void main(String[ ] args)
{

JFrame frame = new JFrame();
frame.setSize(300, 300);
frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
frame.add(new ZigzagSquares());
frame.setVisible(true);

}
}