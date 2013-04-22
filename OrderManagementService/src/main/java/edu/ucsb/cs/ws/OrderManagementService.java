package edu.ucsb.cs.ws;

import java.util.Map;
import java.util.Random;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

public class OrderManagementService {
	
	private static final Map<String,Double> priceList = new ConcurrentHashMap<String,Double>();	
	private static final Map<String,Order> orders = new ConcurrentHashMap<String, Order>();
	
	public Order addOrder(Order order) {
		String orderId = UUID.randomUUID().toString();
		order.setOrderId(orderId);
		order.setPrice(getPrice(order));
		orders.put(orderId, order);
		return order;
	}
	
	public Order getOrder(String orderId) {
		return orders.get(orderId);		
	}
	
	public Order[] getAllOrders() {
		return orders.values().toArray(new Order[orders.size()]);
	}
	
	public Order updateOrder(Order order) {
		if (orders.containsKey(order.getOrderId())) {
			order.setPrice(getPrice(order));
			orders.put(order.getOrderId(), order);
			return order;
		} else {
			return null;
		}
	}
	
	public Order deleteOrder(String orderId) {
		return orders.remove(orderId);		
	}
	
	private double getPrice(Order order) {
		double price = getPriceForItem(order.getName(), false);
		String additions = order.getAdditions();
		if (additions != null) {
			for (String addition : additions.split(",")) {
				price += getPriceForItem(addition.trim(), true);
			}
		}
		return price;
	}
	
	private double getPriceForItem(String name, boolean addition) {
		if (name == null || "".equals(name)) {
			return 0.0;
		}
		Random rand = new Random();
		int limit = addition ? 2 : 6;
		if (!priceList.containsKey(name)) {
			priceList.put(name, (rand.nextInt(limit) + 1) - 0.01);
		}
		return priceList.get(name);
	}

}