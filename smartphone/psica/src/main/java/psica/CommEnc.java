package psica;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.io.UnsupportedEncodingException;
import java.math.BigInteger;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.util.ArrayList;

import org.bouncycastle.crypto.DataLengthException;
import org.bouncycastle.crypto.InvalidCipherTextException;

import com.github.mgunlogson.cuckoofilter4j.CuckooFilter;
import com.github.mgunlogson.cuckoofilter4j.Utils.Algorithm;
import com.google.common.hash.Funnels;

public class CommEnc implements Serializable {
	private static final BigInteger ZERO = BigInteger.valueOf(0);
	private static final BigInteger ONE = BigInteger.valueOf(1);
	private static final BigInteger TWO = BigInteger.valueOf(2);

	public static BigInteger encrypt_BigInteger(BigInteger num, Keys key) {
		return num.modPow(key.getA(), key.getP());
	}

	public static BigInteger decrypt_BigInteger(BigInteger num, Keys key) {
		return num.modPow(key.getAInv(), key.getP());
	}

	public static BigInteger encrypt_Data(String data, Keys key) {// �����ݽ��м���
		byte[] block;
		BigInteger cipher = null;
		try {
			block = data.getBytes("utf-8");
			// System.out.println("����ת��utf-8:" + Arrays.toString(block));
			BigInteger res = new BigInteger(1, block);// �����ı��utf-8���룬�ٱ��BigInteger
			if (res.compareTo(key.getP()) >= 0) {
				throw new DataLengthException("input too large for Pohlig-Hellman cipher.");
			}
			cipher = res.modPow(key.getA(), key.getP());// ��ɼ���
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}
		return cipher;
	}

	public static BigInteger decrypt_Data(BigInteger cipher, Keys key) {// �����ݽ��м���
		return cipher.modPow(key.getAInv(), key.getP());
	}

	// OK
	public static Keys generate_Key(boolean server) {
		Keys key = null;
		try {
			BigInteger p = Params.pub_random;
			key = new Keys(p);
			generate_Keys(key, server);
			// System.out.println("CommEnc::generate_Key - key: " + key.getP().toString());
			// System.out.println("CommEnc::generate_Key - key:" + key.getA().toString());
			// System.out.println("CommEnc::generate_Key - key:" + key.getAInv().toString());
		} catch (NoSuchAlgorithmException e) {
			e.printStackTrace();
		}
		try {
			FileOutputStream fos;
			if (server)
				fos = new FileOutputStream("./server/keys/key.dat");
			else // If client
				fos = new FileOutputStream("./client/keys/key.dat");
			ObjectOutputStream oos = new ObjectOutputStream(fos);
			oos.writeObject(key);
			oos.close();

			if (server) {
				fos = new FileOutputStream("./server/keys/P.dat");
				oos = new ObjectOutputStream(fos);
				oos.writeObject(key.getP());
				oos.close();
			}

		} catch (IOException e) {
			e.printStackTrace();
		}
		// System.out.println("CommEnc::generate_Key (server) - generated key: " + key.toString());
		return key;
	}

	public static int check_Intersection_Cardinality(BigInteger[] elements, CuckooFilter<byte[]> cf) {
		int count = 0;
		long len = elements.length;
		for (int i = 0; i < len; ++i) {
			byte[] block = elements[i].toByteArray();
			if (cf.mightContain(block)) {
				count++;
			}
		}
		return count;
	}


	public static CuckooFilter<byte[]> put_in_CF(BigInteger[] elements, double fpp, int size) {
		long len = elements.length;
		CuckooFilter<byte[]> filter = new CuckooFilter.Builder<>(Funnels.byteArrayFunnel(), size)
				.withFalsePositiveRate(fpp).withHashAlgorithm(Algorithm.sha256).build();
		for (int i = 0; i < len; ++i) {
			byte[] block = elements[i].toByteArray();
			filter.put(block);
		}
		System.out.println("Filter has " + filter.getCount() + " items");
		// ������
		System.out.println("Filter is " + String.format("%.0f%%", filter.getLoadFactor() * 100) + " loaded");
		return filter;
	}

	public static BigInteger quick_Pow(BigInteger m, BigInteger a, BigInteger p) {
		BigInteger result = ONE;
		BigInteger k = a;
		while (!k.equals(ZERO)) {
			if (k.testBit(0)) {
				result = result.multiply(m).remainder(p);
			}
			m = (m.multiply(m)).remainder(p);
			k = k.shiftRight(1);
		}
		return result;
	}

	// OK
	public static void generate_Keys(Keys key, boolean server) throws NoSuchAlgorithmException {
		int len = key.getP().bitLength();
		SecureRandom ran = SecureRandom.getInstance("SHA1PRNG");
		key.setA(new BigInteger(len - 1, ran));
		if (!key.getA().testBit(0)) {
			key.setA(key.getA().add(BigInteger.ONE));
		}
		BigInteger p_minus = key.getP().subtract(ONE);
		key.setA_Inv(key.getA().modInverse(p_minus));// a^(-1) mod (p-1)

		FileOutputStream fos;
		try {
			if (server)

				fos = new FileOutputStream("./server/keys/key.dat");
			else // If client
				fos = new FileOutputStream("./client/keys/key.dat");
			ObjectOutputStream oos = new ObjectOutputStream(fos);
			oos.writeObject(key);
			oos.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
		// System.out.println("CommEnc::generate_Keys (client) - generated key: " + key.toString());
	}

	// OK
	public static Keys restore_Key(boolean server) {
		Keys key = null;
		try {
			FileInputStream fis;
			if (server)
				fis = new FileInputStream("./server/keys/key.dat");
			else
				fis = new FileInputStream("./client/keys/key.dat");
			ObjectInputStream ois = new ObjectInputStream(fis);
			key = (Keys) ois.readObject();
			ois.close();

		} catch (IOException e) {
			e.printStackTrace();
		} catch (ClassNotFoundException e) {
			e.printStackTrace();
		}

		// System.out.println("CommEnc::restore_Key - key: " + key.toString());
		return key;
	}

	public static BigInteger generate_P(int length) throws NoSuchAlgorithmException {
		// ���ɳ���Ϊlength������p��������q=(p-1)/2Ҳ������
		SecureRandom ran = SecureRandom.getInstance("SHA1PRNG");
		// BigInteger p = new BigInteger(length, ran); //���������0~2^(length)-1�������
		BigInteger p = new BigInteger(length, 1, ran);// �Խϴ����������������p
		// BigInteger pBigInteger = new BigInteger(length, ran);
		BigInteger q;
		for (;;) {// ��һ��������p
			if (p.isProbablePrime(40) == true) {// �ҵ�����q
				System.out.println("��������p0��" + p + "����Ϊ:" + p.bitLength());
				q = p.subtract(ONE);
				q = q.divide(TWO);
				System.out.println("q=(p-1)/2��" + q);
				if (q.isProbablePrime(40) == true)// �ж�q=(p-1)/2�Ƿ�Ϊ�������ǵĻ������ҵ�������p
					break;
			}
			p = new BigInteger(1024, 1, ran);
		}
		return p;
	}

	public static void writeTxt(String txtPath, String content) {// д�ļ���׷��ģʽ
		try {
			FileWriter writer;
			writer = new FileWriter(txtPath, true);
			writer.write(content);
			writer.close();
		} catch (IOException e) {

			e.printStackTrace();
		}
	}

	public static BigInteger[] toArrayByFileReader(String name) {// ���ļ��ж�ȡ����
		ArrayList<String> arrayList = new ArrayList<>();
		try {
			FileReader fr;
			fr = new FileReader(name);
			BufferedReader bf = new BufferedReader(fr);
			String str;
			// ���ж�ȡ�ַ���
			while ((str = bf.readLine()) != null) {
				arrayList.add(str);
			}
			bf.close();
			fr.close();
		} catch (IOException e) {

			e.printStackTrace();
		}
		// ��ArrayList�д洢���ַ������д���
		int length = arrayList.size();
		BigInteger[] array = new BigInteger[length];
		for (int i = 0; i < length; i++) {
			String s = arrayList.get(i);
			array[i] = new BigInteger(s);// ʹ�ù��캯�����Խ��ַ�����ʼ��ΪBigInteger
		}
		return array;
	}

	public static ArrayList<String> toStrArrayByFileReader(String name) {// ���ļ��ж�ȡԪ��
		ArrayList<String> arrayList = new ArrayList<>();
		try {
			FileReader fr;
			fr = new FileReader(name);
			BufferedReader bf = new BufferedReader(fr);
			String str;
			// ���ж�ȡ�ַ���
			while ((str = bf.readLine()) != null) {
				arrayList.add(str);
			}
			bf.close();
			fr.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return arrayList;
	}
}
