import javax.swing.*;
import java.awt.*;

public class DrawLine extends JPanel
{

public void paintComponent(Graphics g)
{

super.paintComponent(g);

// Draw a line from (x1=50, y1=50) to (x2=200, y2=50)
g.drawLine(50, 50, 200, 50);

}

public static void main(String[ ] args)
{

JFrame frame = new JFrame();
frame.setSize(300, 200);
frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
frame.add(new DrawLine());
frame.setVisible(true);

}
}

