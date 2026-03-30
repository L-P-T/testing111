import javax.swing.JOptionPane;

public class DialogInput {
    public static void main(String[] args) {
        String name = JOptionPane.showInputDialog("Please enter your name:");
        JOptionPane.showMessageDialog(null, "Your name is: " + name);

        String mark = JOptionPane.showInputDialog("Please enter your mark:");
        int i1 = Integer.parseInt(mark);

        if (i1 >= 50) {
            JOptionPane.showMessageDialog(null, name + " PASS the examination");
            JOptionPane.showMessageDialog(null, "Congratulations! Well done!");
        } else {
            JOptionPane.showMessageDialog(null, name + " FAIL the examination");
            JOptionPane.showMessageDialog(null, "You need to study harder. Don't give up.");
        }
    }
}

