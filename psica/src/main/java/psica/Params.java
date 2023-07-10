package psica;


import java.math.BigInteger;

public class Params {
	public enum ProtocolEnum {//����ѡ��ͬ��Э��
		Unbalanced, Reversed, ECC_Unbalanced, ECC_Reversed
	}
	
	public enum FilterEnum {
		BloomFilter, CuckooFilter
	}
	
	public enum StageEnum {
		Prefix_filter, Prefix_bloom, Encrypt, Enc_bloom, Enc_cuckoo
	}
	
	public static final int THREADS = 8;//����Э��Ĳ�����
	
	public static final boolean pirFilter = false;
	
	public static final boolean preFilter = true;
	
	public static final int client_size = (int)Math.pow(2, 18);//�ͻ������ݼ���С
	public static final int server_size = (int)Math.pow(2, 15);//��������ݼ���С
	
	public static final int prefix_len = 16; //��ϣԤ���˵�ǰ׺����
	
	public static final ProtocolEnum protocol = ProtocolEnum.ECC_Reversed; //���ھ���ִ���ĸ�Э��
	
	public static final ECCEnum eccEnum = ECCEnum.SM2; //���ھ���ʹ���ĸ���Բ����
	
	public static final FilterEnum filterEnum = FilterEnum.CuckooFilter; //���ھ���ʹ���ĸ�������
	
	public static final BigInteger pub_random = new BigInteger("38520159238394498553641278910"); //���ڱ�֤��ȫ�ԵĹ����������
	
}
