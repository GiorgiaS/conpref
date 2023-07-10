package psica;

import java.io.DataInputStream;
import java.io.DataOutputStream;

import java.io.FileNotFoundException;

import java.io.IOException;

import java.io.UnsupportedEncodingException;

import java.net.Socket;
import java.net.UnknownHostException;
import java.security.NoSuchAlgorithmException;

import java.util.concurrent.CountDownLatch;

import org.bouncycastle.jcajce.provider.asymmetric.EC;

import com.github.mgunlogson.cuckoofilter4j.CuckooFilter;

import orestes.bloomfilter.BloomFilter;

public class Client {
	// private EccEnc eccEnc = null;
	private static Network network = new Network();
	// private static final String DB_NAME = "client/clientDB" + Params.client_size
	// + ".txt";
	private static final String DB_NAME = "client/social_ignore.txt";
	private static final String FILTERED_DB = "client/Filtered_serverDB" + Params.server_size + ".txt";
	private static final String PAIR_DB_NAME = "client/Pair_DB" + Params.client_size + ".txt";
	private static final String FILTERED_CLIENT_DB = "client/Filtered_clientDB" + Params.client_size + ".txt";

	private EccEnc eccEnc = new EccEnc();
	private Keys key = new Keys();

	// 0.1 generate keys:
	public void generateECCKey() {
		eccEnc.generateKey(false); // true = server; false = client
	}

	public void generateKey() throws NoSuchAlgorithmException {
		this.key.setP(false);
		CommEnc.generate_Keys(key, false);
	}

	// 0.2 restore keys
	public void restoreECCKey() {
		eccEnc.restoreKey(false);
	}

	public void restoreKey(){
		this.key = CommEnc.restore_Key(false);
	}

	// /**
	//  * Client
	//  * 
	//  * @param enc ObjectͣΪKeysEccEnc
	//  * @return
	//  */
	// public String Pir_Filter() {// ݶԷԪԼԼԪ죬Ҫɵǰ׺ȣӦBF
	// 	try {
	// 		Utils.hash_prefix_enc_mThreads(Integer.valueOf(1), DB_NAME, PAIR_DB_NAME, eccEnc, Params.THREADS);
	// 		// There is a new file; the device (python) will send it to the edge
	// 		return PAIR_DB_NAME;
	// 	} catch (IOException e) {
	// 		e.printStackTrace();
	// 	}
	// 	return "";
	// }

	// /**
	//  * ClientΪСһʱServerĶԪ鼯Ͻй
	//  * 
	//  * @param network
	//  */
	// public void Recv_Pir_Filter() {// նԷBF, նԷԪǰ׺.
	// 	try {
	// 		// 1.նԷĶԪ鼯
	// 		network.d_in = new DataInputStream(network.sock.getInputStream());
	// 		network.receiveFile("client/server_pair_set");
	// 		// 2.ԱԪǰ׺Ĳ¡
	// 		BloomFilter<String> filter = Utils.get_prefix_BF_mThreads(1, DB_NAME, Params.THREADS);
	// 		// 3.ԶԪ鼯Ͻйˣµݼ
	// 		Utils.filter_Pair_Set(filter, "client/server_pair_set", FILTERED_DB);

	// 		System.out.println("Ԫ鼯Ϲ!");
	// 	} catch (IOException e) {
	// 		e.printStackTrace();
	// 	}
	// }

	/**
	 * @param network
	 * @param enc
	 * @return
	 */
	public String Recv_Pre_Filter() {
		// (python) The device has already received the file from the edge
		BloomFilter<String> filter = Utils.BloomReader("client/recv_prefix_filter");// ļжȡbf
		Utils.filter_Set_mThreads(1, filter, DB_NAME, FILTERED_CLIENT_DB, eccEnc, Params.THREADS);
		// return the path of the new file
		return FILTERED_CLIENT_DB;
	}

	// 1. receive the bloom filter from the edge
	// 2. compute clientDB
	public String ECC_PSI_Rev_set_cipher() throws FileNotFoundException {// ƽPSI-CAЭ
		this.generateECCKey();

		// try {
		// System.out.println("Client::ECC_PSI_Rev - begins");
		// if (Params.pirFilter) {
		// 	// System.out.println("Client::ECC_PSI_Rev - pirFilter=true");
		// 	return Pir_Filter();
		// } else if (Params.preFilter) { // Here
			// System.out.println("Client::ECC_PSI_Rev - preFilter=true");
			return Recv_Pre_Filter();
		// } else {
		// 	System.out.println("Client::ECC_PSI_Rev - generate client_cypher.txt");
		// 	Utils.enc_dec_and_Write_mThreads(1, true, DB_NAME, "client/client_cipher.txt", key, Params.THREADS);
		// 	return "client/client_cipher.txt";
		// }
	}
	// 3. send client_cypher to the edge
	// 4. receive the server cypher (recv_server_cipher.txt)
	// 5. Modify the recv_server_cypher file
	public String ECC_PSI_Rev_set_server_cyph() throws FileNotFoundException {
		this.restoreECCKey();
		Utils.ECC_sec_enc_and_Write_mThreads(eccEnc, 1, true, "client/recv_server_cipher.txt",
				"client/server_cipher.txt", Params.THREADS);
		return "client/server_cipher.txt";
	}
	// 6. Receive the cuckoo file from the server (python)
	// 7. Get cardinality with Cuckoo or Bloom filter
	public int ECC_PSI_Rev_cardinality_cuckoo() {
		int cardinality = 0;
		CuckooFilter<byte[]> filter = Utils.cuckooReader("client/client_cuckoo");
		cardinality = Utils.cuckoo_query_cardinality(true, "client/server_cipher.txt", filter);
		return cardinality;
	}

	public int ECC_PSI_Rev_cardinality_bloom() {
		int cardinality = 0;
		BloomFilter<String> filter = Utils.BloomReader("client/client_bloom");
		cardinality = Utils.bloom_query_cardinality("client/server_cipher.txt", filter);
		return cardinality;
	}
	
	// Solution from the paper based on ECC
	// 2. generate key and the client_cipher
	public String ECC_PSI_Unbalanced_set_cipher() {
		this.generateECCKey();
		try {
			Utils.ECC_enc_dec_and_Write_mThreads(eccEnc, 1, true, DB_NAME, "client/client_cipher.txt", Params.THREADS);
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		return "client/client_cipher.txt";
	}

	// 6. Decrypt recv_client_cipher_2.txt file
	public void ECC_PSI_Unbalanced_decrypt_cypher() {
		this.restoreECCKey();
		try {
			Utils.ECC_sec_enc_and_Write_mThreads(eccEnc, 1, false, "client/recv_client_cipher_2.txt",
					"client/recv_client_decrypt_cipher.txt", Params.THREADS);
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
	}

	// 7. Compute cardinality
	public int ECC_PSI_Unbalanced_cardinality_cuckoo() {
		int cardinality = 0;
		CuckooFilter<byte[]> filter = Utils.cuckooReader("client/client_cuckoo");
		cardinality = Utils.cuckoo_query_cardinality(true, "client/recv_client_decrypt_cipher.txt", filter);

		return cardinality;
	}

	public int PSI_Unbalanced_cardinality_bloom() {
		int cardinality = 0;
		BloomFilter<String> filter = Utils.BloomReader("client/client_bloom");
		cardinality = Utils.bloom_query_cardinality("client/recv_client_decrypt_cipher.txt", filter);

		return cardinality;
	}

	// Paper without ECC

	// 1-2. generate key and set cipher
	public String PSI_Unbalanced_set_cipher() throws NoSuchAlgorithmException {
		this.generateKey();
		try {
			Utils.enc_dec_and_Write_mThreads(1, true, DB_NAME, "client/client_cipher.txt", key, Params.THREADS);
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		return "client/client_cipher.txt";
	}

	// 6. Decrypt recv_client_cipher_2.txt file
	public void PSI_Unbalanced_decrypt_cypher() {
		this.restoreKey();
		try {
			Utils.enc_dec_and_Write_mThreads(1, false, "client/recv_client_cipher_2.txt", "client/recv_client_decrypt_cipher.txt", key, Params.THREADS);
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
	}

	// 7. compute PSICA
	// For Bloom file, is the same as PSI_Unbalanced_cardinality_bloom()
	public int PSI_Unbalanced_cardinality_cuckoo() {
		int cardinality = 0;
		CuckooFilter<byte[]> filter = Utils.cuckooReader("client/client_cuckoo");// ļжȡbf
		cardinality = Utils.cuckoo_query_cardinality(true, "client/recv_client_decrypt_cipher.txt", filter);

		return cardinality;
	}
}