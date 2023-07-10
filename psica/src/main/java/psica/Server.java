package psica;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.FileNotFoundException;

import java.io.IOException;
import java.net.ServerSocket;
import java.util.concurrent.CountDownLatch;

import org.bouncycastle.jcajce.provider.asymmetric.EC;

import com.github.mgunlogson.cuckoofilter4j.CuckooFilter;

import orestes.bloomfilter.BloomFilter;
import orestes.bloomfilter.FilterBuilder;
import orestes.bloomfilter.HashProvider.HashMethod;

public class Server {

	// private EccEnc eccEnc = null;
	private Network network = new Network();
	// private static boolean isFiltered = false;
	// private static final String DB_NAME = "server/serverDB" + Params.server_size
	// + ".txt";
	private static final String DB_NAME = "server/connected_list.txt";
	private static final String FILTERED_DB = "server/Filtered_clientDB" + Params.client_size + ".txt";
	// private static final String PAIR_DB_NAME = "server/Pair_DB" +
	// Params.server_size + ".txt";
	// private static final String SERVER_CIPHER = "server/Server_Cipher" +
	// Params.server_size + ".txt";

	private EccEnc eccEnc = new EccEnc();
	private Keys key;

	// 0.1 generate keys:
	public void generateECCKey() {
		eccEnc.generateKey(true); // true = server; false = client
	}

	public void generateKey() {
		CommEnc.generate_Key(true);
	}

	// 0.2 restore keys
	public void restoreECCKey() {
		eccEnc.restoreKey(true);
	}

	public void restoreKey() {
		this.key = CommEnc.restore_Key(true);
	}

	/**
	 * @param network
	 * @param enc
	 * @return
	 */
	public String Pre_Filter() {
		try {
			BloomFilter<String> prefixBloomFilter = new FilterBuilder()
					.expectedElements((int) Math.pow(2, Params.prefix_len))
					.falsePositiveProbability(0.000000001)
					.hashFunction(HashMethod.Murmur3)
					.buildBloomFilter();
			Utils.hash_prefix_enc_mThreads(Integer.valueOf(0), DB_NAME, "server/server_cipher.txt", prefixBloomFilter,
					Params.THREADS);
			// System.out.println("Server::Pre_Filter - file bloom file generated");
			String path = "server/server_prefix_bloom";
			return path;
		} catch (IOException e) {
			e.printStackTrace();
		}
		return "Server::Pre_Filter - error";
	}

	// /**
	// * PIRԤ˷СϽԴ󼯺ϵǰ׺ڱؽй
	// * մ󼯺һĶ飬ڱؽй
	// *
	// * @param network
	// */
	// public void Recv_Pir_Filter(Network network) {// նԷBF, նԷǰ׺.
	// try {
	// // 1.նԷĶ鼯
	// network.d_in = new DataInputStream(network.sock.getInputStream());
	// System.out.println("ȴ󼯺һĶ鼯...");
	// network.receiveFile("server/server_pair_set");
	// // 2.Աǰ׺Ĳ¡
	// BloomFilter<String> filter = Utils.get_prefix_BF_mThreads(1, DB_NAME,
	// Params.THREADS);
	// // 3.Զ鼯Ͻйˣµݼ
	// Utils.filter_Pair_Set(filter, "server/server_pair_set", FILTERED_DB);

	// System.out.println("鼯Ϲ!");
	// } catch (IOException e) {
	// e.printStackTrace();
	// }
	// }

	// 1. Generate bloom file
	public String ECC_PSI_Rev_gen_prefix() {
		String path = "";
		this.generateECCKey();

		// if (Params.pirFilter) {// No
		// Recv_Pir_Filter(network);
		// } else if (Params.preFilter) {// This
		path = Pre_Filter();
		// }
		return path;
	}

	// 2. Generate server_cipher file
	public String ECC_PSI_Rev_gen_serv_cyph() {
		this.restoreECCKey();
		String path = "server/server_cipher.txt";
		// generate the server_cypher.txt file
		try {
			Utils.ECC_enc_dec_and_Write_mThreads(eccEnc, 0, true, DB_NAME, path, Params.THREADS);
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		return path;
	}

	// 3. Receive client cipher file (recv_client_cipher.txt)
	// 4. Send server cypher file (server_cipher.txt)

	// 5. Generate cuckoo or bloom file
	public String ECC_PSI_Rev_gen_cuckoo() {
		// System.out.println("Server::ECC_PSI_Rev_gen_cuckoo - starting cuckoo
		// filter");
		this.restoreECCKey();
		CuckooFilter<byte[]> filter;
		// if (Params.pirFilter) {
		// filter = Utils.sec_encrypt_and_CuckooWriter(0, FILTERED_DB, eccEnc,
		// Params.THREADS);
		// } else { // here
		filter = Utils.sec_encrypt_and_CuckooWriter(0,
				"server/recv_client_cipher.txt", eccEnc, Params.THREADS);
		// System.out.println("Server::ECC_PSI_Rev_gen_cuckoo - recv_client_cipher ");
		// }
		Utils.FilterWriter(filter, "server/server_cuckoo");
		// System.out.println("Server::ECC_PSI_Rev_gen_cuckoo - server_cuckoo file
		// generated");
		return "server/server_cuckoo";
	}

	public String ECC_PSI_Rev_gen_bloom() {
		// System.out.println("Server::ECC_PSI_Rev_gen_bloom - generate the final bloom
		// file");
		this.restoreECCKey();
		BloomFilter<String> bf;
		// if (Params.pirFilter) {
		// 	bf = Utils.sec_encrypt_and_BloomWriter(0, FILTERED_DB, eccEnc, Params.THREADS);
		// } else {
			bf = Utils.sec_encrypt_and_BloomWriter(0, "server/recv_client_cipher.txt", eccEnc, Params.THREADS);
		// }
		Utils.FilterWriter(bf, "server/server_bloom");
		return "server/server_bloom";
	}

	public String ECC_PSI_Unbalanced_gen_bloom() {
		this.generateECCKey();
		String path = "server/server_bloom";
		BloomFilter<String> bf = Utils.encrypt_and_BloomWriter(0, DB_NAME, eccEnc, Params.THREADS);
		Utils.FilterWriter(bf, "server/server_bloom");
		return path;
	}

	public String ECC_PSI_Unbalanced_gen_cuckoo() {
		this.restoreECCKey();
		String path = "server/server_cuckoo";
		CuckooFilter<byte[]> cf = Utils.encrypt_and_CuckooWriter(0, DB_NAME, eccEnc, Params.THREADS);
		Utils.FilterWriter(cf, path);
		return path;
	}

	public String ECC_PSI_Unbalanced_encrypt_client_cipher() throws FileNotFoundException {
		this.restoreECCKey();
		String path = "server/recv_client_cipher2.txt";
		// System.out.println("server::ECC_PSI_Unbalanced_encrypt_client_cipher - before
		// encryption");
		Utils.ECC_sec_enc_and_Write_mThreads(eccEnc, 0, true, "server/recv_client_cipher.txt",
				path, Params.THREADS);
		// System.out.println("server::ECC_PSI_Unbalanced_encrypt_client_cipher - after
		// encryption");
		return path;
	}

	// Paper without ECC
	public String PSI_Unbalanced_gen_bloom() {
		this.restoreKey();
		// System.out.println("Server::PSI_Unbalanced_gen_bloom - restored key: " +
		// this.key.toString());
		String path = "server/server_bloom";
		BloomFilter<String> bf = Utils.encrypt_and_BloomWriter(0, DB_NAME, key, Params.THREADS);
		Utils.FilterWriter(bf, "server/server_bloom");

		return path;
	}

	public String PSI_Unbalanced_gen_cuckoo() {
		this.restoreKey();
		String path = "server/server_cuckoo";
		CuckooFilter<byte[]> cf = Utils.encrypt_and_CuckooWriter(0, DB_NAME, key, Params.THREADS);
		Utils.FilterWriter(cf, path);
		return path;
	}

	public String PSI_Unbalanced_encrypt_client_cipher() throws FileNotFoundException {
		this.restoreKey();
		String path = "server/recv_client_cipher2.txt";
		// System.out.println("server::PSI_Unbalanced_encrypt_client_cipher - before
		// encryption");
		Utils.enc_dec_and_Write_mThreads(0, true, "server/recv_client_cipher.txt", "server/recv_client_cipher2.txt",
				key, Params.THREADS);
		// System.out.println("server::PSI_Unbalanced_encrypt_client_cipher - after
		// encryption");
		return path;
	}
}