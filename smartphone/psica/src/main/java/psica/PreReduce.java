package psica;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import orestes.bloomfilter.BloomFilter;
import orestes.bloomfilter.FilterBuilder;
import orestes.bloomfilter.HashProvider.HashMethod;

public class PreReduce {

	public static void main(String[] args) {
		//ƥ��ɸѡʵ��
		//�����ɼ���С���� n1={2^10,2^11,2^12,2^13,2^14}
		SecureRandom ran;
		String nameString;
		long[] arr = {(long) Math.pow(2, 6), (long) Math.pow(2, 7), (long) Math.pow(2, 8), (long) Math.pow(2, 9), (long) Math.pow(2, 10)};
		long[] arr2 = {(long) Math.pow(2, 15), (long) Math.pow(2, 16), (long) Math.pow(2, 17), (long) Math.pow(2, 18), (long) Math.pow(2, 19), (long) Math.pow(2, 20)};
		//���ɲ������ݼ�
		try {
			for(int i = 0; i < arr.length; ++i) {//
				nameString =  arr[i] + ".txt";
				File file = new File(nameString);
				if(file.exists()) continue;
				for(long j = 0; j < arr[i]; ++j) {
					ran = SecureRandom.getInstance("SHA1PRNG");
					CommEnc.writeTxt(nameString, createMobile(ran.nextInt(3)) + "\n");
					if(j % 100 == 0) {
						System.out.println("��" + i + "���ļ��ĵ�" + j + "���ֻ���������");
					}
				}
			}
			
			//�����ɼ����󼯺� n2={2^16,2^18,2^20,2^22,2^24}
			for(int i = 0; i < arr2.length; ++i) {//
				nameString =  arr2[i] + ".txt";
				File file = new File(nameString);
				if(file.exists()) continue;
				for(long j = 0; j < arr2[i]; ++j) {
					ran = SecureRandom.getInstance("SHA1PRNG");
					CommEnc.writeTxt(nameString, createMobile(ran.nextInt(3)) + "\n");
					if(j % 10000 == 0) {
						System.out.println("��" + i + "���ļ��ĵ�" + j + "���ֻ���������");
					}
				}
			}
		} catch (NoSuchAlgorithmException e) {
			e.printStackTrace();
		}		
		
		//�Դ󼯺�Ҳ���й�ϣ, Ҳ��ȡlog(n1)+1, log(n1)+2, log(n1)+3, log(n1)+4 bits
		
		//�ֱ��󽻼����۲콻����С���ȶԲ�ͬ�����µĹ���Ч��
		//��С���Ϲ�ϣ, Ȼ��ֱ��ȡlog(n1)+1, log(n1)+2, log(n1)+3, log(n1)+4
				//������2^10��
		//String out_nameString;
		String lineString = "";
		byte[] result;
		try {
			File file;
			FileReader fileReader;
			BufferedReader bReader;
			for(int i = 0; i < arr.length; ++i) {//n1={2^6,2^7,2^8,2^9,2^10}
				file = new File(arr[i] + ".txt");
				
				for(int j = 1; j <= 8; ++j) {//����log(n1)+1, log(n1)+2, log(n1)+3, log(n1)+4, log(n1)+5�⼸�ֹ���
					fileReader = new FileReader(file);
					bReader = new BufferedReader(fileReader);
					int cut_len = (int)(log2(arr[i]) + j);
					//out_nameString = arr[i] + "_" + cut_len + ".txt";
					BloomFilter<String> filter = new FilterBuilder()
							.expectedElements((int) arr[i])
							.falsePositiveProbability(0.0000000001)
							.hashFunction(HashMethod.Murmur3)
							.buildBloomFilter();
					//��ʼ���ж�ȡ�ļ����ݲ���ϣ����ȡ��ǰlog(n1)+j����
					while ((lineString = bReader.readLine()) != null) {//��ȡ�ļ�
						result = Hash_and_Get_Bits(lineString, cut_len);
						filter.add(new String(result, StandardCharsets.UTF_8));//����BF
					}
					int cnt;//���ڼ����ж��ٸ���ͬ��Ԫ��
					//�ڴ󼯺��ļ�������ѯ�����ƥ������
					for(int i2 = 0; i2 < arr2.length; ++i2) {
						File file2 = new File(arr2[i2] + ".txt");
						FileReader fileReader2 = new FileReader(file2);
						BufferedReader bReader2 = new BufferedReader(fileReader2);
						cnt = 0;//ÿ���ļ�����0
						for(int j2 = 0; j2 < arr2[i2]; ++j2) {
							while((lineString = bReader2.readLine()) != null) {
								result = Hash_and_Get_Bits(lineString, cut_len);
								if(filter.contains(result)) {
									cnt++;
								}
							}
						}
						System.out.println("�ļ�" + (int)arr2[i2] + "���о���BF��ѯ��" + cnt + "����" + arr[i] + ".txt" + "ǰ׺����Ϊ" + cut_len + "ʱ��ͬ��Ԫ��");
						bReader2.close();
					}
				}
			}
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public static void Pre_Filter() {//���ݶԷ�Ԫ���������������Լ��Լ���Ԫ�����������������죬����Ҫ���ɵ�ǰ׺���ȣ���������Ӧ��BF
		
	}
	
	public static void Rev_Pre_Filter() {//���նԷ�������BF, �����նԷ���Ԫ��ǰ׺����.
		
	}
	
	public static String byteToBit(byte b) {
		return ""
				+ (byte) ((b >> 7) & 0x1) + (byte) ((b >> 6) & 0x1)
				+ (byte) ((b >> 5) & 0x1) + (byte) ((b >> 4) & 0x1)
				+ (byte) ((b >> 3) & 0x1) + (byte) ((b >> 2) & 0x1)
				+ (byte) ((b >> 1) & 0x1) + (byte) ((b >> 0) & 0x1);
	}
	
	public static double log2(double N) {
		return Math.log(N) / Math.log(2);//
	}
	
	public static byte[] Hash_and_Get_Bits(String txt, int b) {//txtΪҪ��ϣ�������ַ���, bΪҪ��õı���λ��
		byte[] output = null;
		try {
			MessageDigest mDigest;
			mDigest = MessageDigest.getInstance("SHA-256");
			mDigest.update(txt.getBytes());
			byte[] digest = mDigest.digest();
			//System.out.println("���sha256��16���ƽ��" + Utils.bytesToHexString(digest));
			if(b == 256) return digest;
			
			int group = b % 8 == 0 ? b / 8 : b / 8 + 1;
			output = new byte[group];
			for(int i = 0; i < group; ++i) {
				output[i] = digest[i];
			}
			
			if(b % 8 != 0) {
				int left = b % 8;
				int shift = 8 - left;
				for(int j = 0; j < shift; ++j) {
					output[group - 1] = (byte) (output[group - 1] >> 1);
				}
			}
//			result = new byte[8 * group];//����Ϊb�ı������� 
//			
//			for(int i = 0; i < group; ++i) {
//				for(int j = 7; j >= 0; j--) {
//					result[i * 8 + j] = (byte)(digest[i] & 1);
//					digest[i] = (byte) (digest[i] >> 1);
//				}
//			}
			
		} catch (NoSuchAlgorithmException e) {
			e.printStackTrace();
		}
		return output;
	}
	
	/**
     * �����ֻ����� 
     */
	//�й��ƶ�
	public static final String[] CHINA_MOBILE = {
            "134", "135", "136", "137", "138", "139", "150", "151", "152", "157", "158", "159",
            "182", "183", "184", "187", "188", "178", "147", "172", "198" };
	//�й���ͨ
    public static final String[] CHINA_UNICOM = {
            "130", "131", "132", "145", "155", "156", "166", "171", "175", "176", "185", "186", "166"
    };
    //�й�����
    public static final String[] CHINA_TELECOME = {
            "133", "149", "153", "173", "177", "180", "181", "189", "199"
    };
	
    /**
     * �����ֻ���
     *
     * @param op 0 �ƶ� 1 ��ͨ 2 ����
     */
    public static String createMobile(int op) {
        StringBuilder sb = new StringBuilder();
        SecureRandom ran;
		try {
			ran = SecureRandom.getInstance("SHA1PRNG");
			String mobile01;//�ֻ���ǰ��λ
	        int temp;
	        switch (op) {
	            case 0:
	                mobile01 = CHINA_MOBILE[ran.nextInt(CHINA_MOBILE.length)];
	                break;
	            case 1:
	                mobile01 = CHINA_UNICOM[ran.nextInt(CHINA_UNICOM.length)];
	                break;
	            case 2:
	                mobile01 = CHINA_TELECOME[ran.nextInt(CHINA_TELECOME.length)];
	                break;
	            default:
	                mobile01 = "op��־λ����";
	                break;
	        }
	        if (mobile01.length() > 3) {
	            return mobile01;
	        }
	        sb.append(mobile01);
	        //�����ֻ��ź�8λ
	        for (int i = 0; i < 8; i++) {
	            temp = ran.nextInt(10);
	            sb.append(temp);
	        }
		} catch (NoSuchAlgorithmException e) {
			
			e.printStackTrace();
		}
		return sb.toString();
    }
}
