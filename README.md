# Custom ISA Assembler and Simulator

A custom assembler and simulator implementation for a 16-bit ISA (Instruction Set Architecture) supporting various operations including arithmetic, data movement, branching, and floating-point computations.

## 🎯 Features

- **16-bit ISA Implementation**
  - 6 distinct instruction encoding types
  - Support for 7 general-purpose registers and 1 FLAGS register
  - 7-bit address space (128 memory locations)
  - Double byte addressable memory system

- **Assembler Capabilities**
  - Converts assembly code to 16-bit binary instructions
  - Handles variables and labels
  - Comprehensive error detection and reporting
  - Support for all instruction types (Type A to Type F)

- **Simulator Features**
  - Complete instruction execution engine
  - Register file management
  - Memory management (256 bytes)
  - Program counter tracking
  - Detailed execution trace output

- **Advanced Features**
  - Custom floating-point arithmetic support
  - 8-bit floating-point format (3-bit exponent, 5-bit mantissa)
  - Error handling for floating-point operations

## 📋 Instruction Set Overview

### Supported Instructions

1. **Arithmetic Operations**
   - `add reg1 reg2 reg3` (Addition)
   - `sub reg1 reg2 reg3` (Subtraction)
   - `mul reg1 reg2 reg3` (Multiplication)
   - `div reg3 reg4` (Division)

2. **Data Movement**
   - `mov reg1 $Imm` (Immediate)
   - `mov reg1 reg2` (Register)
   - `ld reg1 mem_addr` (Load)
   - `st reg1 mem_addr` (Store)

3. **Logical Operations**
   - `xor reg1 reg2 reg3`
   - `or reg1 reg2 reg3`
   - `and reg1 reg2 reg3`
   - `not reg1 reg2`

4. **Branching Operations**
   - `jmp mem_addr` (Unconditional)
   - `jlt mem_addr` (Jump if less than)
   - `jgt mem_addr` (Jump if greater than)
   - `je mem_addr` (Jump if equal)

5. **Floating Point Operations**
   - `addf reg1 reg2 reg3` (Floating-point addition)
   - `subf reg1 reg2 reg3` (Floating-point subtraction)
   - `movf reg1 $Imm` (Floating-point immediate)

## 🛠️ Technical Implementation

### Assembler Components

1. **Parser**
   - Handles instruction syntax validation
   - Processes labels and variables
   - Manages immediate value constraints

2. **Error Handler**
   - Syntax error detection
   - Variable and label validation
   - Instruction sequence validation
   - FLAGS register usage validation

3. **Binary Generator**
   - 16-bit instruction encoding
   - Memory address resolution
   - Variable and label address mapping

### Simulator Components

1. **Memory (MEM)**
   - 256-byte storage
   - 7-bit addressing
   - Double byte addressable

2. **Program Counter (PC)**
   - 7-bit register
   - Instruction pointer management

3. **Register File (RF)**
   - 7 general-purpose registers
   - FLAGS register handling
   - Register state management

4. **Execution Engine (EE)**
   - Instruction fetch and decode
   - Operation execution
   - State updates

## 🚀 Usage

### Assembler Usage

```bash
# Run assembler with input file
./assembler < input.asm > output.bin
```

Example Assembly Code:
```assembly
var X
mov R1 $10
mov R2 $100
mul R3 R2 R1
st R3 X
hlt
```

### Simulator Usage

```bash
# Run simulator with binary file
./simulator < input.bin > trace.txt
```

## 💡 Error Handling

The assembler handles various error conditions including:
- Typos in instruction/register names
- Undefined variables/labels
- Illegal FLAGS register usage
- Invalid immediate values
- Misuse of labels/variables
- Missing or misplaced halt instructions

## 📊 Output Format

### Assembler Output
- Error-free: 16-bit binary instructions (one per line)
- Error case: Error message with line number

### Simulator Output
- Per instruction: `<PC> <R0> <R1> <R2> <R3> <R4> <R5> <R6> <FLAGS>`
- Final memory dump: 128 lines of 16-bit values

## 🤝 Contributing

Feel free to contribute to this project by:
1. Forking the repository
2. Creating a feature branch
3. Committing your changes
4. Opening a pull request

## 📝 License

[MIT License](LICENSE)
