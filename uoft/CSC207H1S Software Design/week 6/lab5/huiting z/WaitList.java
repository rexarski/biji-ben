package w5lab;

import java.util.Collection;
import java.util.concurrent.ConcurrentLinkedQueue;

/**
 * A representation on a waiting list. Works in a first-come first-serve basis.
 */
public class WaitList<E> implements IWaitList<E>{

    /** The content of this WaitList. */
    protected ConcurrentLinkedQueue<E> content;

    /**
     * Creates a new empty WaitList.
     */
    public WaitList() {
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
     *           empty
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
     *              WaitList
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
        return this.content.toString();
    }
}
