-- For NFLOG -> BASE -> IFINDEX -> IP2STR -> SQLITE3.
-- Text addresses preserve both IPv4 and IPv6.
CREATE TABLE ulog_pkt (
    oob_time_sec INTEGER,
    oob_time_usec INTEGER,
    oob_prefix TEXT,
    oob_mark INTEGER,
    oob_in TEXT,
    oob_out TEXT,
    oob_family INTEGER,
    ip_saddr_str TEXT,
    ip_daddr_str TEXT,
    ip_protocol INTEGER,
    tcp_sport INTEGER,
    tcp_dport INTEGER,
    udp_sport INTEGER,
    udp_dport INTEGER,
    raw_pktlen INTEGER
);
