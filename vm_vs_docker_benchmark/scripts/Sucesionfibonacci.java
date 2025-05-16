import java.util.Scanner;

public class Sucesionfibonacci {
    public static void main(String[] args) {
        try (Scanner scanner = new Scanner(System.in)) {
            System.out.print("Ingrese el número de términos de la sucesión de Fibonacci: ");
            int n = scanner.nextInt();

            if (n <= 0) {
                System.out.println("La cantidad debe ser mayor que cero.");
                return;
            }

            long a = 0;
            long b = 1;

            for (int i = 0; i < n; i++) {
                System.out.print(a + " ");
                long temp = a + b;
                a = b;
                b = temp;
            }
        }
    }
}
