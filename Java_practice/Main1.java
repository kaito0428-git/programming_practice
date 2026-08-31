import java.util.Scanner;

public class Main1 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("種類を入力してください(1:収入, 2:支出)");
        int type = scanner.nextInt();

        System.out.println("金額を入力してください");
        int amount = scanner.nextInt();

        int balance = 0;

        if (type == 1) {
            balance = balance + amount;
            System.out.println("収入を記録しました。残高: " + balance + "円");
        } else {
            balance = balance - amount;
            System.out.println("支出を記録しました。残高: " + balance + "円");
        }
    }
}