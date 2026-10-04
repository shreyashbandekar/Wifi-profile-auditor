import re
import subprocess


def run_netsh(*args):
    try:
        result = subprocess.run(
            ["netsh", *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        )
        return result.stdout

    except FileNotFoundError:
        raise RuntimeError("The Windows netsh command was not found.")

    except subprocess.CalledProcessError:
        raise RuntimeError("Unable to retrieve Wi-Fi information from netsh.")


def get_profiles():
    output = run_netsh("wlan", "show", "profiles")
    return re.findall(r"All User Profile\s*:\s*(.+)", output)


def show_profiles(profiles):
    print("\nSaved Wi-Fi Profiles")
    print("-" * 24)

    for number, profile in enumerate(profiles, 1):
        print(f"{number:>2}. {profile}")

    print(f"\nTotal profiles: {len(profiles)}")


def select_profile(profiles):
    selection = input("\nSelect a profile number: ").strip()

    if selection.isdigit() and 1 <= int(selection) <= len(profiles):
        return profiles[int(selection) - 1]

    print("Invalid profile number.")
    return None


def show_profile(profile):
    output = run_netsh(
        "wlan",
        "show",
        "profile",
        f"name={profile}",
    )

    values = {}

    for line in output.splitlines():
        if ":" not in line:
            continue

        key, value = map(str.strip, line.split(":", 1))

        if key in {"Connection mode", "Authentication", "Cipher"}:
            values.setdefault(key, []).append(value)

    print("\n┌─ Profile Information " + "─" * 28 + "┐")
    print(f"│ Profile        : {profile}")
    print(
        f"│ Connection     : "
        f"{', '.join(dict.fromkeys(values.get('Connection mode', ['Unknown'])))}"
    )
    print(
        f"│ Authentication : "
        f"{', '.join(dict.fromkeys(values.get('Authentication', ['Unknown'])))}"
    )
    print(
        f"│ Cipher         : "
        f"{', '.join(dict.fromkeys(values.get('Cipher', ['Unknown'])))}"
    )
    print("└" + "─" * 50 + "┘")


def show_password(profile):
    print("\nWARNING: This displays a credential stored on this computer.")
    print("Use this only on systems you own or are authorized to administer.")

    confirm = input("Continue? [y/N]: ").strip().lower()

    if confirm != "y":
        print("Password display cancelled.")
        return

    output = run_netsh(
        "wlan",
        "show",
        "profile",
        f"name={profile}",
        "key=clear",
    )

    match = re.search(r"Key Content\s*:\s*(.*)", output)

    print("\n┌─ Stored Credential " + "─" * 27 + "┐")
    print(f"│ Profile : {profile}")

    if match:
        print(f"│ Password: {match.group(1).strip()}")
    else:
        print("│ Password: Not available")

    print("└" + "─" * 50 + "┘")


def main():
    profiles = get_profiles()

    while True:
        print("\n╔══════════════════════════════════════╗")
        print("║        WI-FI PROFILE AUDITOR         ║")
        print("║        Windows Security Utility      ║")
        print("╚══════════════════════════════════════╝")

        print(f"\nSaved profiles: {len(profiles)}")
        print("\n  [1] List saved profiles")
        print("  [2] Inspect profile")
        print("  [3] View saved password")
        print("  [Q] Exit")

        choice = input("\nSelect an option: ").strip().lower()

        if choice == "1":
            show_profiles(profiles)

        elif choice == "2":
            show_profiles(profiles)
            profile = select_profile(profiles)

            if profile:
                show_profile(profile)

        elif choice == "3":
            show_profiles(profiles)
            profile = select_profile(profiles)

            if profile:
                show_password(profile)

        elif choice == "q":
            print("\nExiting Wi-Fi Profile Auditor.")
            break

        else:
            print("\nInvalid option. Choose 1, 2, 3, or Q.")


if __name__ == "__main__":
    main()