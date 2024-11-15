import struct
import xml.etree.ElementTree as ET
import sys

# Ассемблерная команда в бинарный формат
def assemble_command(opcode, B, C=0, D=0):
    if opcode == 38:  # Загрузка константы (A B C)
        # Пакуем как 1 байт для opcode, 4 байта для B, 8 байт для C (константа)
        return struct.pack(">B I Q", opcode, B, C)
    elif opcode == 40:  # Чтение значения из памяти (A B C D)
        # Пакуем как 1 байт для opcode, 4 байта для B, 4 байта для C, 2 байта для D
        return struct.pack(">B I I H", opcode, B, C, D)
    elif opcode == 18:  # Запись значения в память (A B C)
        # Пакуем как 1 байт для opcode, 4 байта для B, 4 байта для C
        return struct.pack(">B I I", opcode, B, C)
    elif opcode == 13:  # Унарная операция bitreverse (A B C)
        # Пакуем как 1 байт для opcode, 4 байта для B, 4 байта для C
        return struct.pack(">B I I", opcode, B, C)
    else:
        raise ValueError(f"Неизвестная команда: {opcode}")

# Сборка ассемблерного кода из текстового файла
def assemble(input_file, output_file, log_file):
    with open(input_file, "r") as src, open(output_file, "wb") as dst:
        root = ET.Element("log")
        for line in src:
            parts = line.strip().split()
            if len(parts) < 2:
                continue
            
            try:
                opcode = int(parts[0])
                B = int(parts[1])
                C = int(parts[2]) if len(parts) > 2 else 0
                D = int(parts[3]) if len(parts) > 3 else 0

                # Генерация бинарного кода
                binary_command = assemble_command(opcode, B, C, D)
                print(f"Записана команда: opcode={opcode}, B={B}, C={C}, D={D}")
                dst.write(binary_command)

                # Логирование команды в XML
                instr_elem = ET.SubElement(root, "instruction")
                ET.SubElement(instr_elem, "opcode").text = str(opcode)
                ET.SubElement(instr_elem, "B").text = str(B)
                ET.SubElement(instr_elem, "C").text = str(C)
                ET.SubElement(instr_elem, "D").text = str(D)

            except ValueError as e:
                print(f"Ошибка при обработке строки: {line}")
                print(e)
                continue

        # Запись лога в XML файл
        tree = ET.ElementTree(root)
        tree.write(log_file)

# Пример вызова ассемблера
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Использование: python assembler.py <input_file> <output_file> <log_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    log_file = sys.argv[3]
    assemble(input_file, output_file, log_file)

# python assembler.py program.txt output.bin log.xml
# python check_bin.py
# python interpreter.py output.bin result.xml 0 6
