# Presentation Draft: Chapter 1 & 2

## Presentation Overview
- **Duration**: 10-15 minutes total
- **Format**: Walkthrough of Introduction and Literature Review

---

## SLIDE 1: Title Slide
**Project Title**: Honeyword-Based Intrusion Detection System
**Purpose**: Detect password database breaches in real-time using deception technology
**Presenter**: [Your Name]
**Supervisor Meeting**

---

## SLIDE 2: Background (Chapter 1.1)

### The Problem Context
- Password-based authentication is still the primary security method
- Even with hashing, databases can be compromised
- Attackers perform **offline attacks** to crack password hashes

### Current State
- MD5/SHA-1 are inadequate (too fast)
- bcrypt/scrypt help but don't solve the detection problem
- Once breached, attackers crack hashes at scale **undetected**

### The Gap
- No mechanism to detect when a database has been compromised
- Silent breach = extended attack time

---

## SLIDE 3: Problem Statement (Chapter 1.2)

### Four Key Problems

1. **Silent Database Compromise**
   - No detection until credentials appear in public dumps

2. **Lack of Real-Time Detection**
   - By the time discovered, attackers already moved laterally

3. **Inadequate Protection Against Offline Attacks**
   - GPU clusters make cracking feasible within hours/days

4. **No Alert Mechanism for Decoy Credentials**
   - Systems can't differentiate real vs. decoy password attempts

---

## SLIDE 4: Objectives (Chapter 1.3)

### Main Objective
Automated intrusion detection using honeyword technology

### Specific Objectives
1. **Secure Storage**: Implement Argon2id hashing (memory-hard, GPU-resistant)
2. **Honeyword Generation**: Create believable decoy hashes
3. **Honey-Checker**: HMAC-based mechanism to identify honeyword usage
4. **IDS Alerts**: Silent alerts when honeyword login detected
5. **Evaluation**: Test via simulated "mock breach" scenarios

---

## SLIDE 5: Scope (Chapter 1.4)

### What We're Building
- **Backend**: Python + FastAPI REST API
- **Database**: PostgreSQL
- **Hashing**: Argon2id
- **Detection**: Deception-based (honeywords)

### What We're NOT Building
- Client-side authentication
- Biometric integration
- Production deployment

### Testing
- Controlled virtual environment only
- Simulated data, no real credentials

---

## SLIDE 6: Significance (Chapter 1.5)

### Contributions
1. **Proactive Breach Detection**
   - Detect compromise immediately, not via public dumps

2. **Deception Technology**
   - Practical application of honeypot principles to authentication

3. **Academic Value**
   - Implementation reference for researchers

4. **Practical Proof-of-Concept**
   - Can be adapted to existing systems

---

## SLIDE 7: Literature Review - Password Security (2.2.1)

### Fundamentals
- Passwords persist due to usability, deployability, revocability
- Security depends on **server-side storage**
- Modern systems use one-way cryptographic hash functions

### The Weakness
- Once attackers obtain the database = offline attacks become possible
- Massive scale hash computation with specialized hardware

---

## SLIDE 8: Password Cracking Techniques (2.2.2)

### Attack Vectors
- **Dictionary Attacks**: Common passwords, leaked databases
- **Brute Force**: Exhaust all combinations
- **Rainbow Tables**: Pre-computed hash lookups (defeated by salt)
- **GPU-Based Cracking**: Billions of hashes/second (Hashcat, John the Ripper)
- **Credential Stuffing**: Reuse credentials across platforms

---

## SLIDE 9: Deception-Based Security (2.2.3)

### Paradigm Shift
- From **prevent breach** → to **detect breach immediately**
- Decoys, lures, misinformation

### Honeywords Concept
- Make cracking itself **detectable**
- If someone logs in with a honeyword → database was compromised

---

## SLIDE 10: Honeywords - Core Methodology (2.3.1)

### Juels & Rivest (2013)
- Store k-1 decoy hashes (honeywords) + 1 genuine hash (sugar hash)
- Index of genuine hash is secret (protected by HMAC + server key)
- If attacker cracks a honeyword and logs in → **DETECTED**

### Honeyword Generation Methods
- Tail: Append special suffix
- Digit-Tail: Add random digits
- Password-Transformation: Use other users' passwords
- External Dictionary: Wordlists + user info

---

## SLIDE 11: Password Hashing Algorithms (2.3.3)

### Evolution
| Algorithm | Issue |
|-----------|-------|
| MD5/SHA-1 | Too fast, cryptographically broken |
| bcrypt | Limited memory hardness |
| scrypt | Can be circumvented with high-memory GPUs |
| **Argon2id** | Winner of Password Hashing Competition 2015 |

### Why Argon2id?
- Configurable memory usage
- Parallelism support
- Best balance of GPU resistance + side-channel security

---

## SLIDE 12: Intrusion Detection Systems (2.3.4)

### Types
- **Signature-Based**: Known attack patterns
- **Anomaly-Based**: Deviations from normal behavior

### Honeyword-Based Detection = Anomaly Detection
- Legitimate users should use genuine password
- Any honeyword login = anomaly = potential compromise

---

## SLIDE 13: Gap Analysis (2.5)

### What's Missing in Literature
1. Limited real-world implementation studies
2. No integration with modern frameworks (FastAPI, Django)
3. Limited research on user experience
4. Scalability concerns with multiple hashes per user
5. Hybrid detection approaches

### Our Contribution
Complete implementation using Python/FastAPI + Argon2id

---

## SLIDE 14: Summary

### Chapter 1: Introduction
- Problem: Silent database compromise
- Solution: Honeyword-based detection system
- Tech Stack: Python/FastAPI, PostgreSQL, Argon2id

### Chapter 2: Literature Review
- Password security foundations
- Honeyword detection mechanism (Juels & Rivest 2013)
- Argon2id as current best practice
- Gap: Need modern framework implementation

---

## SLIDE 15: Questions?

### Key Points to Remember
- Honeywords detect database compromise, not prevent it
- HMAC protects the "sugar index"
- Argon2id = memory-hard, GPU-resistant
- If someone logs in with a honeyword → alert triggered

---

## Notes for Presentation

### Be Ready to Explain:
1. How does the Honey-Checker work?
2. What happens if a user accidentally creates a honeyword-like password?
3. How many honeywords per user?
4. How is the HMAC key protected?

### Common Questions:
- "What's the difference between Argon2d, Argon2i, Argon2id?"
- "Why FastAPI?"
- "How do you generate believable honeywords?"

---

## Methodology Summary (For Supervisor)

| Component | Technology | Purpose |
|-----------|------------|---------|
| Backend | Python + FastAPI | REST API |
| Database | PostgreSQL | Store hashes |
| Hashing | Argon2id | Memory-hard password hashing |
| Detection | Honeywords | Decoy-based intrusion detection |
| Index Protection | HMAC | Protect sugar hash location |
| Alerting | IDS | Silent alert on honeyword login |