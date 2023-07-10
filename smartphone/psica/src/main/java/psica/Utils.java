package psica;

import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.LineNumberReader;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.UnsupportedEncodingException;
import java.math.BigInteger;
import java.util.concurrent.CountDownLatch;

import com.github.mgunlogson.cuckoofilter4j.CuckooFilter;
import com.github.mgunlogson.cuckoofilter4j.Utils.Algorithm;
import com.google.common.hash.Funnels;

import orestes.bloomfilter.BloomFilter;
import orestes.bloomfilter.FilterBuilder;
import orestes.bloomfilter.HashProvider.HashMethod;

public class Utils {
	private static BufferedOutputStream out = null;

	public static BigInteger bytesToBigInteger(byte[] in, int inOff, int inLen) {
		byte[] block;

		if (inOff != 0 || inLen != in.length) {
			block = new byte[inLen];
			System.arraycopy(in, inOff, block, 0, inLen);
		} else {
			block = in;
		}

		BigInteger res = new BigInteger(1, block);

		return res;
	}

	public static byte[] bigIntegerToBytes(BigInteger input) {
		byte[] output = input.toByteArray();
		if (output[0] == 0) {
			byte[] tmp = new byte[output.length - 1];
			System.arraycopy(output, 1, tmp, 0, tmp.length);
			return tmp;
		}
		return output;
	}

	public static String bytesToHexString(byte[] src) {
		StringBuilder stringBuilder = new StringBuilder("");
		if (src == null || src.length <= 0) {
			return null;
		}
		for (int i = 0; i < src.length; i++) {
			int v = src[i] & 0xFF;
			String hv = Integer.toHexString(v);
			if (hv.length() < 2) {
				stringBuilder.append(0);
			}
			stringBuilder.append(hv);
		}
		return stringBuilder.toString();
	}

	public static byte[] hexStringToBytes(String hexString) {
		if (hexString == null || hexString.equals("")) {
			return null;
		}
		hexString = hexString.toUpperCase();
		int length = hexString.length() / 2;
		char[] hexChars = hexString.toCharArray();
		byte[] d = new byte[length];
		for (int i = 0; i < length; i++) {
			int pos = i * 2;
			d[i] = (byte) (charToByte(hexChars[pos]) << 4 | charToByte(hexChars[pos + 1]));
		}
		return d;
	}

	private static byte charToByte(char c) {
		return (byte) "0123456789ABCDEF".indexOf(c);
	}

	public static void writeLineToFile(File file, byte[] line, int begin, int end) {
		if (begin == 0) {
			try {
				out = new BufferedOutputStream(new FileOutputStream(file));
			} catch (FileNotFoundException e) {
				e.printStackTrace();
			}
		}
		try {
			out.write(line);
		} catch (IOException e) {
			e.printStackTrace();
		}
		if (begin == end - 1) {
			try {
				out.flush();
				out.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}

	// OK
	public static int getLineNumber(File file) throws IOException {
		if (file.exists()) {
			try {
				FileReader fileReader = new FileReader(file);
				LineNumberReader lineNumberReader = new LineNumberReader(fileReader);
				lineNumberReader.skip(Long.MAX_VALUE);
				int lines = lineNumberReader.getLineNumber();
				fileReader.close();
				lineNumberReader.close();
				return lines;
			} catch (FileNotFoundException e) {
				e.printStackTrace();
			}
		}
		return 0;
	}


	// OK
	public static void FilterWriter(CuckooFilter<byte[]> filter, String filePath) {
		File file = new File(filePath);
		ObjectOutputStream out = null;
		try {
			out = new ObjectOutputStream(new FileOutputStream(file));
			out.writeObject(filter);
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			try {
				if (out != null)
					out.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}

	// OK
	public static void FilterWriter(BloomFilter<String> filter, String filePath) {
		ObjectOutputStream out = null;
		try {
			File file = new File(filePath);
			out = new ObjectOutputStream(new FileOutputStream(file));
			out.writeObject(filter);
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			try {
				if (out != null)
					out.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}

	// OK
	@SuppressWarnings("unchecked")
	public static CuckooFilter<byte[]> cuckooReader(String filePath) {
		File file = new File(filePath);
		FileInputStream fileIn = null;
		ObjectInputStream in = null;
		CuckooFilter<byte[]> filter = null;
		try {
			fileIn = new FileInputStream(file);
			in = new ObjectInputStream(fileIn);
			filter = (CuckooFilter<byte[]>) in.readObject();
		} catch (IOException e) {
			e.printStackTrace();
		} catch (ClassNotFoundException e) {
			e.printStackTrace();
		} finally {
			try {
				if (in != null)
					in.close();
				if (fileIn != null)
					fileIn.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
		// System.out.println("Utils::CuckooFilter - filter: " + filter.toString());
		return filter;
	}

	// OK
	@SuppressWarnings("unchecked")
	public static BloomFilter<String> BloomReader(String filePath) {
		File file = new File(filePath);
		FileInputStream fileIn = null;
		ObjectInputStream in = null;
		BloomFilter<String> filter = null;
		try {
			fileIn = new FileInputStream(file);
			in = new ObjectInputStream(fileIn);
			filter = (BloomFilter<String>) in.readObject();
		} catch (IOException e) {
			e.printStackTrace();
		} catch (ClassNotFoundException e) {
			e.printStackTrace();
		} finally {
			try {
				if (in != null)
					in.close();
				if (fileIn != null)
					fileIn.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
		// System.out.println("Utils::BloomFilter - filter: " + filter.toString());
		return filter;
	}

	public static void encrypt_and_Write(String from_path, String to_path, Keys key) {
		try {
			FileReader fileReader;
			File file = new File(from_path);
			fileReader = new FileReader(file);
			BufferedReader bufferedReader = new BufferedReader(fileReader);
			String line = "";
			FileWriter cipher_writer = new FileWriter(to_path, true);
			// long startTime = System.currentTimeMillis();
			int i = 0;
			while ((line = bufferedReader.readLine()) != null) {

				cipher_writer.write(
						CommEnc.encrypt_BigInteger(new BigInteger(line), key).toString().getBytes("utf-8") + "\r\n");
				if (i++ % 5000 == 0) {
					// System.out.println("��" + i + "�������Ѿ�������ϲ�����" + to_path + "��");
					// long endTime = System.currentTimeMillis();
					// System.out.println("����" + i + "��Ԫ�صĳ�������ʱ�䣺 " + (endTime - startTime) / 1000 + "s" +
					// 		(endTime - startTime) % 1000 + "ms");
				}
			}
			cipher_writer.close();
			bufferedReader.close();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	//OK
	/**
	 * 
	 * @param pathString
	 * @param stage      
	 * @param file       
	 * @param len        
	 * @param threads    
	 */
	public static void split_File(String pathString, String stage, File file, int len, int threads) {
		try {
			String contentLine = "";
			// System.out.println("Utils::split_file - file length: " + len);
			int NumPerThread = len / threads;
			int cnt = 0;
			FileReader fileReader = new FileReader(file);
			BufferedReader bReader = new BufferedReader(fileReader);
			FileWriter fileWriter;

			for (int i = 1; i <= threads; ++i) {
				fileWriter = new FileWriter(pathString + stage + i);
				BufferedWriter bWriter = new BufferedWriter(fileWriter);
				while ((contentLine = bReader.readLine()) != null) {
					bWriter.write(contentLine);
					bWriter.newLine();
					cnt++;
					if (cnt % NumPerThread == 0 && i < threads) {
						break;
					}
				}
				bWriter.close();
			}
			bReader.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	// OK
	public static void join_Files(String pathString, String toPath, int threads) {
		FileWriter fileWriter;
		String temp_line = null;
		try {
			fileWriter = new FileWriter(toPath);
			FileReader fileReader = null;
			BufferedReader bReader = null;
			BufferedWriter bWriter = new BufferedWriter(fileWriter);
			for (int i = 1; i <= threads; ++i) {
				fileReader = new FileReader(pathString + i + "out");
				bReader = new BufferedReader(fileReader);
				// String temp_line = null;
				while ((temp_line = bReader.readLine()) != null) {
					bWriter.write(temp_line + "\r\n");
				}
			}
			bReader.close();
			bWriter.close();
			fileReader.close();
			fileWriter.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	// /**
	//  * ���̹߳�ϣ�ټ���Ԫ�صķ���
	//  * 
	//  * @param role
	//  * @param from_path
	//  * @param to_path
	//  * @param enc       Object���ͣ����ݴ���Ķ������ʹ��Pohlig-Hellman����ECC
	//  * @param threads
	//  * @throws FileNotFoundException
	//  */
	// // �����̣߳���from_path�ж�ȡ���ģ���ֳɶ�����ļ������̷ֱ߳�����ļ���key���ܣ������ܺ�����Ĳ���д��to_path
	// public static void hash_prefix_enc_mThreads(Integer role, String from_path, String to_path, Object enc, int threads)
	// 		throws FileNotFoundException {
	// 	if (threads > 0 && (threads & (threads - 1)) != 0) {// �ж�threads�Ƿ�Ϊ2���ݴ�
	// 		System.out.println("�߳�������Ϊ2���ݴΣ�");
	// 		return;
	// 	}
	// 	// ��ȡ�������ļ��ĸ�Ŀ¼
	// 	String pathString; // ��������or�ͻ��˵ĸ�Ŀ¼
	// 	if (role == 0) {// 0����server
	// 		pathString = "server/";
	// 	} else {
	// 		pathString = "client/";
	// 	}
	// 	// 1.�ȶ�ȡ�ļ�����
	// 	// long startTime = System.currentTimeMillis();
	// 	int len;
	// 	File file = new File(from_path);
	// 	try {
	// 		len = getLineNumber(file);
	// 		if (len < threads) {// ���⼫�����
	// 			threads = 1;
	// 		}
	// 		split_File(pathString, Params.StageEnum.Prefix_filter.toString(), file, len, threads);// ��Ŀ���ļ���ֳ�threads��
	// 	} catch (IOException e1) {
	// 		e1.printStackTrace();
	// 	}
	// 	// 2.��ʼ���̷߳��ʲ�ͬ�ļ����м���,�������ܽ��д��ͬһ��toPath�ļ���
	// 	final CountDownLatch cdl = new CountDownLatch(threads);// ����Ϊ�̸߳���
	// 	for (int j = 1; j <= threads; ++j) {
	// 		int new_j = j;
	// 		new Thread(() -> {
	// 			try {
	// 				FileReader temp_reader = new FileReader(
	// 						pathString + Params.StageEnum.Prefix_filter.toString() + new_j);
	// 				BufferedReader temp_bReader = new BufferedReader(temp_reader);
	// 				FileWriter temp_writer = new FileWriter(
	// 						pathString + Params.StageEnum.Prefix_filter.toString() + new_j + "out");
	// 				BufferedWriter temp_bWriter = new BufferedWriter(temp_writer);
	// 				String temp_line = null;
	// 				String hash_prefix = null;
	// 				String hash_String = null;
	// 				String s = Params.pub_random.toString();

	// 				if (enc.getClass().equals(Keys.class)) {// �����Keys����, �����Pohlig-Hellman����
	// 					Keys key = (Keys) enc;
	// 					while ((temp_line = temp_bReader.readLine()) != null) {// ���ж�ȡԪ�ز�����
	// 						// �����ϣǰ׺h(x)[0:w]
	// 						// System.out.println("prefix_len:" + Params.prefix_len);
	// 						// System.out.println("ǰ׺���ֽڳ���:" + PreReduce.Hash_and_Get_Bits(temp_line,
	// 						// Params.prefix_len).length);
	// 						hash_prefix = Utils
	// 								.bytesToHexString(PreReduce.Hash_and_Get_Bits(temp_line, Params.prefix_len));
	// 						// System.out.println("hash_prefix:" + hash_prefix);
	// 						// �õ���ϣֵh(s,x)�ټ���, ������ϣǰ׺��������ɶ�Ԫ��(h(x)[0:w],h(s,x))д���ļ�
	// 						hash_String = Utils.bytesToHexString(PreReduce.Hash_and_Get_Bits(s + temp_line, 256));
	// 						temp_bWriter.write(hash_prefix + ","
	// 								+ CommEnc.encrypt_BigInteger(new BigInteger(hash_String, 16), key).toString()
	// 								+ "\r\n");
	// 					}
	// 				} else if (enc.getClass().equals(EccEnc.class)) {// �������Բ�������ͣ������ECC����
	// 					org.bouncycastle.math.ec.ECPoint element;
	// 					EccEnc eccEnc = (EccEnc) enc;
	// 					while ((temp_line = temp_bReader.readLine()) != null) {// ���ж�ȡԪ�ز�����
	// 						// �õ���ϣֵh(s,x)�ټ���,д���ļ�
	// 						// System.out.println("prefix_len:" + Params.prefix_len);
	// 						// System.out.println("ǰ׺���ֽڳ���:" + PreReduce.Hash_and_Get_Bits(temp_line,
	// 						// Params.prefix_len).length);
	// 						hash_prefix = Utils
	// 								.bytesToHexString(PreReduce.Hash_and_Get_Bits(temp_line, Params.prefix_len));
	// 						// System.out.println("hash_prefix:" + hash_prefix);
	// 						hash_String = Utils.bytesToHexString(PreReduce.Hash_and_Get_Bits(s + temp_line, 256));
	// 						element = eccEnc.BigIntegerToPoint(new BigInteger(hash_String, 16));
	// 						temp_bWriter.write(hash_prefix + ","
	// 								+ Utils.bytesToHexString(eccEnc.encryptPoint(element).getEncoded(true)) + "\r\n");
	// 					}
	// 				} else {
	// 					System.out.println("����ļ��ܶ������");
	// 					temp_bWriter.close();
	// 					temp_bReader.close();
	// 					return;
	// 				}
	// 				temp_bWriter.close();
	// 				temp_bReader.close();
	// 				cdl.countDown();
	// 			} catch (FileNotFoundException e) {
	// 				e.printStackTrace();
	// 			} catch (IOException e) {
	// 				e.printStackTrace();
	// 			}
	// 		}, "t" + j).start();
	// 	}
	// 	// �߳����������countDownLatch����
	// 	try {
	// 		cdl.await();// ��Ҫ�����쳣���������߳���Ϊ0ʱ����Ż��������
	// 	} catch (InterruptedException e) {
	// 		e.printStackTrace();
	// 	}
	// 	// long endTime = System.currentTimeMillis();
	// 	// System.out.println("����Ԫ�غ�ʱ:" + (endTime - startTime) / 1000 + "s" +
	// 	// (endTime - startTime) % 1000 + "ms");
	// 	// 3.���ļ��ܽ����󣬽����в����������ļ��ϳ�һ��
	// 	join_Files(pathString + Params.StageEnum.Prefix_filter.toString(), to_path, threads);
	// }


	// OK
	/**
	 * This is executed
	 * 
	 * @param role
	 * @param from_path
	 * @param to_path
	 * @param threads
	 * @throws FileNotFoundException
	 */
	public static void hash_prefix_enc_mThreads(Integer role, String from_path, String to_path, BloomFilter<String> bf,
			int threads) throws FileNotFoundException {
		// System.out.println("Utils::hash_prefix_enc_mThreads - no enc");
		if (threads > 0 && (threads & (threads - 1)) != 0) {
			System.out.println("Utils::hash_prefix_enc_mThreads - threads error");
			return;
		}
		String pathString;
		if (role == 0) {
			pathString = "server/";
		} else {
			pathString = "client/";
		}

		// 1.
		int len;
		File file = new File(from_path);
		try {
			len = getLineNumber(file);
			if (len < threads) {
				threads = 1;
			}
			split_File(pathString, Params.StageEnum.Prefix_filter.toString(), file, len, threads);
		} catch (IOException e1) {
			e1.printStackTrace();
		}

		// 2.
		final CountDownLatch cdl = new CountDownLatch(threads);
		for (int j = 1; j <= threads; ++j) {
			int new_j = j;
			new Thread(() -> {
				try {
					FileReader temp_reader = new FileReader(
							pathString + Params.StageEnum.Prefix_filter.toString() + new_j);
					BufferedReader temp_bReader = new BufferedReader(temp_reader);
					FileWriter temp_writer = new FileWriter(
							pathString + Params.StageEnum.Prefix_filter.toString() + new_j + "out");
					BufferedWriter temp_bWriter = new BufferedWriter(temp_writer);
					String temp_line = null;
					String hash_prefix = null;

					while ((temp_line = temp_bReader.readLine()) != null) {
						hash_prefix = Utils.bytesToHexString(PreReduce.Hash_and_Get_Bits(temp_line, Params.prefix_len));
						bf.add(hash_prefix);
						temp_bWriter.write(hash_prefix + "\r\n");
					}
					temp_bWriter.close();
					temp_bReader.close();
				} catch (FileNotFoundException e) {
					e.printStackTrace();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}, "t" + j).start();
		}
		// long endTime = System.currentTimeMillis();
		if (role == 0) {
			Utils.FilterWriter(bf, pathString + "server_prefix_bloom");
		} else {
			Utils.FilterWriter(bf, pathString + "client_prefix_bloom");
		}

		// 3.
		join_Files(pathString + Params.StageEnum.Prefix_filter.toString(), to_path, threads);
	}

	//

	// /**
	//  * С����һ������ǰ׺ֵ��BF���ϣ����̲߳���
	//  * 
	//  * @param role
	//  * @param from_path
	//  * @param to_path
	//  * @param threads
	//  */
	// public static BloomFilter<String> get_prefix_BF_mThreads(Integer role, String from_path, int threads) {
	// 	File file = new File(from_path);// �洢�ͻ������ĵ��ļ�
	// 	String pathString; // ��������or�ͻ��˵ĸ�Ŀ¼
	// 	if (role == 0) {
	// 		pathString = "server/";
	// 	} else {
	// 		pathString = "client/";
	// 	}
	// 	try {
	// 		int len = getLineNumber(file);// ��ȡ�ļ��������Ե�֪Ԫ�ظ���
	// 		if (len < threads) {// ���⼫�����
	// 			threads = 1;
	// 		}
	// 		// ��ʼ����¡������
	// 		BloomFilter<String> filter = new FilterBuilder()
	// 				.expectedElements(len)
	// 				.falsePositiveProbability(0.000000001)
	// 				.hashFunction(HashMethod.Murmur3)
	// 				.buildBloomFilter();

	// 		// long startTime = System.currentTimeMillis(); // ��ȡ��ʼʱ��
	// 		long endTime;
	// 		int i;
	// 		// ���̲߳�������BF
	// 		// 1. ���Ĳ�ֳ��߳��������ļ�
	// 		split_File(pathString, Params.StageEnum.Prefix_bloom.toString(), file, len, threads);
	// 		// 2. �Բ�ֺ�������ļ����в���������ǰ׺,ͬʱ����BF��
	// 		final CountDownLatch cdl = new CountDownLatch(threads);// ����Ϊ�̸߳���
	// 		for (i = 1; i <= threads; ++i) {
	// 			int new_j = i;
	// 			new Thread(() -> {
	// 				try {
	// 					FileReader temp_reader = new FileReader(
	// 							pathString + Params.StageEnum.Prefix_bloom.toString() + new_j);
	// 					BufferedReader temp_bReader = new BufferedReader(temp_reader);
	// 					String temp_line = null;
	// 					while ((temp_line = temp_bReader.readLine()) != null) {// ���ж�ȡԪ�ز�����
	// 						// ��Ԫ�����ϣǰ׺,����BF,�洢���ǹ�ϣֵ��ʮ�������ַ���
	// 						filter.add(
	// 								Utils.bytesToHexString(PreReduce.Hash_and_Get_Bits(temp_line, Params.prefix_len)));
	// 					}
	// 					temp_bReader.close();
	// 					cdl.countDown();
	// 				} catch (FileNotFoundException e) {
	// 					e.printStackTrace();
	// 				} catch (IOException e) {
	// 					e.printStackTrace();
	// 				}
	// 			}, "t" + i).start();
	// 		}
	// 		// �߳����������countDownLatch����
	// 		try {
	// 			cdl.await();// ��Ҫ�����쳣���������߳���Ϊ0ʱ����Ż��������
	// 		} catch (InterruptedException e) {
	// 			e.printStackTrace();
	// 		}
	// 		endTime = System.currentTimeMillis();
	// 		// System.out.println("����Ԫ��ǰ׺������BF��ʱ:" + (endTime - startTime) / 1000 +
	// 		// "s" + (endTime - startTime) % 1000 + "ms");

	// 		return filter;
	// 	} catch (IOException e) {
	// 		e.printStackTrace();
	// 	}
	// 	return null;
	// }

	// /**
	//  * С����һ�������������ɺõĲ�¡���������յ��Ķ�Ԫ�鼯�Ͻ��й���, ����������
	//  * 
	//  * @param bf
	//  * @param from_path
	//  * @param to_path
	//  */
	// // Ҳ���Զ��߳�, ����ʵû��Ҫ, �첻�˶���
	// public static void filter_Pair_Set(BloomFilter<String> bf, String from_path, String to_path) {
	// 	// long startTime = System.currentTimeMillis();
	// 	try {
	// 		File file = new File(from_path);
	// 		FileReader fileReader = new FileReader(file);
	// 		BufferedReader temp_bReader = new BufferedReader(fileReader);
	// 		FileWriter temp_writer = new FileWriter(to_path);
	// 		BufferedWriter temp_bWriter = new BufferedWriter(temp_writer);
	// 		String temp_line = null;

	// 		while ((temp_line = temp_bReader.readLine()) != null) {// ���ж�ȡԪ�ز�����
	// 			// �����ŷָ�, ȡǰ�벿��ǰ׺���в�ѯ, �������, �ͽ���벿��д�����ļ�
	// 			String[] pair = temp_line.split(",");
	// 			if (bf.contains(pair[0])) {
	// 				temp_bWriter.write(pair[1] + "\r\n");
	// 			}
	// 		}
	// 		temp_bReader.close();
	// 		temp_bWriter.close();
	// 		// long endTime = System.currentTimeMillis();
	// 		// System.out.println(
	// 		// 		"���˴󼯺�Ԫ�غ�ʱ:" + (endTime - startTime) / 1000 + "s" + (endTime - startTime) % 1000 + "ms");
	// 	} catch (IOException e) {
	// 		System.out.println("�ļ���д�쳣��");
	// 		e.printStackTrace();
	// 	}
	// }

	// OK
	/**
	 * 
	 * @param bf
	 * @param from_path
	 * @param to_path
	 * @param enc
	 * @param threads
	 */
	public static void filter_Set_mThreads(Integer role, BloomFilter<String> bf, String from_path, String to_path,
			Object enc, int threads) {
		if (threads > 0 && (threads & (threads - 1)) != 0) {
			System.out.println("Utils::filter_Set_mThreads error");
			return;
		}
		String pathString;
		if (role == 0) {
			pathString = "server/";
		} else {
			pathString = "client/";
		}

		// 1.
		int len;
		File file = new File(from_path);
		try {
			len = getLineNumber(file);
			if (len < threads) {
				threads = 1;
			}
			split_File(pathString, Params.StageEnum.Prefix_filter.toString(), file, len, threads);
		} catch (IOException e1) {
			e1.printStackTrace();
		}

		// 2.
		final CountDownLatch cdl = new CountDownLatch(threads);
		for (int j = 1; j <= threads; ++j) {
			int new_j = j;
			new Thread(() -> {
				try {
					FileReader temp_reader = new FileReader(
							pathString + Params.StageEnum.Prefix_filter.toString() + new_j);
					BufferedReader temp_bReader = new BufferedReader(temp_reader);
					FileWriter temp_writer = new FileWriter(
							pathString + Params.StageEnum.Prefix_filter.toString() + new_j + "out");
					BufferedWriter temp_bWriter = new BufferedWriter(temp_writer);
					String temp_line = null;
					String hash_prefix = null;
					String hash_String = null;
					String s = Params.pub_random.toString();

					//  System.out.println("Utils::filter_Set_mThreads - enc class: " + enc.getClass());
					if (enc.getClass().equals(Keys.class)) {
						Keys key = (Keys) enc;
						while ((temp_line = temp_bReader.readLine()) != null) {
							hash_prefix = Utils
									.bytesToHexString(PreReduce.Hash_and_Get_Bits(temp_line, Params.prefix_len));
							if (bf.contains(hash_prefix)) {
								hash_String = Utils.bytesToHexString(PreReduce.Hash_and_Get_Bits(s + temp_line, 256));
								temp_bWriter.write(
										CommEnc.encrypt_BigInteger(new BigInteger(hash_String, 16), key).toString()
												+ "\r\n");
							}
						}
					} else if (enc.getClass().equals(EccEnc.class)) {
						org.bouncycastle.math.ec.ECPoint element;
						EccEnc eccEnc = (EccEnc) enc;
						while ((temp_line = temp_bReader.readLine()) != null) {
							hash_prefix = Utils
									.bytesToHexString(PreReduce.Hash_and_Get_Bits(temp_line, Params.prefix_len));
								// System.out.println("Utils::filter_Set_mThreads - hash_prefix: " + hash_prefix);
								if (bf.contains(hash_prefix)) {
								// System.out.println("Utils::filter_Set_mThreads - bf contains: " + hash_prefix);
								hash_String = Utils.bytesToHexString(PreReduce.Hash_and_Get_Bits(s + temp_line, 256));
								element = eccEnc.BigIntegerToPoint(new BigInteger(hash_String, 16));
								temp_bWriter.write(
										Utils.bytesToHexString(eccEnc.encryptPoint(element).getEncoded(true)) + "\r\n");
							}
						}
					} else {
						System.out.println("Utils::filter_Set_mThreads - no key specified");
						temp_bWriter.close();
						temp_bReader.close();
						return;
					}

					temp_bWriter.close();
					temp_bReader.close();
					cdl.countDown();
				} catch (FileNotFoundException e) {
					e.printStackTrace();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}, "t" + j).start();
		}
		try {
			cdl.await();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		join_Files(pathString + Params.StageEnum.Prefix_filter.toString(), to_path, threads);
	}

	// OK
	public static void enc_dec_and_Write_mThreads(Integer role, Boolean isEnc, String from_path, String to_path,
			Keys key, int threads) throws FileNotFoundException {
		if (threads > 0 && (threads & (threads - 1)) != 0) {
			System.out.println("�߳�������Ϊ2���ݴΣ�");
			return;
		}
		
		String pathString; 
		if (role == 0) {
			pathString = "server/";
		} else {
			pathString = "client/";
		}
		// 1.
		// long startTime = System.currentTimeMillis();
		int len;
		File file = new File(from_path);
		try {
			len = getLineNumber(file);
			if (len < threads) {
				threads = 1;
			}
			split_File(pathString, Params.StageEnum.Encrypt.toString(), file, len, threads);
		} catch (IOException e1) {
			e1.printStackTrace();
		}
		// 2.
		final CountDownLatch cdl = new CountDownLatch(threads);
		for (int j = 1; j <= threads; ++j) {
			int new_j = j;
			new Thread(() -> {
				try {
					FileReader temp_reader = new FileReader(pathString + Params.StageEnum.Encrypt.toString() + new_j);
					BufferedReader temp_bReader = new BufferedReader(temp_reader);
					FileWriter temp_writer = new FileWriter(
							pathString + Params.StageEnum.Encrypt.toString() + new_j + "out");
					BufferedWriter temp_bWriter = new BufferedWriter(temp_writer);
					String temp_line = null;
					if (isEnc) {

						// String hash_String = null;
						// String s = Params.pub_random.toString();

						while ((temp_line = temp_bReader.readLine()) != null) {
							// hash_String = Utils.bytesToHexString(PreReduce.Hash_and_Get_Bits(s +
							// temp_line, 256));
							// temp_bWriter.write(CommEnc.encrypt_BigInteger(new BigInteger(hash_String,
							// 16), key).toString() + "\r\n");
							temp_bWriter.write(
									CommEnc.encrypt_BigInteger(new BigInteger(temp_line), key).toString() + "\r\n");
						}
					} else {
						while ((temp_line = temp_bReader.readLine()) != null) {
							temp_bWriter.write(
									CommEnc.decrypt_BigInteger(new BigInteger(temp_line), key).toString() + "\r\n");
						}
					}
					temp_bWriter.close();
					temp_bReader.close();
					cdl.countDown();
				} catch (FileNotFoundException e) {
					e.printStackTrace();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}, "t" + j).start();
		}
	
		try {
			cdl.await();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		// long endTime = System.currentTimeMillis();
		// System.out.println("����Ԫ�غ�ʱ:" + (endTime - startTime) / 1000 + "s" +
		// (endTime - startTime) % 1000 + "ms");
		// 3.
		join_Files(pathString + Params.StageEnum.Encrypt.toString(), to_path, threads);
	}


	// OK
	/**
	 * 
	 * @param ecc
	 * @param role
	 * @param isEnc
	 * @param from_path
	 * @param to_path
	 * @param threads
	 * @throws FileNotFoundException
	 */
	public static void ECC_enc_dec_and_Write_mThreads(EccEnc ecc, Integer role, Boolean isEnc, String from_path,
			String to_path, int threads) throws FileNotFoundException {
		File file = new File(from_path);
		String pathString;
		if (threads > 0 && (threads & (threads - 1)) != 0) {
			System.out.println("Utils::ECC_enc_dec_and_Write_mThreads - thread error");
			return;
		}
		if (role == 0) {
			pathString = "server/";
		} else {
			pathString = "client/";
		}

		// 1.
		// long startTime = System.currentTimeMillis();
		try {
			int len = getLineNumber(file);
			if (len < threads) {
				threads = 1;
			}
			split_File(pathString, Params.StageEnum.Encrypt.toString(), file, len, threads);
		} catch (IOException e1) {
			e1.printStackTrace();
		}

		// 2.��ʼ���̷߳��ʲ�ͬ�ļ����м���,�������ܽ��д��ͬһ��toPath�ļ���
		final CountDownLatch cdl = new CountDownLatch(threads);// ����Ϊ�̸߳���
		for (int j = 1; j <= threads; ++j) {
			int new_j = j;
			new Thread(() -> {
				try {
					// System.out.println("Utils::ECC_enc_dec_and_Write_mThreads - path to read: " +
					// pathString + Params.StageEnum.Encrypt.toString() + new_j);
					FileReader temp_reader = new FileReader(pathString + Params.StageEnum.Encrypt.toString() + new_j);
					BufferedReader temp_bReader = new BufferedReader(temp_reader);
					// System.out.println("Utils::ECC_enc_dec_and_Write_mThreads - path to write: "
					// + pathString + Params.StageEnum.Encrypt.toString() + new_j + "out");
					FileWriter temp_writer = new FileWriter(
							pathString + Params.StageEnum.Encrypt.toString() + new_j + "out");
					BufferedWriter temp_bWriter = new BufferedWriter(temp_writer);
					String temp_line = null;
					String hash_String = null;
					String s = Params.pub_random.toString();
					org.bouncycastle.math.ec.ECPoint element;
					if (isEnc) {// here
						while ((temp_line = temp_bReader.readLine()) != null) {// ���ж�ȡԪ�ز�����
							// ���ܺ������д��outj�ļ���
							// System.out.println("Utils::ECC_enc_dec_and_Write_mThreads - temp_line value:
							// " + temp_line);
							hash_String = Utils.bytesToHexString(PreReduce.Hash_and_Get_Bits(s + temp_line, 256));
							// System.out.println("Utils::ECC_enc_dec_and_Write_mThreads - hash_string
							// value: " + hash_String);
							// System.out.println("Utils::ECC_enc_dec_and_Write_mThreads - hash_string
							// BigInteger value: " + new BigInteger(hash_String, 16));
							BigInteger pre_element = new BigInteger(hash_String, 16);
							element = ecc.BigIntegerToPoint(pre_element);
							temp_bWriter
									.write(Utils.bytesToHexString(ecc.encryptPoint(element).getEncoded(true)) + "\r\n");
						}
					} else {// isEncΪfalse�������ж�ȡ������
						while ((temp_line = temp_bReader.readLine()) != null) {// ���ж�ȡԪ�ز�����
							// ���ܺ������д��outj�ļ���
							element = ecc.BigIntegerToPoint(new BigInteger(temp_line));
							temp_bWriter
									.write(Utils.bytesToHexString(ecc.decryptPoint(element).getEncoded(true)) + "\r\n");
						}
					}
					temp_bWriter.close();
					temp_bReader.close();
					cdl.countDown();
				} catch (FileNotFoundException e) {
					e.printStackTrace();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}, "t" + j).start();
		}
		// �߳����������countDownLatch����
		try {
			cdl.await();// ��Ҫ�����쳣���������߳���Ϊ0ʱ����Ż��������
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		// long endTime = System.currentTimeMillis();
		// System.out.println("����Ԫ�غ�ʱ:" + (endTime - startTime) / 1000 + "s" +
		// (endTime - startTime) % 1000 + "ms");
		// 3.���ļ��ܽ����󣬽����в����������ļ��ϳ�һ��
		join_Files(pathString + Params.StageEnum.Encrypt.toString(), to_path, threads);
	}

	// OK
	/**
	 * 
	 * @param ecc
	 * @param role
	 * @param isEnc
	 * @param from_path
	 * @param to_path
	 * @param threads
	 * @throws FileNotFoundException
	 */
	public static void ECC_sec_enc_and_Write_mThreads(EccEnc ecc, Integer role, Boolean isEnc, String from_path,
			String to_path, int threads) throws FileNotFoundException {
		if (threads > 0 && (threads & (threads - 1)) != 0) {
			System.out.println("Utils::ECC_sec_enc_and_Write_mThreads - error");
			return;
		}
		// System.out.println("Utils::ECC_sec_enc_and_Write_mThreads - begins");

		String pathString; 
		if (role == 0) {
			pathString = "server/";
		} else {
			pathString = "client/";
		}
		int len;
		try {
			File file = new File(from_path);
			len = getLineNumber(file);
			if (len < threads) {
				threads = 1;
			}
			split_File(pathString, Params.StageEnum.Encrypt.toString(), file, len, threads);
		} catch (IOException e1) {
			e1.printStackTrace();
		}

		// 2.
		final CountDownLatch cdl = new CountDownLatch(threads);
		for (int j = 1; j <= threads; ++j) {
			int new_j = j;
			new Thread(() -> {
				try {
					FileReader temp_reader = new FileReader(pathString + Params.StageEnum.Encrypt.toString() + new_j);
					BufferedReader temp_bReader = new BufferedReader(temp_reader);
					FileWriter temp_writer = new FileWriter(
							pathString + Params.StageEnum.Encrypt.toString() + new_j + "out");
					BufferedWriter temp_bWriter = new BufferedWriter(temp_writer);
					String temp_line = null;
					org.bouncycastle.math.ec.ECPoint element;
					if (isEnc) {
						while ((temp_line = temp_bReader.readLine()) != null) {
							// System.out.println("Utils::ECC_sec_enc_and_Write_mThreads - isEnc");
							element = ecc.bytesToECPoint(Utils.hexStringToBytes(temp_line));
							element = ecc.encryptPoint(element);
							temp_bWriter.write(Utils.bytesToHexString(element.getEncoded(true)) + "\r\n");
						}
					} else {
						while ((temp_line = temp_bReader.readLine()) != null) {
							element = ecc.bytesToECPoint(Utils.hexStringToBytes(temp_line));
							element = ecc.decryptPoint(element);
							temp_bWriter.write(Utils.bytesToHexString(element.getEncoded(true)) + "\r\n");
						}
					}
					// System.out.println("Utils::ECC_sec_enc_and_Write_mThreads - finish
					// writing/reading");
					temp_bWriter.close();
					temp_bReader.close();
					cdl.countDown();
				} catch (FileNotFoundException e) {
					e.printStackTrace();
				} catch (ArithmeticException e) {
					System.err.println("Utils::ECC_sec_enc_and_Write_mThreads - AithmeticException " + pathString
							+ Params.StageEnum.Encrypt.toString());
					e.printStackTrace();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}, "t" + j).start();
		}

		try {
			cdl.await();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		// long endTime = System.currentTimeMillis();
		// System.out.println("Utils::ECC_sec_enc_and_Write_mThreads - time threads
		// creation: " + (endTime - startTime) / 1000 + "s" + (endTime - startTime) %
		// 1000 + "ms");
		join_Files(pathString + Params.StageEnum.Encrypt.toString(), to_path, threads);
	}

	// OK
	public static BloomFilter<String> encrypt_and_BloomWriter(Integer role, String from_path, Keys key, int threads) {
		File file = new File(from_path);
		String pathString;
		if (role == 0) {
			pathString = "server/";
		} else {
			pathString = "client/";
		}
		try {
			int len = getLineNumber(file);
			if (len < threads) {
				threads = 1;
			}

			BloomFilter<String> filter = new FilterBuilder()
					.expectedElements(len)
					.falsePositiveProbability(0.000000001)
					.hashFunction(HashMethod.Murmur3)
					.buildBloomFilter();

			// long startTime = System.currentTimeMillis();
			long endTime;
			int i;
			
			// 1.
			split_File(pathString, Params.StageEnum.Enc_bloom.toString(), file, len, threads);
			// 2.
			final CountDownLatch cdl = new CountDownLatch(threads);
			for (i = 1; i <= threads; ++i) {
				int new_j = i;
				new Thread(() -> {
					try {
						FileReader temp_reader = new FileReader(
								pathString + Params.StageEnum.Enc_bloom.toString() + new_j);
						BufferedReader temp_bReader = new BufferedReader(temp_reader);
						String temp_line = null;
						// String hash_String = null;
						// String s = Params.pub_random.toString();
						while ((temp_line = temp_bReader.readLine()) != null) {
							// hash_String = Utils.bytesToHexString(PreReduce.Hash_and_Get_Bits(s +
							// temp_line, 256));
							// filter.add(CommEnc.encrypt_BigInteger(new BigInteger(hash_String, 16),
							// key).toString());
							filter.add(CommEnc.encrypt_BigInteger(new BigInteger(temp_line), key).toString());
						}
						temp_bReader.close();
						cdl.countDown();
					} catch (FileNotFoundException e) {
						e.printStackTrace();
					} catch (IOException e) {
						e.printStackTrace();
					}
				}, "t" + i).start();
			}
			
			try {
				cdl.await();
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			// endTime = System.currentTimeMillis();
			// System.out.println("����Ԫ�ز�����BF��ʱ:" + (endTime - startTime) / 1000 + "s"
			// + (endTime - startTime) % 1000 + "ms");

			return filter;
		} catch (IOException e) {
			e.printStackTrace();
		}
		return null;
	}

	// OK
	/**
	 * 
	 * @param role
	 * @param from_path
	 * @param enc
	 * @param threads
	 * @return
	 */
	public static BloomFilter<String> encrypt_and_BloomWriter(Integer role, String from_path, EccEnc enc, int threads) {
		File file = new File(from_path);
		String pathString; 
		if (role == 0) {
			pathString = "server/";
		} else {
			pathString = "client/";
		}
		try {
			int len = getLineNumber(file);
			if (len < threads) {
				threads = 1;
			}
	
			BloomFilter<String> filter = new FilterBuilder()
					.expectedElements(len)
					.falsePositiveProbability(0.000000001)
					.hashFunction(HashMethod.Murmur3)
					.buildBloomFilter();

			// long startTime = System.currentTimeMillis(); 
			// 1. 
			split_File(pathString, Params.StageEnum.Enc_bloom.toString(), file, len, threads);

			// 2.
			final CountDownLatch cdl = new CountDownLatch(threads);
			for (int i = 1; i <= threads; ++i) {
				int new_j = i;
				new Thread(() -> {
					try {
						FileReader temp_reader = new FileReader(
								pathString + Params.StageEnum.Enc_bloom.toString() + new_j);
						BufferedReader temp_bReader = new BufferedReader(temp_reader);
						String temp_line = null;
						org.bouncycastle.math.ec.ECPoint element;
						String hash_String = null;
						String s = Params.pub_random.toString();
						byte[] result;
						while ((temp_line = temp_bReader.readLine()) != null) {
							hash_String = Utils.bytesToHexString(PreReduce.Hash_and_Get_Bits(s + temp_line, 256));
							element = enc.BigIntegerToPoint(new BigInteger(hash_String, 16));
							result = enc.encryptPoint(element).getEncoded(true);
							filter.add(Utils.bytesToHexString(result));
						}
						temp_bReader.close();
						cdl.countDown();
					} catch (FileNotFoundException e) {
						e.printStackTrace();
					} catch (IOException e) {
						e.printStackTrace();
					}
				}, "t" + i).start();
			}
			try {
				cdl.await();
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			// long endTime = System.currentTimeMillis();
			// System.out.println("����Ԫ�ز�����BF��ʱ:" + (endTime - startTime) / 1000 + "s"
			// + (endTime - startTime) % 1000 + "ms");

			return filter;
		} catch (IOException e) {
			e.printStackTrace();
		}
		return null;
	}


	// OK
	/**
	 * 
	 * @param role
	 * @param from_path
	 * @param enc
	 * @param threads
	 * @return
	 */
	public static BloomFilter<String> sec_encrypt_and_BloomWriter(Integer role, String from_path, EccEnc enc,
			int threads) {
		File file = new File(from_path);
		String pathString;
		if (role == 0) {
			pathString = "server/";
		} else {
			pathString = "client/";
		}
		try {
			int len = getLineNumber(file);
			if (len < threads) {
				threads = 1;
			}
			BloomFilter<String> filter = new FilterBuilder()
					.expectedElements(len)
					.falsePositiveProbability(0.000000001)
					.hashFunction(HashMethod.Murmur3)
					.buildBloomFilter();

			// long startTime = System.currentTimeMillis(); 
			// 1. 
			split_File(pathString, Params.StageEnum.Enc_bloom.toString(), file, len, threads);

			// 2.
			final CountDownLatch cdl = new CountDownLatch(threads);
			for (int i = 1; i <= threads; ++i) {
				int new_j = i;
				new Thread(() -> {
					try {
						FileReader temp_reader = new FileReader(
								pathString + Params.StageEnum.Enc_bloom.toString() + new_j);
						BufferedReader temp_bReader = new BufferedReader(temp_reader);
						String temp_line = null;
						org.bouncycastle.math.ec.ECPoint element;
						byte[] result;
						while ((temp_line = temp_bReader.readLine()) != null) {
							result = Utils.hexStringToBytes(temp_line);
							element = enc.encryptPoint(enc.bytesToECPoint(result));
							filter.add(Utils.bytesToHexString(element.getEncoded(true)));
						}
						temp_bReader.close();
						cdl.countDown();
					} catch (FileNotFoundException e) {
						e.printStackTrace();
					} catch (IOException e) {
						e.printStackTrace();
					}
				}, "t" + i).start();
			}
			try {
				cdl.await();
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			// long endTime = System.currentTimeMillis();
			// System.out.println("����Ԫ�ز�����BF��ʱ:" + (endTime - startTime) / 1000 + "s"
			// + (endTime - startTime) % 1000 + "ms");

			return filter;
		} catch (IOException e) {
			e.printStackTrace();
		}
		return null;
	}

	// OK?
	/**
	 * Pohlig-Hellman
	 * 
	 * @param role
	 * @param from_path
	 * @param key
	 * @param threads
	 * @return
	 */
	public static CuckooFilter<byte[]> encrypt_and_CuckooWriter(Integer role, String from_path, Keys key, int threads) {
		File file = new File(from_path);
		String pathString; 
		if (role == 0) {
			pathString = "server/";
		} else {
			pathString = "client/";
		}
		try {
			int len = getLineNumber(file);
			if (len < threads) {
				threads = 1;
			}
			CuckooFilter<byte[]> filter = new CuckooFilter.Builder<>(Funnels.byteArrayFunnel(), len)
					.withFalsePositiveRate(0.000000001).withHashAlgorithm(Algorithm.sha256)
					.withExpectedConcurrency(threads).build();

			// long startTime = System.currentTimeMillis();
			// 1. 
			split_File(pathString, Params.StageEnum.Enc_cuckoo.toString(), file, len, threads);
			final CountDownLatch cdl = new CountDownLatch(threads);
			for (int i = 1; i <= threads; ++i) {
				int new_j = i;
				new Thread(() -> {
					try {
						FileReader temp_reader = new FileReader(
								pathString + Params.StageEnum.Enc_cuckoo.toString() + new_j);
						BufferedReader temp_bReader = new BufferedReader(temp_reader);
						String temp_line = null;
						// String hash_String = null;
						// String s = Params.pub_random.toString();
						while ((temp_line = temp_bReader.readLine()) != null) {
							// hash_String = Utils.bytesToHexString(PreReduce.Hash_and_Get_Bits(s +
							// temp_line, 256));
							// System.out.println("hash_string:" + hash_String);
							// filter.put(CommEnc.encrypt_BigInteger(new BigInteger(hash_String,16),
							// key).toString().getBytes("utf-8"));
							filter.put(CommEnc.encrypt_BigInteger(new BigInteger(temp_line), key).toString()
									.getBytes("utf-8"));
						}
						temp_bReader.close();
						cdl.countDown();
					} catch (FileNotFoundException e) {
						e.printStackTrace();
					} catch (IOException e) {
						e.printStackTrace();
					}
				}, "t" + i).start();
			}
			
			try {
				cdl.await();
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			// long endTime = System.currentTimeMillis();
			// System.out.println("����Ԫ�ز�����CF��ʱ:" + (endTime - startTime) / 1000 + "s"
			// + (endTime - startTime) % 1000 + "ms");

			return filter;
		} catch (IOException e) {
			e.printStackTrace();
		}
		return null;
	}

	// OK ?
	/**
	 * Pohlig-Hellman
	 * 
	 * @param role
	 * @param from_path
	 * @param key
	 * @param threads
	 * @return
	 */
	public static CuckooFilter<byte[]> sec_encrypt_and_CuckooWriter(Integer role, String from_path, Keys key,
			int threads) {
		File file = new File(from_path);
		String pathString;
		if (role == 0) {
			pathString = "server/";
		} else {
			pathString = "client/";
		}
		try {
			int len = getLineNumber(file);
			if (len < threads) {
				threads = 1;
			}
		
			CuckooFilter<byte[]> filter = new CuckooFilter.Builder<>(Funnels.byteArrayFunnel(), len)
					.withFalsePositiveRate(0.000000001).withHashAlgorithm(Algorithm.sha256)
					.withExpectedConcurrency(threads).build();

			// long startTime = System.currentTimeMillis(); 
			// 1. 
			split_File(pathString, Params.StageEnum.Enc_cuckoo.toString(), file, len, threads);
			// 2. 
			final CountDownLatch cdl = new CountDownLatch(threads);
			for (int i = 1; i <= threads; ++i) {
				int new_j = i;
				new Thread(() -> {
					try {
						FileReader temp_reader = new FileReader(
								pathString + Params.StageEnum.Enc_cuckoo.toString() + new_j);
						BufferedReader temp_bReader = new BufferedReader(temp_reader);
						String temp_line = null;
						while ((temp_line = temp_bReader.readLine()) != null) {
							filter.put(CommEnc.encrypt_BigInteger(new BigInteger(temp_line), key).toString()
									.getBytes("utf-8"));
						}
						temp_bReader.close();
						cdl.countDown();
					} catch (FileNotFoundException e) {
						e.printStackTrace();
					} catch (IOException e) {
						e.printStackTrace();
					}
				}, "t" + i).start();
			}
			
			try {
				cdl.await();
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			// long endTime = System.currentTimeMillis();
			// System.out.println("����Ԫ�ز�����CF��ʱ:" + (endTime - startTime) / 1000 + "s"
			// + (endTime - startTime) % 1000 + "ms");

			return filter;
		} catch (IOException e) {
			e.printStackTrace();
		}
		return null;
	}

	// OK
	/**
	 * 
	 * @param role
	 * @param from_path
	 * @param enc
	 * @param threads
	 * @return
	 */
	public static CuckooFilter<byte[]> sec_encrypt_and_CuckooWriter(Integer role, String from_path, EccEnc enc,
			int threads) {
		File file = new File(from_path); 
		String pathString;
		if (role == 0) {
			pathString = "server/";
		} else {
			pathString = "client/";
		}
		try {
			int len = getLineNumber(file);
			if (len < threads) {
				threads = 1;
			}
			int cuckoo_size = len < 64 ? 64 : len;
			CuckooFilter<byte[]> filter = new CuckooFilter.Builder<>(Funnels.byteArrayFunnel(), cuckoo_size)
					.withFalsePositiveRate(0.000000001).withHashAlgorithm(Algorithm.sha256)
					.withExpectedConcurrency(threads).build();
			// long startTime = System.currentTimeMillis(); 
	
			// 1. 
			split_File(pathString, Params.StageEnum.Enc_cuckoo.toString(), file, len, threads);

			// 2. 
			final CountDownLatch cdl = new CountDownLatch(threads);
			for (int i = 1; i <= threads; ++i) {
				int new_j = i;
				new Thread(() -> {
					try {
						FileReader temp_reader = new FileReader(
								pathString + Params.StageEnum.Enc_cuckoo.toString() + new_j);
						BufferedReader temp_bReader = new BufferedReader(temp_reader);
						String temp_line = null;
						byte[] temp;
						org.bouncycastle.math.ec.ECPoint element;
						while ((temp_line = temp_bReader.readLine()) != null) {
							temp = Utils.hexStringToBytes(temp_line);
							element = enc.encryptPoint(enc.bytesToECPoint(temp));
							filter.put(element.getEncoded(true));
						}
						temp_bReader.close();
						cdl.countDown();
					} catch (FileNotFoundException e) {
						e.printStackTrace();
					} catch (IOException e) {
						e.printStackTrace();
					}
				}, "t" + i).start();
			}
			
			try {
				cdl.await();
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			// long endTime = System.currentTimeMillis();
			// System.out.println("����Ԫ�ز�����CF��ʱ:" + (endTime - startTime) / 1000 + "s"
			// + (endTime - startTime) % 1000 + "ms");

			return filter;
		} catch (IOException e) {
			e.printStackTrace();
		}
		return null;
	}


	// OK
	/**
	 * 
	 * @param role
	 * @param from_path
	 * @param enc
	 * @param threads
	 * @return
	 */
	public static CuckooFilter<byte[]> encrypt_and_CuckooWriter(Integer role, String from_path, EccEnc enc,
			int threads) {
		File file = new File(from_path);
		String pathString;
		if (role == 0) {
			pathString = "server/";
		} else {
			pathString = "client/";
		}
		try {
			int len = getLineNumber(file);
			if (len < threads) {
				threads = 1;
			}
			CuckooFilter<byte[]> filter = new CuckooFilter.Builder<>(Funnels.byteArrayFunnel(), len)
					.withFalsePositiveRate(0.000000001).withHashAlgorithm(Algorithm.sha256)
					.withExpectedConcurrency(threads).build();
			// long startTime = System.currentTimeMillis();
			// 1. 
			split_File(pathString, Params.StageEnum.Enc_cuckoo.toString(), file, len, threads);

			// 2.
			final CountDownLatch cdl = new CountDownLatch(threads);
			for (int i = 1; i <= threads; ++i) {
				int new_j = i;
				new Thread(() -> {
					try {
						FileReader temp_reader = new FileReader(
								pathString + Params.StageEnum.Enc_cuckoo.toString() + new_j);
						BufferedReader temp_bReader = new BufferedReader(temp_reader);
						String temp_line = null;
						String hash_String = null;
						String s = Params.pub_random.toString();
						org.bouncycastle.math.ec.ECPoint element;
						while ((temp_line = temp_bReader.readLine()) != null) {
							hash_String = Utils.bytesToHexString(PreReduce.Hash_and_Get_Bits(s + temp_line, 256));
							element = enc.BigIntegerToPoint(new BigInteger(hash_String, 16));
							filter.put(enc.encryptPoint(element).getEncoded(true));
						}
						temp_bReader.close();
						cdl.countDown();
					} catch (FileNotFoundException e) {
						e.printStackTrace();
					} catch (IOException e) {
						e.printStackTrace();
					}
				}, "t" + i).start();
			}
			try {
				cdl.await();
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			// long endTime = System.currentTimeMillis();
			// System.out.println("����Ԫ�ز�����CF��ʱ:" + (endTime - startTime) / 1000 + "s"
			// + (endTime - startTime) % 1000 + "ms");

			return filter;
		} catch (IOException e) {
			e.printStackTrace();
		}
		return null;
	}

	// OK
	public static int cuckoo_query_cardinality(Boolean isECC, String from, CuckooFilter<byte[]> filter) {
		File file = new File(from);
		FileReader fileReader;
		int intersect_cardinality = 0;

		try {
			fileReader = new FileReader(file);
			BufferedReader bufferedReader = new BufferedReader(fileReader);
			String line = "";
			// long startTime = System.currentTimeMillis();
			if (!isECC) {
				while ((line = bufferedReader.readLine()) != null) {
					if (filter.mightContain(line.getBytes("utf-8"))) {
						intersect_cardinality++;
					}
				}
			} else {
				while ((line = bufferedReader.readLine()) != null) {
					if (filter.mightContain(Utils.hexStringToBytes(line))) {
						intersect_cardinality++;
					}
				}
			}
			// long endTime = System.currentTimeMillis();
			// System.out.println("Utils::cuckoo_query_cardinality - time:
			// "+(endTime-startTime)/1000 + "s" +
			// (endTime-startTime) % 1000 +"ms");
			bufferedReader.close();
			// System.out.println("Utils::cuckoo_query_cardinality - cardinality: " +
			// intersect_cardinality );
			return intersect_cardinality;
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return 0;
	}

	// OK
	public static int bloom_query_cardinality(String from, BloomFilter<String> filter) {
		File file = new File(from);
		FileReader fileReader;
		int intersect_cardinality = 0;
		try {
			fileReader = new FileReader(file);
			BufferedReader bufferedReader = new BufferedReader(fileReader);
			String line = "";
			while ((line = bufferedReader.readLine()) != null) {
				if (filter.contains(line)) {
					// System.out.println("Utils::bloom_query_cardinality - common line: " + line);
					intersect_cardinality++;
				}
			}
			bufferedReader.close();
			System.out.println("Utils::bloom_query_cardinality - cardinality: " + intersect_cardinality);
			return intersect_cardinality;
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return 0;
	}
}
/**
 * //* ���̹߳�ϣ�ټ���Ԫ�صķ���, ���м�������Բ���߼���
 * //* @param role
 * //* @param isBigSet true�󼯺�һ��ר��: ��Ԫ�鼯�����ɺ���; falseС����һ��ר��:
 * ֻ��������
 * //* @param from_path
 * //* @param to_path
 * //* @param ecc
 * //* @param threads
 * //* @throws FileNotFoundException
 * //
 */
// public static void hash_prefix_enc_mThreads(Integer role, Boolean isBigSet,
// String from_path, String to_path, EccEnc ecc, int threads) throws
// FileNotFoundException {
// if(threads > 0 && (System.out.printlnthreads & (threads - 1)) != 0)
// {//�ж�threads�Ƿ�Ϊ2����
// System.out.println("�߳�������Ϊ2���ݴΣ�");
// return;
// }
// //��ȡ�������ļ��ĸ�Ŀ¼
// String pathString; //��������or�ͻ��˵ĸ�Ŀ¼
// if(role == 0) {//0����server
// pathString = "server/";
// } else {
// pathString = "client/";
// }
// //1.�ȶ�ȡ�ļ�����
// long startTime = System.currentTimeMillis();
// int len;
// File file = new File(from_path);
// try {
// len = getLineNumber(file);
// split_File(pathString, Params.StageEnum.Prefix_filter.toString(), file, len,
// threads);//��Ŀ���ļ���ֳ�threads��
// } catch (IOException e1) {
// e1.printStackTrace();
// }
// //2.��ʼ���̷߳��ʲ�ͬ�ļ����м���,�������ܽ��д��ͬһ��toPath�ļ���
// final CountDownLatch cdl = new CountDownLatch(threads);//����Ϊ�̸߳���
// for(int j = 1; j <= threads; ++j) {
// int new_j = j;
// new Thread(() -> {
// try {
// FileReader temp_reader = new FileReader(pathString +
// Params.StageEnum.Prefix_filter.toString() + new_j);
// BufferedReader temp_bReader = new BufferedReader(temp_reader);
// FileWriter temp_writer = new FileWriter(pathString +
// Params.StageEnum.Prefix_filter.toString() + new_j + "out");
// BufferedWriter temp_bWriter = new BufferedWriter(temp_writer);
// String temp_line = null;
// String hash_prefix = null;
// String hash_String = null;
// String s = Params.pub_random.toString();
// org.bouncycastle.math.ec.ECPoint element;
// if (isBigSet) {// ����Ǵ󼯺�
// while((temp_line = temp_bReader.readLine()) != null) {//���ж�ȡԪ�ز�����
// // �����ϣǰ׺h(x)[0:w]
// hash_prefix = Utils.bytesToHexString(PreReduce.Hash_and_Get_Bits(temp_line,
// Params.prefix_len));
// System.out.println("hash_prefix:" + hash_prefix);
// // �õ���ϣֵh(s,x)�ټ���, ������ϣǰ׺��������ɶ�Ԫ��(h(x)[0:w],h(s,x))д���ļ�
// hash_String = Utils.bytesToHexString(PreReduce.Hash_and_Get_Bits(s +
// temp_line, 256));
// element = ecc.BigIntegerToPoint(new BigInteger(hash_String, 16));
// temp_bWriter.write(hash_prefix + "," +
// Utils.bytesToHexString(ecc.encryptPoint(element).getEncoded(true)) + "\r\n");
// }
// } else {
// while((temp_line = temp_bReader.readLine()) != null) {//���ж�ȡԪ�ز�����
// // �õ���ϣֵh(s,x)�ټ���,д���ļ�
// hash_String = Utils.bytesToHexString(PreReduce.Hash_and_Get_Bits(s +
// temp_line, 256));
// element = ecc.BigIntegerToPoint(new BigInteger(hash_String, 16));
// temp_bWriter.write(Utils.bytesToHexString(ecc.encryptPoint(element).getEncoded(true))
// + "\r\n");
// }
// }
// temp_bWriter.close();
// temp_bReader.close();
// cdl.countDown();
// } catch (FileNotFoundException e) {
// e.printStackTrace();
// } catch (IOException e) {
// e.printStackTrace();
// }
// }, "t" + j).start();
// }
// //�߳����������countDownLatch����
// try {
// cdl.await();//��Ҫ�����쳣���������߳���Ϊ0ʱ����Ż��������
// } catch (InterruptedException e) {
// e.printStackTrace();
// }
// long endTime = System.currentTimeMillis();
// System.out.println("����Ԫ�غ�ʱ:" + (endTime - startTime) / 1000 + "s" +
// (endTime - startTime) % 1000 + "ms");
// //3.���ļ��ܽ����󣬽����в����������ļ��ϳ�һ��
// join_Files(pathString + Params.StageEnum.Prefix_filter.toString(), to_path,
// threads);
// }
