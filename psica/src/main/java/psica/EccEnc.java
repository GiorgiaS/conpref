package psica;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.math.BigInteger;
import java.security.SecureRandom;
import java.util.Enumeration;

import org.bouncycastle.jce.ECNamedCurveTable;
import org.bouncycastle.jce.spec.ECParameterSpec;
import org.bouncycastle.math.ec.ECPoint;

@SuppressWarnings("unchecked")
public class EccEnc implements Serializable {
	// ϣ��������ܷ�װ��ͬ����Բ���߼ӽ����㷨, ��ʼ��ֻ��ָ������������
	// public static void main(String[] args) {
	// EccEnc eccEnc = new EccEnc();
	// eccEnc.generateKey();
	// String telString = "13382958827";//����������
	// BigInteger I = new BigInteger(telString);
	// ECPoint encPoint = eccEnc.G.multiply(I);//��ѹ����ʽ����

	// byte[] result = encPoint.getEncoded(false);

	// System.out.println("����ǰ�ĵ�: " + new String(result));

	// encPoint = encPoint.multiply(eccEnc.key);
	// result = encPoint.getEncoded(false);

	// System.out.println("һ�μ��ܺ�ĵ�: " + new String(result));

	// encPoint = eccEnc.bytesToECPoint(result);//�Ƚ�byte[]��ʽ����תΪ��Բ�����ϵĵ�

	// //encPoint = encPoint.multiply(eccEnc.key2);//���μ���

	// result = encPoint.getEncoded(true);

	// System.out.println("���μ��ܺ�ĵ�: " + new String(result));

	// //ECPoint encPoint2 = eccEnc.bytesToECPoint(result);
	// //encPoint = encPoint.multiply(eccEnc.key2_inv);

	// result = encPoint.getEncoded(true);

	// System.out.println("һ�ν��ܺ�ĵ�: " + new String(result));

	// String tempString = new String(result);

	// byte[] result2 = tempString.getBytes();

	// System.out.println("����string�ָ�������byte����Բ���: " + new
	// String(result2));

	// encPoint = encPoint.multiply(eccEnc.key_inv);
	// result = encPoint.getEncoded(true);

	// System.out.println("2�ν��ܺ�ĵ�: " + new String(result));

	// String hexOutputString = Utils.bytesToHexString(result);

	// System.out.println("2�ν��ܺ�ĵ�(16����): " + hexOutputString);

	// result = Utils.hexStringToBytes(hexOutputString);

	// System.out.println("2�ν��ܺ�ĵ�: " + new String(result));

	// //Vector<String> vector = ECNamedCurveTable.getNames();

	// Enumeration<String> enumeration = ECNamedCurveTable.getNames();
	// System.out.println("�鿴���õ���Բ�����б�:");
	// int cnt = 1;
	// while(enumeration.hasMoreElements()) {
	// System.out.println("��" + cnt++ + "��:" + enumeration.nextElement());
	// }

	// }

	// public EccEnc() {//���캯��
	// generateKey();
	// }

	// �Ȼ���BouncyCastleʵ��һ���򵥵�ECC
	private BigInteger key;
	private BigInteger key_inv;
	private ECPoint G;

	// public EccEnc() {
	// key = new
	// BigInteger("38115980073204919951107998614078657802920642281097345521495768041606252111346");
	// key_inv = new
	// BigInteger("99293001303404139902345183758560683640650352282924224290370164858270519393015");
	// ECParameterSpec ecSpec =
	// ECNamedCurveTable.getParameterSpec(Params.eccEnum.getEccName());
	// G = ecSpec.getG();
	// }

	// OK
	public void generateKey(boolean server) {
		// ECParameterSpec ecSpec = ECNamedCurveTable.getParameterSpec("prime256v1");
		// ECParameterSpec ecSpec = ECNamedCurveTable.getParameterSpec("secp256k1");
		// ECParameterSpec ecSpec = ECNamedCurveTable.getParameterSpec("sm2p256v1");
		// ECParameterSpec ecSpec = ECNamedCurveTable.getParameterSpec("K-283");
		// ECParameterSpec ecSpec = ECNamedCurveTable.getParameterSpec("P-256");
		// ECParameterSpec ecSpec = ECNamedCurveTable.getParameterSpec("K-233");
		// ECParameterSpec ecSpec = ECNamedCurveTable.getParameterSpec("secp224r1");
		ECParameterSpec ecSpec = ECNamedCurveTable.getParameterSpec(Params.eccEnum.getEccName());
		BigInteger n = ecSpec.getN();
		G = ecSpec.getG();
		key = org.bouncycastle.util.BigIntegers.createRandomInRange(BigInteger.ONE,
				n.subtract(BigInteger.ONE), new SecureRandom());
		key_inv = key.modInverse(n);
		// System.out.println("EccEnc::generateKey - generated key: " + key);
		// System.out.println("EccEnc::generateKey - generated key_inv: " + key_inv);
		// System.out.println("EccEnc::generateKey - generated G: " + G);

		// Store the data into a file for future usage
		try {
			FileOutputStream fos;
			if (server)
				fos = new FileOutputStream("./server/keys/key.dat");
			else // If client
				fos = new FileOutputStream("./client/keys/key.dat");
			ObjectOutputStream oos = new ObjectOutputStream(fos);
			oos.writeObject(key);
			oos.close();

			if (server)
				fos = new FileOutputStream("./server/keys/key_inv.dat");
			else
				fos = new FileOutputStream("./client/keys/key_inv.dat");
			oos = new ObjectOutputStream(fos);
			oos.writeObject(key_inv);
			oos.close();

		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public void restoreKey(boolean server) {
		try {
			FileInputStream fis;
			if (server)
				fis = new FileInputStream("./server/keys/key.dat");
			else
				fis = new FileInputStream("./client/keys/key.dat");
			ObjectInputStream ois = new ObjectInputStream(fis);
			key = (BigInteger) ois.readObject();
			ois.close();

			if (server)
				fis = new FileInputStream("./server/keys/key_inv.dat");
			else
				fis = new FileInputStream("./client/keys/key_inv.dat");
			ois = new ObjectInputStream(fis);
			key_inv = (BigInteger) ois.readObject();
			ois.close();

		} catch (IOException e) {
			e.printStackTrace();
		} catch (ClassNotFoundException e) {
			e.printStackTrace();
		}

	}

	public ECPoint hashToPoint(byte[] hash) {
		BigInteger element = new BigInteger(hash);
		return G.multiply(element);
	}

	public ECPoint BigIntegerToPoint(BigInteger element) {
		return G.multiply(element);
	}

	public ECPoint encryptPoint(ECPoint point){
		return point.multiply(key);
	}

	public ECPoint decryptPoint(ECPoint point) {
		return point.multiply(key_inv);
	}

	public ECPoint bytesToECPoint(byte[] bytes) {
		ECParameterSpec ecSpec = ECNamedCurveTable.getParameterSpec(Params.eccEnum.getEccName());
		ECPoint point = ecSpec.getCurve().decodePoint(bytes);
		return point;
	}

}
