import java.util.Scanner;

public class Main2 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        String[] tasks = new String[3];
        int[] status = new int[3];

        for (int i = 0; i < 3; i++) {
            System.out.println((i + 1) + "件目のタスク名を入力してください");
            tasks[i] = scanner.nextLine();

            System.out.println("完了していますか?(1:はい, 0:いいえ)");
            status[i] = scanner.nextInt();
            scanner.nextLine(); // 改行の読み残し対策
        }

        System.out.println("----- タスク一覧 -----");
        for (int i = 0; i < 3; i++) {
            if (status[i] == 1) {
                System.out.println("[完了] " + tasks[i]);
            } else {
                System.out.println("[未完了] " + tasks[i]);
            }
        }
    }
}