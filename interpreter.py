import struct
import xml.etree.ElementTree as ET

class VirtualMachine:
    def __init__(self):
        self.memory = [0] * 1024  # Простая память на 1024 ячейки

    def execute(self, binary_data):
        pc = 0
        print("Начало выполнения программы")
        while pc < len(binary_data):
            opcode = binary_data[pc]
            print(f"Текущая команда: opcode={opcode}, pc={pc}")

            if opcode == 38:  # Загрузка константы (A B C)
                if len(binary_data[pc:pc+13]) < 13:
                    print("Ошибка: недостаточно данных для команды загрузки константы")
                    break
                _, B, C = struct.unpack(">B I Q", binary_data[pc:pc+13])
                print(f"Команда загрузки: B={B}, C={C}")
                self.memory[B] = C
                pc += 13

            elif opcode == 40:  # Чтение значения из памяти (A B C D)
                if len(binary_data[pc:pc+11]) < 11:
                    print("Ошибка: недостаточно данных для команды чтения из памяти")
                    break
                _, B, C, D = struct.unpack(">B I I H", binary_data[pc:pc+11])
                addr = self.memory[C] + D
                print(f"Чтение из памяти: B={B}, C={C}, D={D}, addr={addr}")
                self.memory[B] = self.memory[addr]
                pc += 11

            elif opcode == 18:  # Запись значения в память (A B C)
                if len(binary_data[pc:pc+9]) < 9:
                    print("Ошибка: недостаточно данных для команды записи в память")
                    break
                _, B, C = struct.unpack(">B I I", binary_data[pc:pc+9])
                print(f"Запись в память: B={B}, C={C}")
                self.memory[C] = self.memory[B]
                pc += 9

            elif opcode == 13:  # Унарная операция bitreverse (A B C)
                if len(binary_data[pc:pc+9]) < 9:
                    print("Ошибка: недостаточно данных для команды bitreverse")
                    break
                _, B, C = struct.unpack(">B I I", binary_data[pc:pc+9])
                value = self.memory[C]
                bit_reversed_value = int('{:032b}'.format(value)[::-1], 2)
                print(f"bitreverse: B={B}, C={C}, value={value}, reversed={bit_reversed_value}")
                self.memory[B] = bit_reversed_value
                pc += 9

            else:
                print(f"Неизвестная команда: {opcode}")
                break

    def save_memory(self, start, end, result_file):
        root = ET.Element("memory")
        for addr in range(start, end):
            mem_elem = ET.SubElement(root, "cell", address=str(addr))
            mem_elem.text = str(self.memory[addr])
        tree = ET.ElementTree(root)
        tree.write(result_file)
        print(f"Память сохранена в {result_file}")

# Пример использования интерпретатора
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 5:
        print("Использование: python interpreter.py <input_file> <result_file> <start> <end>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    result_file = sys.argv[2]
    start = int(sys.argv[3])
    end = int(sys.argv[4])
    
    with open(input_file, "rb") as f:
        binary_data = f.read()

    vm = VirtualMachine()
    vm.execute(binary_data)
    vm.save_memory(start, end, result_file)
