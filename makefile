Initial = main.py
BuildDirectory = builds
ExecutableName = midi-humanizer
ExecutablePath = $(BuildDirectory)/$(ExecutableName)

all: build

${BuildDirectory}:
	mkdir -p ${BuildDirectory}

build: ${BuildDirectory}
	nuitka --mode=onefile --enable-plugin=pyside6 --windows-console-mode=disabled --output-dir=${BuildDirectory} ${Initial}
	@echo "Build successfuly completed! Executable location: ${ExecutablePath}"

clean:
	rm -rf ${BuildDirectory}

.PHONY: all build clean