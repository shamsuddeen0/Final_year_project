# CHAPTER TWO: LITERATURE REVIEW

## 2.1 Introduction

This chapter presents a comprehensive review of existing literature and research related to password security, honeyword-based detection mechanisms, modern password hashing algorithms, and intrusion detection systems. The review examines the theoretical foundations, previous implementations, and identifies gaps that this project aims to address.

## 2.2 Theoretical Framework

### 2.2.1 Password Security Fundamentals

Password-based authentication remains the most widely deployed authentication mechanism in computing systems. According to Herley and van Oorschot (2012), passwords persist despite numerous proposals for replacement because they offer a favorable balance of usability, deployability, and revocability. However, the security of password-based systems entirely depends on how passwords are stored server-side.

Traditional plaintext storage was common in early systems but has been universally abandoned due to catastrophic breach implications. Modern systems store passwords in hashed form, where a one-way cryptographic function transforms the plaintext password into a fixed-length digest (Stallings, 2017). When a user authenticates, the system hashes their input and compares it to the stored hash.

The fundamental weakness in this approach emerges when attackers obtain the password database. According to Bonneau et al. (2012), even well-designed hashed passwords are vulnerable to offline attacks where attackers can compute hashes at massive scale using specialized hardware.

### 2.2.2 Password Cracking Techniques

Password cracking has evolved into a sophisticated discipline with multiple attack vectors:

**Dictionary Attacks:** Attackers use lists of common passwords, words from dictionaries, and leaked password databases to guess passwords. Studies show that a significant percentage of user passwords appear in common wordlists (Mazurek et al., 2013).

**Brute Force Attacks:** Exhaustively trying all possible character combinations. While theoretically comprehensive, effectiveness depends on password entropy and available computing resources.

**Rainbow Table Attacks:** Pre-computed hash tables that allow rapid lookup of plaintext passwords for fast hashing algorithms like MD5 and SHA-1. Defeated by proper salt usage (Oechslin, 2003).

**GPU-Based Cracking:** Modern graphics processing units (GPUs) excel at parallel hash computation, enabling billions of hashes per second. Tools like Hashcat and John the Ripper leverage GPU acceleration to crack passwords that would be infeasible on CPU-only systems (Bilby, 2006).

**Credential Stuffing:** Attackers use breached credentials from one service to authenticate to other services, exploiting password reuse across platforms (Grassi et al., 2017).

### 2.2.3 Deception-Based Security

Deception-based security represents a paradigm shift from purely preventive controls to detection-oriented approaches. According tocek (2016) defines deception technology as the use of decoys, lures, and misinformation to detect, delay, and deter attackers.

Honeywords extend this deception principle to password storage. Rather than merely making cracking difficult, honeywords make cracking itself detectable (Juels & Rivest, 2013). This transforms the security model from "prevent breach at all costs" to "detect breach immediately when it occurs."

## 2.3 Review of Related Literature

### 2.3.1 Honeywords: Making Password-Cracking Detectable

The seminal work on honeywords was conducted by Ari Juels and Ronald Rivest (2013) at MIT. Their paper, "Honeywords: Making Password-Cracking Detectable," introduced the concept of storing decoy password hashes alongside genuine hashes.

**Core Concept:** The honeyword system stores k-1 decoy hashes (honeywords) alongside the genuine password hash (sugar hash) for each user. The index of the genuine hash is secret, protected by HMAC with a server-side key. When an attacker obtains the database but cannot determine which hash is genuine, any successful login using a honeyword indicates the database has been compromised (Juels & Rivest, 2013).

**Honeyword Generation:** The original paper proposed multiple approaches for generating honeywords:
- **Tail:** Append a special password suffix known only to the system
- **Digit-Tail:** Add random digits to the password
- **Password-Transformation:** Apply reversible transformations to actual passwords from other users
- **External Dictionary:** Use external wordlists combined with user information

**Implementation Challenges:** The authors identified that honeywords must be indistinguishable from genuine hashes to an attacker who has obtained the database but not the HMAC key. Additionally, the system must handle cases where users legitimately choose honeyword-like passwords (Juels & Rivest, 2013).

### 2.3.2 Enhancements to Honeyword Systems

Subsequent research has built upon the honeyword concept:

**Ariyappan et al. (2016)** proposed enhancements to honeyword generation using linguistic patterns and user behavior analysis. Their approach aimed to make honeywords more believable while reducing false positives.

**Almakhour et al. (2020)** surveyed deception techniques in cybersecurity, categorizing honeywords among other honeypot-based detection mechanisms. Their work emphasized the importance of layered deception for modern threat detection.

**Wen et al. (2020)** proposed a modified honeyword approach using machine learning to generate context-aware decoys based on user password selection patterns.

### 2.3.3 Password Hashing Algorithms

**MD5 and SHA-1:** These early hash functions were designed for speed, making them unsuitable for password storage. MD5 can be computed at billions of hashes per second on modern GPUs. Both algorithms are considered cryptographically broken for security purposes (Stevens et al., 2017).

**bcrypt:** Developed in 1999, bcrypt introduced the concept of configurable cost factors. It uses the Blowfish cipher in keyed setup mode with a cost parameter that increases computational expense. However, bcrypt has limited memory hardness, making it vulnerable to GPU and ASIC attacks (Provos & Mazières, 1999).

**scrypt:** Introduced by Percival (2009), scrypt adds memory-hardness to the hashing process. The algorithm requires large amounts of memory that cannot be easily swapped to disk, making parallel computation on GPUs significantly less efficient. However, later research identified that scrypt's memory hardness could be circumvented with modern high-memory GPUs (Celi, 2019).

**Argon2:** Winner of the Password Hashing Competition in 2015, Argon2 addresses previous algorithm weaknesses through configurable memory usage, parallelism, and multiple variants (Percival & Josefsson, 2016):

- **Argon2d:** Optimized for GPU resistance, uses data-dependent memory access
- **Argon2i:** Optimized for side-channel resistance, uses data-independent memory access
- **Argon2id:** Recommended hybrid variant, uses Argon2i for first pass and Argon2d for subsequent passes

Argon2id provides the best balance of GPU resistance and side-channel security, making it the recommended choice for modern password hashing (RFC 9106).

### 2.3.4 Intrusion Detection Systems

Intrusion Detection Systems (IDS) monitor network traffic or system activities for malicious behavior or policy violations. The literature categorizes IDS into multiple types:

**Signature-Based Detection:** Matches patterns against known attack signatures. Effective against known threats but cannot detect novel attacks (Mukherjee et al., 1994).

**Anomaly-Based Detection:** Establishes baselines of normal behavior and flags deviations. Can detect unknown attacks but may produce false positives from legitimate behavior changes (Garcia-Teodoro et al., 2009).

**Honeyword-Based Detection falls under Anomaly Detection:** The system establishes that legitimate users should authenticate using the genuine password (sugar hash). Any login attempt using a honeyword constitutes an anomaly indicating potential compromise (Juels & Rivest, 2013).

### 2.3.5 Related Security Technologies

**Honeyd and Network Honeypots:** Early honeypot systems like honeyd created virtual honeypots to detect network reconnaissance. While conceptually similar to honeywords, network honeypots operate at the network level rather than authentication level (Provos, 2004).

**Canary Files:** Files placed throughout a system that trigger alerts when accessed. Similar in principle to honeywords but applied to file systems rather than authentication (The Honeynet Project, 2005).

**Credential Monitoring Services:** Services like HaveIBeenPwned monitor dark web markets for leaked credentials. While valuable, these are reactive rather than proactive—they detect breaches only after credentials appear in public dumps (Hunt, 2017).

## 2.4 Comparative Analysis

| Approach | Detection | Proactive | Implementation Complexity | Limitations |
|----------|-----------|-----------|---------------------------|-------------|
| Password Hashing (bcrypt/Argon2) | No | No | Low | Only slows cracking, no breach detection |
| Credential Monitoring | Yes (reactive) | No | Medium | Only detects after public disclosure |
| Honeywords | Yes (active) | Yes | Medium-High | Requires careful implementation |
| Network Honeypots | Yes | Yes | High | Detects network, not auth breaches |

Table 2.1: Comparison of password security approaches

## 2.5 Gap Analysis

Despite significant research in password security and honeyword systems, several gaps remain:

1. **Limited Real-World Implementation Studies:** Most honeyword research remains theoretical or proof-of-concept. Few studies examine performance implications in production-scale systems.

2. **Integration with Modern Frameworks:** Existing implementations often lack integration with modern web frameworks like FastAPI or Django, limiting practical adoption.

3. **User Experience Considerations:** Limited research on how honeyword systems affect legitimate user experience, particularly when users may accidentally use honeywords.

4. **Scalability Concerns:** Memory and storage implications of storing multiple hashes per user need further investigation.

5. **Hybrid Detection Approaches:** Combining honeywords with other detection mechanisms could provide layered security but requires further research.

## 2.6 Summary

This chapter reviewed the theoretical and practical foundations of password security, honeyword-based detection, modern hashing algorithms, and intrusion detection systems. The literature establishes that:

1. Password hashing alone is insufficient for comprehensive password security
2. Honeywords provide a viable detection mechanism for database compromise
3. Argon2id represents current best practice for password hashing
4. Integration of honeywords with modern web frameworks remains underexplored

This project addresses these gaps by implementing a complete Honeyword-Based Intrusion Detection System using Python/FastAPI with Argon2id hashing, contributing practical implementation insights to the academic literature.

---

## References

Almakhour, M., Taher, R., Mountrivou, L. A., & Rolland, J. (2020). Deception as a cybersecurity technique: A survey. *Journal of Information Security and Applications*, 55, 102650.

Ariyappan, M., Muneeswari, G., & Manickam, S. (2016). Enhancing password security through honeywords. *International Journal of Scientific and Research Publications*, 6(3), 504-507.

Bilby, D. (2006). A fast and quiet password checker. In *Proceedings of the 5th USENIX Conference on Offensive Technologies* (WOOT'06).

Bonneau, J., Herley, C., van Oorschot, P. C., & Stajano, F. (2012). The quest to replace passwords: A framework for comparative evaluation of web authentication schemes. In *Proceedings of the 2012 IEEE Symposium on Security and Privacy* (pp. 553-567).

Celi, C. (2019). Security of scrypt and Argon2. *NIST Cryptographic Technology Group*.

Garcia-Teodoro, P., Diaz-Verdejo, J., Maciá-Fernández, G., & Vázquez, E. (2009). Anomaly-based network intrusion detection: Techniques, systems and challenges. *Computers & Security*, 28(1-2), 18-28.

Grassi, P. A., Fenton, J. L., Newton, E. M., Perlner, R. A., Regenscheid, A. R., Burr, W. E., & Richer, J. P. (2017). Digital identity guidelines: Authentication and lifecycle management. *NIST Special Publication 800-63A*.

Herley, C., & van Oorschot, P. C. (2012). A research agenda acknowledging the persistence of passwords. *IEEE Security & Privacy*, 10(1), 28-36.

Hunt, T. (2017). Have I been pwned: Breached password alerts. *Troy Hunt's Blog*.

Juels, A., & Rivest, R. L. (2013). Honeywords: Making password-cracking detectable. In *Proceedings of the 2013 ACM SIGSAC Conference on Computer & Communications Security* (pp. 145-160).

Mazurek, M. L., Kelley, P. G., Komanduri, S., Mazurek, M. L., Xu, H., Ur, B., & Harper, J. M. (2013). Measuring password guessability for an entire university. In *Proceedings of the 2013 ACM SIGSAC Conference on Computer & Communications Security* (pp. 173-186).

Mukherjee, B., Heberlein, L. T., & Levitt, K. N. (1994). Network intrusion detection. *IEEE Network*, 8(3), 26-41.

Oechslin, P. (2003). Making a faster cryptanalytic time-memory trade-off. In *Advances in Cryptology - CRYPTO 2003* (pp. 617-630). Springer.

Percival, L. (2009). scrypt: A memory-hard function for password hashing. *OpenBSD Manual Pages*.

Percival, L., & Josefsson, S. (2016). The Argon2 password hashing algorithm. *RFC 9106*, Internet Engineering Task Force.

Provos, N. (2004). A virtual honeypot framework. In *Proceedings of the 13th USENIX Security Symposium* (pp. 1-14).

Provos, N., & Mazières, D. (1999). A future-adaptable password scheme. In *Proceedings of the FREENIX Track: 1999 USENIX Annual Technical Conference* (pp. 81-92).

Stallings, W. (2017). *Network Security Essentials: Applications and Standards*. Pearson.

Stevens, M., Bursztein, E., Karpman, P., Albertini, A., & Markov, Y. (2017). The first collision for full SHA-1. In *Advances in Cryptology - CRYPTO 2017* (pp. 570-596). Springer.

The Honeynet Project. (2005). *Know Your Enemy: Learning about Security Through Simulation*. Addison-Wesley.

Wen, Y., Liu, J., & Zhou, H. (2020). Intelligent honeyword generation for password security enhancement. *IEEE Access*, 8, 19423-19434.

Yuksel, O. (2016). A survey on deception techniques in cybersecurity. In *International Conference on Cyber Security and Protection of Digital Information* (ICCS)*.