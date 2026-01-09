# AI-Enhanced Password Security Tool

A cybersecurity research project exploring how AI can be leveraged to conduct intelligent, targeted password attacks by analyzing user social media activity—and how to defend against them.

## Research Questions

1. How can AI be used to conduct attacks on passwords?
2. What are the limitations of AI-powered password attacks?

## Key Findings

Traditional brute-force attacks on a 16-character password would require testing **3.72 × 10³⁷** combinations. Using AI-powered analysis of social media posts, the search space was reduced to **18,360 candidates**—a reduction factor of **~10³³**, making the attack computationally feasible.

## How It Works

### Attack Simulation (Educational)

1. **Keyword Extraction**: GPT-3.5 analyzes user posts to extract personal information (names, locations, hobbies, dates, relationships)

2. **Candidate Generation**:
   - Combines extracted keywords (1-2 word combinations)
   - Applies leet speak substitutions (`a→@`, `e→3`, `i→1`, `o→0`, `s→$`)
   - Appends common patterns (`123`, `!`, `2024`, etc.)

3. **Comparison**: Uses Levenshtein distance to find exact or close matches

### Defense Mechanisms

- **Password Strength Validation**: Enforces modern requirements (8+ chars, mixed case, numbers, special chars)
- **Post Content Warning**: Alerts users if they're about to post content containing parts of their password
- **Vulnerability Scanning**: Users can check if their password is vulnerable to AI-based attacks

## Tech Stack

- Python 3
- OpenAI GPT-3.5-turbo API
- Levenshtein (string distance)
- JSON (data persistence)

## Installation

```bash
# Clone the repository
git clone https://github.com/azharsal/ai-password-security.git
cd ai-password-security

# Install dependencies
pip install openai python-Levenshtein

# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Run the application
python AIpassword.py
```

## Usage

The tool includes a simulated social media platform ("FakeBook") to demonstrate the vulnerability:

```
1. Sign in / Create Account
2. Make posts (with password-content warnings)
3. Check password strength (runs AI attack simulation)
4. View vulnerability report
```

## Project Structure

```
├── AIpassword.py      # Main application
├── accounts.json      # Test user accounts (sample data)
├── posts.json         # Sample social media posts
└── README.md
```

## Security Implications

This project demonstrates that:
- Passwords based on personal information are increasingly vulnerable
- AI can automate what previously required manual profiling
- Multi-factor authentication and password managers are essential

## Recommended Mitigations

1. Use **password managers** with randomly generated passwords
2. Enable **multi-factor authentication** (MFA)
3. Avoid using personal information in passwords
4. Use **hardware security keys** (FIDO2)

## Disclaimer

This tool is for **educational and research purposes only**. It demonstrates vulnerabilities to promote better security practices. Do not use these techniques for unauthorized access.

## What I Learned

- AI/ML integration with OpenAI APIs
- Cybersecurity attack vectors and defense strategies
- Natural language processing for information extraction
- String similarity algorithms (Levenshtein distance)
- Ethical considerations in security research
