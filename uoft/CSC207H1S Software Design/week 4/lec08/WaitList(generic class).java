package university;

import java.util.Queue;
import java.util.concurrent.ConcurrentLinkedQueue;

/*
 * WaitList is a generic class.
 * We say that WaitList is a parameterized type
 * Typically we use T (stands for type), but for collections,
 * we use E (stands for element), as in the Java API.
 */
public class WaitList<E> {
    
    /** The waitlist contents. */
    private Queue<E> content;
    
    public WaitList() {
        content = new ConcurrentLinkedQueue<E>();
    }
    
    public void add(E element) {
        content.add(element);
    }

    // More next lecture.

}
