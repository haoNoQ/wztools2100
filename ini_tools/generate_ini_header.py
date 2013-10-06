from profile_loader import get_profiles

for profile in get_profiles():
    print "\n" * 3
    print profile.get_header()