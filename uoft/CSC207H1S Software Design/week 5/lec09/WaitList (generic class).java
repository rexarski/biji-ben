package university;

import java.util.Collection;
import java.util.Queue;
import java.util.concurrent.ConcurrentLinkedQueue;

/*
 * WaitList is a generic class.
 * We say that WaitList is a parameterized type.
 * Typically we use T (stands for type), but for collections,
 * we use E (stands for element), as in the Java API.
 */
public class WaitList<E> {
    
    /*
     * Check out documentation at:
     * http://docs.oracle.com/javase/7/docs/api/java/util/concurrent/ConcurrentLinkedQueue.html
     */
    /** The waitlist contents. */
    private Queue<E> content; 


    /**
     * Creates a new empty WaitList.
     */
    public WaitList() {
        
        // One approach for initializing the instance variable:
        // this.content = new ConcurrentLinkedQueue<E>();
        
        // Alternatively, using the "box" operator, the type is inferred from
        // the type of the variable declared above:
        this.content = new ConcurrentLinkedQueue<>(); 

    }   

    /**
     * Creates a new WaitList containing elements from the given Collection.
     * @param c elements from this Collection are added to the new WaitList
     */
    public WaitList(Collection<E> c) {
        this.content = new ConcurrentLinkedQueue<>(c);
    }   

    /**
     * Adds the specified element to this WaitList.
     * @param element the new element to be added to this WaitList
     */
    public void add(E element) { 
        this.content.add(element);  
    }

    /**
     * Removes and returns the next element from this WaitList. The elements are
     * removed in first-in-first-out order. Returns null if this WaitList is
     * empty.
     * @return the next element in this WaitList, or null if this WaitList is
     *         empty
     */
    public E remove() { 
        return this.content.poll();
    }

    /**
     * Returns true if and only if this WaitList contains element.
     * @param element the element to test for membership in this WaitList
     * @return true if this WaitList contains element and false, otherwise
     */
    public boolean contains(E element) {
        return this.content.contains(element);
    }

    /**
     * Returns true if and only if this WaitList contains all elements in the given
     * collection.
     * @param c the Collection of elements to test for membership in this
     *          WaitList
     * @return true if this WaitList contains all elements in the given
     *         collection and false otherwise
     */
    public boolean containsAll(Collection<E> c){
        return this.content.containsAll(c);
    }

    /**
     * Returns true if and only if this WaitList has no elements.
     * @return true if and only if this WaitList has no elements
     */
    public boolean isEmpty() {
        return this.content.isEmpty();
    }

    @Override
    public String toString() {
        return "WaitList:" + this.content;
    }
}
