#include <iostream>
#include <string>

#ifndef DIRECTIONAL_VERSION
#define DIRECTIONAL_VERSION "0.1.0"
#endif

extern "C" const char *directional_build_info();

namespace {

void print_usage(std::ostream &stream) {
  stream << "Directional native command line interface\n\n"
         << "Usage:\n"
         << "  directional info\n"
         << "  directional --version\n"
         << "  directional --help\n\n"
         << "Commands:\n"
         << "  info        Show native library build information.\n\n"
         << "Notes:\n"
         << "  The native CLI is intentionally minimal. Use the Python `directional`\n"
         << "  command for .npz-based remeshing input/output.\n";
}

} // namespace

int main(int argc, char **argv) {
  if (argc <= 1) {
    print_usage(std::cout);
    return 0;
  }

  const std::string command = argv[1];
  if (command == "--help" || command == "-h" || command == "help") {
    print_usage(std::cout);
    return 0;
  }

  if (command == "--version" || command == "-V") {
    std::cout << "directional-cli " << DIRECTIONAL_VERSION << '\n';
    return 0;
  }

  if (command == "info") {
    std::cout << "directional-cli " << DIRECTIONAL_VERSION << '\n';
    std::cout << "native library: " << directional_build_info() << '\n';
    return 0;
  }

  std::cerr << "directional-cli: unknown command: " << command << '\n';
  std::cerr << "Run `directional --help` for usage.\n";
  return 2;
}
