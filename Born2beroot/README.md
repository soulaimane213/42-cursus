*This project has been created as part of the 42 curriculum by sofadl.*

## Description

Born2beRoot is a system administration project from the 42 curriculum.  
The goal of this project is to create and configure a secure Linux server inside a virtual machine, following strict rules.

This project helps understand the basics of Linux system administration, security, user management, services, and automation.  
The server is installed without a graphical interface and only the minimum required services are configured.

## Instructions

### Requirements
- VirtualBox (or UTM if VirtualBox cannot be used)
- Debian (latest stable version) or Rocky Linux (latest stable version)

### Installation Overview
1. Create a virtual machine using VirtualBox.
2. Install the operating system without a graphical interface.
3. Configure encrypted partitions using LVM.
4. Set the correct hostname.
5. Create required users and groups.
6. Apply a strong password policy.
7. Install and configure sudo with security rules.
8. Configure SSH on port 4242 and disable root login.
9. Configure the firewall (UFW or firewalld).
10. Create and schedule the `monitoring.sh` script using cron.

### Execution
- The server starts automatically when the virtual machine is launched.
- The `monitoring.sh` script runs at startup and every 10 minutes.
- The script displays system information on all terminals using the `wall` command.

## Project Description and Technical Choices

### Operating System Choice

**Debian (chosen):**
- Very stable and reliable
- Beginner-friendly
- Large community and documentation

**Rocky Linux (alternative):**
- Enterprise-oriented distribution
- Compatible with Red Hat Enterprise Linux
- More complex for beginners

### Main Design Choices

- **Partitioning:** Encrypted partitions using LVM
- **Security Policies:** AppArmor enabled (Debian)
- **User Management:** Root user + personal user in `user42` and `sudo` groups
- **Services Installed:** SSH, sudo, cron, firewall

## Comparisons

### Debian vs Rocky Linux
- Debian: simpler, easier to configure, recommended for beginners
- Rocky Linux: enterprise-focused, stricter security, more complex

### AppArmor vs SELinux
- AppArmor: profile-based, easier to understand and manage
- SELinux: policy-based, very powerful but harder to configure

### UFW vs firewalld
- UFW: simple and user-friendly firewall for Debian
- firewalld: dynamic and advanced firewall used in Rocky Linux

### VirtualBox vs UTM
- VirtualBox: widely used, cross-platform, recommended
- UTM: good alternative, mainly used on macOS

## Resources

### Documentation and References
- Official Debian Documentation
- Linux manual pages (`man sudo`, `man sshd`, `man cron`, `man ufw`)
- 42 Born2beRoot subject

### AI Usage
AI was used to:
- Clarify project requirements
- Explain Linux concepts (LVM, SSH, sudo, firewall, cron)
- Help structure the monitoring script logic
- Improve clarity and structure of this README

## Conclusion

This project builds a strong foundation in Linux system administration and security.  
It focuses on understanding how and why each component is configured, which is essential for real-world server management.

