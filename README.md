# Wi-Fi Profile Auditor

A lightweight Windows security utility built with Python for inspecting saved Wi-Fi profiles and auditing locally stored wireless credentials.

## Features

- List saved Wi-Fi profiles
- Inspect authentication and cipher configuration
- View a selected profile's stored Wi-Fi password
- Handle spaces, apostrophes, and Unicode profile names
- Interactive terminal interface
- Confirmation before displaying stored credentials
- Automated unit tests
- GitHub Actions CI
- No third-party Python dependencies

## Requirements

- Windows
- Python 3.14+
- Saved Wi-Fi profiles
- Windows `netsh` WLAN support

No third-party Python packages are required.

## Usage

Run the application from PowerShell:

    python wifi_auditor.py

The application provides the following menu:

    ╔══════════════════════════════════════╗
    ║        WI-FI PROFILE AUDITOR         ║
    ║        Windows Security Utility      ║
    ╚══════════════════════════════════════╝

    Saved profiles: 13

      [1] List saved profiles
      [2] Inspect profile
      [3] View saved password
      [Q] Exit

### 1. List Saved Profiles

Displays all Wi-Fi profiles currently saved on the Windows system.

Example:

    Saved Wi-Fi Profiles
    ------------------------
     1. Galaxy M 5G
     2. Sangeeta_Jio_5G
     3. Sangeeta_5G
     4. Sangeeta's Galaxy M 5G
     5. Shishir's Galaxy A
     ...
    Total profiles: 13
### 2. Inspect Profile

Displays security and connection information for a selected Wi-Fi profile.

The tool extracts:

- Connection mode
- Authentication method
- Cipher configuration

Example:

    ┌─ Profile Information ────────────────────────────┐
    │ Profile        : ExampleWiFi                     │
    │ Connection     : Connect automatically           │
    │ Authentication : WPA3-Personal                   │
    │ Cipher         : GCMP-256, GCMP, CCMP            │
    └──────────────────────────────────────────────────┘

### 3. View Saved Password

Allows an authorized local user to view the password stored for a selected Wi-Fi profile.

Before displaying the credential, the application requires explicit confirmation:

    WARNING: This displays a credential stored on this computer.
    Use this only on systems you own or are authorized to administer.

    Continue? [y/N]:

If the user selects `N`, the credential is not displayed:

    Password display cancelled.

## Testing

The project uses Python's built-in `unittest` framework.

Run the complete test suite with:

    python -m unittest discover -s tests -v

Current tests cover:

- Wi-Fi profile parsing
- Unicode profile names
- Empty profile output
- Multiple profile detection

Example successful test output:

    test_empty_profile_output ... ok
    test_profile_count ... ok
    test_profile_parsing ... ok
    test_unicode_profile ... ok

    ----------------------------------------------------------------------
    Ran 4 tests in 0.002s

    OK

## GitHub Actions
The project includes GitHub Actions CI.

The workflow automatically runs the test suite when code is:

- Pushed to GitHub
- Submitted through a pull request

Workflow:

    Push / Pull Request
            ↓
    GitHub Actions
            ↓
    Python 3.14
            ↓
    Automated Tests
            ↓
    Pass / Fail

Workflow file:

    .github/workflows/ci.yml


## Project Structure

    wifi-profile-auditor/
    │
    ├── .github/
    │   └── workflows/
    │       └── ci.yml
    │
    ├── tests/
    │   └── test_wifi_auditor.py
    │
    ├── .gitignore
    ├── README.md
    └── wifi_auditor.py

## Technical Details

The application uses Windows `netsh` commands to retrieve locally stored WLAN profile information.

Examples of the commands used internally include:

    netsh wlan show profiles

and:

    netsh wlan show profile name="<profile>"

For authorized credential recovery, the application uses:

    netsh wlan show profile name="<profile>" key=clear

The Python implementation executes commands without using a shell, reducing command-injection risk from profile names.

## Error Handling

The application validates user selections before accessing a profile.

Invalid menu selections are rejected:

    Invalid option. Choose 1, 2, 3, or Q.

Invalid profile numbers are also rejected:

    Invalid profile number.


## Limitations

- Windows-only
- Depends on Windows `netsh wlan`
- Requires locally saved Wi-Fi profiles
- Output parsing depends on the English `netsh` field names
- Does not support Linux or macOS
- Does not perform Wi-Fi password cracking
- Does not perform wireless penetration testing
- Does not access remote computers

## Learning Objectives

This project demonstrates practical cybersecurity and Python development concepts including:

- Python scripting
- Windows networking
- WLAN profile inspection
- Command execution
- Subprocess management
- Regular-expression parsing
- Unicode handling
- Input validation
- Security-conscious credential handling
- Automated testing
- Continuous integration with GitHub Actions

## Project Goal

The goal of Wi-Fi Profile Auditor is to provide a small, practical Windows security utility while demonstrating how Python can interact with native Windows networking tools.

The project is intentionally lightweight and focuses on doing one task well rather than introducing unnecessary dependencies or infrastructure.

## Security Note

Wi-Fi credentials displayed by this application are sensitive information.

Only use the credential viewing functionality on systems you own or are explicitly authorized to administer.

Avoid sharing terminal output containing real passwords in screenshots, issue reports, GitHub repositories, or public documentation.

## License

For educational and authorized security testing purposes.