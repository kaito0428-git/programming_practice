public class JavaDrill {
    public static void main(String[] args) {
        int a = -5;
        System.out.println("a=" +a);
        if(a > 0){
            System.out.println("aは正の数です。");
        } else {
            System.out.println("aは正の数ではありません。");
        }


        int num = 1;
        if(num == 1){
            System.out.println("one");
        }else if(num == 2){
            System.out.println("two");
        }else if(num == 3){
            System.out.println("three");
        }else{
            System.out.println("不適切な値です。");
        }


        int dice = (int)(Math.random()*7)+1;
        System.out.println("さいころの目:"+dice);
        if(1 <= dice && dice <= 6){
           if(dice == 2 || dice == 4 || dice == 6){
                 System.out.println("丁(チョウ)です。");
            }else{
                 System.out.println("半(ハン)です。");
            }
        }else{
                System.out.println("範囲外の数値です。"); 
              }


        int naum = 5;
        switch(naum){
        case 1:
            System.out.println("one");
            break;
        case 2:
            System.out.println("two");
            break;
        case 3:
            System.out.println("three");
            break;
        default:
            System.out.println("不適切な値です。");
        }


//練習問題//
        int s = (int)(Math.random()*10);
        System.out.println(s);
        if(s >=5){
            System.out.println("5以上です。");
        }else{
            System.out.println("5以下です。");
        }


        int q = (int)(Math.random()*10);
        System.out.println(q);
        if(q == 1){
            System.out.println("1です。");
        }else{
            System.out.println("1ではありません。");
        }


        int y = (int)(Math.random()*100);
        System.out.println(y);
        if(y < 50){
            System.out.println("50未満です。");
        }else{
            System.out.println("50以上です。");
        };


        int u = (int)(Math.random()*100);
        System.out.println(u);
            if(u <= 10 || u >= 90){
            System.out.println("10以下か90以上の値です。");
            }else{
                System.out.println("10以下か90以上の値ではありません。");
            }


        int b = (int)(Math.random()*100);
        System.out.println(b);
            if(b >= 20 && b < 80){
                System.out.println("20以上80未満です。");
            }else{
                System.out.println("20以上80未満ではありません。");
            }


        int m = (int)(Math.random()*6)+1;
        System.out.println("数値 : " + m);
        if(m >= 3){
            System.out.println("3以上です。");
        }


        int p = (int)(Math.random()*10);
            System.out.println(p);
                if(p < 5){
                System.out.println("5未満です");
            }else{
                System.out.println("5以上です。");
            }


        int w = (int)(Math.random()*10);
        System.out.println(w);
            if(w == 1){
                System.out.println("1です。");
            }else{
                System.out.println("1ではありません。");
            }


        int j = (int)(Math.random()*100);
        System.out.println(j);
            if(j < 50){
                System.out.println("50未満です。");
            }else{
                System.out.println("50以上です。");
            }


        int v = (int)(Math.random()*100);
        System.out.println(v);
            if(10 <= v || 90 > v){
            System.out.println("10以下か90以上の値です。");
        }else{
            System.out.println("10より大きく90未満です。");
        }

//https://java.sevendays-study.com/problem3.html Q3-11






    }

}
