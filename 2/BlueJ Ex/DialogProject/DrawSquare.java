import javax.swing.*;
import java.awt.*;

public class DrawSquare extends JPanel
{
public void paintComponent(Graphics g)
{

super.paintComponent(g);

// Draw a square (x=50, y=50, width=100, height=100)
g.drawRect(50, 50, 100, 100);

// Draw first diagonal (top-left to bottom-right)
g.drawLine(50, 50, 150, 150);

// Draw second diagonal (top-right to bottom-left)
g.drawLine(150, 50, 50, 150);

}
public static void main(String[ ] args)
{

JFrame frame = new JFrame();
frame.setSize(250, 250);
frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
frame.add(new DrawSquare());

frame.setVisible(true);

}
}