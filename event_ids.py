EVENT_ID_DESCRIPTIONS = {
    # --- Logon / Authentication ---
    "4624": "Successful logon",
    "4625": "Failed logon attempt",
    "4634": "Logoff",
    "4647": "User initiated logoff",
    "4648": "Logon with explicit credentials",
    "4675": "SIDs filtered",
    "4776": "NTLM authentication",
    "4768": "Kerberos TGT requested",
    "4769": "Kerberos service ticket requested",
    "4771": "Kerberos pre-authentication failed",
    "4778": "Session reconnected",
    "4779": "Session disconnected",

    # --- Privileges / Admin ---
    "4672": "Special privileges assigned (admin logon)",
    "4673": "Sensitive privilege use attempted",
    "4674": "Privileged operation attempted",

    # --- Process Activity ---
    "4688": "Process creation",
    "4689": "Process termination",
    "4690": "Handle duplicated",

    # --- Account Management ---
    "4720": "User account created",
    "4722": "User account enabled",
    "4723": "Password change attempt",
    "4724": "Password reset attempt",
    "4725": "User account disabled",
    "4726": "User account deleted",
    "4738": "User account changed",

    # --- Group Management ---
    "4727": "Security group created",
    "4728": "User added to security-enabled global group",
    "4729": "User removed from global group",
    "4732": "User added to local group",
    "4733": "User removed from local group",
    "4735": "Security-enabled local group changed",
    "4737": "Security-enabled global group changed",

    # --- Policy / Audit ---
    "4715": "Audit policy changed",
    "4719": "System audit policy changed",
    "4902": "Per-user audit policy table created",
    "4907": "Auditing settings changed",

    # --- Log / Detection ---
    "1100": "Event log service shut down",
    "1102": "Event log cleared",
    "1104": "Security log is full",

    # --- Services ---
    "7040": "Service start type changed",
    "7045": "Service installed",

    # --- Scheduled Tasks ---
    "4698": "Scheduled task created",
    "4699": "Scheduled task deleted",
    "4700": "Scheduled task enabled",
    "4701": "Scheduled task disabled",
    "4702": "Scheduled task updated",

    # --- Object Access / Files ---
    "4656": "Handle requested to object",
    "4663": "Object accessed",
    "4660": "Object deleted",
    "4658": "Handle closed",

    # --- Registry ---
    "4657": "Registry value modified",

    # --- Network / Shares ---
    "5140": "Network share accessed",
    "5142": "Network share added",
    "5143": "Network share modified",
    "5144": "Network share deleted",
    "5156": "Allowed network connection",
    "5157": "Blocked network connection",

    # --- Firewall ---
    "5025": "Windows Firewall stopped",
    "5031": "Firewall blocked application",
    "5152": "Packet dropped",
    "5153": "Connection blocked",

    # --- System Integrity ---
    "4616": "System time changed",
    "4608": "Windows started",
    "4609": "Windows shutting down",

    # --- Driver / Kernel ---
    "6": "Driver loaded",
    "7": "Driver unloaded",

    # --- PowerShell (very important in attacks) ---
    "4103": "PowerShell command invocation",
    "4104": "PowerShell script block executed",

    # --- Remote Access / RDP ---
    "1149": "RDP login attempt",
    "21": "RDP session logon",
    "24": "RDP session disconnect",

    # --- DNS ---
    "3008": "DNS query",
    "3010": "DNS response",

    # --- Misc Security Signals ---
    "4697": "Service installed (legacy)",
    "4964": "Special groups assigned to logon",
    "5038": "Code integrity violation",
    "5058": "Cryptographic key operation",
    "5061": "Crypto operation performed",

    # --- Account Lockouts ---
    "4740": "User account locked out",

    # --- Trust / Domain ---
    "4713": "Kerberos policy changed",
    "4716": "Trusted domain modified",
    "4721": "Computer account created",

    # --- Advanced ---
    "4985": "Transaction state changed",
    "5032": "Windows Firewall driver started",
    "5447": "Firewall rule modified",

    # --- Rare but suspicious ---
    "4611": "Trusted logon process registered",
    "4696": "Primary token assigned",
    "6416": "External device recognized",

    # --- Defender / AV (varies by system) ---
    "1116": "Malware detected",
    "1117": "Malware action taken",
    "1118": "Malware remediation failed",

    # --- Extras ---
    "1": "System startup or general system event (low-level system provider)",
    "3": "Network connection detected (often from Sysmon - network connection)",
    "18": "Pipe event / inter-process communication (provider-specific, often Sysmon)",
    "5145": "Detailed file share access (network share object access check)",
}