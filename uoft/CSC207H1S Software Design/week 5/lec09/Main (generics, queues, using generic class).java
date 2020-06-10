package university;

import java.util.ArrayList;
import java.util.List;
import java.util.Queue;
import java.util.concurrent.ConcurrentLinkedQueue;

public class Main {

    public static void main(String[] args) {

        //demoWhyGenerics();
        demoQueues();
    }

    public static void demoWhyGenerics() {

        // == Why use generics? ==
        
        // == Using non-generic code == 
        // If we don't specify the type of items in the ArrayList,
        // type Object is used.
        // Methods like get() would return type Object.
        // This is for example purposes, but don't declare this way!
        // Notice that this code results in compiler warnings.
        List firstList = new ArrayList();

        // Let's imagine that we want an ArrayList of String, but
        // we declared it as shown above. Nothing stops us from
        // adding non-Strings to the list.
        firstList.add("Hello");
        firstList.add(new Integer(3));
        
        // To call a String method, we would need to typecast:
        ((String) firstList.get(0)).charAt(0);

        // But the item at index 1 is not a String!
        // This error won't be detected until runtime and this approach
        // is considered unsafe.  Use generics!
        //((String) firstList.get(1)).charAt(0);    // Runtime exception

        // == Using generics ==
        // If we had specified that the List should hold items of type
        // String, then the second call on add would have caught the
        // bug and resulted in a compile error.
        List<String> secondList = new ArrayList<>();
        secondList.add("Hello");
        //secondList.add(new Integer(3));  // Compile error

        secondList.get(0).charAt(2);
    }

    public static void demoQueues() {

        // Example of Java's Queues
        Queue<String> lineUp = new  ConcurrentLinkedQueue<>();
        lineUp.add("first in line");
        lineUp.add("second in line");

        System.out.println(lineUp);
        lineUp.poll();

        System.out.println(lineUp);
    }
    
    public static void demoWaitList() {
        
        WaitList<Student> waiting = new WaitList<>();
        Student jane = new Student(new String[] {"Jane", "Doe"}, "01012001", "F", "1234");
        waiting.add(jane);
        System.out.println(waiting);
    }
}
