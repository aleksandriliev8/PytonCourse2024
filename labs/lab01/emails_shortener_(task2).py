
def emails_shortener(emails):

    domain_dict = {}

    for email in emails:
        user_name, domain = email.split('@')
        if domain in domain_dict:
            domain_dict[domain].append(user_name)
        else:
            domain_dict[domain] = [user_name]

    result = set()

    for domain, user_names in domain_dict.items():
        if len(user_names) > 1:
            same_domain_names = ",".join(user_names)
            result.add(f"{{{same_domain_names}}}@{domain}")
        else: 
            result.add(f"{user_names[0]}@{domain}")

    return result

assert emails_shortener([
    "tinko@fmi.uni-sofia.bg", 
    "minko@fmi.uni-sofia.bg", 
    "pesho@pesho.org",
]) == {
    "{tinko,minko}@fmi.uni-sofia.bg", 
    "pesho@pesho.org",
}

assert emails_shortener([
    "toi_e@pesho.org",
    "golemiq@cyb.org",
]) == {
    "toi_e@pesho.org",
    "golemiq@cyb.org",
}