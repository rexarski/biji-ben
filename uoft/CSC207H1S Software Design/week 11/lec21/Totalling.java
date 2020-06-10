package floatingpoint;

public class Totalling {

    public static double sum1(double startingAmount, double amount,
            int howMany) {

        double answer = startingAmount;
        for (int i = 0; i < howMany; i++) {
            answer += amount;
        }
        
        return answer;
    }

    public static double sum2(double startingAmount, double amount,
            int howMany) {

        double answer = 0;
        for (int i = 0; i < howMany; i++) {
            answer += amount;
        }
        answer += startingAmount;
        
        return answer;
    }

    public static void main(String[] args) {
        double v1 = sum1(1, 10e-17, 10);
        double v2 = sum2(1, 10e-17, 10);
        System.out.println(v1 + " vs " + v2);
    }
}