import sys
from lexer import Lexer
from parser import Parser
from codegen import CodeGenerator


def compile_cpp(source_code):
    # Phase 1: Lexing
    print("=== LEXER ===")
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    for token in tokens:
        print(f"  {token}")

    # Phase 2: Parsing
    print("\n=== PARSER ===")
    parser = Parser(tokens)
    ast = parser.parse()
    print(f"  {ast}")

    # Phase 3: Code Generation
    print("\n=== GENERATED PYTHON CODE ===")
    generator = CodeGenerator()
    python_code = generator.generate(ast)
    print(python_code)

    # Phase 4: Execute!
    print("\n=== OUTPUT ===")
    namespace = {"__name__": "__main__"}
    exec(python_code, namespace)


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <filename.cpp>")
        print("       python main.py --test")
        sys.exit(1)

    if sys.argv[1] == "--test":
        test_code = """
int main() {
    int x = 10;
    int y = 3;
    int sum = x + y;
    print(sum);
    if (x > y) {
        print(1);
    } else {
        print(0);
    }
    int i = 0;
    while (i < 5) {
        print(i);
        i = i + 1;
    }
    return 0;
}
"""
        compile_cpp(test_code)
    else:
        filename = sys.argv[1]
        with open(filename, "r") as f:
            source = f.read()
        compile_cpp(source)


if __name__ == "__main__":
    main()
