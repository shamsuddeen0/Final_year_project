# Honeyword-Based Intrusion Detection System (IDS)
## Comprehensive Research Thesis - Part 1 (Expanded)

---

# TITLE PAGE

**Project Title:** Honeyword-Based Intrusion Detection System (IDS)  
**Institution:** Federal University of Technology Babura  
**Department:** Cyber Security  
**Course:** COS 409  
**Date:** April 2026  
**Author:** [Your Name]  

---

# ABSTRACT

Traditional password storage mechanisms, such as salted hashing with memory-hard functions like Argon2id, are designed to prevent the recovery of passwords after a database breach but provide no mechanism to detect when such a breach has occurred. This "detection gap" allows attackers to use stolen credentials long before the compromise is discovered. This research implements a Honeyword-Based Intrusion Detection System (IDS) based on the Juels and Rivest (2013) framework. By inserting statistically indistinguishable decoy passwords (honeywords) into the database, the system transforms the authentication layer into a high-precision sensor. 

The implemented system utilizes a characteristic-mimicking generator to ensure honeywords match the entropy and length of real passwords, and a dual-path cryptographic verification process using Argon2id and AES. Experimental results demonstrate a zero-false-positive detection rate: legitimate users never trigger alerts, while attackers using stolen honeywords are detected with high probability without being alerted to the detection. This work validates the efficacy of decoy credentials in providing immediate, stealthy, and absolute notification of database exfiltration.

---

# ACKNOWLEDGMENTS

I would like to thank the faculty of the Cyber Security department at the Federal University of Technology Babura for providing the resources and environment necessary to conduct this research.

---

# TABLE OF CONTENTS

1. **Chapter 1: Introduction**
   - 1.1 Background and Context
   - 1.2 Problem Statement
   - 1.3 Research Objectives
   - 1.4 Research Questions
   - 1.5 Scope and Limitations
   - 1.6 Significance of the Study
   - 1.7 Definition of Terms
   - 1.8 Thesis Structure
2. **Chapter 2: Literature Review**
   - 2.1 Evolution of Password Storage and Cryptographic Hardening
   - 2.2 Deep Dive into Argon2id
   - 2.3 Theoretical Analysis of the Honeyword Framework
   - 2.4 Comparative Analysis of Intrusion Detection Systems
   - 2.5 Security Concepts, Threats, and Vulnerabilities
   - 2.6 Summary and Research Gap
3. **Chapter 3: Methodology**
   - 3.1 Overview
   - 3.2 System Architecture and Infrastructure
   - 3.3 Detailed Design and Implementation
   - 3.4 Intrusion Detection and Stealth Analysis

---

# Chapter 1: Introduction

## 1.1 Background and Context
The security of user authentication systems constitutes the most critical layer of defense in modern digital infrastructure. As organizations migrate their core operations to the cloud and expand their digital footprints, the volume and sensitivity of stored user credentials have increased exponentially. The fundamental challenge of authentication security is the secure storage of passwords—a problem that has evolved over several decades of cryptographic advancement.

Historically, the primary defense against password theft has been the application of cryptographic one-way hash functions. In a standard implementation, a system does not store the password itself but rather a fixed-length representation (the hash) of that password. This ensures that even in the event of a database compromise, an attacker does not immediately possess the plaintext credentials. To further harden these systems, "salting"—the addition of a unique, random string to the password before hashing—was introduced to prevent the use of pre-computed "rainbow tables."

Despite these advancements, the current landscape of password cracking has undergone a paradigm shift. The democratization of high-performance computing, specifically the use of General-Purpose Graphics Processing Units (GPGPUs) and Application-Specific Integrated Circuits (ASICs), has shifted the balance of power in favor of the attacker. A modern GPU cluster can compute billions of hashes per second, rendering traditional algorithms like MD5 or SHA-1 obsolete and making even some salted hashes vulnerable to high-speed offline brute-force attacks.

While the industry has responded by adopting "memory-hard" functions—such as Argon2id—which significantly increase the computational cost of each guess, these measures are purely preventative. They increase the *time* required to crack a password, but they provide no mechanism for the system administrator to *know* that an attack is occurring. This is the "observability gap" in modern security: the system is blind to the theft and use of its own data once that data has been exfiltrated from the secure perimeter.

## 1.2 Problem Statement
The fundamental flaw in contemporary authentication storage is the total lack of intrusion detection capabilities within the data layer. Current security architectures are designed around the concept of "Hard Shell, Soft Center." Once a perimeter defense (such as a firewall or a Web Application Firewall) is bypassed and the database is exfiltrated, the data becomes a passive target.

The "detection gap" refers to the critical window of time between the exfiltration of a password database and the moment an attacker attempts to use the stolen data. In most catastrophic data breaches, organizations only discover the compromise after the damage is done—when stolen credentials are used to exfiltrate proprietary data, commit financial fraud, or launch further attacks within the network.

The core research problem addressed in this thesis is the development of a mechanism that can provide a mathematically guaranteed, zero-false-positive alert the moment an attacker attempts to use a stolen password database. This system must satisfy two conflicting requirements:
1. **High Observability**: It must provide a definitive signal of compromise.
2. **Absolute Stealth**: It must not inform the attacker that they have been detected, as any such signal would allow the attacker to refine their strategy and identify the real passwords by process of elimination.

## 1.3 Research Objectives
The overarching goal of this research is to design, implement, and evaluate a Honeyword-Based Intrusion Detection System. To achieve this, the following specific technical and theoretical objectives have been established:

### 1.3.1 Implementation of the Juels and Rivest Framework
The primary objective is to translate the theoretical framework proposed by Juels and Rivest (2013) into a functional, modern web application. This involves creating a system where "honeywords"—decoy passwords—are indistinguishable from the real password to anyone who does not possess the system's master encryption key.

### 1.3.2 Development of a Characteristic-Mimicking Generator
A key technical challenge is the generation of decoys that do not stand out. The research aims to develop a generator that analyzes the entropy, length, and character distribution of the real password to create honeywords that are statistically symmetric. If the real password contains a mix of uppercase letters, digits, and special characters, the honeywords must mirror this pattern to avoid detection via statistical analysis.

### 1.3.3 Guarantee of Zero-False-Positives
In an intrusion detection system, "noise" (false positives) is the primary cause of alert fatigue. A central objective of this project is to ensure that the detection mechanism is deterministic. Since a legitimate user only knows their real password and has no knowledge of the system-generated honeywords, any authentication attempt using a honeyword constitutes a mathematically certain indicator of an intrusion.

### 1.3.4 Engineering of a Deceptive Response Architecture
To maintain stealth, the system must implement a "deceptive success" or "honey-potting" response. The objective is to engineer a login flow where the attacker is granted access to a simulated or restricted environment upon providing a honeyword, thereby convincing the attacker that they have successfully guessed the correct password while the administrator is silently notified.

## 1.4 Research Questions
To guide the evaluation of the system, this research seeks to answer the following questions:
1. **Detection Probability**: To what extent does the number of honeywords ($N$) increase the probability of detecting an attacker who possesses the stolen database?
2. **Performance Overhead**: Does the addition of honeyword decryption and verification introduce a statistically significant delay in the authentication process for legitimate users?
3. **Indistinguishability**: Can a honeyword generated by a characteristic-mimicking algorithm be distinguished from a real password through basic frequency analysis or length-distribution checks?
4. **Stealth Efficacy**: Does the "deceptive success" response effectively prevent an attacker from identifying decoys compared to a standard "Invalid Credentials" response?

## 1.5 Scope and Limitations
This research focuses on the implementation of a proof-of-concept IDS using a Python-based FastAPI backend and a PostgreSQL database. 

**Included in Scope:**
- Design and implementation of a registration flow that generates and encrypts $N$ honeywords per user.
- Development of an authentication engine that handles the dual-path verification of real hashes and encrypted honeywords.
- Creation of a secure, out-of-band alerting system for logging critical security events.
- Theoretical analysis of the detection probabilities based on the number of decoys.

**Excluded from Scope:**
- **Multi-Factor Authentication (MFA)**: While MFA is a critical security layer, it is excluded from this specific research to focus exclusively on the detection of database exfiltration.
- **Physical Key Security**: This research assumes the existence of a secure environment for the master encryption key (e.g., an HSM or Vault) and does not cover the hardware security of the key itself.
- **Network-Level IDS**: The project is focused on the *data layer* IDS; it does not implement network-layer packet inspection or firewalling.

## 1.6 Significance of the Study
This research is significant as it addresses the critical "detection gap" inherent in traditional password storage. By shifting the security paradigm from passive protection to active detection, this project provides several key benefits:

1. **Reduction in Attacker Dwell Time**: Traditionally, database breaches are discovered months after the fact. This system provides a real-time alert the moment stolen credentials are used, drastically reducing the window an attacker has to operate undetected.
2. **High-Fidelity Alerting**: By providing a zero-false-positive guarantee, this research eliminates "alert fatigue" for security administrators. Every honeyword hit is a definitive indicator of compromise, allowing for immediate and confident incident response.
3. **Blueprint for Active Defense**: This work demonstrates how organizations can transform their most vulnerable assets—user credential stores—into active sensors, turning a liability (stolen data) into a strategic advantage (intrusion detection).
4. **Academic Contribution**: The implementation validates the theoretical framework of Juels and Rivest (2013) within a modern, asynchronous web architecture, proving the viability of decoy credentials in contemporary environments.

## 1.7 Definition of Terms
To ensure clarity for the reader, the following key terms are defined as they are used within this thesis:

- **Argon2id**: A memory-hard password hashing algorithm that resists both GPU-based brute-force attacks and side-channel timing attacks.
- **Honeywords**: Decoy passwords that are statistically indistinguishable from the real password but are known only to the system. They act as "tripwires" for intrusion detection.
- **Entropy**: A measure of the randomness or unpredictability of a password. Higher entropy makes a password more resistant to dictionary attacks.
- **Salting**: The process of adding a unique, random string to a password before hashing to ensure that identical passwords produce different hashes.
- **Zero-False-Positive**: A state where the system never triggers an alert for a legitimate user; every alert is guaranteed to be a true positive.
- **Dwell Time**: The duration of time between an initial breach and the moment the security team detects the intrusion.

## 1.8 Thesis Structure
The remainder of this thesis is organized as follows:
- **Chapter 2: Literature Review** provides an exhaustive analysis of password storage evolution, a deep dive into the Argon2id algorithm, and a theoretical exploration of the Juels and Rivest honeyword framework.
- **Chapter 3: Methodology** details the system architecture, the mathematical design of the honeyword generator, the cryptographic workflow, and the complexity analysis of the implementation.
- **Chapter 4: Implementation and Results** describes the experimental setup, the test scenarios used to validate the system, and the resulting data regarding detection rates and performance.
- **Chapter 5: Discussion and Conclusion** analyzes the findings, discusses the trade-offs of the implemented approach, and suggests avenues for future research.

---

# Chapter 2: Literature Review

## 2.1 Evolution of Password Storage and Cryptographic Hardening
The history of password storage is a constant arms race between system administrators and attackers. The evolution can be categorized into four distinct epochs of cryptographic hardening.

### 2.1.1 The Epoch of Plaintext and Simple Hashing
In the earliest iterations of user authentication, passwords were stored in plaintext files. Any unauthorized access to the server resulted in a total compromise of all accounts. This led to the adoption of one-way cryptographic hash functions like MD5 and SHA-1. These functions are designed to be "one-way," meaning it is computationally infeasible to reverse the hash to find the original password. However, these functions were designed for speed, which became their primary weakness. Attackers began using "Rainbow Tables"—massive pre-computed databases of hashes for billions of common passwords—to reverse hashes in milliseconds.

### 2.1.2 The Introduction of Salting
To defeat rainbow tables, the concept of "salting" was introduced. A salt is a unique, random string appended to the password before it is hashed. Because the salt is unique for every user, the same password results in a different hash for different users. This forces the attacker to compute a new set of hashes for every single user in the database, effectively neutralizing the advantage of pre-computed tables.

### 2.1.3 The Rise of Hardware-Accelerated Cracking
As compute power grew, the nature of attacks shifted from pre-computation to raw brute-force. The emergence of GPGPUs (General-Purpose Graphics Processing Units) allowed attackers to parallelize hash computations. While a CPU can compute a few thousand hashes per second, a high-end GPU can compute millions. Specialized ASIC (Application-Specific Integrated Circuit) hardware further accelerated this process, making even salted SHA-256 hashes vulnerable to high-speed cracking if the password entropy was low.

### 2.1.4 Memory-Hard Functions and the Modern Era
To counter hardware acceleration, the cryptographic community developed "memory-hard" functions. Unlike traditional hashes, which only require CPU cycles, memory-hard functions require a significant, fixed amount of RAM to compute. This makes them "expensive" to run in parallel on GPUs or ASICs, as the hardware must allocate dedicated memory for every concurrent thread. This drastically increases the cost and time for an attacker to perform brute-force attacks.

## 2.2 Deep Dive into Argon2id
For the purpose of this research, **Argon2id** was selected as the primary hashing algorithm. Argon2id is the result of the Password Hashing Competition (PHC) and is currently the gold standard recommended by OWASP and NIST.

### 2.2.1 Internal Mechanics
Argon2id is a hybrid of two other variants: Argon2i and Argon2d.
- **Argon2d**: Optimizes for resistance against GPU cracking attacks by using data-dependent memory access.
- **Argon2i**: Optimizes for resistance against side-channel attacks (like timing attacks) by using data-independent memory access.

By combining both, Argon2id provides a defense-in-depth approach. It ensures that the system is resistant to both the hardware acceleration of a remote attacker and the timing analysis of a local attacker.

### 2.2.2 Parameterization and Cost Tuning
The strength of Argon2id lies in its three primary tunable parameters:
1. **Time Cost (t)**: The number of iterations over the memory. Increasing this increases the time required to compute the hash.
2. **Memory Cost (m)**: The amount of memory used by the algorithm. This is the primary defense against ASIC/GPU attacks.
3. **Parallelism (p)**: The number of threads used to compute the hash.

In this implementation, these parameters are tuned to balance security with user experience, ensuring that a legitimate login takes roughly 100-500ms, while an attacker attempting billions of guesses would face a prohibitive computational cost.

## 2.3 Theoretical Analysis of the Honeyword Framework
The concept of honeywords, as formalized by Juels and Rivest (2013), shifts the security paradigm from "Prevention" to "Detection."

### 2.3.1 The Core Mechanism
A honeyword is a decoy credential that is functionally identical to a real password but is not known to the legitimate user. The system stores the real password hash and several encrypted honeywords. If an attacker steals the database, they cannot distinguish the real password hash from the encrypted honeywords without the system's master secret key.

### 2.3.2 Probability of Detection
The effectiveness of a honeyword system is measured by its **Detection Probability ($P_d$)**. If a user has one real password and $N$ honeywords, and an attacker attempts to guess the password by picking one of the entries in the stolen database, the probability of triggering an alert is defined by:

$$P_d = \frac{N}{N+1}$$

This formula demonstrates a diminishing return as $N$ increases. For $N=1$, the detection probability is 50%. For $N=5$, it rises to 83.3%. For $N=10$, it reaches 90.9%. This theoretical guarantee is the primary strength of the system: it provides a mathematical certainty of detection that does not rely on the complexity of the password itself.

### 2.3.3 The Deception Paradox and Stealth Requirements
A critical theoretical requirement of the Juels and Rivest model is the "Deception Paradox." In a standard authentication system, a wrong password results in an "Invalid Credentials" error. However, if the system denies access when a honeyword is used, it provides a "negative signal" to the attacker.

An attacker can use this signal to perform a process of elimination. By attempting various entries and observing which ones are rejected, the attacker can eventually isolate the real password. Therefore, the system must implement a **Stealth Response**: when a honeyword is hit, the system must mimic a successful login. This keeps the attacker in a state of uncertainty, effectively neutralizing their ability to filter out the decoys.

## 2.4 Comparative Analysis of Intrusion Detection Systems
To properly situate honeywords within the broader field of cybersecurity, it is necessary to compare them with other decoy-based systems.

| Feature | Honeypots | Canary Tokens | Honeywords |
| :--- | :--- | :--- | :--- |
| **Target Layer** | Network/System | File/URL/API | Credential/Data |
| **Detection Trigger** | Unauthorized Connection | File Access/DNS Query | Authentication Attempt |
| **Precision** | Medium (Noise from scans) | High | Absolute (Zero False Positives) |
| **Attacker Awareness** | High (if honey-pot is discovered) | Medium | Very High (Stealthy) |
| **Resource Cost** | High (requires full VM/Service) | Low (single token) | Very Low (extra DB rows) |
| **Primary Goal** | Divert and Observe | Notify of Breach | Detect Database Theft |

Unlike honeypots, which attract attackers to a fake system, honeywords protect the *actual* production database by turning the stolen data itself into the sensor.

## 2.5 Security Concepts, Threats, and Vulnerabilities
To properly evaluate the effectiveness of honeywords, the system must be analyzed within the context of established security models and the specific threats it is designed to mitigate.

### 2.5.1 Security Concepts and Models
The fundamental security model applied in this research is the **Defense-in-Depth** strategy. Rather than relying on a single monolithic barrier, security is layered. In the context of authentication, this project introduces a new layer: the *Detection Layer*. 

While the "Prevention Layer" (Argon2id) attempts to make password cracking computationally expensive, the "Detection Layer" (Honeywords) ensures that if prevention fails and the data is stolen, the system is notified of the breach. This transforms the security posture from a static defense to an active, observational defense.

### 2.5.2 Threat Modeling: The Adversary Profile
In this research, the threat model assumes a "Capable Adversary" who has achieved the following:
1. **Full Database Exfiltration**: The attacker has successfully bypassed perimeter defenses and obtained a copy of the user table and honeywords table.
2. **Knowledge of the Algorithm**: The attacker knows the system uses honeywords (Kerckhoffs's Principle) and understands the Juels and Rivest framework.
3. **Computational Resources**: The attacker possesses high-performance hardware (GPUs/ASICs) to attempt offline cracking of the hashes.

The primary **vulnerability** being addressed is the "Post-Exfiltration Blindness"—the inability of the system to detect that its data has been stolen until the stolen data is used for malicious purposes.

### 2.5.3 Analysis of Attacks
The system is designed to resist two specific categories of attacks:
- **Offline Brute-Force/Dictionary Attacks**: Mitigated by the memory-hard properties of Argon2id.
- **Credential Stuffing/Replay Attacks**: Using the stolen database to authenticate. This is the specific attack vector that honeywords are designed to detect. By inserting decoys, the system forces the attacker to guess between $N+1$ options, where $N$ options trigger a critical alert.

## 2.6 Summary and Research Gap
The literature review demonstrates that while password storage has evolved from plaintext to highly secure memory-hard functions like Argon2id, the focus has remained almost exclusively on *prevention*. 

Existing security systems focus on preventing the recovery of passwords through cryptographic hardening and protecting the database perimeter through firewalls and access controls. However, there is a critical gap in **post-compromise observability**. Once the database is exfiltrated, current systems are blind to the theft, leaving a massive "detection gap" that attackers exploit.

This project aims to fill this gap by implementing a Honeyword-Based IDS. By transforming the stolen data itself into a sensor, this research moves beyond mere prevention and provides a mechanism for absolute, zero-false-positive detection of credential theft, thereby providing organizations with the immediate observability they currently lack.

---

# Chapter 3: Methodology

## 3.1 Overview
The primary objective of this research is to implement a Honeyword-Based Intrusion Detection System (IDS) based on the principles established by Juels and Rivest (2013). The system is designed to detect unauthorized access to a user password database by inserting "honeywords"—fake passwords that appear legitimate to an attacker but are recognized by the system as traps.

## 3.2 System Architecture and Infrastructure
The system is developed using a modular architecture to ensure a clean separation between the application logic, the cryptographic operations, and the data persistence layer. This decoupling is essential for maintaining the "Master Secret" key in a separate security domain from the application logic.

### 3.2.1 Technology Selection and Justification
The choice of technologies was driven by the need for high concurrency, strong data consistency, and modern cryptographic primitives.

- **Backend Framework (FastAPI)**: FastAPI was selected over traditional frameworks like Flask or Django due to its asynchronous nature (`async/await`), which allows the system to handle multiple authentication requests concurrently without blocking. Given that cryptographic operations (like Argon2id) are computationally intensive, an asynchronous event loop prevents a single login attempt from stalling the entire system.
- **Database (PostgreSQL)**: PostgreSQL was chosen for its robustness and support for advanced indexing. To store honeywords, the system requires a one-to-many relationship between users and their decoys. PostgreSQL's relational integrity (foreign keys with `ON DELETE CASCADE`) ensures that when a user is deleted, their honeywords are purged atomically, preventing "orphan" decoys in the database.
- **Cryptography (Argon2id & AES-Fernet)**: 
    - **Argon2id** is utilized for the real password hashing. It is specifically chosen for its memory-hard properties, which effectively neutralize the advantage of ASIC-based attackers.
    - **AES (Fernet)** is utilized for the honeyword encryption. While Argon2id is a one-way hash, honeywords must be reversible (decryptable) by the system to verify the login. AES-256 in CBC mode with HMAC (via the Fernet specification) provides the necessary authenticated encryption to ensure honeywords cannot be tampered with in the database.

## 3.3 Detailed Design and Implementation

### 3.3.1 Data Schema and Normalization
To optimize for both security and performance, the database is normalized into two primary entities. This avoids the overhead of storing large arrays of encrypted strings within a single user row.

**The Users Entity:**
- `id` (Integer, Primary Key): Unique identifier.
- `username` (Varchar, Unique): The login identifier.
- `password_hash` (Text): The Argon2id hash.
- `created_at` (Timestamp): For auditing account age.

**The Honeywords Entity:**
- `id` (Integer, Primary Key): Unique identifier.
- `user_id` (Integer, Foreign Key): Links the decoy to a specific user.
- `encrypted_word` (Text): The AES-encrypted honeyword.
- `created_at` (Timestamp): For auditing.

An index (`idx_honeywords_user_id`) is applied to the `user_id` column in the honeywords table. This ensures that the retrieval of $N$ honeywords during the authentication phase occurs in $O(1)$ or $O(\log M)$ time, where $M$ is the total number of decoys in the system, preventing the database from becoming a bottleneck.

### 3.3.2 The Characteristic-Mimicking Generator
A central requirement of the Juels & Rivest model is that honeywords must be indistinguishable from the real password. A naive random string generator would produce honeywords that differ in length or character entropy, allowing an attacker to filter them out using basic statistical analysis.

The implemented **Characteristic-Mimicking Generator** follows a strict symmetrical logic:
1. **Entropy Analysis**: The generator first calculates the length $L$ of the real password.
2. **Set Derivation**: It analyzes the character set of the real password. If the password contains at least one digit, the pool of available characters for the honeywords is expanded to include all digits (0-9). The same logic is applied to uppercase, lowercase, and special characters.
3. **Symmetric Sampling**: The generator then samples $L$ characters from this derived pool. This ensures that if a user's password is `P@ssw0rd123` (11 characters, alphanumeric + symbol), the honeywords will also be 11 characters long and contain a similar mix of alphanumeric and symbol characters.
4. **Collision Avoidance**: The generator checks that the resulting honeyword is not identical to the real password.

**Formal Algorithm Logic:**
```python
Algorithm MimicHoneywords(real_password, count):
    L = length of real_password
    S = empty set
    For char in real_password:
        if char is digit: S = S U {0..9}
        if char is lowercase: S = S U {a..z}
        if char is uppercase: S = S U {A..Z}
        if char is symbol: S = S U {punctuation_set}
    
    result_list = []
    while size(result_list) < count:
        candidate = random_sample(S, size=L)
        if candidate != real_password:
            result_list.append(candidate)
    return result_list
```

### 3.3.3 Cryptographic Workflow and Sequence
The system operates through two primary cryptographic pipelines: the Registration Pipeline and the Authentication Pipeline.

#### Pipeline A: Registration (Setup)
1. **Input**: User provides `username` and `password`.
2. **Hashing**: The `CryptoManager` computes the Argon2id hash of the password.
3. **Decoy Generation**: The `HoneywordGenerator` creates $N$ honeywords based on the password's characteristics.
4. **Decoy Encryption**: Each honeyword is encrypted using the system-wide AES Master Key.
5. **Persistence**: The user record and the $N$ encrypted honeywords are committed to PostgreSQL.

#### Pipeline B: Authentication (Detection)
1. **Input**: User provides `username` and `password_attempt`.
2. **Primary Verification**: The system retrieves the stored Argon2id hash and verifies the `password_attempt`.
    - *If match:* Access granted (Normal Path).
3. **Decoy Verification**: If the primary check fails, the system retrieves all encrypted honeywords for that user.
4. **Decryption and Comparison**: Each encrypted honeyword is decrypted using the AES Master Key.
    - *If match:* Trigger Critical Alert $\rightarrow$ Grant Access (Stealth Path).
5. **Rejection**: If neither the real hash nor any honeyword matches, the system returns a `401 Unauthorized` response.

## 3.4 Intrusion Detection and Stealth Analysis

### 3.4.1 The Zero-False-Positive Proof
A false positive in an IDS occurs when a legitimate action is flagged as an attack. In this system, a false positive is mathematically impossible.
**Proof**: 
- Let $P_{real}$ be the real password.
- Let $H = \{h_1, h_2, \dots, h_N\}$ be the set of honeywords.
- The legitimate user $U$ only knows $P_{real}$.
- The system only triggers an alert if the input $I \in H$.
- Since $U$ does not know any $h \in H$, $U$ can never provide an input that matches a honeyword.
- Therefore, any trigger of the alert system must be caused by an actor who is not the legitimate user, specifically one who has obtained the honeywords from the stolen database.

### 3.4.2 Analysis of the Stealth Response
The "Stealth Response" is the system's primary defense against the "process of elimination" attack. If the system returned a "Wrong Password" error for honeywords, an attacker could simply try every entry in the stolen database and eliminate all those that produce an error, eventually leaving only the real password.

By returning a "Success" message for both the real password and the honeywords, the system maintains **Equivalence of Outcome**. To the attacker, there is no observable difference between a correct guess and a decoy guess. This forces the attacker to remain in a state of uncertainty, effectively rendering the stolen database a liability rather than an asset.

### 3.3.5 Complexity Analysis
The system's performance is analyzed in terms of time and space complexity:

- **Time Complexity (Registration)**: $O(T_{argon} + N \cdot T_{aes})$. The Argon2id hash is the dominant cost, as AES encryption is computationally trivial.
- **Time Complexity (Authentication)**: $O(T_{argon} + N \cdot T_{aes})$. Similar to registration, the bottleneck is the password hash verification. Since $N$ (the number of honeywords) is small, the additional AES decryptions do not introduce a perceptible delay for the user.
- **Space Complexity**: $O(U \cdot (S_{hash} + N \cdot S_{encrypted}))$, where $U$ is the number of users. The space overhead per user is linear relative to the number of honeywords $N$. Given that a typical password and its encrypted decoy are only a few dozen bytes, this is highly scalable.

## 3.6 System Requirements
To ensure the reliability and security of the implementation, the following hardware and software specifications are required.

### 3.6.1 Software Requirements
- **Operating System**: Linux (Ubuntu 22.04 LTS or similar)
- **Language Runtime**: Python 3.13.0 (Selected for latest security patches and performance improvements)
- **Web Framework**: FastAPI 0.110.0
- **Database Management System**: PostgreSQL 16.2
- **Cryptographic Libraries**: `argon2-cffi` (for Argon2id), `cryptography` (for AES-Fernet)

### 3.6.2 Hardware Requirements
- **CPU**: Quad-core 2.5GHz processor (minimum) to handle Argon2id computations.
- **RAM**: 8GB RAM (minimum) to support memory-hard hashing parameters.
- **Storage**: 20GB SSD for database persistence and logging.

## 3.7 Security Requirements Analysis and Risk Assessment
As a security-critical system, the Honeyword IDS must adhere to strict security requirements to prevent the system from becoming a vulnerability itself.

### 3.7.1 Security Requirements Analysis
The primary security goals of the system are as follows:
1. **Confidentiality of the Master Key**: The AES master key must remain secret. If the key is compromised, the attacker can distinguish honeywords from real hashes, neutralizing the system.
2. **Integrity of the Honeyword Table**: Attackers must not be able to modify honeywords to trigger false alerts or remove decoys to lower detection probability.
3. **Availability of the Alerting System**: The alerting mechanism must be decoupled from the authentication flow to ensure that an attack on the web server does not disable the reporting system.

### 3.7.2 Risk Assessment Methodology
The primary risk is the **Compromise of the Master Key**.

| Risk Scenario | Impact | Probability | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| Master Key is stored in plaintext on disk | Critical | High | Use Environment Variables or `.env` files (Development) $\rightarrow$ Transition to AWS Secrets Manager or HashiCorp Vault (Production). |
| Master Key is leaked via Version Control | Critical | Medium | Implement strict `.gitignore` policies and utilize secret scanning tools (e.g., Gitleaks). |
| Attacker obtains Key via Memory Dump | High | Low | Implement memory-zeroing for the key after use and use secure memory enclaves if hardware allows. |

The mitigation strategy for the most critical risk (Key Theft) is the transition to a Hardware Security Module (HSM) or a managed secret vault, ensuring the key never exists in plaintext on the application server.

## 3.8 UML Design Representations
To provide a visual mapping of the system logic, the following UML diagrams are designed for the final documentation:

1. **Use Case Diagram**: Illustrating the interactions between the User (Legitimate vs. Attacker) and the System (Registration, Authentication, Alerting).
2. **Sequence Diagram**: Detailing the dual-path verification process—from the initial password attempt to the either the Normal Path (Real Hash) or the Stealth Path (Honeyword Decryption).
3. **Entity-Relationship (ER) Diagram**: Visualizing the one-to-many relationship between the `Users` table and the `Honeywords` table, including the `idx_honeywords_user_id` index.
