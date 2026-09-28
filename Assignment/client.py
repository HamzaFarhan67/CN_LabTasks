import socket
import struct
import random


PORT = 53
TIMEOUT = 5

def domain_to_dns(domain):
    result = b""

    pieces = domain.split(".")

    for piece in pieces:
        result += bytes([len(piece)])
        result += piece.encode()

    result += b"\x00"

    return result


def create_dns_request(domain):
    tx_id = random.randint(0, 65535)

    flags = 0x0100

    questions = 1

    answers = 0
    authority = 0
    additional = 0

    header = struct.pack(
        "!HHHHHH",
        tx_id,
        flags,
        questions,
        answers,
        authority,
        additional
    )

    name = domain_to_dns(domain)

    question = name + struct.pack("!HH", 1, 1)

    packet = header + question

    return packet, tx_id


def read_dns_name(data, position):
    labels = []
    jumped = False
    next_position = position

    while True:
        length = data[position]

        if length == 0:
            position += 1

            if not jumped:
                next_position = position

            break

        if (length & 192) == 192:
            pointer = ((length & 63) << 8) | data[position + 1]

            if not jumped:
                next_position = position + 2

            position = pointer
            jumped = True

        else:
            position += 1

            label = data[position:position + length]

            labels.append(
                label.decode("ascii", errors="replace")
            )

            position += length

            if not jumped:
                next_position = position

    return ".".join(labels), next_position


def show_response(data, tx_id):

    if len(data) < 12:
        print("Error: DNS response is too short.")
        return

    response_id, flags, qd, an, ns, ar = struct.unpack(
        "!HHHHHH",
        data[:12]
    )

    if response_id != tx_id:
        print("Error: Transaction ID does not match.")
        return

    response_code = flags & 15

    print("\n====== DNS RESPONSE: ")
    print("Transaction ID:", response_id)
    print("Flags: 0x{:04X}".format(flags))

    if response_code == 0:
        print("Status: NOERROR")
    elif response_code == 3:
        print("Status: NXDOMAIN")
        print("The requested domain does not exist.")
        return
    elif response_code == 2:
        print("Status: SERVFAIL")
        return
    elif response_code == 1:
        print("Status: FORMERR")
        return
    else:
        print("Status: DNS Error Code", response_code)
        return

    if flags & 0x0400:
        print("Authoritative Answer: True")
    else:
        print("Authoritative Answer: False")

    if flags & 0x0080:
        print("Recursion Available: True")
    else:
        print("Recursion Available: False")

    print("Questions:", qd)
    print("Answers:", an)


    position = 12

    for i in range(qd):

        question_name, position = read_dns_name(
            data,
            position
        )

        if position + 4 > len(data):
            print("Error: Invalid question section.")
            return

        qtype, qclass = struct.unpack(
            "!HH",
            data[position:position + 4]
        )

        position += 4

        print("\nQuery Name:", question_name)

        if qtype == 1:
            print("Query Type: A")
        else:
            print("Query Type:", qtype)

    if an == 0:
        print("\nNo answer records were returned.")
        return

    print("\nANSWERS:")

    found_address = False

    for record_number in range(1, an + 1):

        record_name, position = read_dns_name(
            data,
            position
        )

        if position + 10 > len(data):
            print("Error: Invalid answer record.")
            return

        record_type, record_class, ttl, length = struct.unpack(
            "!HHIH",
            data[position:position + 10]
        )

        position += 10

        if position + length > len(data):
            print("Error: Invalid record data.")
            return

        record_data = data[position:position + length]

        print("\nRecord", record_number)
        print("Name:", record_name)
        print("TTL:", ttl, "seconds")

        if record_type == 1:

            if length != 4:
                print("Invalid A record.")
            else:
                ip = socket.inet_ntoa(record_data)

                print("Type: A")
                print("IPv4 Address:", ip)

                found_address = True

        elif record_type == 5:

            cname, unused = read_dns_name(
                data,
                position
            )

            print("Type: CNAME")
            print("Canonical Name:", cname)

        else:
            print("Record Type:", record_type)

        position += length

    if not found_address:
        print("\nNo IPv4 A record was found.")


def lookup_domain(domain, dns_server):

    packet, tx_id = create_dns_request(domain)

    dns_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM
    )

    dns_socket.settimeout(TIMEOUT)

    try:
        print("\nSending DNS query...")
        print("Domain:", domain)
        print("DNS Server:", dns_server)
        print("Port:", PORT)

        dns_socket.sendto(
            packet,
            (dns_server, PORT)
        )

        response, address = dns_socket.recvfrom(512)

        print("Response received from:", address[0])

        show_response(response, tx_id)

    except socket.timeout:
        print("\nError: DNS server did not respond within",
              TIMEOUT, "seconds.")

    except OSError as error:
        print("\nSocket error:", error)

    finally:
        dns_socket.close()

def run_program():
    print("-------- DNS QUERY PROGRAM --------")

    dns_server = input(
        "\nEnter DNS server IP address: "
    ).strip()

    while True:

        domain = input(
            "\nEnter domain name "
            "(or type 'exit' to quit): "
        ).strip()

        if domain.lower() == "exit":
            print("\nProgram ended.")
            break

        if domain == "":
            print("Error: Please enter a domain name.")
            continue

        lookup_domain(
            domain,
            dns_server
        )

run_program()