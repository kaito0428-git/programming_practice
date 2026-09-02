public class math {
    public static void main(String[] arges){
        int a = 20;
        int b = a + 5;
        System.out.println(a);
        System.out.println(b);

        System.out.println("私の好きな記号は二重引用符(\")です。");

        a = 100;
        a++;
        System.out.println(a);

        float f = 3;
        double d = f;
        System.out.println(f);
        System.out.println(d);
        
        int age = (int)3.2;
        System.out.println(age);

        d= 8.5 / 2;
        long l = 5 + 2L;
        System.out.println(d);
        System.out.println(l);

        String msg = "私の年齢は" + 23;
        System.out.println(msg);

        String name = "すがわら";
        String message;
        message = name + "さん、こんにちは";
        System.out.println(message);

        String name1 = "すがわら";
        System.out.print("私の名前は");
        System.out.print(name1);
        System.out.println("です。");

        a = 5;
        b = 3;
        int m = Math.max(a,b);
        System.out.println("比較実験：" + a + "と" + b + "の大きい方は" + m + "です。");

        String ageText = "31";
        int n = Integer.parseInt(ageText);
        System.out.println("あなたは来年、" + (n + 1) + "歳になりますね。");

        int r = new java.util.Random().nextInt(90);
        System.out.println("あなたはたぶん、" + r + "歳ですね？");

        System.out.println("あなたの名前を入力してください。");
        String userName = new java.util.Scanner(System.in).nextLine();
        System.out.println("あなたの年齢を入力してください。");
        int userAge = new java.util.Scanner(System.in).nextInt();
        System.out.println("ようこそ、" + userAge + "歳の" + userName + "さん。");
    
    
    
    }
}
