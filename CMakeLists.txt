cmake_minimum_required(VERSION 3.16)
project(mycpp VERSION 0.1.0 LANGUAGES CXX)

# ── C++ Standard ────────────────────────────────────────────────
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# ── Compiler Warnings ──────────────────────────────────────────
if(MSVC)
    add_compile_options(/W4 /permissive-)
else()
    add_compile_options(-Wall -Wextra -Wpedantic -Werror=return-type)
endif()

# ── Include Directories ────────────────────────────────────────
include_directories(${PROJECT_SOURCE_DIR}/include)

# ── Driver Executable ──────────────────────────────────────────
add_executable(mycpp tools/main.cpp)

# ── Testing ─────────────────────────────────────────────────────
enable_testing()
