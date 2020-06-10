package floatingpoint;

public class Adding {

    public static void main(String[] args) {
        
        double x = 0.1;
        double sum = x + x + x;
        System.out.println(sum == 0.3);
        System.out.println(sum);

        double bigger = 1.0;
        double s = 1.0e-6;  // 0.000001
        double sum1 = s + s + s + s + s + s + s + s + s + s + bigger;  
        double sum2 = bigger + s + s + s + s + s + s + s + s + s + s;
        System.out.println(sum1 == sum2);
        System.out.println(sum1);
        System.out.println(sum2);
    }
}