package psica;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.OutputStream;
import java.io.UnsupportedEncodingException;
import java.math.BigInteger;
import java.net.ServerSocket;
import java.net.Socket;

//import javax.xml.bind.DataBindingException;


public class Network {
	protected Socket sock;
	protected ServerSocket serverSock;
	public InputStream is;
	public OutputStream os;
	public DataInputStream d_in;
	public DataOutputStream d_out;
	
	public Network() {
	}
	
	public Network(InputStream is, OutputStream os, Socket sock) {//���캯��,��Network����������ͺͽ��չ���
		this.is = is;
		this.os = os;
		this.sock = sock;
	}
	
	public void sendFile(String filePath) {//�����������������Ϣֱ�ӷ����ļ�
		File file = new File(filePath);
        try {
        	d_out = new DataOutputStream(sock.getOutputStream());
        	//�Ȼ�ȡ�ļ����Ȳ����͸��Է�
        	long length = file.length();
        	//System.out.println("Send file length: " + length);
        	d_out.writeLong(length);
            FileInputStream f_in = new FileInputStream(file);
            byte[] buffer = new byte[1024];
            int read = 0;
            while ((read = (f_in.read(buffer))) > 0) {
                d_out.write(buffer, 0, read);
            }
            d_out.flush();
            f_in.close();
            //d_out.write("\n");
            //d_out.close();//û�����д�����Bug��ʹ���ļ��޷�����
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
	
	//�ڶ��̵߳�����£�����ֺ�Ķ���ļ�������͸�����ˣ�����threads���ڷ�����Щ�ļ�
	public void sendFiles(int threads) {//�����������������Ϣֱ�ӷ����ļ�
		File file;
		for(int i = 1; i <= threads; ++i) {
			file = new File("client/" + i + "out");
			try {
	        	d_out = new DataOutputStream(sock.getOutputStream());
	            FileInputStream f_in = new FileInputStream(file);
	            int all = 0;
	            byte[] buffer = new byte[1024];
	            int read = 0;
	            while ((read = (f_in.read(buffer))) > 0) {
	                d_out.write(buffer, 0, read);
	                all += read;
	            }
	            System.out.println("Send file length: "+all);
	            d_out.flush();
	            f_in.close();
	        } catch (IOException e) {
	            e.printStackTrace();
	        }
		}
		//File file = new File(filePath);    
    }
	
	public void receiveFile(String filePath) {//�����ļ�
		try {
			long startTime; //��ȡ��ʼʱ��
			long endTime;
			byte[] buf = new byte[1024];
			int len = 0;
			//System.out.println("��ʼ�����ļ���");
			startTime = System.currentTimeMillis();
			d_in = new DataInputStream(sock.getInputStream());
			//�Ȼ�ȡ�ļ����ȣ��ٿ�ʼ��������
			long length = d_in.readLong();//�ļ��ܳ���
			//System.out.println("�ļ�����Ϊ:" + length);
			long group = length % 1024 == 0 ? length / 1024 : length / 1024 + 1;//�ļ�����
			long cnt = 0;//������
			DataOutputStream dosOutputStream = new DataOutputStream(new FileOutputStream(filePath));
			while((len = d_in.read(buf)) != -1) {//ʹ������������ʽ�����һ�� 
				dosOutputStream.write(buf, 0, len);
				cnt++;
				if(cnt >= group) break;
			}
			dosOutputStream.flush();
			endTime = System.currentTimeMillis();
			System.out.println("��������ʱ�䣺 "+(endTime-startTime)/1000 + "s" +
					 (endTime-startTime) % 1000 +"ms");
			System.out.println("�ļ����ս���!");
			//d_in.close();
			dosOutputStream.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	//sendBytes:����byte����
	public void sendBytes(byte[] data) {
		try {
			ObjectOutputStream out = new ObjectOutputStream(sock.getOutputStream());
            out.writeObject(data);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	//sendBI:����BigInteger��������з�װ
	public void sendBI(BigInteger bi) {
		System.out.println("����P:"+bi.toString());
		sendBytes(Utils.bigIntegerToBytes(bi));
	}
	
	//sendStr:����String������������з�װ
	public void sendStr(String str) {//����String���ͱ�����Ҫת��utf-8�����ٷ���
		try {
			byte[] block = str.getBytes("utf-8");
			sendBytes(block);
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}
	}
	
	//readBytes:��ȡ����
	public byte[] readBytes(int len) {//�Ը������ȵ����ݽ��ж�ȡ
		byte[] temp = new byte[len];
		try {
			int remain = len;
			int readBytes;//ʵ�ʶ�ȡ��byte����
			readBytes = is.read(temp, len - remain, remain);//len-remain������Ƕ����ݵ���ʼ��
			System.out.println(readBytes);
			if (readBytes != -1) {
				remain -= readBytes;
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
		return temp;
	}
	
	
	public void readBytes(byte[] temp) {
		try {
			int remain = temp.length;
			while (0 < remain) {
				int readBytes;
				readBytes = is.read(temp, temp.length - remain, remain);
				if (readBytes != -1) {
					remain -= readBytes;
				}  
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public byte[] readBytes() {
		byte[] bytes = null;
        try {
            ObjectInputStream in = new ObjectInputStream(sock.getInputStream());
            bytes = (byte[])in.readObject();
            System.out.println("Receive bytes[] length: "+bytes.length);
        } catch (IOException e) {
            e.printStackTrace();
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }
        return bytes;
	}
	
	public void flush() {//ˢ�������
		try {
			os.flush();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public void disconnect() {//�Ͽ�����
		try {
			if(sock != null) {
				sock.close();
			}
			if(serverSock != null){
				serverSock.close();
			}
			if(d_in != null) {
				d_in.close();
			}
			if(d_out != null) {
				d_out.close();
			}
			if(is != null) {
				is.close();
			}
			if(os != null) {
				os.close();
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
