package edu.ucsb.cs.ws;

public class Order {
	
	private String orderId;
	private String name;
	private String additions;
	private double price;
	
	public String getOrderId() {
		return orderId;
	}
	
	public void setOrderId(String orderId) {
		this.orderId = orderId;
	}
	
	public String getName() {
		return name;
	}
	
	public void setName(String name) {
		this.name = name;
	}
	
	public String getAdditions() {
		return additions;
	}
	
	public void setAdditions(String additions) {
		this.additions = additions;		
	}
	
	public double getPrice() {
		return price;
	}
	
	public void setPrice(double price) {
		this.price = price;
	}
	
}
