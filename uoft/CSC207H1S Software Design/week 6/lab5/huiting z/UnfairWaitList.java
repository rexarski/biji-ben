package w5lab;

public class UnfairWaitList<E> extends WaitList<E> {

	public UnfairWaitList(){
		super();
	}
	
	public void remove(E element){
		if (! super.isEmpty()) {
			for (E item: this.content){
				if (element == item) {
					this.content.remove(element);
					break;
				}
			}
		}
	}
	
	public void moveToBack(E element){
		remove(element);
		super.add(element);
	}
}
