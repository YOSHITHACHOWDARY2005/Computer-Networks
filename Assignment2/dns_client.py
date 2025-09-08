import dns.resolver

domain = "example.com"

with open("dns_results.txt", "w") as f:
    # A record
    for r in dns.resolver.resolve(domain, "A"):
        f.write(f"A record: {r.to_text()}\n")
        print("A record:", r.to_text())

    # MX record
    for r in dns.resolver.resolve(domain, "MX"):
        f.write(f"MX record: {r.to_text()}\n")
        print("MX record:", r.to_text())

    # CNAME
    try:
        for r in dns.resolver.resolve(domain, "CNAME"):
            f.write(f"CNAME record: {r.to_text()}\n")
            print("CNAME record:", r.to_text())
    except Exception:
        print("No CNAME found")

