package psica;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.Serializable;
import java.math.BigInteger;

public class Keys implements Serializable {
	private BigInteger p;// ѡ������p
	private BigInteger a, a_inv;

	public Keys() {
	}

	public Keys(BigInteger p) {
		this.p = p;
	}

	public Keys(BigInteger p, BigInteger a, BigInteger a_inv) {
		this.p = p;
		this.a = a;
		this.a_inv = a_inv;
	}

	// OK
	public void setA(BigInteger a) { 
		this.a = a;
	}

	public void setA_Inv(BigInteger a_inv) {
		this.a_inv = a_inv;
	}

	public void setP(boolean server) {
		FileInputStream fis;
		ObjectInputStream ois;
		try {
			if (server)
				fis = new FileInputStream("./server/keys/P.dat");
			else
				fis = new FileInputStream("./client/keys/P.dat");

			ois = new ObjectInputStream(fis);
			BigInteger newP = (BigInteger) ois.readObject();
			this.p = newP;
			ois.close();
		} catch (IOException | ClassNotFoundException e) {
			e.printStackTrace();
		}
	}

	// OK
	public BigInteger getA() {
		return a;
	}

	public BigInteger getAInv() {
		return a_inv;
	}

	public BigInteger getP() {
		return p;
	}

	@Override
	public String toString() {
		String string = "p:" + p.toString() + "\n"
				+ "a:" + a.toString() + "\n"
				+ "a_inv:" + a_inv.toString() + "\n";
		return string;
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;// �����ַ��ȣ��ǿ���ֱ�ӷ���

		if (obj == null) {
			return false;// �ǿ��ԣ���������ǿ�����x��x.equals(null)Ӧ�÷���false��
		}

		if (obj instanceof Keys) {
			Keys other = (Keys) obj;
			// ��Ҫ�Ƚϵ��ֶ���ȣ����������������
			if (this.a.compareTo(other.getA()) == 0 &&
					this.a_inv.compareTo(other.getAInv()) == 0 &&
					this.p.compareTo(other.getP()) == 0)
				return true;
		}

		return false;
	}

	@Override
	public int hashCode() {
		int result = 17;
		result = 31 * result + (a == null ? 0 : a.hashCode());
		result = 31 * result + (a_inv == null ? 0 : a_inv.hashCode());
		result = 31 * result + (p == null ? 0 : p.hashCode());
		return result;
	}
}
