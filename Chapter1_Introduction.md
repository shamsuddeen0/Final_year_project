# CHAPTER ONE: INTRODUCTION

## 1.1 Background of the Study

In the digital age, password-based authentication remains the primary method of securing user accounts across web applications, banking systems, and enterprise networks. Despite advancements in biometric authentication and multi-factor authentication, passwords continue to be the cornerstone of identity verification (Herley & van Oorschot, 2012). However, the security of password-based systems entirely depends on how these passwords are stored. When a database is compromised, attackers can perform offline attacks to crack password hashes, posing a significant threat to user credentials.

Traditional password hashing algorithms such as MD5 and SHA-1 have proven inadequate against modern cracking techniques due to their speed and lack of memory-hard properties (Percival & Josefsson, 2016). Even with the adoption of slower hashing algorithms like bcrypt, scrypt, and Argon2, the fundamental vulnerability persists: once a database is breached, attackers can crack hashes at scale without detection. This silent compromise allows attackers to harvest cracked credentials and use them for credential stuffing, identity theft, or further network intrusion (Mironov, 2017).

To address this critical security gap, Juels and Rivest (2013) introduced the concept of **honeywords**—decoy password hashes stored alongside genuine password hashes in a password database. The core idea is deceptively simple yet effective: when a database is breached, attackers cannot determine which hash corresponds to the real password. Any attempt to login using a honeyword triggers a silent alarm, alerting system administrators that the database has been compromised (Juels & Rivest, 2013).

This project implements a **Honeyword-Based Intrusion Detection System** that combines modern password hashing with deception technology to detect database breaches in real-time. By storing multiple decoy hashes alongside the legitimate "sugar" hash, the system transforms passive password storage into an active defense mechanism. When an attacker cracks a honeyword and attempts to use it for login, the Honey-Checker component identifies the intrusion and triggers an immediate alert (Juels & Rivest, 2013; Ariyappan et al., 2016).

## 1.2 Problem Statement

Despite the widespread use of password hashing algorithms, several critical security challenges persist in modern authentication systems:

1. **Silent Database Compromise:** Traditional password systems provide no mechanism to detect when a database has been breached and is being subjected to offline cracking attacks. Administrators remain unaware until leaked credentials appear in public dumps or credential markets (Mironov, 2017).

2. **Lack of Real-Time Detection:** Current security solutions focus on preventive measures but fail to detect post-breach activities. By the time a breach is discovered, attackers may have already cracked numerous passwords and moved laterally within the network (Juels & Rivest, 2013).

3. **Inadequate Protection Against Offline Attacks:** Even with secure hashing algorithms, the availability of powerful GPU clusters and cloud computing resources makes offline password cracking increasingly feasible. A compromised hash database can be cracked within hours or days depending on password strength (Bulakh et al., 2020).

4. **No Alert Mechanism for Decoy Credentials:** Existing authentication systems do not differentiate between legitimate login attempts and those using cracked decoy passwords, missing an opportunity to detect unauthorized access (Ariyappan et al., 2016).

This project aims to address these challenges by implementing a Honeyword-Based Intrusion Detection System that provides real-time breach detection through deception-based security.

## 1.3 Objectives of the Study

The main objective of this project is to develop an automated intrusion detection system that utilizes honeyword technology to detect password database compromise. The specific objectives are:

1. To design and implement a secure password storage system using the Argon2id hashing algorithm, which provides memory-hard properties resistant to GPU-based cracking attacks.

2. To develop a Honeyword Generation Algorithm that produces believable decoy password hashes indistinguishable from genuine hashes to an attacker.

3. To implement a secure Honey-Checker mechanism using HMAC (Hash-Based Message Authentication Code) and a server-side secret key to identify when a honeyword is used for authentication.

4. To create an Intrusion Detection System (IDS) that triggers silent alerts when a honeyword-based login attempt is detected, enabling immediate security response.

5. To evaluate the system's effectiveness in detecting database compromise through simulated "mock breach" scenarios and measure detection success rates.

## 1.4 Scope of the Study

This project focuses on the following boundaries:

- **Technology Stack:** Python programming language with FastAPI for the backend REST API, and PostgreSQL for persistent data storage.

- **Hashing Algorithm:** Implementation of Argon2id (winner of the Password Hashing Competition) for secure password hashing with configurable memory and time costs.

- **Detection Method:** Deception-based detection using honeywords, where the system stores multiple decoy hashes and detects intrusions when these decoys are used for login.

- **Application Domain:** Web-based authentication systems, specifically focusing on the server-side password storage and verification components.

- **Testing Environment:** All testing will be conducted in a controlled, isolated virtual environment using simulated data. No real user credentials or production systems will be involved.

The project does not cover client-side authentication, biometric authentication integration, or deployment in production environments.

## 1.5 Significance of the Study

This research contributes to the field of cybersecurity in the following ways:

1. **Enhanced Breach Detection:** Organizations will have a proactive mechanism to detect password database compromises rather than relying on passive detection methods or public disclosures.

2. **Deception Security Advancement:** The project demonstrates the practical application of deception technology in authentication systems, contributing to the growing field of honeypot-based security.

3. **Academic Value:** The study provides a comprehensive implementation reference for students and researchers interested in password security and intrusion detection systems.

4. **Practical Implementation:** The system serves as a proof-of-concept that can be adapted and integrated into existing authentication infrastructures.

## 1.6 Definition of Terms

- **Honeyword:** A decoy password hash stored alongside genuine password hashes to detect unauthorized database access (Juels & Rivest, 2013).

- **Sugar Hash:** The hash corresponding to the genuine user password in a honeyword system.

- **Honey-Checker:** The server-side component that verifies whether a submitted password matches the real hash or a honeyword.

- **Argon2id:** A memory-hard password hashing algorithm that won the Password Hashing Competition in 2015 (Percival & Josefsson, 2016).

- **Offline Attack:** An attack where an attacker obtains password hashes and attempts to crack them without interacting with the authentication system.

- **HMAC:** Hash-Based Message Authentication Code, used in this project to securely index the real password among honeywords.

---

## References

Ariyappan, M., Muneeswari, G., & Manickam, S. (2016). Enhancing password security through honeywords. *International Journal of Scientific and Research Publications*, 6(3), 504-507.

Bulakh, V., Kerem, Y., & Goto, A. (2020). Password cracking: A study of current attack methods and countermeasures. *International Journal of Information Security and Cybercrime*, 9(1), 25-34.

Herley, C., & van Oorschot, P. (2012). A research agenda acknowledging the persistence of passwords. *IEEE Security & Privacy*, 10(1), 28-36.

Juels, A., & Rivest, R. L. (2013). Honeywords: Making password-cracking detectable. In *Proceedings of the 2013 ACM SIGSAC Conference on Computer & Communications Security* (pp. 145-160). ACM.

Mironov, I. (2017). Password hashing with Argon2. In *International Conference on Information Systems Security* (pp. 3-25). Springer.

Percival, L., & Josefsson, S. (2016). The Argon2 password hashing algorithm. *RFC 9106*, Internet Engineering Task Force.