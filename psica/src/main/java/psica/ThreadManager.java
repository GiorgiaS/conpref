package psica;

import java.util.concurrent.ExecutionException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import lombok.extern.slf4j.Slf4j;

@Slf4j(topic = "c.Test2")
public class ThreadManager {
	protected static Logger logger = LoggerFactory.getLogger(ThreadManager.class);
	public static void main(String[] args) throws InterruptedException, ExecutionException {
		Thread t1 = new Thread() {
			@Override
			public void run() {
				method1(20);
			}
		};
		t1.setName("t1");
		t1.start();
		method1(10);
	}
	private static void method1(int x) {
		Object mObject = method2();
		System.out.println(mObject);
	}
	
	private static Object method2() {
		Object nObject = new Object();
		return nObject;
	}
}
//Runnable runnable = new Runnable() {//�����������߳����߳�
//@Override
//public void run() {
//	// Ҫִ�е�����
//	logger.debug("running");
//}
//};
////�����̶߳���
//Thread t1 = new Thread(runnable, "t1");
////�����߳�
//t1.start();
//
////�����������
//Runnable task2 = () -> {logger.debug("hello");};
////����1 ��������� ����2 ���߳����֣��Ƽ�
//Thread t2 = new Thread(task2, "t2");
//t2.start();
//
//Runnable r = () -> {
//	// Ҫִ�е�����
//	logger.debug("running");
//	logger.debug("running2");
//	logger.debug("running3");
//};
//Thread t3 = new Thread(r, "t3");
//t3.start();
//
////�������
//FutureTask<Integer> task = new FutureTask<Integer>(new Callable<Integer>() {
//@Override
//public Integer call() throws Exception {
//	logger.debug("running...");
//	Thread.sleep(2000);
//	return 100;
//}
//});
//
////����Threadִ��
//Thread thread = new Thread(task,"t4");
//thread.start();
//logger.debug("{}", task.get());//"{}"��ʾռλ��

//new Thread(() -> {
//while(true) {
//	logger.debug("running");
//}
//}, "t1").start();
//
//new Thread(() -> { 
//while(true) {
//	logger.debug("running");
//}
//}, "t2").start();
