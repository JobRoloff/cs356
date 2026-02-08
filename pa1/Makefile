# Java compiler and runner
JC = javac
JV = java

# Output directory for .class files
BUILD_DIR = build

# Main class name (must match public class in Cipher.java)
MAIN_CLASS = Cipher

# All Java sources are in the top-level directory
SRCS = $(wildcard *.java)

# Default target: compile everything
all: $(BUILD_DIR) $(BUILD_DIR)/$(MAIN_CLASS).class

# Create build directory
$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

# Compile all sources (do it in one javac call so dependencies are handled cleanly)
$(BUILD_DIR)/$(MAIN_CLASS).class: $(SRCS) | $(BUILD_DIR)
	$(JC) -d $(BUILD_DIR) $(SRCS)

# Run (optional for you; TAs usually just do `make`)
# Usage: make run FILE=input.txt
run: all
	$(JV) -cp $(BUILD_DIR) $(MAIN_CLASS) $(TYPE) $(IN) $(OUT) $(KEY) $(MODE)

# Clean build artifacts
clean:
	rm -rf $(BUILD_DIR)

.PHONY: all run clean
