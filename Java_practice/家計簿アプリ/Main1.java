package 家計簿アプリ;

import java.util.Scanner;

public class Main1 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int balance = 0;

        while (true) {
            System.out.println("種類を入力してください(1:収入, 2:支出, 0:終了)");
            int type = scanner.nextInt();

            if (type == 0) {
                break;
            }

            System.out.println("金額を入力してください");
            int amount = scanner.nextInt();

            if (type == 1) {
                balance = balance + amount;
                System.out.println("収入を記録しました。残高: " + balance + "円");
            } else if (type == 2) {
                balance = balance - amount;
                System.out.println("支出を記録しました。残高: " + balance + "円");
            } else {
                System.out.println("不正な入力です。1か2を入力してください。");
            }
        }

        System.out.println("終了します。最終残高: " + balance + "円");
        scanner.close();
    }
}