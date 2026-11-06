# Day 15: Finite State Machines (FSM)

Table-driven transition matrices vs switch-case FSMs for deterministic industrial sequencers and safety controllers.

---

## 📋 Program Index & Summary

| # | Program File | Primary Focus | Time Complexity | Space Complexity | Embedded Key Insight |
| :-: | :--- | :--- | :---: | :---: | :--- |
| **01** | **`01_table_driven_fsm.c`** | Table-Driven Finite State Machine in C99 | O(1) transition lookup | O(States x Events) in Flash | Table-driven FSMs eliminate deeply nested switch statements and guarantee constant O(1) transition dispatch time. |

---

## 💡 Embedded Notes & Key Hardware Takeaways

### 1. Table-Driven Finite State Machine in C99
- **Key Silicon Insight:** Table-driven FSMs eliminate deeply nested switch statements and guarantee constant O(1) transition dispatch time.
- **Technical Design Question:** *When is switch-case preferred over a table-driven FSM?*
- **Engineering Rationale:** When the transition matrix is sparse (few events per state), switch-case saves Flash memory by avoiding empty table entries.

---

## 🛠 How to Compile & Run

```bash
# Compile all programs in this module with strict C99 warnings
gcc -Wall -Wextra -std=c99 -pedantic 01_table_driven_fsm.c -o 01_table_driven_fsm && ./01_table_driven_fsm
```
