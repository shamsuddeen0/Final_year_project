# Honeyword-Based Intrusion Detection System (IDS)
## Research Report

---

# Chapter 1: Introduction

## 1.1 Background
The security of user authentication systems is the cornerstone of digital privacy and corporate security. For decades, the primary defense against password theft has been the use of cryptographic one-way hashes. By storing a hash rather than a plaintext password, systems ensure that even if a database is compromised, the attacker must perform computationally expensive "brute-force" or "dictionary" attacks to recover the original credentials.

However, the landscape of password cracking has evolved. The advent of high-performance GPU clusters and specialized ASIC hardware has dramatically reduced the time required to crack traditional hashes. While modern algorithms like Argon2id have increased the cost of these attacks, they remain purely defensive. They prevent the *recovery* of the password but offer no mechanism to *detect* the theft. In most real-world breaches, organizations only discover a compromise after stolen credentials are used to commit fraud or exfiltrate data—often months after the initial theft.

## 1.2 Problem Statement
The fundamental flaw in current authentication storage is the lack of observability. There is a "detection gap" between the moment a database is exfiltrated and the moment an attacker attempts to use the stolen data. Current security measures (such as firewalls and 2FA) protect the *perimeter*, but they do not protect the *data* once it has left the perimeter.

The core problem this research addresses is: *How can a system provide a mathematically guaranteed, zero-false-positive alert the moment an attacker attempts to use a stolen password database, without tipping off the attacker that they have been detected?*

## 1.3 Objectives
The primary objective of this research is to implement and evaluate a Honeyword-Based Intrusion Detection System. The specific technical goals are:
1. **Implementation of the Juels and Rivest (2013) Framework**: Applying the concept of decoy passwords to a modern web architecture.
2. **Symmetry in Decoy Generation**: Developing a generator that ensures honeywords are statistically indistinguishable from the real password in terms of length and character entropy.
3. **Zero-False-Positive Guarantee**: Ensuring that no legitimate user can ever trigger a honeyword alert.
4. **Stealthy Response Architecture**: Implementing a "deceptive success" response that grants access to an attacker while triggering a background critical alert.

## 1.4 Scope of Work
This project focuses on the implementation of a proof-of-concept IDS using a Python-based FastAPI backend and a PostgreSQL database. The scope includes:
- The development of a registration flow that generates and encrypts honeywords.
- An authentication flow that distinguishes between real passwords and honeywords.
- An alerting system that logs intrusions to a secure audit trail.
The project does *not* cover the implementation of multi-factor authentication (MFA) or the physical security of the server hosting the master encryption key.

---

# Chapter 2: Literature Review

## 2.1 Evolution of Password Storage
Password security has evolved through several stages:
1. **Plaintext Storage**: Highly vulnerable; any breach results in total compromise.
2. **Simple Hashing (MD5, SHA-1)**: Faster to compute, making them vulnerable to rainbow tables and rapid brute-forcing.
3. **Salted Hashing**: Prevents rainbow table attacks by adding a unique random value to each password before hashing.
4. **Memory-Hard Functions (Argon2, bcrypt, scrypt)**: Designed to thwart GPU/ASIC attackers by requiring significant memory to compute, making the cost of hardware acceleration prohibitively expensive.

## 2.2 In-Depth Analysis of Argon2id
For this implementation, **Argon2id** was selected as the primary hashing algorithm. Argon2id is the winner of the Password Hashing Competition (PHC) and is recommended by OWASP. It combines:
- **Argon2d**: Resists GPU cracking attacks.
- **Argon2i**: Resists side-channel attacks.
By utilizing the "id" variant, the system achieves a hybrid defense that is optimal for password storage. The algorithm's strength lies in its configurable parameters: `time_cost` (iterations), `memory_cost` (RAM usage), and `parallelism` (threads).

## 2.3 The Honeyword Theory (Juels & Rivest)
The concept of honeywords transforms a password database from a passive target into an active trap. A honeyword is a decoy password that is functionally identical to a real password from the perspective of the system's authentication logic.

### 2.3.1 Detection Probability
If a user has one real password and $N$ honeywords, an attacker who has stolen the database and attempts to guess the correct password has a probability of $\frac{1}{N+1}$ of picking the real password, and a probability of $\frac{N}{N+1}$ of picking a honeyword. 

As $N$ increases, the probability that the attacker will trigger an alert increases significantly. For example, with $N=5$, there is an 83.3% chance that the first attempt by an attacker using a stolen record will trip the alarm.

### 2.3.2 The Deception Paradox
A critical component of honeywords is the "Deception Paradox." If the system were to deny access when a honeyword is used, the attacker would immediately know that the word they chose was a fake. This would allow the attacker to eliminate that word from their list and eventually find the real password. Therefore, the system must mimic a successful login, providing the attacker with a false sense of security while the administrator is notified.

## 2.4 Comparative Analysis of Detection Mechanisms
| Feature | Honeypots | Canary Tokens | Honeywords |
| :--- | :--- | :--- | :--- |
| **Target** | Entire System/Network | Specific File/URL | User Credentials |
| **Precision** | Medium (Noise possible) | High | Absolute (Zero FP) |
| **Stealth** | High | Medium | Very High |
| **Trigger** | Connection Attempt | File Access | Authentication Attempt |
| **Data Source** | Network Traffic | File System Events | Database Records |

Unlike honeypots, which attract attackers to a fake system, honeywords protect the *actual* production database by turning the stolen data itself into the sensor.

---

# Chapter 3: Methodology

## 3.1 Overview
The primary objective of this project is to implement a Honeyword-Based Intrusion Detection System (IDS) based on the principles established by Juels and Rivest (2013). The system is designed to detect unauthorized access to a user password database by inserting "honeywords"—fake passwords that appear legitimate to an attacker but are recognized by the system as traps.

## 3.2 System Architecture
The system is developed using a modular architecture to ensure a clean separation between the application logic, the cryptographic operations, and the data persistence layer.

### 3.2.1 Tech Stack
- **Backend Framework**: FastAPI (Python) was selected for its high performance and native support for asynchronous operations.
- **Database**: PostgreSQL was utilized for relational data storage, ensuring ACID compliance and efficient indexing.
- **Cryptography**:
    - **Argon2id**: Used for hashing real passwords due to its resistance against GPU/ASIC cracking and side-channel attacks.
    - **AES (Advanced Encryption Standard)**: Used via the Fernet specification to encrypt honeywords, ensuring that only the system possessing the master secret key can identify the honey-traps.

## 3.3 Design and Implementation

### 3.3.1 Data Schema
The database is structured into two primary entities:
1. **Users Table**: Stores the `username` and the `password_hash` (Argon2id).
2. **Honeywords Table**: A one-to-many relationship linked to the user, storing `encrypted_word` values. This separation allows the system to generate a variable number of honeywords per user to increase the attacker's uncertainty.

### 3.3.2 The Honeyword Generation Process
To prevent an attacker from distinguishing honeywords from the real password through statistical analysis, the system employs a **Characteristic-Mimicking Generator**. 

**Pseudo-code for Generation Algorithm:**
```python
Algorithm GenerateHoneywords(real_password, count):
    1. Extract length L = len(real_password)
    2. Initialize set S = {characters in real_password}
    3. For each char in real_password:
       If char is digit, S.update(AllDigits)
       If char is lower, S.update(AllLowercase)
       If char is upper, S.update(AllUppercase)
       If char is symbol, S.update(AllSymbols)
    4. While honeyword_list.size < count:
       Candidate = RandomSelection(S, length=L)
       If Candidate != real_password:
           Add Candidate to honeyword_list
    5. Return honeyword_list
```
By analyzing the character entropy and length of the original password, the generator ensures that honeywords are visually and statistically indistinguishable from the real credential.

### 3.3.3 Cryptographic Workflow
The system implements a dual-path verification process:

1. **Registration Phase**:
    - The real password is hashed using **Argon2id** and stored.
    - The generator creates $N$ honeywords.
    - These honeywords are encrypted using a system-level secret key via **AES** and stored in the database.

2. **Authentication Phase**:
    - Upon login, the system first performs a constant-time verification against the Argon2id hash.
    - If the real password check fails, the system decrypts all associated honeywords for that user.
    - If the input matches a decrypted honeyword, the system recognizes an intrusion.

### 3.3.4 Complexity Analysis
- **Registration Complexity**: $O(H + N \cdot E)$, where $H$ is the cost of the Argon2id hash and $E$ is the encryption cost per honeyword.
- **Authentication Complexity**: $O(H + N \cdot D)$, where $H$ is the hash verification cost and $D$ is the decryption cost per honeyword. Since $N$ is typically small (e.g., 5-10), the overhead is negligible.

## 3.4 Intrusion Detection and Alerting
The core value of the system lies in its ability to provide **Zero False Positives**. Because a legitimate user only knows their real password, any attempt to authenticate using a honeyword is a definitive indicator of a database compromise.

### 3.4.1 Stealth and Deception
To avoid alerting the attacker that they have been detected, the system implements a **Stealth Response**:
- When a honeyword is hit, the system returns a `Login Successful` response.
- Simultaneously, a **Critical Intrusion Alert** is triggered in the background.

### 3.4.2 Alerting Mechanism
The alerting system is decoupled from the user response. It logs the following metadata to a secure audit trail:
- **User Identity**: The account being targeted.
- **Honeyword Signature**: Which specific fake password was used.
- **Source Metadata**: The IP address and timestamp of the attack.

---

# Chapter 4: Implementation and Results

## 4.1 Implementation Environment
The system was implemented in a virtualized Linux environment using Python 3.13. The PostgreSQL database was hosted locally to simulate a production environment. 

## 4.2 Test Case Design
To evaluate the efficacy of the system, three distinct test scenarios were developed:

### Test Case 1: Legitimate User Access
- **Scenario**: A registered user provides the correct real password.
- **Expected Result**: Access granted, no alert triggered.
- **Actual Result**: System verified Argon2id hash; access granted successfully.

### Test Case 2: Unauthorized Access Attempt (Blind Guessing)
- **Scenario**: An attacker attempts to login with a password that is neither the real password nor a honeyword.
- **Expected Result**: Access denied, no alert triggered.
- **Actual Result**: Both Argon2id and AES checks failed; `401 Unauthorized` response returned.

### Test Case 3: Database Compromise Simulation (Honeyword Hit)
- **Scenario**: An attacker has exfiltrated the database, decrypted a honeyword using the stolen system key, and attempts to login.
- **Expected Result**: Access granted (stealth), Critical Alert triggered.
- **Actual Result**: Real password check failed $\rightarrow$ Honeyword check succeeded $\rightarrow$ User received `Login Successful` $\rightarrow$ `intrusion_alerts.log` recorded a CRITICAL event.

## 4.3 Result Analysis
The experimental results demonstrate that the system achieves its primary objective of **Zero False Positives**. The stealth mechanism successfully deceived the simulated attacker, while the alerting system provided an immediate notification of the breach.

---

# Chapter 5: Discussion and Conclusion

## 5.1 Discussion
The implementation proves that honeywords are a viable method for transforming a passive database into an active IDS. The primary trade-off is the storage overhead; for every user, the database must store $N$ additional encrypted strings. However, given the small size of passwords, this overhead is trivial compared to the security benefit.

A potential limitation is the "Master Secret" problem: if the attacker steals both the database and the system-level AES key, they can identify which passwords are honeywords. To mitigate this, the secret key should be stored in a Hardware Security Module (HSM) or a secure vault.

## 5.2 Conclusion
This research successfully implemented a Honeyword-Based Intrusion Detection System. By integrating Argon2id for security and AES for decoy management, the system provides a robust mechanism for detecting database exfiltration. The project validates the Juels and Rivest theory that decoy credentials can offer an absolute guarantee of intrusion detection.

## 5.3 Future Work
Future iterations of this system could include:
- **Dynamic Honeyword Scaling**: Adjusting $N$ based on the user's risk profile.
- **Automatic Account Locking**: Automatically disabling an account's real password upon a honeyword hit to prevent further access.
- **Integration with SIEM**: Connecting the alert system to a Security Information and Event Management (SIEM) tool for real-time SOC response.
