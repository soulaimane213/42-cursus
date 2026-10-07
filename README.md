# 42 Cursus — Common Core & Specialization Projects

A comprehensive collection of projects completed during my journey at **42 Network** (1337 / 42 Casablanca).

This repository encompasses foundational C libraries, low-level Unix system programming, sorting algorithms, system administration, and advanced Python modules.

[![42 Network](https://img.shields.io/badge/42-Network-black?style=for-the-badge&logo=42)](https://42.fr)
[![YouTube Channel](https://img.shields.io/badge/YouTube-Zero2Segfault-red?style=for-the-badge&logo=youtube)](https://www.youtube.com/@Zero2Segfault)

---

## 🗺️ Curriculum Roadmap

| Project | Language | Category | Description |
| :--- | :--- | :--- | :--- |
| **[`libft`](./libft)** | C | Core / Libc | Custom implementation of standard C standard library routines and linked list utilities. |
| **[`ft_printf`](./ft_printf)** | C | Variadic Functions | Re-implementation of standard `printf` handling `%c`, `%s`, `%p`, `%d`, `%i`, `%u`, `%x`, `%X`, `%%`. |
| **[`get_next_line`](./get_next_line)** | C | File I/O & Buffers | Fast, line-by-line file descriptor reading with static buffer management. |
| **[`Born2beroot`](./Born2beroot)** | Shell / Linux | SysAdmin | Debian server setup with LVM, encrypted partitions, SSH hardening, UFW firewall, and sudo policies. |
| **[`push_swap`](./push_swap)** | C | Algorithms | Optimized sorting algorithm utilizing two stacks (`a` and `b`) and a restricted instruction set. |
| **[`A-Maze-ing`](./A-Maze-ing)** | Python | Algorithms / AI | Procedural maze generation, graph traversal, and parsing engine. |
| **[`Call_Me_Maybe`](./Call_Me_Maybe)** | Python | LLM SDK / API | Python module integrating LLM APIs and tools via clean SDK architecture. |
| **[`Fly-in`](./Fly-in)** | Python | Simulation / Graph | Network graph pathfinding, parser, and aircraft simulation engine. |

---

## 🛠️ General Guidelines

All C projects strictly adhere to 42's coding standards:
- Zero memory leaks (verified using `valgrind` and `-fsanitize=address`).
- Robust error handling with zero unexpected crashes (`SIGSEGV`, `SIGBUS`, etc.).
- Custom `Makefile` for every project providing `all`, `clean`, `fclean`, and `re` rules.

---

## 👨‍💻 Author

**Soulaimane FADL**  
*42 Student & Low-Level Systems Hacker*  
YouTube: [@Zero2Segfault](https://www.youtube.com/@Zero2Segfault)  
GitHub: [@soulaimane213](https://github.com/soulaimane213)
