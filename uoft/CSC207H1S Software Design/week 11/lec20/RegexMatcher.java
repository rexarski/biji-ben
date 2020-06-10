package regex;

import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * A demo of Java regular expressions.
 * @author campbell
 */
public class RegexMatcher {

    /**
     * Prompts the user to enter a regular expression and a string, 
     * and reports whether that regular expression matches the string.
     * The user types quit to exit.
     */
    public static void doMatching() {
        Scanner sc = new Scanner(System.in);
        String re, line;
        System.out.print("Regular expression: ");
        re = sc.nextLine();
        while (!re.equals("quit")) {
            System.out.print("String: ");
            line = sc.next();
            System.out.println(Pattern.matches(re, line));
            System.out.print("Regular expression: ");
            re = sc.nextLine();
        }
        sc.close();
    }

    public static void main(String[] args) {

        // You can do an individual match in one easy line:
        System.out.println(Pattern.matches("a*b", "aaaaab"));
        
        // Notice that it automatically anchors
        // That is, it is equivalent to ^a*b$
        System.out.println(Pattern.matches("a*b", "baaaaab"));
        System.out.println();

        // If you never reuse the same pattern, this is fine.
        // As in this method:
        doMatching();

        // But if you plan to reuse a pattern, it's more efficient
        // to let Java build the matching infrastructure once and 
        // reuse it for each match against that pattern.
        Pattern p = Pattern.compile("CSC[0-9][0-9][0-9]H1(F|S)");
        Matcher m = p.matcher("CSC207H1S");
        System.out.println("Does CSC207H1S match " + p + " ?");
        System.out.println(m.matches());

        // Here we reuse that (under the hood) infrastructure.
        System.out.println("Does CSC199H1Y match " + p + " ?");
        System.out.println(p.matcher("CSC199H1Y").matches() + "\n");

        // The matcher has other methods that let you find out 
        // which substrings matched with which "capturing group"
        // of the pattern.  Each capturing groups begins with a 
        // left bracket.  The capturing groups are numbered from 0,
        // and group 0 is the whole pattern.

        // Here I add more brackets to the pattern.
        // This will allow us to capture the group of characters
        // that is the course number.
        // (Exercise: rewrite the pattern to be more concise)
        p = Pattern.compile("CSC([0-9][0-9][0-9])H1(F|S)");
        m = p.matcher("CSC207H1S");
        System.out.println(m.matches());
        System.out.println(m.group(0));  // the entire string
        System.out.println(m.group(1));  // the first group: 207
        System.out.println(m.group(2));  // the second group: S

        // Using a backreference.
        p = Pattern.compile("(\\d\\d\\d)ABC\\1");
        m = p.matcher("123ABC123");      
        System.out.println(m.matches());     
        m = p.matcher("123ABC456");      
        System.out.println(m.matches());
    }
}