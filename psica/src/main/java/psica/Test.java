
package psica;

import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.LineNumberReader;
import java.io.UnsupportedEncodingException;
import java.math.BigInteger;
import java.net.URLDecoder;
import java.net.URLEncoder;
import java.util.HashSet;
import java.util.Set;

import com.google.common.primitives.Bytes;

public class Test {

//	public static void main(String[] args) {
//		// TODO Auto-generated method stub
//		Keys key1 = new Keys(new BigInteger("1234"), new BigInteger("5678"), new BigInteger("91011"));
//		Keys key2 = new Keys(new BigInteger("1234"), new BigInteger("5678"), new BigInteger("91011"));
//		Set<Keys> keysSet = new HashSet<Keys>();
//		keysSet.add(key1);
//		keysSet.add(key2);
//		System.out.println(key1.equals(key2));
//		System.out.println(key1.hashCode() == key2.hashCode());
//        System.out.println(keysSet);
//	}
//	 public static void main(String[] args) {
//		 long startTime = System.currentTimeMillis(); //��ȡ��ʼʱ��
// 		 long endTime;
//	    	try {
//	    		File file = new File("client/clientDB3.txt");
//	    		if(file.exists()){
//	    			long fileLength = file.length();
//	    			LineNumberReader lineNumberReader = new LineNumberReader(new FileReader(file));
//	    			lineNumberReader.skip(fileLength);
//	                int lines = lineNumberReader.getLineNumber();
//	                System.out.println("Total number of lines : " + lines);
//	                endTime = System.currentTimeMillis();
//	                System.out.println("�Ȼ�ȡfile.length()��skip�ķ�ʱ�䣺" + (endTime-startTime)/1000 + "s" +
//	       				 (endTime-startTime) % 1000 +"ms");
//	                lineNumberReader.close();
//	    		}else {
//	    			System.out.println("File does not exists!");
//	    		}
//	    		
//	    		startTime = System.currentTimeMillis();
//	    		File file2 = new File("client/clientDB3.txt");
//	    		if(file2.exists()){
//	    			//long fileLength = file2.length();
//	    			LineNumberReader lineNumberReader = new LineNumberReader(new FileReader(file2));
//	    			lineNumberReader.skip(Long.MAX_VALUE);
//	                int lines = lineNumberReader.getLineNumber();
//	                System.out.println("Total number of lines : " + lines);
//	                endTime = System.currentTimeMillis();
//	                System.out.println("ֱ��skip Long.MAX_VALUE�ķ�ʱ�䣺" + (endTime-startTime)/1000 + "s" +
//	       				 (endTime-startTime) % 1000 +"ms");
//	                lineNumberReader.close();
//	    		}else {
//	    			System.out.println("File does not exists!");
//	    		}
//	    		
//	    	}catch(IOException e) {
//	    		e.printStackTrace();
//	    	}
//	    }
	 
	 public static void main(String[] args) {
		 String s1 = "�����к�����ѧԺ·37��123123�����к�����ѧԺ·37�ű����к�����ѧԺ·37��";
		 try {
			byte[] bytes = s1.getBytes("utf-8");
			String s3 = new String(bytes);
			System.out.println("����:" + s1);
			System.out.println("����תΪbyte����,��byte�����ʼ��String:" + s3);
			String decryptData2 = new String(s3.getBytes(), "utf-8");
			System.out.println("��Stringͨ��utf-8����ת������:" + decryptData2);
			
			
			String s2 = bytes.toString();
			String decryptData1 = new String(s2.getBytes(), "utf-8");
			System.out.println("����תΪutf-8��byte��������toString()תΪString:" + s2);
			System.out.println("byte����תΪString:" + decryptData1);

		} catch (UnsupportedEncodingException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	 }

}
