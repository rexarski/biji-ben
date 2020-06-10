package floatingpoint;

public class Examine {

    public static void main(String[] args) {
        float x;
        
        // Compute the single precision IEEE floating-point approximation 
        // to 4/5. 
        // You need to say "f" to get single precision (i.e., float).
        // constants rather than double precision (i.e., double) constants.
        x = 4.0f / 5.0f;
        
        // print the value of x to 7 decimal places
        System.out.println(String.format("x = %.7f  \n", x));  

        // to 16 decimal places
        System.out.println(String.format("x = %.16f \n", x));     
    }
}