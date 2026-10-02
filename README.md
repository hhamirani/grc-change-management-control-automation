# grc-change-management-control-automation
**Prototype File Integrity Monitoring Script for Change Management Control Automation**

# Overview
This project is a proof-of-concept for automating aspects of an IT SOX change-management control for the Qlik application (but could be refactored to apply generally for any applicable file change management).

The underlying control concept was that a production Qlik application file (baseline.QVS) should not be modified without a corresponding ServiceNow change ticket documenting the change and required approvals.

The proposed workflow was:
1. Compare the current Qlik file against the approved baseline.

2. Detect and document differences between the two versions.

3. Identify a corresponding ServiceNow change ticket for the detected change.

4. Compare the documented change against the actual file modification.

5. If the change is appropriately authorized, update the approved baseline.

6. If no corresponding authorization exists, flag the change for investigation.

7. Investigate the source of an unauthorized change, including who developed and migrated the change and why the required change-management process was not followed.



# Current Prototype
**The prototype implements the file comparison, metadata collection, hashing, and audit-oriented output components of this concept.**

The Python prototype currently:

1. Compares two versions of a file line-by-line.

2. Identifies and reports content differences.

3. Records file metadata including timestamps and file size.

4. Generates a cryptographic hash for each file.

5. Produces a timestamped audit output.

6. Writes output to both the console and a log file.

# Example Control Flow

```text
              ┌─────────────────────┐
              │ Current Qlik File   │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ Compare to Approved │
              │ Baseline            │
              └──────────┬──────────┘
                         │
                 Change detected?
                    /          \
                  No            Yes
                  │              │
                  ▼              ▼
               No action   Search for ServiceNow
                           change record
                                  │
                         ┌────────┴────────┐
                         │                 │
                      Found             Not Found
                         │                 │
                         ▼                 ▼
                  Validate change     Investigate /
                  against ticket      escalate
                         │
                         ▼
                  Update baseline
```

# Changes and Reconfigurations for Further Development

1. Currently the filenames are hardcoded, I'd like to change it to be more generic.
   
2. Currently the file generates hashes using MD5, but that should be updated to SHA256 for more robust cryptographic fingerprinting.
   
3. The file needs to be manually run; it should be automated to run on a daily interval.
 
4. The file should be encrypted or otherwise password protected to prevent unauthorized modification to the script.
 
5. Log file is dumped to the directory; should be automatically sent out in an email to a designated reviewer or mailbox.
 
6. Error handling + associated logs in case the script fails to run or encounters an error. 

# Development Note
The initial prototype was developed with AI-assisted coding support. The control design, use case, and proposed workflow were defined around the intended IT change-management process.
